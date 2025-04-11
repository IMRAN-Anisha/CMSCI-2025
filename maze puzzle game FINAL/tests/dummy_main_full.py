import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from source.UI import MainMenu, GameSelectionMenu, InstructionsScreen
from games.word_game import WordGame
from source.constants import WIDTH, HEIGHT

def run_dummy_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dummy Game Suite")
    clock = pygame.time.Clock()

    while True:
        # Show the Main Menu
        menu = MainMenu(screen, WIDTH, HEIGHT)
        next_action = menu.run()

        if next_action == "select_game":
            # Show the Game Selection Menu
            selection_menu = GameSelectionMenu(screen, WIDTH, HEIGHT)
            game_choice = selection_menu.run()

            # Launch the selected game
            if game_choice == "maze":
                game = (screen, clock)
                game.run()
            elif game_choice == "word":
                game = WordGame(screen, clock)
                game.run()
            elif game_choice == "number":
                print("Math game not implemented yet")
        elif next_action == "instructions":
            instructions = InstructionsScreen(screen)
            instructions.run()
        elif next_action == "quit":
            break

    pygame.quit()

if __name__ == "__main__":
    run_dummy_game()