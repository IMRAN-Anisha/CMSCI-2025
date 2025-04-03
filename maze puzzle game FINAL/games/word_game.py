import pygame
import sys
import random
from source.UI import Button
from source.words import *

pygame.init()

class WordGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.font = pygame.font.Font(None, 50)
        self.word_length = 5
        self.correct_word = ""
        self.guesses = [[] for _ in range(6)]
        self.current_guess = []
        self.guess_string = ""
        self.guess_count = 0
        self.game_result = ""

    def run(self):
        self.show_difficulty_menu()

    def show_difficulty_menu(self):
        print("Showing difficulty menu")  # Debug
        buttons = [
            Button("Easy (3 letters)", 200, 200, 200, 50, (50, 50, 255), (180, 180, 180), lambda: self.start_game(3)),
            Button("Medium (4 letters)", 200, 300, 200, 50, (50, 50, 255), (180, 180, 180), lambda: self.start_game(4)),
            Button("Hard (5 letters)", 200, 400, 200, 50, (50, 50, 255), (180, 180, 180), lambda: self.start_game(5)),
            Button("Back", 200, 500, 200, 50, (50, 50, 255), (180, 180, 180), self.back_to_menu)
        ]
        while self.running:
            self.screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
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
        print(f"Starting game with {length} letters")  # Debug
        try:
            if length == 3:
                self.correct_word = random.choice(WORDS_3).upper()
            elif length == 4:
                self.correct_word = random.choice(WORDS_4).upper()
            else:
                self.correct_word = random.choice(WORDS_5).upper()
            print(f"Correct word set to: {self.correct_word}")  # Debug
        except NameError as e:
            print(f"Error with word lists: {e}")
            self.correct_word = "TEST"  # Fallback
        self.game_loop()

    def back_to_menu(self):
        self.running = False

    def game_loop(self):
        print("Entering game loop")  # Debug
        while self.running:
            self.screen.fill((0, 0, 0))
            print("Drawing frame")  # Debug
            test_text = self.font.render("Game is working", True, (255, 255, 255))
            self.screen.blit(test_text, (200, 50))
            if self.game_result != "":
                self.show_result()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_RETURN:
                        if self.game_result != "":
                            self.reset()
                        elif len(self.guess_string) == self.word_length:
                            self.check_guess()
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.guess_string) > 0:
                            self.delete_letter()
                    else:
                        key = event.unicode.upper()
                        if key in "QWERTYUIOPASDFGHJKLZXCVBNM" and len(self.guess_string) < self.word_length:
                            self.add_letter(key)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        print("Exiting game loop")  # Debug

    def add_letter(self, letter):
        self.guess_string += letter
        x_pos = 200 + len(self.current_guess) * 60
        text = self.font.render(letter, True, (255, 255, 255))
        self.current_guess.append({"letter": letter, "x": x_pos, "color": "white"})
        print(f"Added letter: {letter}, Guess: {self.guess_string}")  # Debug
        self.draw()

    def delete_letter(self):
        self.guess_string = self.guess_string[:-1]
        self.current_guess.pop()
        print(f"Deleted letter, Guess: {self.guess_string}")  # Debug

    def check_guess(self):
        guess = self.guess_string.lower()
        print(f"Checking guess: {guess} against {self.correct_word}")  # Debug
        if guess == self.correct_word.lower():
            self.game_result = "W"
            for i, letter in enumerate(self.current_guess):
                letter["color"] = "#6aaa64"
        else:
            for i, letter in enumerate(self.current_guess):
                if i < len(self.correct_word) and letter["letter"] == self.correct_word[i]:
                    letter["color"] = "#6aaa64"
                elif letter["letter"] in self.correct_word:
                    letter["color"] = "#c9b458"
                else:
                    letter["color"] = "#787c7e"
            self.guesses[self.guess_count] = self.current_guess
            self.guess_count += 1
            self.current_guess = []
            self.guess_string = ""
            if self.guess_count == 6:
                self.game_result = "L"

    def draw(self):
        # Draw past guesses with colors
        y_offset = 100
        for i, guess in enumerate(self.guesses[:self.guess_count]):
            for j, letter in enumerate(guess):
                # Draw a colored square
                pygame.draw.rect(self.screen, letter["color"], (200 + j * 60, y_offset + i * 50, 50, 50))
                # Draw the letter on top
                letter_text = self.font.render(letter["letter"], True, (255, 255, 255))
                self.screen.blit(letter_text, (210 + j * 60, y_offset + i * 50))
        # Draw current guess (white, since not evaluated yet)
        for j, letter in enumerate(self.current_guess):
            pygame.draw.rect(self.screen, "white", (200 + j * 60, y_offset + self.guess_count * 50, 50, 50))
            letter_text = self.font.render(letter["letter"], True, (255, 255, 255))
            self.screen.blit(letter_text, (210 + j * 60, y_offset + self.guess_count * 50))
        print(f"Drawing guess: {self.guess_string}, Past guesses: {[ ''.join(l['letter'] for l in g) for g in self.guesses[:self.guess_count] ]}")  # Debug

    def show_result(self):
        result_text = "You Win!" if self.game_result == "W" else f"You Lose! Word was {self.correct_word}"
        text = self.font.render(result_text, True, (255, 255, 255))
        self.screen.blit(text, (200, 400))
        again_text = self.font.render("Press ENTER to play again", True, (255, 255, 255))
        self.screen.blit(again_text, (200, 450))

    def reset(self):
        self.guess_count = 0
        self.current_guess = []
        self.guess_string = ""
        self.game_result = ""
        self.guesses = [[] for _ in range(6)]
        self.start_game(self.word_length)