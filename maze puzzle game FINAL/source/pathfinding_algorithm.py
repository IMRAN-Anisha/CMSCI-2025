# sabstract class
from abc import ABC, abstractmethod

class PathfindingAlgorithm(ABC):
    @abstractmethod
    def solve(self, maze, start, end):
        """Find a path from start to end in the maze."""
        pass