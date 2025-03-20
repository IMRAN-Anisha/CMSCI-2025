# Delvierable 3 - initial prototype: core functionality

import pygame
import pygame
import sys
from dfs_solver import DFSSolver

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# Maze (0 = open path, 1 = wall)
maze = [[0 if (i % 2 == 1 and j % 2 == 1) else 1 for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
start, end = (1, 1), (GRID_SIZE - 2, GRID_SIZE - 2)

# Solve the maze using DFS
solver = DFSSolver()
solution_path = solver.solve(maze, start, end)

def draw_maze():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = WHITE if maze[i][j] == 0 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw start and end points
    pygame.draw.rect(screen, BLUE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw solution path
    if solution_path:
        for (x, y) in solution_path:
            pygame.draw.rect(screen, (0, 255, 0), (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    running = True
    while running:
        screen.fill(WHITE)
        draw_maze()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
