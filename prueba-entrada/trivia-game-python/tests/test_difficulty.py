import pytest
from app.models.question import Question
from app.models.difficulty import DifficultyLevel
from app.models.game_stats import GameStats

def test_difficulty_level_values():
    assert DifficultyLevel.EASY.value == "easy"
    assert DifficultyLevel.MEDIUM.value == "medium"
    assert DifficultyLevel.HARD.value == "hard"

def test_difficulty_score_multipliers():
    assert DifficultyLevel.EASY.get_score_multiplier() == 1
    assert DifficultyLevel.MEDIUM.get_score_multiplier() == 2
    assert DifficultyLevel.HARD.get_score_multiplier() == 3

def test_question_with_difficulty():
    q1 = Question("Test?", ["1", "2", "3", "4"], "1", DifficultyLevel.EASY)
    q2 = Question("Test?", ["1", "2", "3", "4"], "1", DifficultyLevel.MEDIUM)
    q3 = Question("Test?", ["1", "2", "3", "4"], "1", DifficultyLevel.HARD)
    
    assert q1.difficulty == DifficultyLevel.EASY
    assert q2.difficulty == DifficultyLevel.MEDIUM
    assert q3.difficulty == DifficultyLevel.HARD
    
    assert q1.get_points() == 1
    assert q2.get_points() == 2
    assert q3.get_points() == 3

def test_question_default_difficulty():
    q = Question("Test?", ["1", "2", "3", "4"], "1")
    assert q.difficulty == DifficultyLevel.EASY
    assert q.get_points() == 1

def test_game_stats_initialization():
    stats = GameStats()
    assert stats.total_rounds == 0
    assert stats.correct_answers == 0
    assert stats.incorrect_answers == 0
    assert stats.total_score == 0
    
    for difficulty in [DifficultyLevel.EASY, DifficultyLevel.MEDIUM, DifficultyLevel.HARD]:
        assert difficulty in stats.difficulty_stats
        assert stats.difficulty_stats[difficulty]['correct'] == 0
        assert stats.difficulty_stats[difficulty]['total'] == 0

def test_game_stats_update_stats():
    stats = GameStats()
    q_easy = Question("Test?", ["1", "2", "3", "4"], "1", DifficultyLevel.EASY)
    q_medium = Question("Test?", ["1", "2", "3", "4"], "1", DifficultyLevel.MEDIUM)
    q_hard = Question("Test?", ["1", "2", "3", "4"], "1", DifficultyLevel.HARD)
  
    stats.update_stats(q_easy, True)
    assert stats.total_rounds == 1
    assert stats.correct_answers == 1
    assert stats.incorrect_answers == 0
    assert stats.total_score == 1
    assert stats.difficulty_stats[DifficultyLevel.EASY]['correct'] == 1
    assert stats.difficulty_stats[DifficultyLevel.EASY]['total'] == 1
    
    stats.update_stats(q_medium, True)
    assert stats.total_rounds == 2
    assert stats.correct_answers == 2
    assert stats.incorrect_answers == 0
    assert stats.total_score == 3 
    assert stats.difficulty_stats[DifficultyLevel.MEDIUM]['correct'] == 1
    assert stats.difficulty_stats[DifficultyLevel.MEDIUM]['total'] == 1
    
    stats.update_stats(q_hard, True)
    assert stats.total_rounds == 3
    assert stats.correct_answers == 3
    assert stats.incorrect_answers == 0
    assert stats.total_score == 6  
    assert stats.difficulty_stats[DifficultyLevel.HARD]['correct'] == 1
    assert stats.difficulty_stats[DifficultyLevel.HARD]['total'] == 1
    
    stats.update_stats(q_hard, False)
    assert stats.total_rounds == 4
    assert stats.correct_answers == 3
    assert stats.incorrect_answers == 1
    assert stats.total_score == 6  # unchanged
    assert stats.difficulty_stats[DifficultyLevel.HARD]['correct'] == 1
    assert stats.difficulty_stats[DifficultyLevel.HARD]['total'] == 2

def test_game_stats_get_summary():
    stats = GameStats()
    q_easy = Question("Test?", ["1", "2", "3", "4"], "1", DifficultyLevel.EASY)
    q_medium = Question("Test?", ["1", "2", "3", "4"], "1", DifficultyLevel.MEDIUM)
    
    stats.update_stats(q_easy, True)
    stats.update_stats(q_medium, False)
    
    summary = stats.get_summary()
    assert summary['total_rounds'] == 2
    assert summary['correct_answers'] == 1
    assert summary['incorrect_answers'] == 1
    assert summary['total_score'] == 1
    assert summary['accuracy'] == 50.0
    assert summary['difficulty_stats'] == stats.difficulty_stats 