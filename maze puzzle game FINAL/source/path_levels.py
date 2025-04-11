from games.puzzle_game import PuzzleGame
from source.constants import WIDTH

class EasyMaze(PuzzleGame):
    GRID_SIZE = 15  # Smaller maze
    CELL_SIZE = WIDTH // GRID_SIZE

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.set_time_limit(-1)  # No timer for Easy

class MediumMaze(PuzzleGame):
    GRID_SIZE = 21  # Default maze size
    CELL_SIZE = WIDTH // GRID_SIZE

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.set_time_limit(120)  # 120 seconds

class HardMaze(PuzzleGame):
    GRID_SIZE = 25  # Larger maze
    CELL_SIZE = WIDTH // GRID_SIZE

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.set_time_limit(60)  # 60 seconds