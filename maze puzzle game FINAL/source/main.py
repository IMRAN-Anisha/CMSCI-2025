# source/main.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from source.UI import MainMenu, GameSelectionMenu
from games.puzzle_game import PuzzleGame
from games.word_game import WordGame
from games.number_game import SudokuGame
from source.path_levels import EasyMaze, MediumMaze, HardMaze
from source.constants import WIDTH, HEIGHT

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
            elif game_choice == "quit":
                pygame.quit()
                return
            elif game_choice == "word":
                word_length_menu = GameSelectionMenu(screen, WIDTH, HEIGHT, is_word_length_menu=True)
                word_length = word_length_menu.run()
                if word_length == "back":
                    continue
                if word_length == "quit":
                    pygame.quit()
                    return
                game_class = game_classes[game_choice]
                game = game_class(screen, clock)
                return_to_menu = game.start_game(word_length)
            elif game_choice in ["puzzle", "sudoku"]:
                difficulty_menu = GameSelectionMenu(screen, WIDTH, HEIGHT, is_difficulty_menu=True)
                difficulty = difficulty_menu.run()
                if difficulty == "back":
                    continue
                if difficulty == "quit":
                    pygame.quit()
                    return
                if game_choice == "puzzle":
                    game_class = puzzle_difficulty_classes.get(difficulty, puzzle_difficulty_classes["medium"])
                else:  # sudoku
                    game_class = game_classes[game_choice]
                game = game_class(screen, clock)
                return_to_menu = game.start_game(difficulty)

            if not return_to_menu:
                pygame.quit()
                return

if __name__ == "__main__":
    run_game()