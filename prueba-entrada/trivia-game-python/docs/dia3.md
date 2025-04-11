# Día 3 - Implementación de la Clase Quiz y Flujo Básico del Juego

## Objetivos Completados
-  Implementación de la clase `Quiz`
-  Refactorización de la estructura del proyecto a modelo MVC
-  Creación del flujo básico del juego
-  Integración de clases `Question` y `Quiz`
-  Implementación de la interfaz de consola
-  Pruebas unitarias para la clase `Quiz`

## Refactorización de la Estructura del Proyecto

Se realizó una importante refactorización del proyecto, moviendo de una estructura básica a una arquitectura más organizada basada en modelos:

- Se creó el directorio `app/models/` para almacenar los modelos del juego
- Se movió la clase `Question` desde `app/trivia.py` a `app/models/question.py`
- Se eliminaron los archivos originales tras la migración (`trivia.py`, `test_trivia.py`)
- Se actualizó el archivo `app/__init__.py` para reflejar la nueva estructura

Esta refactorización permite una mejor separación de responsabilidades y facilita el mantenimiento futuro.

## Implementación de la Clase Quiz

Se implementó la clase `Quiz` en `app/models/quiz.py` con las siguientes funcionalidades:

```python
class Quiz:
    def __init__(self):
        self.questions = []
        self.current_question_index = 0

    def add_question(self, question):
        self.questions.append(question)

    def get_next_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.current_question_index += 1
            return question
        return None
```

La clase `Quiz` gestiona una colección de preguntas y proporciona métodos para:
- Añadir nuevas preguntas
- Obtener la siguiente pregunta (manteniendo un índice interno)
- Controlar cuando se ha llegado al final de las preguntas

## Implementación del Administrador del Juego

Se implementó la clase `GameManager` en `app/game_manager.py` para manejar la lógica del juego:

- Creación y carga de preguntas de ejemplo
- Procesamiento de respuestas del usuario
- Seguimiento de la puntuación (respuestas correctas e incorrectas)
- Generación de resumen del juego

## Implementación de la Interfaz de Consola

Se creó la clase `ConsoleInterface` en `app/console_interface.py` para gestionar todas las interacciones con el usuario:

- Mostrar mensaje de bienvenida
- Presentar preguntas y opciones
- Recibir respuestas del usuario
- Mostrar resultados (correcto/incorrecto)
- Presentar el resumen final

## Pruebas Unitarias

Se implementaron pruebas exhaustivas para la clase `Quiz` en `tests/test_quiz.py`:

- Verificación de la creación de un objeto Quiz
- Pruebas de adición de preguntas
- Pruebas para obtener la siguiente pregunta
- Manejo de casos límite (Quiz vacío, fin de preguntas)

## Ejecución del Juego

Se creó un punto de entrada principal en `app/main.py` que:
- Inicializa el administrador del juego
- Crea la interfaz de consola
- Ejecuta el flujo completo del juego
