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

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Suite")
    clock = pygame.time.Clock()

    while True:
        menu = MainMenu(screen, WIDTH, HEIGHT)
        next_action = menu.run()

        if next_action == "select_game":
            selection_menu = GameSelectionMenu(screen, WIDTH, HEIGHT)
            game_choice = selection_menu.run()

            if game_choice == "puzzle":  # Updated to "puzzle" to match GameSelectionMenu
                game = PuzzleGame(screen, clock)  # Fixed: Use PuzzleGame instead of MazeGame
                game.run()
            elif game_choice == "word":
                game = WordGame(screen, clock)
                game.run()
            elif game_choice == "number":
                game = SudokuGame(screen, clock)
                game.run()

        if next_action == "instructions":
            instructions = InstructionsScreen(screen)
            instructions.run()  # Fix this ASAP

    pygame.quit()

if __name__ == "__main__":
    run_game()