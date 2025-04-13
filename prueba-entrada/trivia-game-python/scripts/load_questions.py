import json
import os
import sys
import random
import asyncio
import argparse
from databases import Database
from dotenv import load_dotenv

from app.models.difficulty import DifficultyLevel

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def create_tables(database):
    try:
        await database.execute("DROP TABLE IF EXISTS questions CASCADE")
        await database.execute("DROP TABLE IF EXISTS categories CASCADE")
        
        await database.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        
        await database.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                description TEXT NOT NULL,
                options TEXT NOT NULL,
                correct_answer VARCHAR(255) NOT NULL,
                category_id INTEGER REFERENCES categories(id),
                difficulty VARCHAR(20) NOT NULL
            )
        """)
        
        print("Tablas creadas correctamente.")
    except Exception as e:
        print(f"Error al crear tablas: {e}")
        sys.exit(1)

async def load_questions_from_json(json_file):
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['questions']
    except FileNotFoundError:
        print(f"Archivo no encontrado: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo JSON: {json_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar preguntas desde JSON: {e}")
        sys.exit(1)

def validate_difficulty(difficulty_str):
    """Valida y normaliza el valor de dificultad"""
    valid_difficulties = [d.value for d in DifficultyLevel]
    
    if not difficulty_str:
        return DifficultyLevel.EASY.value
    
    difficulty_str = difficulty_str.lower()
    
    # Manejar variantes en español
    if difficulty_str == "fácil" or difficulty_str == "facil":
        return DifficultyLevel.EASY.value
    elif difficulty_str == "medio":
        return DifficultyLevel.MEDIUM.value
    elif difficulty_str == "difícil" or difficulty_str == "dificil":
        return DifficultyLevel.HARD.value
    
    # Verificar si ya es un valor válido
    if difficulty_str in valid_difficulties:
        return difficulty_str
    
    # Valor por defecto
    print(f"Advertencia: Dificultad '{difficulty_str}' no reconocida, usando 'easy' por defecto")
    return DifficultyLevel.EASY.value

async def insert_categories(database, questions):
    try:
        categories = set()
        for question in questions:
            categories.add(question['category'])
   
        category_map = {}
        for category in categories:
            result = await database.fetch_one(
                "SELECT id FROM categories WHERE name = :name",
                {"name": category}
            )
            
            if result:
                category_id = result['id']
            else:
                category_id = await database.execute(
                    "INSERT INTO categories (name) VALUES (:name) RETURNING id",
                    {"name": category}
                )
            
            category_map[category] = category_id
        
        print(f"Categorías insertadas: {len(category_map)}")
        return category_map
    except Exception as e:
        print(f"Error al insertar categorías: {e}")
        return {}

async def insert_questions(database, questions, category_map):
    try:
        count = 0
        for question in questions:
            category_id = category_map.get(question['category'])
            
            # Normalizar dificultad
            difficulty = validate_difficulty(question.get('difficulty', 'easy'))
            
            await database.execute("""
                INSERT INTO questions 
                (description, options, correct_answer, category_id, difficulty)
                VALUES (:description, :options, :correct_answer, :category_id, :difficulty)
            """, {
                "description": question['description'],
                "options": json.dumps(question['options']),
                "correct_answer": question['correct_answer'],
                "category_id": category_id,
                "difficulty": difficulty
            })
            count += 1
        
        print(f"Preguntas insertadas: {count}")
        # Mostrar estadísticas de dificultad
        print("Análisis de niveles de dificultad:")
        for difficulty in [d.value for d in DifficultyLevel]:
            count_query = "SELECT COUNT(*) FROM questions WHERE difficulty = :difficulty"
            result = await database.fetch_one(count_query, {"difficulty": difficulty})
            count = result[0] if result else 0
            print(f"  - {difficulty.upper()}: {count} preguntas")
    except Exception as e:
        print(f"Error al insertar preguntas: {e}")

async def load_questions_to_database():
    if not DATABASE_URL:
        print("La URL de la base de datos no está configurada. Verifique el archivo .env")
        sys.exit(1)

    database = Database(DATABASE_URL)
    
    try:
        await database.connect()
        print("Conexión a la base de datos establecida")
        
        await create_tables(database)
        
        json_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')
        questions = await load_questions_from_json(json_file)
        
        category_map = await insert_categories(database, questions)
        
        await insert_questions(database, questions, category_map)
        
        print("Datos cargados correctamente en la base de datos")
    except Exception as e:
        print(f"Error al cargar datos: {e}")
    finally:
        await database.disconnect()
        print("Conexión a la base de datos cerrada")

def main():
    parser = argparse.ArgumentParser(description='Carga preguntas en la base de datos.')
    parser.add_argument('--local', action='store_true', help='Solo verificar el archivo JSON local')
    parser.add_argument('--analyze', action='store_true', help='Analizar dificultad de preguntas sin cargar a DB')
    args = parser.parse_args()
    
    if args.local:
        json_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')
        questions = asyncio.run(load_questions_from_json(json_file))
        print(f"Archivo JSON verificado correctamente: {json_file}")
        if args.analyze:
            print("\nAnálisis de dificultad:")
            difficulty_counts = {"easy": 0, "medium": 0, "hard": 0, "unknown": 0}
            for q in questions:
                difficulty = q.get('difficulty', 'unknown')
                if difficulty.lower() in ["easy", "fácil", "facil"]:
                    difficulty_counts["easy"] += 1
                elif difficulty.lower() in ["medium", "medio"]:
                    difficulty_counts["medium"] += 1
                elif difficulty.lower() in ["hard", "difícil", "dificil"]:
                    difficulty_counts["hard"] += 1
                else:
                    difficulty_counts["unknown"] += 1
            
            print(f"  - EASY: {difficulty_counts['easy']} preguntas")
            print(f"  - MEDIUM: {difficulty_counts['medium']} preguntas")
            print(f"  - HARD: {difficulty_counts['hard']} preguntas")
            if difficulty_counts["unknown"] > 0:
                print(f"  - Sin dificultad especificada: {difficulty_counts['unknown']} preguntas")
    else:
        asyncio.run(load_questions_to_database())

if __name__ == "__main__":
    main() 