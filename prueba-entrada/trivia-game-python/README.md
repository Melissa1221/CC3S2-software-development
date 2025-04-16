# Trivia Game Python

Un juego de trivia en consola desarrollado en Python con soporte para base de datos PostgreSQL y API REST con FastAPI.

## Características

- 30 preguntas de trivia en múltiples categorías
- Niveles de dificultad (fácil, medio, difícil) con sistema de puntuación variable
- Sistema de puntuación y seguimiento de rondas
- Interfaz de consola interactiva mejorada
- Estadísticas detalladas por nivel de dificultad
- Integración con PostgreSQL para almacenar preguntas
- API REST con FastAPI para acceso web
- Soporte para modo offline (fallback local)
- Pipeline CI/CD con GitHub Actions
- Análisis de código con SonarCloud

## Requisitos

- Python 3.10+
- Docker y Docker Compose (para el entorno con base de datos)
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
   ```bash
   cd trivia-game-python
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configuración de variables de entorno:
   - Copiar `.env.example` a `.env`
   - Ajustar las variables según tu entorno

## Ejecución

### Modo Docker (recomendado)

1. Iniciar los contenedores:
   ```bash
   docker-compose up -d
   ```

2. Cargar preguntas en la base de datos:
   ```bash
   docker-compose exec api python -m scripts.load_questions
   ```

3. Ejecutar el juego en consola:
   ```bash
   docker-compose exec api python -m app.main
   ```

4. Acceder a la API (disponible automáticamente):
   - API: http://localhost:8000
   - Documentación: http://localhost:8000/docs

### Modo Local

1. Ejecutar el juego sin Docker:
   ```bash
   python -m app.main
   ```

2. Ejecutar la API sin Docker:
   ```bash
   uvicorn app.api:app --reload
   ```

   > El juego y la API funcionarán en modo local, usando las preguntas predefinidas o el archivo JSON.

## API REST con FastAPI

La API proporciona acceso a todas las funcionalidades del juego y permite crear interfaces web o móviles:

### Endpoints disponibles

- **GET /** - Página de bienvenida
- **GET /questions/random** - Obtiene preguntas aleatorias
  - Parámetros: 
    - count (opcional, default=10)
    - difficulty (opcional, valores: "easy", "medium", "hard")
  - Ejemplo: `/questions/random?count=5&difficulty=medium`
  
- **POST /questions/answer** - Verifica si una respuesta es correcta
  - Body: `{ "question_id": 1, "answer": "París" }`
  - Retorna: `{ "correct": true, "points_earned": 2 }`
  
- **GET /quiz/summary** - Obtiene el resumen del quiz con estadísticas detalladas
  - Retorna: `{ "total_questions": 10, "correct_answers": 7, "incorrect_answers": 3, "total_score": 12, "accuracy": 70.0, "difficulty_stats": {...} }`
  
- **POST /quiz/reset** - Reinicia las estadísticas
  - Retorna: `{ "message": "Estadísticas del quiz reiniciadas" }`

### Uso con curl

```bash
# Obtener preguntas aleatorias de dificultad media
curl -X GET "http://localhost:8000/questions/random?count=3&difficulty=medium"

# Enviar una respuesta
curl -X POST "http://localhost:8000/questions/answer" \
  -H "Content-Type: application/json" \
  -d '{"question_id": 1, "answer": "París"}'

# Obtener resumen
curl -X GET "http://localhost:8000/quiz/summary"
```

## Carga de preguntas en la base de datos

El script `load_questions.py` permite cargar las preguntas desde el archivo JSON a la base de datos:

```bash
# Verificar el archivo JSON sin cargar a la base de datos
python -m scripts.load_questions --local

# Cargar preguntas en la base de datos
python -m scripts.load_questions
```

## Modo de juego

1. El juego selecciona aleatoriamente 10 preguntas de la base de datos o del archivo local.
2. En cada ronda se muestra una pregunta con 4 opciones, su nivel de dificultad y los puntos que vale.
3. El jugador selecciona una respuesta mediante el número correspondiente.
4. Se muestra inmediatamente si la respuesta es correcta o incorrecta.
5. Las preguntas tienen diferentes valores según su dificultad:
   - Fácil: 1 punto
   - Medio: 2 puntos
   - Difícil: 3 puntos
6. Al finalizar todas las rondas, se muestra un resumen detallado con la puntuación total y estadísticas por nivel de dificultad.

## Desarrollo

### Pruebas

```bash
# Ejecutar todas las pruebas
python -m pytest

# Ejecutar pruebas específicas
python -m pytest tests/test_quiz.py
python -m pytest tests/test_difficulty.py

# Ejecutar pruebas de integración
python -m pytest tests/integration/ -v

# Generar informe de cobertura
python -m pytest --cov=app --cov-report=xml --cov-report=term
```

### CI/CD con GitHub Actions

El proyecto incluye un pipeline CI/CD configurado con GitHub Actions que se ejecuta automáticamente al hacer push a las ramas `develop` y `main`:

1. **Pruebas unitarias**: Verifica el funcionamiento correcto de los componentes individuales
2. **Pruebas de integración**: Valida la interacción entre componentes, especialmente la API
3. **Análisis de código**: Utiliza SonarCloud para analizar la calidad del código

Para ver los resultados del CI/CD:
- Ve a la pestaña "Actions" en el repositorio de GitHub
- Consulta el dashboard en SonarCloud (requiere configuración)

### Análisis de código con SonarCloud

Para ejecutar el análisis de código localmente antes de subir cambios:

1. Instala SonarScanner
2. Ejecuta el análisis:
   ```bash
   sonar-scanner \
     -Dsonar.projectKey=trivia-game-python \
     -Dsonar.sources=app \
     -Dsonar.python.coverage.reportPaths=coverage.xml
   ```

### Notas 

- El sistema está diseñado para funcionar tanto con base de datos como en modo local.
- Si la conexión a la base de datos falla, el sistema utilizará automáticamente las preguntas del archivo JSON local.
- El archivo `data/questions.json` contiene 30 preguntas predefinidas en español con distintos niveles de dificultad.
- La documentación interactiva de la API (Swagger UI) facilita las pruebas y el desarrollo.
- Se ha implementado un sistema de normalización de dificultad que permite manejar valores tanto en español como en inglés.
- Para solucionar problemas de importación en las pruebas, utiliza `PYTHONPATH=. python -m pytest`.
