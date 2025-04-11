from app.game_manager import GameManager
from app.console_interface import ConsoleInterface

def main():
    game_manager = GameManager()
    console = ConsoleInterface(game_manager)
    console.run_game()

if __name__ == "__main__":
    main()
