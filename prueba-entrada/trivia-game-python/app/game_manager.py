from app.models.quiz import Quiz
from app.models.question import Question

class GameManager:
    def __init__(self):
        self.quiz = Quiz()
        self.total_rounds = 10
        self.current_round = 0

    def load_questions(self):
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

    def run_game(self):
        self.load_questions()
        while self.current_round < self.total_rounds:
            question = self.quiz.get_next_question()
            if not question:
                break
            self.play_round(question)
            self.current_round += 1
        self.show_final_score()

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