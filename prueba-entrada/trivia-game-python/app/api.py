from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import asyncio
import random
import json

from app.models.question import Question
from app.models.db_manager import DBManager

# Crear la aplicación FastAPI
app = FastAPI(title="Trivia Game API", description="API para el juego de trivia", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class QuestionResponse(BaseModel):
    id: Optional[int] = None
    description: str
    options: List[str]
    
class AnswerRequest(BaseModel):
    question_id: int
    answer: str
    
class AnswerResponse(BaseModel):
    correct: bool
    correct_answer: Optional[str] = None
    
class QuizSummary(BaseModel):
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    accuracy: float

# Variable global para almacenar db_manager
db_manager = None

# Diccionario para almacenar preguntas en memoria para la demostración
questions_cache = {}
current_question_id = 1
quiz_stats = {"correct": 0, "incorrect": 0, "total": 0}

# Evento de inicio
@app.on_event("startup")
async def startup_event():
    global db_manager
    db_manager = DBManager()
    success = await db_manager.connect()
    if not success:
        print("⚠️ No se pudo conectar a la base de datos. Usando modo local.")

# Evento de cierre
@app.on_event("shutdown")
async def shutdown_event():
    global db_manager
    if db_manager:
        await db_manager.disconnect()

# Endpoints
@app.get("/")
async def root():
    return {"message": "Bienvenido a la API del Juego de Trivia"}

@app.get("/questions/random", response_model=List[QuestionResponse])
async def get_random_questions(count: int = 10):
    global db_manager, questions_cache, current_question_id
    
    questions = []
    
    # Intentar obtener preguntas de la base de datos
    if db_manager and await db_manager.is_database_ready():
        db_questions = await db_manager.get_random_questions(count)
        for q in db_questions:
            question_id = current_question_id
            current_question_id += 1
            
            question_data = {
                "id": question_id,
                "description": q.description,
                "options": q.options,
            }
            
            # Almacenar la pregunta en caché con su respuesta correcta
            questions_cache[question_id] = {
                "description": q.description,
                "options": q.options,
                "correct_answer": q.correct_answer
            }
            
            questions.append(question_data)
    else:
        # Usar preguntas locales si no hay base de datos
        # Cargar desde JSON o usar preguntas predefinidas
        try:
            with open("data/questions.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                sample_questions = random.sample(data["questions"], min(count, len(data["questions"])))
                
                for q in sample_questions:
                    question_id = current_question_id
                    current_question_id += 1
                    
                    question_data = {
                        "id": question_id,
                        "description": q["description"],
                        "options": q["options"],
                    }
                    
                    questions_cache[question_id] = {
                        "description": q["description"],
                        "options": q["options"],
                        "correct_answer": q["correct_answer"]
                    }
                    
                    questions.append(question_data)
        except Exception as e:
            # Preguntas predefinidas en caso de error
            default_questions = [
                {
                    "id": current_question_id,
                    "description": "¿Cuál es la capital de Francia?",
                    "options": ["Madrid", "Londres", "París", "Berlín"]
                }
            ]
            
            questions_cache[current_question_id] = {
                "description": "¿Cuál es la capital de Francia?",
                "options": ["Madrid", "Londres", "París", "Berlín"],
                "correct_answer": "París"
            }
            
            current_question_id += 1
            questions = default_questions
    
    return questions

@app.post("/questions/answer", response_model=AnswerResponse)
async def check_answer(answer_request: AnswerRequest):
    global questions_cache, quiz_stats
    
    question_id = answer_request.question_id
    
    if question_id not in questions_cache:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")
    
    question = questions_cache[question_id]
    is_correct = question["correct_answer"] == answer_request.answer
    
    # Actualizar estadísticas
    quiz_stats["total"] += 1
    if is_correct:
        quiz_stats["correct"] += 1
    else:
        quiz_stats["incorrect"] += 1
    
    return {
        "correct": is_correct,
        "correct_answer": question["correct_answer"] if not is_correct else None
    }

@app.get("/quiz/summary", response_model=QuizSummary)
async def get_quiz_summary():
    global quiz_stats
    
    total = quiz_stats["total"]
    correct = quiz_stats["correct"]
    accuracy = (correct / total) * 100 if total > 0 else 0
    
    return {
        "total_questions": total,
        "correct_answers": correct,
        "incorrect_answers": quiz_stats["incorrect"],
        "accuracy": accuracy
    }

@app.post("/quiz/reset")
async def reset_quiz():
    global quiz_stats
    quiz_stats = {"correct": 0, "incorrect": 0, "total": 0}
    return {"message": "Estadísticas del quiz reiniciadas"} 