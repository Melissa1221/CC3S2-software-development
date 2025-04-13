# Trivia Game Python

Un juego de trivia en consola desarrollado en Python con soporte para base de datos PostgreSQL y API REST con FastAPI.

## Características

- 30 preguntas de trivia en múltiples categorías
- Sistema de puntuación y seguimiento de rondas
- Interfaz de consola interactiva
- Integración con PostgreSQL para almacenar preguntas
- API REST con FastAPI para acceso web
- Soporte para modo offline (fallback local)

## Requisitos

- Python 3.10+
- Docker y Docker Compose (para el entorno con base de datos)
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone <repositorio>
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
  - Parámetros: count (opcional, default=10)
  - Ejemplo: `/questions/random?count=5`
  
- **POST /questions/answer** - Verifica si una respuesta es correcta
  - Body: `{ "question_id": 1, "answer": "París" }`
  - Retorna: `{ "correct": true }`
  
- **GET /quiz/summary** - Obtiene el resumen del quiz
  - Retorna: `{ "total_questions": 10, "correct_answers": 7, "incorrect_answers": 3, "accuracy": 70.0 }`
  
- **POST /quiz/reset** - Reinicia las estadísticas
  - Retorna: `{ "message": "Estadísticas del quiz reiniciadas" }`

### Uso con curl

```bash
# Obtener preguntas aleatorias
curl -X GET "http://localhost:8000/questions/random?count=3"

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

## Estructura del proyecto

```
trivia-game-python/
├── app/                    # Código principal
│   ├── models/             # Modelos de datos
│   │   ├── question.py     # Clase Question
│   │   ├── quiz.py         # Clase Quiz
│   │   └── db_manager.py   # Gestor de base de datos
│   ├── main.py             # Punto de entrada (consola)
│   ├── api.py              # API REST con FastAPI
│   ├── game_manager.py     # Lógica del juego
│   └── console_interface.py # Interfaz de consola
├── data/
│   └── questions.json      # Banco de preguntas
├── tests/                  # Pruebas unitarias
├── scripts/
│   └── load_questions.py   # Script para cargar preguntas
├── docs/                   # Documentación
├── .env.example            # Plantilla de variables de entorno
├── requirements.txt        # Dependencias
├── Dockerfile              # Configuración de Docker
└── docker-compose.yml      # Configuración de Docker Compose
```

## Modo de juego

1. El juego selecciona aleatoriamente 10 preguntas de la base de datos o del archivo local.
2. En cada ronda se muestra una pregunta con 4 opciones.
3. El jugador selecciona una respuesta mediante el número correspondiente.
4. Se muestra inmediatamente si la respuesta es correcta o incorrecta.
5. Al finalizar todas las rondas, se muestra un resumen con la puntuación.

## Desarrollo

### Pruebas

```bash
# Ejecutar todas las pruebas
python -m pytest

# Ejecutar pruebas específicas
python -m pytest tests/test_quiz.py
python -m pytest tests/test_scoring.py
```

### Notas para desarrolladores

- El sistema está diseñado para funcionar tanto con base de datos como en modo local.
- Si la conexión a la base de datos falla, el sistema utilizará automáticamente las preguntas del archivo JSON local.
- El archivo `data/questions.json` contiene 30 preguntas predefinidas en español.
- La documentación interactiva de la API (Swagger UI) facilita las pruebas y el desarrollo.
