# easy_maze.py
from games.puzzle_game import PuzzleGame
from source.constants import WIDTH

class EasyMaze(PuzzleGame):
    GRID_SIZE = 15  # Smaller maze
    CELL_SIZE = WIDTH // GRID_SIZE

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.time_limit = -1  # No timer for Easy

# medium_maze.py
from games.puzzle_game import PuzzleGame
from source.constants import WIDTH

class MediumMaze(PuzzleGame):
    GRID_SIZE = 21  # Default maze size
    CELL_SIZE = WIDTH // GRID_SIZE

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.time_limit = 120  # 120 seconds

# hard_maze.py
from games.puzzle_game import PuzzleGame
from source.constants import WIDTH

class HardMaze(PuzzleGame):
    GRID_SIZE = 25  # Larger maze
    CELL_SIZE = WIDTH // GRID_SIZE

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.time_limit = 60  # 60 seconds