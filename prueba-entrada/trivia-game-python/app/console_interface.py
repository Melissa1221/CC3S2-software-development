class ConsoleInterface:
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def display_welcome(self):
        print("¡Bienvenido al juego de Trivia!")
        print("Responde las siguientes preguntas seleccionando el número de la opción correcta.")

    def display_question(self, question, question_number):
        print(f"\nPregunta {question_number}: {question.description}")
        for idx, option in enumerate(question.options, 1):
            print(f"{idx}) {option}")

    def get_user_answer(self):
        return input("\nTu respuesta (1-4): ")
        
    def display_answer_result(self, is_correct):
        if is_correct:
            print("¡Correcto!")
        else:
            print("Incorrecto.")
            
    def display_game_summary(self, summary):
        print("\nJuego terminado. Aquí está tu puntuación:")
        print(f"Preguntas contestadas: {summary['total_questions']}")
        print(f"Respuestas correctas: {summary['correct_answers']}")
        print(f"Respuestas incorrectas: {summary['incorrect_answers']}")
        
    def run_game(self):
        self.display_welcome()
        self.game_manager.load_questions()
        
        question_number = 1
        while True:
            question = self.game_manager.get_next_question()
            if not question:
                break
                
            self.display_question(question, question_number)
            answer = self.get_user_answer()
            is_correct = self.game_manager.answer_question(question, answer)
            self.display_answer_result(is_correct)
            question_number += 1
            
        self.display_game_summary(self.game_manager.get_game_summary()) 