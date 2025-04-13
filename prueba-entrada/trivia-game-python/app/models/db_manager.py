import json
import os
import random
import asyncio
from databases import Database
from dotenv import load_dotenv
from app.models.question import Question
from app.models.difficulty import DifficultyLevel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class DBManager:
    
    def __init__(self):
        self.database = Database(DATABASE_URL) if DATABASE_URL else None
        self.connected = False
        
    async def connect(self):
        if not self.database:
            return False
            
        try:
            await self.database.connect()
            self.connected = True
            return True
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False
        
    async def disconnect(self):
        if self.connected:
            await self.database.disconnect()
            self.connected = False
    
    async def get_random_questions(self, limit=10):
        if not self.connected:
            return []
            
        try:
            query = """
                SELECT q.id, q.description, q.options, q.correct_answer, q.difficulty
                FROM questions q
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
                
                difficulty_str = row.get("difficulty", "easy").lower()
                difficulty = DifficultyLevel.EASY
                if difficulty_str == "medium":
                    difficulty = DifficultyLevel.MEDIUM
                elif difficulty_str == "hard":
                    difficulty = DifficultyLevel.HARD
                    
                question = Question(
                    description=row["description"],
                    options=options,
                    correct_answer=row["correct_answer"],
                    difficulty=difficulty
                )
                questions.append(question)
                
            return questions
        except Exception as e:
            
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