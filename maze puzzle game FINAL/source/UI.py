# source/UI.py
import pygame
import sys

pygame.init()

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
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.title_font = pygame.font.Font(None, 50)
        self.buttons = [
            Button("Start Game", 200, 250, 200, 50, (50, 50, 255), (180, 180, 180), self.start_game),
            Button("Instructions", 200, 320, 200, 50, (50, 50, 255), (180, 180, 180), self.show_instructions),
            Button("Exit", 200, 390, 200, 50, (50, 50, 255), (180, 180, 180), self.exit_game)
        ]
        self.running = True

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        title_surface = self.title_font.render("Maze Game", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 100))
        for button in self.buttons:
            button.draw(self.screen)

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
        self.running = False  # Exit menu to start game

    def show_instructions(self):
        print("Instructions - Show game mechanics")

    def exit_game(self):
        pygame.quit()
        sys.exit()