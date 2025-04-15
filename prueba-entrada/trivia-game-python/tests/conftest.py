import pytest
import asyncio
import os
from dotenv import load_dotenv
from app.models.db_manager import DBManager

load_dotenv()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def db_manager():
    manager = DBManager()
    if os.getenv("DATABASE_URL"):
        connected = await manager.connect()
        if not connected:
            pytest.skip("No se pudo conectar a la base de datos de pruebas")
    else:
        pytest.skip("No hay URL de base de datos configurada para pruebas")
        
    yield manager
    
    await manager.disconnect()

@pytest.fixture(scope="session")
def test_data():
    return {
        "sample_question": {
            "description": "¿Cuál es la capital de Francia?",
            "options": ["Madrid", "Londres", "París", "Berlín"],
            "correct_answer": "París",
            "difficulty": "easy"
        }
    } 