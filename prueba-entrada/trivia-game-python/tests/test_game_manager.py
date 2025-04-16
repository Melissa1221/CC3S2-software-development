import unittest
from unittest.mock import patch, MagicMock, mock_open
import asyncio
import json
import pytest

from app.game_manager import GameManager
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.db_manager import DBManager
from app.models.game_stats import GameStats
from app.models.difficulty import DifficultyLevel

class TestGameManager(unittest.TestCase):
    def setUp(self):
        self.game_manager = GameManager()
        self.game_manager.quiz = MagicMock(spec=Quiz)
        self.game_manager.db_manager = MagicMock(spec=DBManager)
        self.game_manager.game_stats = MagicMock(spec=GameStats)
        
    @pytest.mark.asyncio
    async def test_initialize_with_db_success(self):
        self.game_manager.db_manager.connect.return_value = asyncio.Future()
        self.game_manager.db_manager.connect.return_value.set_result(True)
        self.game_manager.db_manager.is_database_ready.return_value = asyncio.Future()
        self.game_manager.db_manager.is_database_ready.return_value.set_result(True)
        
        await self.game_manager.initialize()
        
        self.game_manager.db_manager.connect.assert_called_once()
        self.game_manager.db_manager.is_database_ready.assert_called_once()
        self.assertIsNotNone(self.game_manager.db_manager)
        
    @pytest.mark.asyncio
    async def test_initialize_with_db_connection_failure(self):
        self.game_manager.db_manager.connect.return_value = asyncio.Future()
        self.game_manager.db_manager.connect.return_value.set_result(False)
        
        await self.game_manager.initialize()
        
        self.game_manager.db_manager.connect.assert_called_once()
        self.game_manager.db_manager.is_database_ready.assert_not_called()
        self.assertIsNone(self.game_manager.db_manager)
        
    @pytest.mark.asyncio
    async def test_initialize_with_db_not_ready(self):
        self.game_manager.db_manager.connect.return_value = asyncio.Future()
        self.game_manager.db_manager.connect.return_value.set_result(True)
        self.game_manager.db_manager.is_database_ready.return_value = asyncio.Future()
        self.game_manager.db_manager.is_database_ready.return_value.set_result(False)
        
        await self.game_manager.initialize()
        
        self.game_manager.db_manager.connect.assert_called_once()
        self.game_manager.db_manager.is_database_ready.assert_called_once()
        self.assertIsNone(self.game_manager.db_manager)
        
    @pytest.mark.asyncio
    async def test_load_questions_from_db(self):
        self.game_manager.db_manager = MagicMock(spec=DBManager)
        mock_question = MagicMock(spec=Question)
        self.game_manager.db_manager.get_random_questions.return_value = asyncio.Future()
        self.game_manager.db_manager.get_random_questions.return_value.set_result([mock_question])
        
        result = await self.game_manager.load_questions_from_db()
        
        self.game_manager.db_manager.get_random_questions.assert_called_once_with(self.game_manager.total_rounds)
        self.game_manager.quiz.add_question.assert_called_once_with(mock_question)
        self.assertTrue(result)
        
    @pytest.mark.asyncio
    async def test_load_questions_from_db_empty(self):
        self.game_manager.db_manager = MagicMock(spec=DBManager)
        self.game_manager.db_manager.get_random_questions.return_value = asyncio.Future()
        self.game_manager.db_manager.get_random_questions.return_value.set_result([])
        
        result = await self.game_manager.load_questions_from_db()
        
        self.game_manager.db_manager.get_random_questions.assert_called_once_with(self.game_manager.total_rounds)
        self.game_manager.quiz.add_question.assert_not_called()
        self.assertFalse(result)
        
    @patch('os.path.join')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "questions": [
            {
                "description": "¿Cuál es la capital de Francia?",
                "options": ["Madrid", "Londres", "París", "Berlín"],
                "correct_answer": "París",
                "difficulty": "easy"
            }
        ]
    }))
    def test_load_questions_from_local(self, mock_file, mock_join):
        mock_join.return_value = "fake_path/questions.json"
        
        result = self.game_manager.load_questions_from_local()
        
        mock_join.assert_called()
        mock_file.assert_called_once_with("fake_path/questions.json", 'r', encoding='utf-8')
        self.game_manager.quiz.add_question.assert_called_once()
        self.assertTrue(result)
        
    @patch('os.path.join')
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_questions_from_local_file_not_found(self, mock_file, mock_join):
        mock_join.return_value = "fake_path/questions.json"
        
        result = self.game_manager.load_questions_from_local()
        
        mock_join.assert_called()
        mock_file.assert_called_once_with("fake_path/questions.json", 'r', encoding='utf-8')
        self.assertEqual(self.game_manager.quiz.add_question.call_count, 10)
        self.assertTrue(result)
        
    @pytest.mark.asyncio
    async def test_load_questions_with_db(self):
        self.game_manager.db_manager = MagicMock(spec=DBManager)
        self.game_manager.load_questions_from_db = MagicMock(return_value=asyncio.Future())
        self.game_manager.load_questions_from_db.return_value.set_result(True)
        self.game_manager.load_questions_from_local = MagicMock()
        
        await self.game_manager.load_questions()
        
        self.game_manager.load_questions_from_db.assert_called_once()
        self.game_manager.load_questions_from_local.assert_not_called()
        
    @pytest.mark.asyncio
    async def test_load_questions_with_db_failure(self):
        self.game_manager.db_manager = MagicMock(spec=DBManager)
        self.game_manager.load_questions_from_db = MagicMock(return_value=asyncio.Future())
        self.game_manager.load_questions_from_db.return_value.set_result(False)
        self.game_manager.load_questions_from_local = MagicMock()
        
        await self.game_manager.load_questions()
        
        self.game_manager.load_questions_from_db.assert_called_once()
        self.game_manager.load_questions_from_local.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_load_questions_without_db(self):
        self.game_manager.db_manager = None
        self.game_manager.load_questions_from_local = MagicMock()
        
        await self.game_manager.load_questions()
        
        self.game_manager.load_questions_from_local.assert_called_once()
        
    def test_answer_question_correct(self):
        mock_question = MagicMock(spec=Question)
        mock_question.options = ["Madrid", "París", "Roma", "Berlín"]
        self.game_manager.quiz.answer_question.return_value = True
        
        result = self.game_manager.answer_question(mock_question, "2")
        
        self.game_manager.quiz.answer_question.assert_called_once_with(mock_question, "París")
        self.game_manager.game_stats.update_stats.assert_called_once_with(mock_question, True)
        self.assertTrue(result)
        
    def test_answer_question_incorrect(self):
        mock_question = MagicMock(spec=Question)
        mock_question.options = ["Madrid", "París", "Roma", "Berlín"]
        self.game_manager.quiz.answer_question.return_value = False
        
        result = self.game_manager.answer_question(mock_question, "1")
        
        self.game_manager.quiz.answer_question.assert_called_once_with(mock_question, "Madrid")
        self.game_manager.game_stats.update_stats.assert_called_once_with(mock_question, False)
        self.assertFalse(result)
        
    def test_answer_question_invalid_option(self):
        mock_question = MagicMock(spec=Question)
        mock_question.options = ["Madrid", "París", "Roma", "Berlín"]
        
        result = self.game_manager.answer_question(mock_question, "5")
        
        self.game_manager.quiz.answer_question.assert_not_called()
        self.game_manager.game_stats.update_stats.assert_not_called()
        self.assertFalse(result)
        
    def test_answer_question_empty_answer(self):
        mock_question = MagicMock(spec=Question)
        
        result = self.game_manager.answer_question(mock_question, "")
        
        self.game_manager.quiz.answer_question.assert_not_called()
        self.game_manager.game_stats.update_stats.assert_not_called()
        self.assertFalse(result)
        
    def test_answer_question_non_numeric(self):
        mock_question = MagicMock(spec=Question)
        
        result = self.game_manager.answer_question(mock_question, "a")
        
        self.game_manager.quiz.answer_question.assert_not_called()
        self.game_manager.game_stats.update_stats.assert_not_called()
        self.assertFalse(result)
        
    def test_get_next_question(self):
        mock_question = MagicMock(spec=Question)
        self.game_manager.quiz.get_next_question.return_value = mock_question
        
        result = self.game_manager.get_next_question()
        
        self.game_manager.quiz.get_next_question.assert_called_once()
        self.assertEqual(result, mock_question)
        
    def test_get_game_summary(self):
        quiz_score = {"total": 10, "correct": 7, "incorrect": 3}
        stats_summary = {
            "total_score": 15,
            "difficulty_stats": {
                DifficultyLevel.EASY: {"total": 4, "correct": 3},
                DifficultyLevel.MEDIUM: {"total": 4, "correct": 3},
                DifficultyLevel.HARD: {"total": 2, "correct": 1}
            }
        }
        self.game_manager.quiz.get_score.return_value = quiz_score
        self.game_manager.game_stats.get_summary.return_value = stats_summary
        
        result = self.game_manager.get_game_summary()
        
        self.game_manager.quiz.get_score.assert_called_once()
        self.game_manager.game_stats.get_summary.assert_called_once()
        self.assertEqual(result["total"], 10)
        self.assertEqual(result["correct"], 7)
        self.assertEqual(result["incorrect"], 3)
        self.assertEqual(result["total_score"], 15)
        self.assertEqual(result["difficulty_stats"], stats_summary["difficulty_stats"])
        
    @pytest.mark.asyncio
    async def test_cleanup(self):
        self.game_manager.db_manager = MagicMock(spec=DBManager)
        self.game_manager.db_manager.disconnect.return_value = asyncio.Future()
        self.game_manager.db_manager.disconnect.return_value.set_result(None)
        
        await self.game_manager.cleanup()
        
        self.game_manager.db_manager.disconnect.assert_called_once()
        
    @pytest.mark.asyncio
    async def test_cleanup_without_db(self):
        self.game_manager.db_manager = None
        
        await self.game_manager.cleanup() 