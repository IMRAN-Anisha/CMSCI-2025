import unittest
from unittest.mock import Mock, patch
import sys
import os

# Adjust path to find 'games' from 'tests'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'games')))
from games.word_game import WordGame

class TestWordGame(unittest.TestCase):
    @patch('pygame.display.flip', Mock())  # Mock display.flip to avoid display errors
    @patch('pygame.draw.rect', Mock())  # Mock draw.rect to avoid surface errors
    @patch('pygame.font.Font', Mock(return_value=Mock(render=Mock(return_value=Mock()))))  # Mock font rendering
    def setUp(self):
        # Fake Pygame stuff
        self.mock_screen = Mock()
        self.mock_clock = Mock()
        self.game = WordGame(self.mock_screen, self.mock_clock)
        # Reset game state
        self.game.running = True
        self.game.guess_count = 0
        self.game.current_guess = []
        self.game.guess_string = ""
        self.game.game_result = ""

    @patch('word_game.WordGame.game_loop', Mock())  # Mock game_loop to avoid display issues
    @patch('word_game.WordGame.draw', Mock())
    def test_start_game_sets_word_length(self):
        # Test if start_game sets the right word length and picks a word
        with patch("random.choice") as mock_choice:
            mock_choice.side_effect = ["cat", "cake", "coder"]  # Fake words
            self.game.start_game(3)
            self.assertEqual(self.game.word_length, 3)
            self.assertEqual(self.game.correct_word, "CAT")
            self.game.start_game(4)
            self.assertEqual(self.game.word_length, 4)
            self.assertEqual(self.game.correct_word, "CAKE")
            self.game.start_game(5)
            self.assertEqual(self.game.word_length, 5)
            self.assertEqual(self.game.correct_word, "CODER")

    @patch('word_game.WordGame.draw', Mock())
    def test_add_letter_builds_guess(self):
        # Test adding letters to the guess
        self.game.word_length = 3
        self.game.add_letter("A")
        self.assertEqual(self.game.guess_string, "A")
        self.assertEqual(len(self.game.current_guess), 1)
        self.assertEqual(self.game.current_guess[0]["letter"], "A")
        self.game.add_letter("B")
        self.assertEqual(self.game.guess_string, "AB")
        self.assertEqual(len(self.game.current_guess), 2)

    @patch('word_game.WordGame.draw', Mock())
    def test_delete_letter_removes_last(self):
        # Test deleting the last letter
        self.game.word_length = 3
        self.game.add_letter("A")
        self.game.add_letter("B")
        self.game.delete_letter()
        self.assertEqual(self.game.guess_string, "A")
        self.assertEqual(len(self.game.current_guess), 1)
        self.assertEqual(self.game.current_guess[0]["letter"], "A")

    @patch('word_game.WordGame.draw', Mock())
    def test_check_guess_wins(self):
        # Test winning with a correct guess
        self.game.word_length = 3
        self.game.correct_word = "CAT"
        self.game.add_letter("C")
        self.game.add_letter("A")
        self.game.add_letter("T")
        self.game.check_guess()
        self.assertEqual(self.game.game_result, "W")
        self.assertEqual(self.game.current_guess[0]["color"], "#6aaa64")  # Green
        self.assertEqual(self.game.current_guess[1]["color"], "#6aaa64")
        self.assertEqual(self.game.current_guess[2]["color"], "#6aaa64")

    @patch('word_game.WordGame.draw', Mock())
    def test_check_guess_loses(self):
        # Test losing after 6 wrong guesses
        self.game.word_length = 3
        self.game.correct_word = "CAT"
        for _ in range(6):
            self.game.add_letter("D")
            self.game.add_letter("O")
            self.game.add_letter("G")
            self.game.check_guess()
            if _ < 5:  # Before the 6th guess
                self.assertEqual(self.game.game_result, "")
                self.assertEqual(self.game.guess_count, _ + 1)
        self.assertEqual(self.game.game_result, "L")

    @patch('word_game.WordGame.draw', Mock())
    def test_check_guess_colors(self):
        # Test coloring (green, yellow, grey)
        self.game.word_length = 3
        self.game.correct_word = "CAT"
        self.game.add_letter("C")  # Right spot
        self.game.add_letter("T")  # In word, wrong spot
        self.game.add_letter("X")  # Not in word
        self.game.check_guess()
        # Check colors in the stored guess (not current_guess, since it's cleared)
        last_guess = self.game.guesses[self.game.guess_count - 1]
        self.assertEqual(last_guess[0]["color"], "#6aaa64")  # Green
        self.assertEqual(last_guess[1]["color"], "#c9b458")  # Yellow
        self.assertEqual(last_guess[2]["color"], "#787c7e")  # Grey

if __name__ == "__main__":
    unittest.main()