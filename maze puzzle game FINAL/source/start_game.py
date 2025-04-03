import random
from words import Three_LETTER,Four_LETTER,Five_Letter
if length == 3:
    self.correct_word = random.choice(Three_LETTER).upper()
elif length == 4:
    self.correct_word = random.choice(Four_LETTER).upper()
else:
    self.correct_word = random.choice(Five_Letter).upper()

def start_game(self, length):
    self.word_length = length
    print(f"Starting game with {length} letters")
    try:
        if length == 3:
            self.correct_word = random.choice(Three_LETTER).upper()
        elif length == 4:
            self.correct_word = random.choice(Four_LETTER).upper()
        else:
            self.correct_word = random.choice(Five_Letter).upper()
        print(f"Correct word set to: {self.correct_word}")
    except NameError as e:
        print(f"Error with word lists: {e}")
        self.correct_word = "TEST"  # Fallback
    self.game_loop()