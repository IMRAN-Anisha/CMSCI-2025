import pygame
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from games.word_game import WordGame
from source.constants import WIDTH, HEIGHT

def run_dummy_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Dummy Game Suite")
    clock = pygame.time.Clock()

    # Directly run WordGame
    game = WordGame(screen, clock)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    run_dummy_game()