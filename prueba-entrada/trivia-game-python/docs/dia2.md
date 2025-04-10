# Día 2 - Implementación de la clase Question y Pruebas Unitarias

## Tareas Realizadas

### 1. Implementación de la Clase Question
Se ha implementado la clase `Question` en el archivo `app/trivia.py` con las siguientes características:
- Constructor que recibe descripción, opciones y respuesta correcta
- Método `is_correct()` para validar si una respuesta es correcta

```python
class Question:
    def __init__(self, description, options, correct_answer):
        self.description = description
        self.options = options
        self.correct_answer = correct_answer

    def is_correct(self, answer):
        return self.correct_answer == answer
```

### 2. Configuración de Pruebas Unitarias
Se han implementado pruebas unitarias para la clase `Question` en el archivo `tests/test_trivia.py`:
- Prueba para verificar respuestas correctas
- Prueba para verificar respuestas incorrectas

```python
import pytest
from app.trivia import Question

def test_question_correct_answer():
    question = Question("What is 2 + 2?", ["1", "2", "3", "4"], "4")
    assert question.is_correct("4")

def test_question_incorrect_answer():
    question = Question("What is 2 + 2?", ["1", "2", "3", "4"], "4")
    assert not question.is_correct("2")
```

### 3. Actualización de Dependencias
Se ha actualizado el archivo `requirements.txt` para incluir pytest como dependencia:
- pytest>=8.3.0

### 4. Actualización del Archivo __init__.py
Se ha actualizado el archivo `app/__init__.py` para exponer la clase Question:
```python
from app.trivia import Question
```

### 5. Gestión de Git
Se ha creado una nueva rama para el desarrollo del día 2:
- feature/day2

## Estado Actual
- Clase Question implementada y funcional
- Pruebas unitarias implementadas y pasando correctamente
- Estructura de proyecto actualizada para soportar la clase Question
- Dependencias actualizadas para incluir pytest

## Notas Técnicas
- Las pruebas se pueden ejecutar con el comando: `python -m pytest tests/test_trivia.py -v`
- La implementación sigue el enfoque de desarrollo basado en pruebas (TDD) 