from app.models.quiz import Quiz
from app.models.question import Question
from app.models.db_manager import DBManager
from app.models.game_stats import GameStats
from app.models.difficulty import DifficultyLevel
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
        self.game_stats = GameStats()
        
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
                    # Convert difficulty string to enum
                    difficulty_str = q_data.get('difficulty', 'easy').lower()
                    difficulty = DifficultyLevel.EASY
                    if difficulty_str == "medium" or difficulty_str == "medio":
                        difficulty = DifficultyLevel.MEDIUM
                    elif difficulty_str == "hard" or difficulty_str == "difícil":
                        difficulty = DifficultyLevel.HARD
                    
                    question = Question(
                        description=q_data['description'],
                        options=q_data['options'],
                        correct_answer=q_data['correct_answer'],
                        difficulty=difficulty
                    )
                    self.quiz.add_question(question)
                return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            questions = [
                Question("¿Cuál es la capital de Francia?", ["Madrid", "Londres", "París", "Berlín"], "París", DifficultyLevel.EASY),
                Question("¿Qué planeta es conocido como el Planeta Rojo?", ["Venus", "Marte", "Júpiter", "Saturno"], "Marte", DifficultyLevel.EASY),
                Question("¿Cuánto es 2 + 2?", ["1", "2", "3", "4"], "4", DifficultyLevel.EASY),
                Question("¿Quién escribió Romeo y Julieta?", ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "William Shakespeare", DifficultyLevel.MEDIUM),
                Question("¿Cuál es el océano más grande de la Tierra?", ["Océano Atlántico", "Océano Índico", "Océano Ártico", "Océano Pacífico"], "Océano Pacífico", DifficultyLevel.MEDIUM),
                Question("¿Cuál es el símbolo químico del oro?", ["Go", "Gd", "Au", "Ag"], "Au", DifficultyLevel.MEDIUM),
                Question("¿Qué país es hogar del canguro?", ["Nueva Zelanda", "Sudáfrica", "Australia", "Brasil"], "Australia", DifficultyLevel.EASY),
                Question("¿Cuál es la montaña más alta del mundo?", ["K2", "Monte Everest", "Kilimanjaro", "Denali"], "Monte Everest", DifficultyLevel.MEDIUM),
                Question("¿Quién pintó la Mona Lisa?", ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Miguel Ángel"], "Leonardo da Vinci", DifficultyLevel.EASY),
                Question("¿Cuál es el número primo más pequeño?", ["0", "1", "2", "3"], "2", DifficultyLevel.HARD)
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
        try:
            # Verificar si la respuesta está vacía
            if not answer or answer.strip() == "":
                print("Debe ingresar una opción (1-4).")
                return False
            
            # Validar que sea un número
            if not answer.isdigit():
                print("Debe ingresar un número (1-4).")
                return False
            
            option_index = int(answer) - 1
            if 0 <= option_index < len(question.options):
                selected_option = question.options[option_index]
                is_correct = self.quiz.answer_question(question, selected_option)
                self.game_stats.update_stats(question, is_correct)
                return is_correct
            else:
                print(f"Opción inválida. Debe ser un número entre 1 y {len(question.options)}.")
                return False
        except Exception as e:
            print(f"Error al procesar respuesta: {e}")
            return False

    def get_next_question(self):
        return self.quiz.get_next_question()
        
    def get_game_summary(self):
        quiz_score = self.quiz.get_score()
        stats_summary = self.game_stats.get_summary()
        
        # Combine the information
        combined_summary = {**quiz_score}
        combined_summary['total_score'] = stats_summary['total_score']
        combined_summary['difficulty_stats'] = stats_summary['difficulty_stats']
        
        return combined_summary
        
    def show_final_score(self):
        summary = self.get_game_summary()
        print("\n¡Juego terminado!")
        print(f"Puntuación total: {summary['total_score']}")
        print(f"Respuestas correctas: {summary['correct']}")
        print(f"Respuestas incorrectas: {summary['incorrect']}")
        
    async def cleanup(self):
        if self.db_manager:
            await self.db_manager.disconnect() 