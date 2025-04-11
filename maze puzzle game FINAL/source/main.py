# source/main.py
# Main game structure, putting it all together.
import sys  # Added sys import
import os
# Add the parent directory (maze_puzzle_game_FINAL) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Moved to top

import pygame
from source.UI import *
print("a")
from games.puzzle_game import PuzzleGame
print("a")
from games.word_game import WordGame  
print("a")
from source.constants import WIDTH, HEIGHT
print("a")
from games.number_game import SudokuGame

from source.path_levels import EasyMaze, MediumMaze, HardMaze

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Adventure")
    clock = pygame.time.Clock()

    current_difficulty = "medium"  # Default starting difficulty
    game_classes = {
        "easy": EasyMaze,
        "medium": MediumMaze,
        "hard": HardMaze
    }

    while True:
        main_menu = MainMenu(screen, WIDTH, HEIGHT)
        choice = main_menu.run()
        if choice == "quit":
            pygame.quit()
            return

        if choice == "play":
            game_selection_menu = GameSelectionMenu(screen, WIDTH, HEIGHT)
            game_choice = game_selection_menu.run()
            if game_choice == "back":
                continue

            if game_choice == "puzzle":
                difficulty_menu = GameSelectionMenu(screen, WIDTH, HEIGHT)  # Reuse for difficulty
                difficulty = difficulty_menu.run()  # Assume modified to show difficulties
                if difficulty == "back":
                    continue
                if difficulty in game_classes:
                    current_difficulty = difficulty  # Update current difficulty

            game_class = game_classes.get(current_difficulty)
            if game_class:
                game = game_class(screen, clock)
                return_to_menu = game.start_game(current_difficulty)
                # After game ends, get the suggested difficulty
                current_difficulty = game.get_current_difficulty()
                if not return_to_menu:
                    pygame.quit()
                    return

if __name__ == "__main__":
    run_game()