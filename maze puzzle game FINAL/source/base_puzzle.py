#examples of abstraction OOP techniques 
import pygame
import sys
from abc import ABC, abstractmethod

class BasePuzzle(ABC):
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.font = pygame.font.Font(None, 30)  # Default font for HUD

    @abstractmethod
    def generate_puzzle(self):
        """Generate the puzzle (e.g., maze, word list, sudoku grid)."""
        pass

    @abstractmethod
    def run(self):
        """Run the game loop for this puzzle."""
        pass

    @abstractmethod
    def handle_key(self, event):
        """Handle keyboard input for the puzzle."""
        pass

    @abstractmethod
    def draw(self):
        """Draw the puzzle and HUD elements."""
        pass

    def quit_game(self, return_to_menu=False):
        """Handle quitting the game."""
        print(f"quit_game called with return_to_menu={return_to_menu}, setting running to False")
        self.running = False
        if not return_to_menu:
            pygame.quit()
            sys.exit()
        return True