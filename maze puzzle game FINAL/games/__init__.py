import pygame
import sys

from games.number_game import SudokuGame
from games.puzzle_game import Game      
from games.word_game import WordGame     

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Collection")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)
GRAY = (150, 150, 150)

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class GameLauncher:
    def __init__(self):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.font = pygame.font.Font(None, 50)

    def main_menu(self):
        buttons = [
            Button("Sudoku", 200, 200, 200, 50, BLUE, GRAY, self.play_sudoku),
            Button("Maze", 200, 300, 200, 50, BLUE, GRAY, self.play_maze),
            Button("Word Game", 200, 400, 200, 50, BLUE, GRAY, self.play_word),
            Button("Quit", 200, 500, 200, 50, BLUE, GRAY, self.quit_game)
        ]
        self.menu_loop(buttons)

    def menu_loop(self, buttons):
        while self.running:
            self.screen.fill(BLACK)
            title = self.font.render("Game Collection", True, WHITE)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.is_clicked(event):
                            button.action()
                            return  # Return to allow game to run

            for button in buttons:
                button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def play_sudoku(self):
        sudoku = SudokuGame()
        sudoku.main_menu()
        # After game ends, return to main menu
        self.main_menu()

    def play_maze(self):
        maze = Game()
        maze.main_menu()
        # After game ends, return to main menu
        self.main_menu()

    def play_word(self):
        word = WordGame()
        word.run()
        # After game ends, return to main menu
        self.main_menu()

    def quit_game(self):
        self.running = False
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.main_menu()