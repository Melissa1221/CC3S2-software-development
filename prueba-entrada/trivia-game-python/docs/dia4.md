# Día 4 - Sistema de Puntuación y Rondas de Juego

## Objetivos Completados
- Implementación del sistema de puntuación
- Gestión de rondas de juego
- Lógica de finalización del juego
- Pruebas unitarias para el sistema de puntuación
- Integración con base de datos PostgreSQL
- Carga de preguntas desde JSON a la base de datos
- Implementación de API REST con FastAPI

## Mejoras Realizadas

### 1. Actualización de la Clase Quiz
Se ha mejorado la clase `Quiz` con funcionalidades de puntuación:

```python
class Quiz:
    def __init__(self):
        self.questions = []
        self.current_question_index = 0
        self.correct_answers = 0
        self.incorrect_answers = 0

    def answer_question(self, question, answer):
        if question.is_correct(answer):
            self.correct_answers += 1
            return True
        else:
            self.incorrect_answers += 1
            return False
            
    def get_score(self):
        return {
            'correct': self.correct_answers,
            'incorrect': self.incorrect_answers,
            'total': len(self.questions)
        }
```

Esta mejora permite:
- Mantener el conteo de respuestas correctas e incorrectas
- Calcular y proporcionar información de puntuación

### 2. Implementación de Rondas de Juego
Se ha actualizado `GameManager` para manejar rondas de juego:

```python
class GameManager:
    def __init__(self):
        self.quiz = Quiz()
        self.total_rounds = 10
        self.current_round = 0

    # ...

    def run_game(self):
        self.load_questions()
        while self.current_round < self.total_rounds:
            question = self.quiz.get_next_question()
            if not question:
                break
            self.play_round(question)
            self.current_round += 1
        self.show_final_score()
```

Estas mejoras permiten:
- Limitar el número de rondas
- Gestionar el progreso del juego
- Visualizar el avance por rondas

### 3. Mejora de la Interfaz de Consola
Se ha actualizado `ConsoleInterface` para mostrar información de rondas y puntuación:

```python
class ConsoleInterface:
    
    def display_round(self, round_number, total_rounds):
        print(f"\nRonda {round_number} de {total_rounds}")
        print("-" * 40)
            
    def display_score(self, score):
        print("\nPuntuación actual:")
        print(f"Respuestas correctas: {score['correct']}")
        print(f"Respuestas incorrectas: {score['incorrect']}")
            
    def display_final_score(self, score):
        print("\n¡Juego terminado!")
        print("=" * 40)
        print(f"Total de preguntas: {score['total']}")
        print(f"Respuestas correctas: {score['correct']}")
        print(f"Respuestas incorrectas: {score['incorrect']}")
        print(f"Precisión: {(score['correct']/score['total'])*100:.1f}%")
```

### 4. Pruebas Unitarias
Se han implementado pruebas para validar el sistema de puntuación:

```python
def test_quiz_scoring():
    quiz = Quiz()
    question = Question("Test?", ["1", "2", "3", "4"], "1")
    quiz.add_question(question)
    
    assert quiz.answer_question(question, "1") == True
    assert quiz.correct_answers == 1
    assert quiz.incorrect_answers == 0
    
    assert quiz.answer_question(question, "2") == False
    assert quiz.correct_answers == 1
    assert quiz.incorrect_answers == 1
```

### 5. Integración con Base de Datos PostgreSQL

Se ha implementado la integración con PostgreSQL para almacenar y recuperar preguntas de trivia:

```python
class DBManager:
    def __init__(self):
        self.database = Database(DATABASE_URL) if DATABASE_URL else None
        self.connected = False
        
    async def get_random_questions(self, limit=10):
        query = """
            SELECT q.id, q.description, q.options, q.correct_answer, c.name as category, q.difficulty
            FROM questions q
            JOIN categories c ON q.category_id = c.id
            ORDER BY RANDOM()
            LIMIT :limit
        """
        
```

Las principales características implementadas son:

- **Carga de preguntas desde JSON**: Se creó un script para cargar preguntas desde un archivo JSON a la base de datos.
- **Gestión de categorías**: Las preguntas se organizan en categorías para futura expansión del juego.
- **Selección aleatoria**: El juego selecciona 10 preguntas aleatorias de la base de datos.
- **Fallback mode**: Si no hay conexión a la base de datos, el juego funciona con preguntas locales.

#### Script de Carga de Datos

Se creó un script `load_questions.py` que:

1. Crea las tablas necesarias en PostgreSQL
2. Carga las categorías únicas
3. Inserta las preguntas con sus opciones y respuestas correctas
4. Maneja errores graciosamente

#### Modo de Operación Dual

El juego ahora opera en dos modos:

- **Modo con base de datos**: Selecciona preguntas aleatorias de PostgreSQL.
- **Modo local**: Usa preguntas del archivo JSON o preguntas predefinidas en el código si no hay JSON disponible.

### 6. API REST con FastAPI

Se ha implementado una API REST con FastAPI para exponer las funcionalidades del juego como servicio web:

```python
app = FastAPI(title="Trivia Game API", description="API para el juego de trivia", version="1.0.0")

@app.get("/questions/random", response_model=List[QuestionResponse])
async def get_random_questions(count: int = 10):
    
@app.post("/questions/answer", response_model=AnswerResponse)
async def check_answer(answer_request: AnswerRequest):
    
@app.get("/quiz/summary", response_model=QuizSummary)
async def get_quiz_summary():
```

La API proporciona los siguientes endpoints:

- **GET /questions/random**: Obtiene un número de preguntas aleatorias (por defecto 10)
- **POST /questions/answer**: Verifica si una respuesta es correcta
- **GET /quiz/summary**: Obtiene un resumen del quiz con estadísticas
- **POST /quiz/reset**: Reinicia las estadísticas del quiz

Esta implementación permite:
- Acceder al juego de trivia desde aplicaciones web o móviles
- Mantener estadísticas de juego entre sesiones
- Separar la lógica de negocio de la interfaz de usuario
- Proporcionar un servicio escalable para múltiples clientes

## Estado Actual
- Sistema de puntuación completo y funcional
- Gestión de rondas implementada
- Interfaz mejorada con información de progreso
- Tests para validar el funcionamiento del sistema de puntuación
- Integración con PostgreSQL operativa
- Banco de 30 preguntas en múltiples categorías
- API REST con FastAPI implementada y funcional

## Reglas de Puntuación
- Cada respuesta correcta suma un punto
- Las respuestas incorrectas se contabilizan pero no restan puntos
- Al final se muestra un resumen con estadísticas y porcentaje de aciertos

## Notas Técnicas
- Las pruebas se pueden ejecutar con `pytest`
- El juego ahora muestra información de la ronda actual
- Se visualiza la puntuación tras cada respuesta
- Al finalizar se muestra un resumen completo con estadísticas
- Para cargar preguntas en la base de datos: `python -m scripts.load_questions`
- Para verificar solo el archivo JSON: `python -m scripts.load_questions --local`
- La API FastAPI se ejecuta en el puerto 8000: http://localhost:8000
- Documentación interactiva de la API disponible en: http://localhost:8000/docs 