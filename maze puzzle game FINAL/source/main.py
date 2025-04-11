import sys
import os
# Add the parent directory (maze_puzzle_game_FINAL) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from source.UI import MainMenu, GameSelectionMenu
print("a")
from games.puzzle_game import PuzzleGame
print("a")
from games.word_game import WordGame
print("a")
from source.constants import WIDTH, HEIGHT
print("a")
from games.number_game import SudokuGame
print("a")
from source.path_levels import EasyMaze, MediumMaze, HardMaze
print("a")

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Adventure")
    clock = pygame.time.Clock()

    game_classes = {
        "puzzle": PuzzleGame,
        "word": WordGame,
        "sudoku": SudokuGame
    }

    puzzle_difficulty_classes = {
        "easy": EasyMaze,
        "medium": MediumMaze,
        "hard": HardMaze
    }

    while True:
        print("Starting main menu loop")  # Debug output
        main_menu = MainMenu(screen, WIDTH, HEIGHT)
        choice = main_menu.run()
        print(f"Main menu choice: {choice}")  # Debug output
        if choice == "quit":
            pygame.quit()
            return

        if choice == "play":
            print("Starting game selection menu")  # Debug output
            game_selection_menu = GameSelectionMenu(screen, WIDTH, HEIGHT)
            game_choice = game_selection_menu.run()
            print(f"Game selection choice: {game_choice}")  # Debug output
            if game_choice == "back":
                continue

            if game_choice in game_classes:
                if game_choice == "puzzle":
                    print("Starting difficulty selection menu")  # Debug output
                    difficulty_menu = GameSelectionMenu(screen, WIDTH, HEIGHT)  # Reuse for difficulty
                    difficulty = difficulty_menu.run()
                    print(f"Difficulty choice: {difficulty}")  # Debug output
                    if difficulty == "back":
                        continue
                    if difficulty in puzzle_difficulty_classes:
                        game_class = puzzle_difficulty_classes[difficulty]
                    else:
                        game_class = PuzzleGame  # Fallback to default
                else:
                    game_class = game_classes[game_choice]

                print(f"Starting game: {game_choice}")  # Debug output
                game = game_class(screen, clock)
                return_to_menu = game.start_game(difficulty if game_choice == "puzzle" else None)
                print(f"Game ended, return_to_menu: {return_to_menu}")  # Debug output
                if not return_to_menu:
                    pygame.quit()
                    return

if __name__ == "__main__":
    run_game()