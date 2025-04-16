import unittest
import json
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
import pytest
from databases import Database

from app.models.db_manager import DBManager
from app.models.question import Question
from app.models.difficulty import DifficultyLevel

class TestDBManager(unittest.TestCase):
    def setUp(self):
        self.mock_database = MagicMock(spec=Database)
   
        self.mock_database.connect = AsyncMock()
        self.mock_database.disconnect = AsyncMock()
        self.mock_database.fetch_all = AsyncMock()
        self.mock_database.fetch_one = AsyncMock()
        
        self.db_url_patcher = patch('app.models.db_manager.DATABASE_URL', 'mock_url')
        self.db_url_patcher.start()
       
        self.db_patcher = patch('app.models.db_manager.Database', return_value=self.mock_database)
        self.db_patcher.start()
       
        self.db_manager = DBManager()
    
    def tearDown(self):
        self.db_url_patcher.stop()
        self.db_patcher.stop()
    
    @pytest.mark.asyncio
    async def test_connect_success(self):
        result = await self.db_manager.connect()
        
        self.mock_database.connect.assert_called_once()
        self.assertTrue(result)
        self.assertTrue(self.db_manager.connected)
    
    @pytest.mark.asyncio
    async def test_connect_failure(self):
        self.mock_database.connect.side_effect = Exception("Connection error")
        
        result = await self.db_manager.connect()
        
        self.mock_database.connect.assert_called_once()
        self.assertFalse(result)
        self.assertFalse(self.db_manager.connected)
    
    @pytest.mark.asyncio
    async def test_disconnect(self):
        self.db_manager.connected = True
        
        await self.db_manager.disconnect()
        
        self.mock_database.disconnect.assert_called_once()
        self.assertFalse(self.db_manager.connected)
    
    @pytest.mark.asyncio
    async def test_get_random_questions_connected(self):
        self.db_manager.connected = True
        
        mock_results = [
            {
                "id": 1,
                "description": "¿Cuál es la capital de Francia?",
                "options": json.dumps(["Madrid", "París", "Roma", "Berlín"]),
                "correct_answer": 2,
                "difficulty": "medium"
            },
            {
                "id": 2,
                "description": "¿Cuál es el río más largo del mundo?",
                "options": json.dumps(["Nilo", "Amazonas", "Misisipi", "Yangtsé"]),
                "correct_answer": 1,
                "difficulty": "easy"
            }
        ]
        self.mock_database.fetch_all.return_value = mock_results
        
        questions = await self.db_manager.get_random_questions(limit=2)
        
        self.mock_database.fetch_all.assert_called_once()
        call_args = self.mock_database.fetch_all.call_args[0][1]
        self.assertEqual(call_args, {"limit": 2})
        
        self.assertEqual(len(questions), 2)
        self.assertIsInstance(questions[0], Question)
        self.assertEqual(questions[0].description, "¿Cuál es la capital de Francia?")
        self.assertEqual(questions[0].difficulty, DifficultyLevel.MEDIUM)
        
        self.assertIsInstance(questions[1], Question)
        self.assertEqual(questions[1].difficulty, DifficultyLevel.EASY)
    
    @pytest.mark.asyncio
    async def test_get_random_questions_not_connected(self):
        self.db_manager.connected = False
        
        questions = await self.db_manager.get_random_questions()
        
        self.mock_database.fetch_all.assert_not_called()
        
        self.assertEqual(questions, [])
    
    @pytest.mark.asyncio
    async def test_question_count_connected(self):
        self.db_manager.connected = True
        
        self.mock_database.fetch_one.return_value = {"count": 42}
        
        count = await self.db_manager.question_count()
        
        self.mock_database.fetch_one.assert_called_once()
        
        self.assertEqual(count, 42)
    
    @pytest.mark.asyncio
    async def test_question_count_not_connected(self):
        self.db_manager.connected = False
        
        count = await self.db_manager.question_count()
        
        self.mock_database.fetch_one.assert_not_called()
        
        self.assertEqual(count, 0)
    
    @pytest.mark.asyncio
    async def test_is_database_ready_connected_and_ready(self):
        self.db_manager.connected = True
        
        self.mock_database.fetch_one.side_effect = [
            {"questions_exists": True, "categories_exists": True},
            {"count": 10}
        ]
        
        ready = await self.db_manager.is_database_ready()
        
        self.assertEqual(self.mock_database.fetch_one.call_count, 2)
        
        self.assertTrue(ready)
    
    @pytest.mark.asyncio
    async def test_is_database_ready_tables_missing(self):
        self.db_manager.connected = True
        
        self.mock_database.fetch_one.return_value = {"questions_exists": False, "categories_exists": True}
        
        ready = await self.db_manager.is_database_ready()
        
        self.assertEqual(self.mock_database.fetch_one.call_count, 1)
        
        self.assertFalse(ready)
    
    @pytest.mark.asyncio
    async def test_is_database_ready_no_questions(self):
        self.db_manager.connected = True
        
        self.mock_database.fetch_one.side_effect = [
            {"questions_exists": True, "categories_exists": True},
            {"count": 0}
        ]
        
        ready = await self.db_manager.is_database_ready()
        
        self.assertEqual(self.mock_database.fetch_one.call_count, 2)
        
        self.assertFalse(ready)
    
    @pytest.mark.asyncio
    async def test_is_database_ready_not_connected(self):
        self.db_manager.connected = False
        
        ready = await self.db_manager.is_database_ready()
        
        self.mock_database.fetch_one.assert_not_called()
        
        self.assertFalse(ready)