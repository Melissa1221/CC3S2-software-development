import asyncio
from app.game_manager import GameManager
from app.console_interface import ConsoleInterface

async def main():
    game_manager = GameManager()
    console = ConsoleInterface(game_manager)
    await console.run_game()

if __name__ == "__main__":
    asyncio.run(main())
