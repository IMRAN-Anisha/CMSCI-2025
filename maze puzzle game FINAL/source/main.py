# source/main.py
import pygame
from source.UI import MainMenu
from source.maze_game import MazeGame
from source.constants import WIDTH, HEIGHT

def run_game():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    menu = MainMenu(screen, WIDTH, HEIGHT)
    menu.run()

    game = MazeGame(screen, clock)
    game.run()

    pygame.quit()

if __name__ == "__main__":
    run_game()