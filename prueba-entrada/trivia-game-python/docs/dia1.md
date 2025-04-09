# Día 1 - Configuración del Proyecto y Estructura Básica

## Tareas Realizadas

### 1. Configuración del Entorno del Proyecto
Estructura del directorio del proyecto creada:
```
trivia-game-python/
├── app/
│   ├── __init__.py
│   
├── tests/
│   └── __init__.py
├── docs/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── .env                 
└── .env.example         
```

### 2. Configuración de Variables de Entorno
Archivos de configuración creados:
- `.env`: Archivo con las variables de entorno reales (no versionado)
  ```
  POSTGRES_USER=trivia_user
  POSTGRES_PASSWORD=trivia_password
  POSTGRES_DB=trivia_db
  DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
  ```

- `.env.example`: Plantilla para otros desarrolladores
  ```
  POSTGRES_USER=your_user
  POSTGRES_PASSWORD=your_password
  POSTGRES_DB=your_db_name
  DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
  ```

### 3. Configuración de Dependencias
Archivo requirements.txt creado con las siguientes dependencias:
- fastapi>=0.109.0
- uvicorn>=0.27.0
- asyncpg>=0.29.0
- databases>=0.8.0

### 4. Configuración de Docker
Dockerfile creado con:
- Imagen base Python 3.13 (Esto dado a que las versiones anteriores tenían problemas de vulnerabilidad)
- Instalación de dependencias
- Configuración del directorio de trabajo
- Configuración del punto de entrada

docker-compose.yml configurado con:
- Servicio PostgreSQL
- Servicio FastAPI
- Configuración de red entre servicios
- Variables de entorno establecidas

### 5. Configuración de Git
Archivos de Git configurados:
- .gitignore con exclusiones para:
  - Archivos específicos de Python
  - Entornos virtuales
  - IDE
  - Archivos de Docker

Estructura de ramas:
- feature/day1

## Estado Actual
- Contenedor de PostgreSQL funcionando en puerto 5432
- Servicio FastAPI funcionando en puerto 8000
- Comunicación establecida entre servicios
- Estructura base del proyecto lista para desarrollo

![[/images/docker-running.png]]

## Notas Técnicas
- Base de datos PostgreSQL accesible con:
  - Usuario: trivia_user
  - Base de datos: trivia_db
  - Puerto: 5432
- API FastAPI accesible en:
  - http://localhost:8000
  - Documentación API: http://localhost:8000/docs 