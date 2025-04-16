# Día 6: Pipeline CI/CD y Pruebas de Integración

## Objetivos
- Configurar GitHub Actions para ejecutar pruebas unitarias e integración.
- Integrar análisis de código estático con SonarCloud.
- Implementar pruebas de integración para la API de FastAPI.
- Documentar el pipeline y el proceso de configuración.

## Implementación del Pipeline CI/CD

### 1. Configuración de GitHub Actions

Se creó el archivo `.github/workflows/ci.yml` para definir el flujo de trabajo de integración continua:

```yaml
name: Python CI

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  build:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: trivia_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run unit tests
        run: pytest tests/unit/ --cov=app
        
      - name: Run integration tests
        run: |
          cp .env.example .env
          echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/trivia_test" >> .env
          pytest tests/integration/
          
      - name: SonarQube Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        with:
          args: >
            -Dsonar.projectKey=trivia-game-python
            -Dsonar.organization=nombre-organizacion
            -Dsonar.sources=app
            -Dsonar.python.coverage.reportPaths=coverage.xml
            -Dsonar.python.xunit.reportPath=junit-report.xml
```

El workflow define:
- Los eventos que activan el pipeline (push/PR a las ramas develop y main)
- Configuración del servicio PostgreSQL para pruebas
- Instalación de dependencias necesarias
- Ejecución de pruebas unitarias y de integración
- Análisis de código con SonarCloud

### 2. Configuración de SonarCloud

Se creó el archivo `sonar-project.properties` para definir la configuración del análisis de código:

```properties
sonar.projectKey=trivia-game-python
sonar.organization=nombre-de-la-organizacion

# Ruta del codigo fuente
sonar.sources=app
sonar.tests=tests

# Rutas de los informes de cobertura de código
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.xunit.reportPath=junit-report.xml

# Exclusiones
sonar.exclusions=**/tests/**,**/__pycache__/**

# Codificación
sonar.sourceEncoding=UTF-8
```

## Pruebas de Integración

Se implementaron pruebas de integración para la API REST usando el TestClient de FastAPI:

```python
# tests/integration/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.models.difficulty import DifficultyLevel
from app.models.game_stats import GameStats
import app.api as api_module

# Inicializar las variables globales que necesitan las pruebas
api_module.quiz_stats = GameStats()

client = TestClient(app)

def test_welcome_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Bienvenido" in response.json()["message"]

```

Se verifican:
- El funcionamiento del endpoint de bienvenida
- La obtención de preguntas aleatorias
- El filtrado de preguntas por dificultad
- El envío y validación de respuestas
- La obtención del resumen del quiz
- El reinicio del quiz

## Mejoras Implementadas

### 1. Normalización de Dificultad

Se agregó una función para normalizar los valores de dificultad entre español e inglés:

```python
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
```

### 2. Actualización a Lifespan de FastAPI

Se modernizó el código para usar el sistema de lifespan de FastAPI en lugar de los métodos obsoletos on_event:

```python
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
```

## Configuración


1. Configurar un token en SonarCloud y agregarlo como secreto `SONAR_TOKEN` en GitHub.
2. Modificar los valores de `sonar.organization` y `sonar.projectKey` según corresponda.
3. Ejecutar localmente las pruebas de integración:
   ```bash
   # Asegúrate de estar en el directorio raíz del proyecto
   python -m pytest tests/integration/ -v
   ```
4. Generar informes de cobertura:
   ```bash
   # Este comando funciona independientemente de la estructura de módulos
   python -m pytest --cov=app --cov-report=xml --cov-report=term
   ```
5. Si tienes problemas con las importaciones de módulos, puedes usar:
   ```bash
   PYTHONPATH=. python -m pytest tests/integration/
   ``` 