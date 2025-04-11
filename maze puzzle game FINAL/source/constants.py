#Constants.py
#Common within games
WIDTH, HEIGHT = 600, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Used for paths or correct answers
YELLOW = (255, 255, 0)  # Used for hints or partial correct
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (120, 124, 126)  # Wrong letter in word game

# Word game 
WORD_GREEN = (106, 170, 100)  # Correct letter, correct position
WORD_YELLOW = (201, 180, 88)  # Correct letter, wrong position

# Grid and cell sizes
GRID_SIZE = 21  # For maze game
CELL_SIZE = WIDTH // GRID_SIZE  # For maze game
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_OFFSET_X = (WIDTH - GRID_WIDTH) // 2
GRID_OFFSET_Y = 80  # Moved up from 100 to 80 for number game

# Number game
NUMBER_GRID_SIZE = 9  # Sudoku grid (9x9)
NUMBER_CELL_SIZE = 50  # Sudoku cells

