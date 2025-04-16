import unittest
from unittest.mock import patch, MagicMock
import io
import sys
import asyncio
import pytest

from app.console_interface import ConsoleInterface
from app.game_manager import GameManager
from app.models.question import Question
from app.models.difficulty import DifficultyLevel

class TestConsoleInterface(unittest.TestCase):
    def setUp(self):
        self.mock_game_manager = MagicMock(spec=GameManager)
        self.mock_game_manager.current_round = 0
        self.mock_game_manager.total_rounds = 10
        
        self.interface = ConsoleInterface(self.mock_game_manager)
        
    def test_display_welcome(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.interface.display_welcome()
        
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("¡Bienvenido al juego de Trivia!", output)
        self.assertIn("Reglas:", output)
        self.assertIn("Niveles de dificultad:", output)
        
    def test_display_question(self):
        mock_question = MagicMock(spec=Question)
        mock_question.description = "¿Cuál es la capital de Francia?"
        mock_question.difficulty = DifficultyLevel.MEDIUM
        mock_question.get_points.return_value = 2
        mock_question.options = ["Madrid", "París", "Roma", "Berlín"]
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.interface.display_question(mock_question, 1)
        
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("Pregunta 1: ¿Cuál es la capital de Francia?", output)
        self.assertIn("Dificultad: MEDIUM", output)
        self.assertIn("Puntos: 2", output)
        self.assertIn("1) Madrid", output)
        self.assertIn("2) París", output)
        
    @patch('builtins.input', side_effect=["", "a", "0", "5", "3"])
    def test_get_user_answer(self, mock_input):
        answer = self.interface.get_user_answer()
        
        self.assertEqual(answer, "3")
        self.assertEqual(mock_input.call_count, 5)
        
    def test_display_answer_result(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.interface.display_answer_result(True)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("¡Correcto!", output)
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.interface.display_answer_result(False)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Incorrecto.", output)
        
    def test_display_score(self):
        score = {
            "correct": 7,
            "incorrect": 3,
            "total_score": 15
        }
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.interface.display_score(score)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Puntuación actual:", output)
        self.assertIn("Respuestas correctas: 7", output)
        self.assertIn("Puntuación total: 15", output)
        
    def test_display_final_score(self):
        score = {
            "total": 10,
            "correct": 8,
            "incorrect": 2,
            "total_score": 18,
            "difficulty_stats": {
                DifficultyLevel.EASY: {"total": 4, "correct": 4},
                DifficultyLevel.MEDIUM: {"total": 4, "correct": 3},
                DifficultyLevel.HARD: {"total": 2, "correct": 1}
            }
        }
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.interface.display_final_score(score)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("¡Juego terminado!", output)
        self.assertIn("RESUMEN FINAL", output)
        self.assertIn("Precisión: 80.0%", output)
        self.assertIn("Desglose por dificultad:", output)
        
    @pytest.mark.asyncio
    async def test_run_game(self):
        with patch.object(ConsoleInterface, 'get_user_answer', return_value="2"):
            self.mock_game_manager.initialize = MagicMock(return_value=asyncio.Future())
            self.mock_game_manager.initialize.return_value.set_result(None)
            
            self.mock_game_manager.load_questions = MagicMock(return_value=asyncio.Future())
            self.mock_game_manager.load_questions.return_value.set_result(None)
            
            self.mock_game_manager.cleanup = MagicMock(return_value=asyncio.Future())
            self.mock_game_manager.cleanup.return_value.set_result(None)
            
            mock_question1 = MagicMock(spec=Question)
            mock_question1.description = "Pregunta 1"
            mock_question1.difficulty = DifficultyLevel.EASY
            mock_question1.get_points.return_value = 1
            mock_question1.options = ["A", "B", "C", "D"]
            
            mock_question2 = MagicMock(spec=Question)
            mock_question2.description = "Pregunta 2"
            mock_question2.difficulty = DifficultyLevel.MEDIUM
            mock_question2.get_points.return_value = 2
            mock_question2.options = ["W", "X", "Y", "Z"]
            
            self.mock_game_manager.get_next_question.side_effect = [mock_question1, mock_question2, None]
            self.mock_game_manager.answer_question.return_value = True
            
            summary = {
                "total": 2,
                "correct": 2,
                "incorrect": 0,
                "total_score": 3
            }
            self.mock_game_manager.get_game_summary.return_value = summary
            
            await self.interface.run_game()
            
            self.mock_game_manager.initialize.assert_called_once()
            self.mock_game_manager.load_questions.assert_called_once()
            self.assertEqual(self.mock_game_manager.get_next_question.call_count, 3)
            self.assertEqual(self.mock_game_manager.answer_question.call_count, 2)
            self.mock_game_manager.cleanup.assert_called_once()