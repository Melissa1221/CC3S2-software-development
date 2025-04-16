from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import random
import secrets
import json
from enum import Enum
import os
from contextlib import asynccontextmanager

from app.models.question import Question
from app.models.db_manager import DBManager
from app.models.difficulty import DifficultyLevel
from app.models.game_stats import GameStats

db_manager = None
questions_cache = {}
current_question_id = 1
quiz_stats = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_manager, quiz_stats
    print("Iniciando aplicación...")
    db_manager = DBManager()
    quiz_stats = GameStats()
    success = await db_manager.connect()
    if not success:
        print("⚠️ No se pudo conectar a la base de datos. Usando modo local.")
    
    yield  
    
    print("Cerrando aplicación...")
    if db_manager:
        await db_manager.disconnect()

app = FastAPI(
    title="Trivia Game API", 
    description="API para el juego de trivia", 
    version="1.0.0",
    lifespan=lifespan
)

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

def normalize_difficulty(difficulty_str: str) -> str:
    difficulty_map = {
        "fácil": "easy",
        "facil": "easy",
        "medio": "medium",
        "difícil": "hard", 
        "dificil": "hard",
        "easy": "easy",
        "medium": "medium", 
        "hard": "hard"
    }
    normalized = difficulty_str.lower() if difficulty_str else "easy"
    return difficulty_map.get(normalized, "easy")

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
        
        if db_questions and len(db_questions) > 0:
            use_local_mode = False
            print(f"Base de datos disponible, obteniendo {len(db_questions)} preguntas")
        else:
            print("Base de datos vacía, cambiando a modo local")
    else:
        print("Base de datos no disponible, usando modo local")
        
    if not use_local_mode:
        for q in db_questions:
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
        print("Usando archivo local para obtener preguntas")
        try:
            json_path = "data/questions.json"
            if not os.path.exists(json_path):
                json_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')
                print(f"Buscando archivo en: {json_path}")
                
            if not os.path.exists(json_path):
                print(f"ERROR: No se encontró el archivo 'questions.json' en {json_path}")
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
                
                if not all_questions:
                    print("ERROR: El archivo JSON no contiene preguntas o tiene un formato incorrecto")
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
                
                if len(all_questions) > count:
                    print(f"Seleccionando {count} preguntas aleatorias")
                    indices = set()
                    while len(indices) < count:
                        indices.add(secrets.randbelow(len(all_questions)))
                    
                    selected_questions = [all_questions[i] for i in indices]
                    all_questions = selected_questions
                
                if difficulty:
                    all_questions = [q for q in all_questions if normalize_difficulty(q.get("difficulty", "")) == difficulty]
                
                print(f"Devolviendo {len(all_questions)} preguntas")
                for q_data in all_questions:
                    question_id = current_question_id
                    current_question_id += 1
                    
                    difficulty_normalized = normalize_difficulty(q_data.get("difficulty", "easy"))
                    
                    points = 1
                    if difficulty_normalized == "medium":
                        points = 2
                    elif difficulty_normalized == "hard":
                        points = 3
                    
                    question_response = {
                        "id": question_id,
                        "description": q_data["description"],
                        "options": q_data["options"],
                        "difficulty": difficulty_normalized,
                        "points": points
                    }
                    
                    difficulty_level = DifficultyLevel.EASY
                    if difficulty_normalized == "medium":
                        difficulty_level = DifficultyLevel.MEDIUM
                    elif difficulty_normalized == "hard":
                        difficulty_level = DifficultyLevel.HARD
                        
                    questions_cache[question_id] = {
                        "description": q_data["description"],
                        "options": q_data["options"],
                        "correct_answer": q_data["correct_answer"],
                        "difficulty": difficulty_level,
                        "points": points
                    }
                    
                    questions.append(question_response)
        except Exception as e:
            print(f"ERROR al cargar preguntas desde JSON: {e}")
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