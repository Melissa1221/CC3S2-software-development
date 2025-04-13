import pytest
from app.models.quiz import Quiz
from app.models.question import Question

def test_quiz_scoring():
    quiz = Quiz()
    question = Question("Test?", ["1", "2", "3", "4"], "1")
    quiz.add_question(question)
    
    assert quiz.answer_question(question, "1") == True
    assert quiz.correct_answers == 1
    assert quiz.incorrect_answers == 0
    
    assert quiz.answer_question(question, "2") == False
    assert quiz.correct_answers == 1
    assert quiz.incorrect_answers == 1

def test_quiz_score_calculation():
    quiz = Quiz()
    quiz.add_question(Question("Q1?", ["1", "2"], "1"))
    quiz.add_question(Question("Q2?", ["1", "2"], "2"))
    quiz.add_question(Question("Q3?", ["1", "2"], "1"))
    
    quiz.answer_question(quiz.questions[0], "1")  # Correct
    quiz.answer_question(quiz.questions[1], "1")  # Incorrect
    quiz.answer_question(quiz.questions[2], "1")  # Correct
    
    score = quiz.get_score()
    assert score['correct'] == 2
    assert score['incorrect'] == 1
    assert score['total'] == 3

def test_empty_quiz_score():
    quiz = Quiz()
    score = quiz.get_score()
    
    assert score['correct'] == 0
    assert score['incorrect'] == 0
    assert score['total'] == 0 