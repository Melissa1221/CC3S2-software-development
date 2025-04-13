from app.models.quiz import Quiz
from app.models.question import Question
from app.models.db_manager import DBManager
import json
import os
import random
import asyncio

class GameManager:
    def __init__(self):
        self.quiz = Quiz()
        self.total_rounds = 10
        self.current_round = 0
        self.db_manager = DBManager()
        
    async def initialize(self):
        db_connected = await self.db_manager.connect()
        if db_connected:
            print("Conectado a la base de datos")
            db_ready = await self.db_manager.is_database_ready()
            if not db_ready:
                print("La base de datos no tiene preguntas cargadas")
                print("Usando modo local...")
                self.db_manager = None
        else:
            print("No se pudo conectar a la base de datos")
            print("Usando modo local...")
            self.db_manager = None
            
    async def load_questions_from_db(self):
        questions = await self.db_manager.get_random_questions(self.total_rounds)
        for question in questions:
            self.quiz.add_question(question)
        return len(questions) > 0

    def load_questions_from_local(self):
        try:
            json_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'questions.json')
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                questions_data = data.get('questions', [])
                
                if len(questions_data) > self.total_rounds:
                    questions_data = random.sample(questions_data, self.total_rounds)
                
                for q_data in questions_data:
                    question = Question(
                        description=q_data['description'],
                        options=q_data['options'],
                        correct_answer=q_data['correct_answer']
                    )
                    self.quiz.add_question(question)
                return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            questions = [
                Question("¿Cuál es la capital de Francia?", ["Madrid", "Londres", "París", "Berlín"], "París"),
                Question("¿Qué planeta es conocido como el Planeta Rojo?", ["Venus", "Marte", "Júpiter", "Saturno"], "Marte"),
                Question("¿Cuánto es 2 + 2?", ["1", "2", "3", "4"], "4"),
                Question("¿Quién escribió Romeo y Julieta?", ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "William Shakespeare"),
                Question("¿Cuál es el océano más grande de la Tierra?", ["Océano Atlántico", "Océano Índico", "Océano Ártico", "Océano Pacífico"], "Océano Pacífico"),
                Question("¿Cuál es el símbolo químico del oro?", ["Go", "Gd", "Au", "Ag"], "Au"),
                Question("¿Qué país es hogar del canguro?", ["Nueva Zelanda", "Sudáfrica", "Australia", "Brasil"], "Australia"),
                Question("¿Cuál es la montaña más alta del mundo?", ["K2", "Monte Everest", "Kilimanjaro", "Denali"], "Monte Everest"),
                Question("¿Quién pintó la Mona Lisa?", ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Miguel Ángel"], "Leonardo da Vinci"),
                Question("¿Cuál es el número primo más pequeño?", ["0", "1", "2", "3"], "2")
            ]
            
            for question in questions:
                self.quiz.add_question(question)
                
            return True

    async def load_questions(self):
        if self.db_manager:
            success = await self.load_questions_from_db()
            if success:
                return
                
        self.load_questions_from_local()

    async def run_game(self):
        await self.initialize()
        await self.load_questions()
        while self.current_round < self.total_rounds:
            question = self.quiz.get_next_question()
            if not question:
                break
            self.current_round += 1

    def play_round(self, question):
        pass

    def answer_question(self, question, answer):
        option_index = int(answer) - 1
        if 0 <= option_index < len(question.options):
            selected_option = question.options[option_index]
            return self.quiz.answer_question(question, selected_option)
        else:
            print("Opción inválida seleccionada.")
            return False

    def get_next_question(self):
        return self.quiz.get_next_question()
        
    def get_game_summary(self):
        return self.quiz.get_score()
        
    def show_final_score(self):
        pass
        
    async def cleanup(self):
        if self.db_manager:
            await self.db_manager.disconnect() 