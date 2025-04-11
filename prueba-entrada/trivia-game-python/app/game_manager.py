from app.models.quiz import Quiz
from app.models.question import Question

class GameManager:
    def __init__(self):
        self.quiz = Quiz()
        self.score = 0
        self.total_questions = 0
        self.correct_answers = 0
        self.incorrect_answers = 0

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
            
        self.total_questions = len(questions)

    def answer_question(self, question, answer):
        option_index = int(answer) - 1
        if 0 <= option_index < len(question.options):
            selected_option = question.options[option_index]
            if question.is_correct(selected_option):
                self.correct_answers += 1
                return True
            else:
                self.incorrect_answers += 1
                return False
        else:
            print("Opción inválida seleccionada.")
            return False

    def get_next_question(self):
        return self.quiz.get_next_question()
        
    def get_game_summary(self):
        return {
            "total_questions": self.total_questions,
            "correct_answers": self.correct_answers,
            "incorrect_answers": self.incorrect_answers
        } 