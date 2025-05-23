import pygame
import sys
import random
from source.constants import WIDTH, HEIGHT, WHITE, BLACK, GRAY, BLUE, WORD_GREEN, WORD_YELLOW, DARK_GRAY
from source.UI import Button

# Testing dummy values
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Adventure")
clock = pygame.time.Clock()

# Dummy for testing
THREE_LETTER = ["CAT", "DOG", "BAT"]
FOUR_LETTER = ["CAKE", "BOOK", "FISH"]
FIVE_LETTER = ["APPLE", "BREAD", "CANDY"]

class WordGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.font = pygame.font.Font(None, 50)
        self.tile_font = pygame.font.Font(None, 60)
        self.word_length = 5
        self.correct_word = ""
        self.guesses = [[] for _ in range(6)]
        self.current_guess = []
        self.guess_string = ""
        self.guess_count = 0
        self.game_result = ""
        self.tile_size = 60
        self.tile_spacing = 5

    def run(self):
        self.show_difficulty_menu()

    def show_difficulty_menu(self):
        buttons = [
            Button("Easy (3 letters)", 200, 200, 200, 50, BLUE, GRAY, lambda: self.start_game(3)),
            Button("Medium (4 letters)", 200, 300, 200, 50, BLUE, GRAY, lambda: self.start_game(4)),
            Button("Hard (5 letters)", 200, 400, 200, 50, BLUE, GRAY, lambda: self.start_game(5)),
            Button("Quit", 200, 500, 200, 50, BLUE, GRAY, self.quit_game)
        ]
        self.menu_loop(buttons)

    def menu_loop(self, buttons):
        while self.running:
            self.screen.fill(BLACK)
            title = self.font.render("Word Adventure", True, WHITE)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                for button in buttons:
                    if button.is_clicked(event):
                        button.action()
                        return
            
            for button in buttons:
                button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def start_game(self, length):
        self.word_length = length
        self.guess_count = 0
        self.current_guess = []
        self.guess_string = ""
        self.game_result = ""
        self.guesses = [[] for _ in range(6)]
        
        if length == 3:
            self.correct_word = random.choice(THREE_LETTER).upper()
        elif length == 4:
            self.correct_word = random.choice(FOUR_LETTER).upper()
        else:
            self.correct_word = random.choice(FIVE_LETTER).upper()
        
        self.game_loop()

    def quit_game(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def game_loop(self):
        while self.running:
            self.screen.fill(BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.game_result != "":
                            self.show_difficulty_menu()
                        elif len(self.guess_string) == self.word_length:
                            self.check_guess()
                    elif event.key == pygame.K_BACKSPACE:
                        self.delete_letter()
                    elif event.unicode.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and len(self.guess_string) < self.word_length:
                        self.add_letter(event.unicode.upper())
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def add_letter(self, letter):
        self.guess_string += letter
        self.current_guess.append({"letter": letter, "color": WHITE})

    def delete_letter(self):
        if self.guess_string:
            self.guess_string = self.guess_string[:-1]
            self.current_guess.pop()

    def check_guess(self):
        if self.guess_string.lower() == self.correct_word.lower():
            self.game_result = "W"
            for i, letter in enumerate(self.current_guess):
                letter["color"] = WORD_GREEN
        else:
            for i, letter in enumerate(self.current_guess):
                if i < len(self.correct_word) and letter["letter"] == self.correct_word[i]:
                    letter["color"] = WORD_GREEN
                elif letter["letter"] in self.correct_word:
                    letter["color"] = WORD_YELLOW
                else:
                    letter["color"] = DARK_GRAY
            
            self.guesses[self.guess_count] = self.current_guess
            self.guess_count += 1
            self.current_guess = []
            self.guess_string = ""
            if self.guess_count == 6:
                self.game_result = "L"

    def draw(self):
        # Draw title
        title = self.font.render("Word Adventure", True, WHITE)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        # Calculate starting position to center tiles
        total_width = self.word_length * (self.tile_size + self.tile_spacing) - self.tile_spacing
        start_x = (WIDTH - total_width) // 2
        start_y = 100

        # Draw past guesses
        for i, guess in enumerate(self.guesses):
            for j, letter in enumerate(guess):
                if letter:  # Check if letter exists
                    x = start_x + j * (self.tile_size + self.tile_spacing)
                    y = start_y + i * (self.tile_size + self.tile_spacing)
                    pygame.draw.rect(self.screen, letter["color"], (x, y, self.tile_size, self.tile_size))
                    text = self.tile_font.render(letter["letter"], True, WHITE)
                    text_rect = text.get_rect(center=(x + self.tile_size//2, y + self.tile_size//2))
                    self.screen.blit(text, text_rect)

        # Draw current guess
        for j, letter in enumerate(self.current_guess):
            x = start_x + j * (self.tile_size + self.tile_spacing)
            y = start_y + self.guess_count * (self.tile_size + self.tile_spacing)
            pygame.draw.rect(self.screen, GRAY, (x, y, self.tile_size, self.tile_size), 2)  # Outline only
            text = self.tile_font.render(letter["letter"], True, WHITE)
            text_rect = text.get_rect(center=(x + self.tile_size//2, y + self.tile_size//2))
            self.screen.blit(text, text_rect)

        # Draw empty slots
        for j in range(len(self.current_guess), self.word_length):
            x = start_x + j * (self.tile_size + self.tile_spacing)
            y = start_y + self.guess_count * (self.tile_size + self.tile_spacing)
            pygame.draw.rect(self.screen, GRAY, (x, y, self.tile_size, self.tile_size), 2)

        # Draw result
        if self.game_result:
            result_text = "You Win!" if self.game_result == "W" else f"You Lose! Word was {self.correct_word}"
            text = self.font.render(result_text, True, WHITE)
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 100))
            again_text = self.font.render("Press ENTER to play again", True, WHITE)
            self.screen.blit(again_text, (WIDTH//2 - again_text.get_width()//2, HEIGHT - 50))

if __name__ == "__main__":
    pygame.init()  # Temporary 
    game = WordGame()
    game.run()