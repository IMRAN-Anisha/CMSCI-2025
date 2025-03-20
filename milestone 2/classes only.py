class Player:
    def __init__(self, name):
        self.name = name
        self.position = (0, 0)  # Example start position
        self.score = 0
        self.performance = "neutral"
    
    def update_position(self, new_position):
        self.position = new_position
    
    def update_score(self, points):
        self.score += points
    
    def evaluate_performance(self):
        # Example: Update performance based on score or time
        if self.score > 100:
            self.performance = "quick"
        elif self.score < 50:
            self.performance = "struggling"
        else:
            self.performance = "neutral"

class GameManager:
    def __init__(self, player, puzzle_type):
        self.player = player
        self.current_puzzle = puzzle_type
        self.game_state = "ongoing"
    
    def start_game(self):
        # Initialize the first puzzle and start the game loop
        self.current_puzzle.generate_puzzle()
        print(f"Game started for {self.player.name}.")
    
    def next_puzzle(self):
        # Transition to the next puzzle
        self.current_puzzle = PuzzleFactory.create_puzzle()
        self.current_puzzle.generate_puzzle()
    
    def end_game(self):
        self.game_state = "ended"
        print("Game Over!")
    
    def evaluate_game(self):
        self.player.evaluate_performance()
        if self.player.performance == "quick":
            # Adjust difficulty or end game
            print("Player is performing well. Increasing difficulty.")
        elif self.player.performance == "struggling":
            print("Player is struggling. Adjusting difficulty.")

# Might not include anymore in final project, SUBJECT TO CHANGE.
'''
class PuzzleFactory:
    @staticmethod
    def create_puzzle(puzzle_type="math"):
        if puzzle_type == "math":
            return MathPuzzle()
        elif puzzle_type == "word":
            return WordPuzzle()
        elif puzzle_type == "logic":
            return LogicPuzzle()
        else:
            raise ValueError("Invalid puzzle type")
'''

import time

class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
    
    def start_timer(self):
        self.start_time = time.time()
    
    def stop_timer(self):
        self.end_time = time.time()
    
    def get_time_taken(self):
        return self.end_time - self.start_time

class ScoreManager:
    def __init__(self):
        self.score = 0
    
    def update_score(self, points):
        self.score += points
    
    def get_score(self):
        return self.score

