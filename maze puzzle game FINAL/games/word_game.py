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
        self.word_length = 5  # Default, will change with difficulty
        self.correct_word = ""
        self.guesses = [[] for _ in range(6)]  # 6 tries
        self.current_guess = []
        self.guess_string = ""
        self.guess_count = 0
        self.game_result = ""

    def run(self):
        self.show_difficulty_menu()  # Pick level

    def show_difficulty_menu(self):
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
        # Pick word based on length (adjust these names if your words.py is different)
        if length == 3:
            self.correct_word = random.choice(Three_LETTER).upper()
        elif length == 4:
            self.correct_word = random.choice(Four_LETTER).upper()
        else:
            self.correct_word = random.choice(Five_Letter).upper()
        self.game_loop()

    def back_to_menu(self):
        self.running = False

    def game_loop(self):
        while self.running:
            self.screen.fill((0, 0, 0))  
            test_text = self.font.render("Game is working", True, (255, 255, 255)) # this is not showing.
            self.screen.blit(test_text, (200, 50))
            if self.game_result != "":
                self.show_result()
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

    def add_letter(self, letter):
        self.guess_string += letter
        x_pos = 200 + len(self.current_guess) * 60  # Space letters out
        text = self.font.render(letter, True, (255, 255, 255))
        self.current_guess.append({"letter": letter, "x": x_pos, "color": "white"})
        self.draw()

    def delete_letter(self):
        self.guess_string = self.guess_string[:-1]
        self.current_guess.pop()

    def check_guess(self):
        guess = self.guess_string.lower()
        # Simple check (not perfect like Wordle yet)
        if guess == self.correct_word.lower():
            self.game_result = "W"
            for i, letter in enumerate(self.current_guess):
                letter["color"] = "#6aaa64"  # Green
        else:
            for i, letter in enumerate(self.current_guess):
                if letter["letter"] in self.correct_word and letter["letter"] == self.correct_word[i]:
                    letter["color"] = "#6aaa64"  
                elif letter["letter"] in self.correct_word:
                    letter["color"] = "#c9b458"  # Yellow
                else:
                    letter["color"] = "#787c7e"  # Grey
            self.guesses[self.guess_count] = self.current_guess
            self.guess_count += 1
            self.current_guess = []
            self.guess_string = ""
            if self.guess_count == 6:
                self.game_result = "L"

    def draw(self):
        self.screen.fill((0, 0, 0))
        #past guesses
        for guess in self.guesses[:self.guess_count]:
            for letter in guess:
                pygame.draw.rect(self.screen, letter["color"], (letter["x"], 100 + self.guesses.index(guess) * 60, 50, 50))
                text = self.font.render(letter["letter"], True, (255, 255, 255))
                self.screen.blit(text, (letter["x"] + 10, 110 + self.guesses.index(guess) * 60))
        # current guess
        for letter in self.current_guess:
            pygame.draw.rect(self.screen, letter["color"], (letter["x"], 100 + self.guess_count * 60, 50, 50))
            text = self.font.render(letter["letter"], True, (255, 255, 255))
            self.screen.blit(text, (letter["x"] + 10, 110 + self.guess_count * 60))

    def show_result(self):
        result_text = "You Win!" if self.game_result == "W" else f"You Lose! Word was {self.correct_word}"
        text = self.font.render(result_text, True, (255, 255, 255))
        self.screen.blit(text, (200, 400))
        again_text = self.font.render("Press ENTER to play again", True, (255, 255, 255))
        self.screen.blit(again_text, (200, 450))

    def reset(self):
        self.start_game(self.word_length)  # Restart with same difficulty