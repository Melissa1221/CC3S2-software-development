# Día 5 - Mejoras de Interfaz y Niveles de Dificultad

## Objetivos Completados
- Implementación de niveles de dificultad
- Mejora de la interfaz de usuario
- Sistema de puntuación basado en dificultad
- Estadísticas detalladas del juego
- Adaptación de la API para incluir dificultad

## Mejoras Realizadas

### 1. Niveles de Dificultad
Se ha implementado un sistema de niveles de dificultad usando Enum de Python:

```python
class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    def get_score_multiplier(self):
        return {
            DifficultyLevel.EASY: 1,
            DifficultyLevel.MEDIUM: 2,
            DifficultyLevel.HARD: 3
        }[self]
```

Esto permite:
- Categorizar preguntas por su nivel de dificultad
- Asignar puntos variables según la dificultad (fácil: 1 punto, medio: 2 puntos, difícil: 3 puntos)
- Filtrar preguntas por dificultad en la API

### 2. Clase Question Mejorada
Se ha actualizado la clase `Question` para incluir dificultad:

```python
class Question:
    def __init__(self, description, options, correct_answer, difficulty=DifficultyLevel.EASY):
        self.description = description
        self.options = options
        self.correct_answer = correct_answer
        self.difficulty = difficulty

    def get_points(self):
        return self.difficulty.get_score_multiplier()
```

Estas mejoras permiten:
- Asignar un nivel de dificultad a cada pregunta
- Calcular la puntuación basada en la dificultad

### 3. Estadísticas Detalladas
Se ha creado una nueva clase `GameStats` para gestionar estadísticas avanzadas:

```python
class GameStats:
    def __init__(self):
        self.total_rounds = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.total_score = 0
        self.difficulty_stats = {
            DifficultyLevel.EASY: {'correct': 0, 'total': 0},
            DifficultyLevel.MEDIUM: {'correct': 0, 'total': 0},
            DifficultyLevel.HARD: {'correct': 0, 'total': 0}
        }
```

La clase permite:
- Rastrear estadísticas por nivel de dificultad
- Calcular la puntuación total teniendo en cuenta el valor de cada pregunta
- Proporcionar un resumen detallado del rendimiento del jugador

### 4. Mejora de la Interfaz de Usuario
Se ha actualizado `ConsoleInterface` con una mejor experiencia de usuario:

```python
def display_welcome(self):
    print("=" * 50)
    print("¡Bienvenido al juego de Trivia!")
    print("=" * 50)
    print("\nReglas:")
    print("1. Responderás 10 preguntas")
    print("2. Cada pregunta tiene 4 opciones")
    print("3. Los puntos dependen del nivel de dificultad")
    

def display_question(self, question, question_number):
    print(f"\nPregunta {question_number}: {question.description}")
    print(f"Dificultad: {question.difficulty.value.upper()}")
    print(f"Puntos: {question.get_points()}")
  
```

Las mejoras incluyen:
- Pantalla de bienvenida con reglas del juego
- Visualización de la dificultad y puntos para cada pregunta
- Resumen final detallado con estadísticas por nivel de dificultad

### 5. Actualización de la API REST
Se ha adaptado la API para soportar niveles de dificultad:

```python
@app.get("/questions/random", response_model=List[QuestionResponse])
async def get_random_questions(
    count: int = 10, 
    difficulty: Optional[DifficultyLevelAPI] = None
):
    
```

Cambios destacados:
- Filtrado de preguntas por dificultad
- Inclusión de información de puntos en las respuestas
- Estadísticas detalladas en el resumen del quiz

### 6. Pruebas Unitarias
Se han implementado pruebas para validar la nueva funcionalidad:

```python
def test_difficulty_score_multipliers():
    assert DifficultyLevel.EASY.get_score_multiplier() == 1
    assert DifficultyLevel.MEDIUM.get_score_multiplier() == 2
    assert DifficultyLevel.HARD.get_score_multiplier() == 3

def test_game_stats_update_stats():
    stats = GameStats()
    q_medium = Question("Test?", ["1", "2", "3", "4"], "1", DifficultyLevel.MEDIUM)
    stats.update_stats(q_medium, True)
    assert stats.total_score == 2  
```

## Estado Actual
- Sistema de puntuación basado en dificultad implementado
- Interfaz de usuario mejorada con información más detallada
- API REST actualizada para soportar niveles de dificultad
- Estadísticas detalladas por nivel de dificultad
- Pruebas unitarias para validar la nueva funcionalidad

