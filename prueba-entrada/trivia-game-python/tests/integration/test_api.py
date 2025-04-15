import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.models.difficulty import DifficultyLevel
from app.models.game_stats import GameStats
import app.api as api_module  # Importar el módulo para acceder a variables globales

# Inicializar las variables globales que necesitan las pruebas
api_module.quiz_stats = GameStats()

client = TestClient(app)

def test_welcome_endpoint():
    """Prueba que el endpoint de bienvenida responda correctamente"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Bienvenido" in response.json()["message"]

def test_get_random_questions():
    """Prueba que se puedan obtener preguntas aleatorias"""
    response = client.get("/questions/random?count=3")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "description" in data[0]
    assert "options" in data[0]
    # No validamos el valor exacto de difficulty porque puede variar entre "easy", "medium", "hard"
    # o sus equivalentes en español "fácil", "medio", "difícil"
    assert "difficulty" in data[0]

def test_get_random_questions_with_difficulty():
    """Prueba que se puedan filtrar preguntas por dificultad"""
    response = client.get("/questions/random?count=2&difficulty=easy")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:  # Pueden no existir preguntas de esa dificultad
        assert data[0]["difficulty"] == "easy"

def test_answer_question():
    """Prueba que se pueda responder a una pregunta"""
    # Primero obtenemos una pregunta
    response = client.get("/questions/random?count=1")
    assert response.status_code == 200
    data = response.json()
    
    if len(data) == 0:
        pytest.skip("No hay preguntas disponibles para probar")
    
    question = data[0]
    question_id = question["id"]
    
    # Ahora enviamos una respuesta (correcta o incorrecta, no importa para la integración)
    answer = question["options"][0]
    response = client.post(
        "/questions/answer",
        json={"question_id": question_id, "answer": answer}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "correct" in result
    assert isinstance(result["correct"], bool)
    assert "points_earned" in result

def test_get_quiz_summary():
    """Prueba que se pueda obtener el resumen del quiz"""
    response = client.get("/quiz/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_questions" in data
    assert "correct_answers" in data
    assert "incorrect_answers" in data
    assert "total_score" in data
    assert "accuracy" in data
    assert "difficulty_stats" in data

def test_reset_quiz():
    """Prueba que se pueda reiniciar el quiz"""
    response = client.post("/quiz/reset")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data 