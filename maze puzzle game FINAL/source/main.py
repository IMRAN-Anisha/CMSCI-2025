import pygame
from source.UI import MainMenu, GameSelectionMenu, InstructionsScreen
from source.maze_game import MazeGame
from source.constants import WIDTH, HEIGHT

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

            if game_choice == "maze":
                game = MazeGame(screen, clock)
                game.run()
            elif game_choice == "word":
                print("game")
            elif game_choice == "number":
                print("game")
        if next_action == "instructions":
            instructions = InstructionsScreen(screen)
            instructions.run()  # Runs but doesn't return to menu properly yet

    pygame.quit()

if __name__ == "__main__":
    run_game()