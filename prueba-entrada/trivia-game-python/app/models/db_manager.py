import json
import os
import random
import asyncio
from databases import Database
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class DBManager:
    
    def __init__(self):
        self.database = Database(DATABASE_URL) if DATABASE_URL else None
        self.connected = False
        
    async def connect(self):
        if self.database:
            try:
                await self.database.connect()
                self.connected = True
                return True
            except Exception as e:
                print(f"Error de conexión a la base de datos: {e}")
                self.connected = False
        return False
        
    async def disconnect(self):
        if self.database and self.connected:
            await self.database.disconnect()
            self.connected = False
    
    async def get_random_questions(self, limit=10):
        from app.models.question import Question
        
        if not self.connected:
            return []
            
        try:
            query = """
                SELECT q.id, q.description, q.options, q.correct_answer, c.name as category, q.difficulty
                FROM questions q
                JOIN categories c ON q.category_id = c.id
                ORDER BY RANDOM()
                LIMIT :limit
            """
            results = await self.database.fetch_all(query, {"limit": limit})
            
            questions = []
            for row in results:
                try:
                    options = json.loads(row["options"])
                except (json.JSONDecodeError, TypeError):
                    print(f"Error al deserializar opciones para pregunta ID {row['id']}")
                    continue
                    
                question = Question(
                    description=row["description"],
                    options=options,
                    correct_answer=row["correct_answer"]
                )
                questions.append(question)
                
            return questions
        except Exception as e:
            print(f"Error al obtener preguntas: {e}")
            return []
    
    async def question_count(self):
        if not self.connected:
            return 0
            
        try:
            query = "SELECT COUNT(*) as count FROM questions"
            result = await self.database.fetch_one(query)
            return result["count"] if result else 0
        except Exception as e:
            print(f"Error al contar preguntas: {e}")
            return 0
            
    async def is_database_ready(self):
        if not self.connected:
            return False
            
        try:
            tables_query = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'questions'
                ) as questions_exists,
                EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'categories'
                ) as categories_exists
            """
            tables_result = await self.database.fetch_one(tables_query)
            
            if not (tables_result["questions_exists"] and tables_result["categories_exists"]):
                return False
                
            count = await self.question_count()
            return count > 0
        except Exception as e:
            print(f"Error al verificar base de datos: {e}")
            return False 