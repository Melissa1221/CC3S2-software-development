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
            
    def display_round(self, round_number, total_rounds):
        print(f"\nRonda {round_number} de {total_rounds}")
        print("-" * 40)
            
    def display_score(self, score):
        print("\nPuntuación actual:")
        print(f"Respuestas correctas: {score['correct']}")
        print(f"Respuestas incorrectas: {score['incorrect']}")
            
    def display_final_score(self, score):
        print("\n¡Juego terminado!")
        print("=" * 40)
        print(f"Total de preguntas: {score['total']}")
        print(f"Respuestas correctas: {score['correct']}")
        print(f"Respuestas incorrectas: {score['incorrect']}")
        accuracy = (score['correct']/score['total'])*100 if score['total'] > 0 else 0
        print(f"Precisión: {accuracy:.1f}%")
        
    def display_game_summary(self, summary):
        self.display_final_score(summary)
        
    async def run_game(self):
        self.display_welcome()
        
        await self.game_manager.initialize()
        await self.game_manager.load_questions()
        
        while True:
            question = self.game_manager.get_next_question()
            if not question:
                break
                
            self.display_round(self.game_manager.current_round + 1, self.game_manager.total_rounds)
            self.display_question(question, self.game_manager.current_round + 1)
            
            answer = self.get_user_answer()
            is_correct = self.game_manager.answer_question(question, answer)
            self.display_answer_result(is_correct)
            
            score = self.game_manager.get_game_summary()
            self.display_score(score)
            
            self.game_manager.current_round += 1
            if self.game_manager.current_round >= self.game_manager.total_rounds:
                break
            
        self.display_final_score(self.game_manager.get_game_summary())
        
        await self.game_manager.cleanup() 