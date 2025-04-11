#shared UI that can be used in multiple games, enhances code maintainabilty,
#keeps consistency in graphics (button design, etc.)
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
        text_surface = self.font.render(self.text, True, (255, 255, 255))
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
        self.next_action = None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.title_font.render("Game Suite", True, (255, 255, 255))
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
        return self.next_action

    def start_game(self):
        self.next_action = "select_game"
        self.running = False

    def show_instructions(self):
        self.next_action = "instructions" 
        self.running = False

    def exit_game(self):
        pygame.quit()
        sys.exit()

class GameSelectionMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.title_font = pygame.font.Font(None, 50)
        self.buttons = [
            Button("Maze Game", 200, 200, 200, 50, (50, 50, 255), (180, 180, 180), self.select_maze),
            Button("Word Game", 200, 270, 200, 50, (50, 50, 255), (180, 180, 180), self.select_word),
            Button("Number Game", 200, 340, 200, 50, (50, 50, 255), (180, 180, 180), self.select_number),
            Button("Back", 200, 410, 200, 50, (50, 50, 255), (180, 180, 180), self.back_to_menu)
        ]
        self.running = True
        self.next_action = None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.title_font.render("Select a Game", True, (255, 255, 255))
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
        return self.next_action

    def select_maze(self):
        self.next_action = "maze"
        self.running = False

    def select_word(self):
        self.next_action = "word"
        self.running = False

    def select_number(self):
        self.next_action = "number"
        self.running = False

    def back_to_menu(self):
        self.next_action = "back"
        self.running = False

class InstructionsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.button = Button("Back", 200, 500, 200, 50, (50, 50, 255), (180, 180, 180), self.back)
        self.running = True

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black 
        font = pygame.font.Font(None, 50)
        title = font.render("Instructions", True, (255, 255, 255))
        self.screen.blit(title, (100, 50))  # Hardcoded position
        font2 = pygame.font.Font(None, 36)
        text1 = font2.render("Use arrows to move in maze", True, (255, 255, 255))
        self.screen.blit(text1, (100, 150))
        text2 = font2.render("Press Q to quit game", True, (255, 255, 255))
        self.screen.blit(text2, (100, 200))
        self.button.draw(self.screen)

    def run(self):
        while self.running:
            self.draw()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.button.is_clicked(event):
                    self.back()

    def back(self):
        self.running = False  