import pytest
from app.models.quiz import Quiz
from app.models.question import Question

def test_quiz_creation():
    quiz = Quiz()
    assert len(quiz.questions) == 0
    assert quiz.current_question_index == 0

def test_add_question():
    quiz = Quiz()
    question = Question("¿Prueba?", ["1", "2", "3", "4"], "1")
    quiz.add_question(question)
    assert len(quiz.questions) == 1
    assert quiz.questions[0] == question

def test_get_next_question():
    quiz = Quiz()
    question1 = Question("¿Pregunta 1?", ["1", "2", "3", "4"], "1")
    question2 = Question("¿Pregunta 2?", ["1", "2", "3", "4"], "2")
    quiz.add_question(question1)
    quiz.add_question(question2)
    
    next_question = quiz.get_next_question()
    assert next_question == question1
    assert quiz.current_question_index == 1
    
    next_question = quiz.get_next_question()
    assert next_question == question2
    assert quiz.current_question_index == 2

def test_get_next_question_empty():
    quiz = Quiz()
    assert quiz.get_next_question() is None
    
def test_get_next_question_end():
    quiz = Quiz()
    question = Question("¿Prueba?", ["1", "2", "3", "4"], "1")
    quiz.add_question(question)
    
    quiz.get_next_question()
    assert quiz.get_next_question() is None 