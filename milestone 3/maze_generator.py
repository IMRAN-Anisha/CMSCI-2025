import random

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]  # 1 represents walls
        self.visited = set()

    def generate_maze(self, x=1, y=1):
        #Generates a maze using Recursive Backtracking (DFS).
        self.maze[y][x] = 0  # Mark as path (0 represents open space)
        self.visited.add((x, y))
        
        # Define movement directions (randomized for variation)
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (1 <= nx < self.width-1 and 1 <= ny < self.height-1) and (nx, ny) not in self.visited:
                self.maze[y + dy // 2][x + dx // 2] = 0  # Remove wall between cells
                self.generate_maze(nx, ny)  # Recursive call

    def get_maze(self):
        return self.maze