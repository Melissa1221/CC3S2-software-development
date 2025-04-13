from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import random
import json
from enum import Enum
import os

from app.models.question import Question
from app.models.db_manager import DBManager
from app.models.difficulty import DifficultyLevel
from app.models.game_stats import GameStats

app = FastAPI(title="Trivia Game API", description="API para el juego de trivia", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DifficultyLevelAPI(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionResponse(BaseModel):
    id: Optional[int] = None
    description: str
    options: List[str]
    difficulty: DifficultyLevelAPI = DifficultyLevelAPI.EASY
    points: int = 1
    
class AnswerRequest(BaseModel):
    question_id: int
    answer: str
    
class AnswerResponse(BaseModel):
    correct: bool
    correct_answer: Optional[str] = None
    points_earned: int = 0
    
class DifficultyStats(BaseModel):
    correct: int
    total: int
    
class QuizSummary(BaseModel):
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    total_score: int = 0
    accuracy: float
    difficulty_stats: Dict[str, DifficultyStats] = {}


db_manager = None

questions_cache = {}
current_question_id = 1
quiz_stats = GameStats()

@app.on_event("startup")
async def startup_event():
    global db_manager
    db_manager = DBManager()
    success = await db_manager.connect()
    if not success:
        print("⚠️ No se pudo conectar a la base de datos. Usando modo local.")

@app.on_event("shutdown")
async def shutdown_event():
    global db_manager
    if db_manager:
        await db_manager.disconnect()

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API del Juego de Trivia"}

@app.get("/questions/random", response_model=List[QuestionResponse])
async def get_random_questions(
    count: int = 10, 
    difficulty: Optional[DifficultyLevelAPI] = None
):
    global db_manager, questions_cache, current_question_id
    
    questions = []
    
    db_questions = []
    use_local_mode = True
    
    if db_manager and await db_manager.is_database_ready():
        print("Intentando usar base de datos para obtener preguntas")
        db_questions = await db_manager.get_random_questions(count)
        
        # Solo usamos la base de datos si realmente tiene preguntas
        if db_questions and len(db_questions) > 0:
            use_local_mode = False
            print(f"Base de datos disponible, obteniendo {len(db_questions)} preguntas")
        else:
            print("Base de datos vacía, cambiando a modo local")
    else:
        print("Base de datos no disponible, usando modo local")
        
    if not use_local_mode:
        # Usamos las preguntas de la base de datos
        for q in db_questions:
            # Skip if difficulty filter is set and doesn't match
            if difficulty and q.difficulty.value != difficulty:
                continue
                
            question_id = current_question_id
            current_question_id += 1
            
            difficulty_value = q.difficulty.value
            points = q.get_points()
            
            question_data = {
                "id": question_id,
                "description": q.description,
                "options": q.options,
                "difficulty": difficulty_value,
                "points": points
            }
            
            questions_cache[question_id] = {
                "description": q.description,
                "options": q.options,
                "correct_answer": q.correct_answer,
                "difficulty": q.difficulty,
                "points": points
            }
            
            questions.append(question_data)
    else:
        # Modo local - Cargar desde JSON
        print("Usando archivo local para obtener preguntas")
        try:
            # Intentar localizar el archivo questions.json
            json_path = "data/questions.json"
            if not os.path.exists(json_path):
                # Probar ruta relativa desde la raíz del proyecto
                json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')
                print(f"Buscando archivo en: {json_path}")
                
            if not os.path.exists(json_path):
                print(f"ERROR: No se encontró el archivo 'questions.json' en {json_path}")
                # Usar preguntas por defecto
                default_questions = [
                    {
                        "id": current_question_id,
                        "description": "¿Cuál es la capital de Francia?",
                        "options": ["Madrid", "Londres", "París", "Berlín"],
                        "difficulty": "easy",
                        "points": 1
                    }
                ]
                
                questions_cache[current_question_id] = {
                    "description": "¿Cuál es la capital de Francia?",
                    "options": ["Madrid", "Londres", "París", "Berlín"],
                    "correct_answer": "París",
                    "difficulty": DifficultyLevel.EASY,
                    "points": 1
                }
                
                current_question_id += 1
                return default_questions
                
            print(f"Leyendo archivo: {json_path}")
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"Archivo JSON cargado, contiene {len(data.get('questions', []))} preguntas")
                
                all_questions = data.get("questions", [])
                
                # Validar contenido
                if not all_questions:
                    print("ERROR: El archivo JSON no contiene preguntas o tiene un formato incorrecto")
                    # Devolver pregunta por defecto
                    default_question = {
                        "id": current_question_id,
                        "description": "¿Cuál es la capital de Francia?",
                        "options": ["Madrid", "Londres", "París", "Berlín"],
                        "difficulty": "easy",
                        "points": 1
                    }
                    
                    questions_cache[current_question_id] = {
                        "description": "¿Cuál es la capital de Francia?",
                        "options": ["Madrid", "Londres", "París", "Berlín"],
                        "correct_answer": "París",
                        "difficulty": DifficultyLevel.EASY,
                        "points": 1
                    }
                    
                    current_question_id += 1
                    return [default_question]
                
                # Filter by difficulty if specified
                if difficulty:
                    filtered_questions = [q for q in all_questions if q.get("difficulty", "easy").lower() == difficulty.value]
                    if filtered_questions:
                        all_questions = filtered_questions
                        print(f"Filtro por dificultad {difficulty.value}: {len(filtered_questions)} preguntas encontradas")
                    else:
                        print(f"Advertencia: No se encontraron preguntas con dificultad '{difficulty.value}', usando todas las preguntas")
                
                sample_size = min(count, len(all_questions))
                if sample_size == 0:
                    print("ERROR: No hay preguntas disponibles para seleccionar")
                    return []
                    
                print(f"Seleccionando {sample_size} preguntas aleatorias")
                sample_questions = random.sample(all_questions, sample_size)
                
                for q in sample_questions:
                    question_id = current_question_id
                    current_question_id += 1
                    
                    # Convert difficulty string to enum
                    difficulty_str = q.get("difficulty", "easy").lower()
                    q_difficulty = DifficultyLevel.EASY
                    if difficulty_str == "medium" or difficulty_str == "medio":
                        q_difficulty = DifficultyLevel.MEDIUM
                    elif difficulty_str == "hard" or difficulty_str == "difícil" or difficulty_str == "dificil":
                        q_difficulty = DifficultyLevel.HARD
                    
                    points = q_difficulty.get_score_multiplier()
                    
                    question_data = {
                        "id": question_id,
                        "description": q["description"],
                        "options": q["options"],
                        "difficulty": difficulty_str,
                        "points": points
                    }
                    
                    questions_cache[question_id] = {
                        "description": q["description"],
                        "options": q["options"],
                        "correct_answer": q["correct_answer"],
                        "difficulty": q_difficulty,
                        "points": points
                    }
                    
                    questions.append(question_data)
        except Exception as e:
            print(f"ERROR al cargar preguntas desde JSON: {e}")
            # Preguntas por defecto cuando falla todo lo demás
            default_questions = [
                {
                    "id": current_question_id,
                    "description": "¿Cuál es la capital de Francia?",
                    "options": ["Madrid", "Londres", "París", "Berlín"],
                    "difficulty": "easy",
                    "points": 1
                }
            ]
            
            questions_cache[current_question_id] = {
                "description": "¿Cuál es la capital de Francia?",
                "options": ["Madrid", "Londres", "París", "Berlín"],
                "correct_answer": "París",
                "difficulty": DifficultyLevel.EASY,
                "points": 1
            }
            
            current_question_id += 1
            questions = default_questions
    
    print(f"Devolviendo {len(questions)} preguntas")
    return questions

@app.post("/questions/answer", response_model=AnswerResponse)
async def check_answer(answer_request: AnswerRequest):
    global questions_cache, quiz_stats
    
    question_id = answer_request.question_id
    
    if question_id not in questions_cache:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    
    question_data = questions_cache[question_id]
    is_correct = question_data["correct_answer"] == answer_request.answer
    
    question = Question(
        description=question_data["description"],
        options=question_data["options"],
        correct_answer=question_data["correct_answer"],
        difficulty=question_data["difficulty"]
    )
    
    quiz_stats.update_stats(question, is_correct)
    
    points_earned = question_data["points"] if is_correct else 0
    
    return {
        "correct": is_correct,
        "correct_answer": question_data["correct_answer"] if not is_correct else None,
        "points_earned": points_earned
    }

@app.get("/quiz/summary", response_model=QuizSummary)
async def get_quiz_summary():
    global quiz_stats
    
    summary = quiz_stats.get_summary()
    
    difficulty_stats = {}
    for diff, stats in summary["difficulty_stats"].items():
        difficulty_stats[diff.value] = stats
    
    return {
        "total_questions": summary["total_rounds"],
        "correct_answers": summary["correct_answers"],
        "incorrect_answers": summary["incorrect_answers"],
        "total_score": summary["total_score"],
        "accuracy": summary["accuracy"],
        "difficulty_stats": difficulty_stats
    }

@app.post("/quiz/reset")
async def reset_quiz():
    global quiz_stats, questions_cache
    quiz_stats = GameStats()
    questions_cache = {}
    return {"message": "Estadísticas del quiz reiniciadas"} 