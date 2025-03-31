import pygame
import sys

# Constants
WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (50, 50, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

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
        button_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, button_color, self.rect, border_radius=10)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class MainMenu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 50)
        self.buttons = [
            Button("Start Game", 200, 250, 200, 50, BLUE, GRAY, self.start_game),
            Button("Instructions", 200, 320, 200, 50, BLUE, GRAY, self.show_instructions),
            Button("Exit", 200, 390, 200, 50, BLUE, GRAY, self.exit_game)
        ]
        self.running = True

    def draw(self):
        screen.fill(BLACK)
        title_surface = self.title_font.render("Maze Game", True, WHITE)
        screen.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 100))

        for button in self.buttons:
            button.draw(screen)

    def run(self):
        while self.running:
            self.draw()
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                for button in self.buttons:
                    if button.is_clicked(event):
                        button.action()

    def start_game(self):
        print("Game Start - Navigate to game mode selection")

    def show_instructions(self):
        print("Instructions - Show game mechanics")

    def exit_game(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    menu = MainMenu()
    menu.run()
