# Deliverable 3 - Initial Prototype: Core Functionality

import pygame
import sys
import random
from dfs_solver import DFSSolver

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 21  # Must be odd for proper maze generation
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Player
RED = (255, 0, 0)  # Goal
GREEN = (0, 255, 0)  # Solution Path

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

def generate_maze(): # backtracking part 
    maze = [[1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    start = (1, 1)
    stack = [start]
    visited = set([start])
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    
    while stack:
        x, y = stack[-1]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < GRID_SIZE-1 and 1 <= ny < GRID_SIZE-1 and (nx, ny) not in visited:
                maze[nx][ny] = 0
                maze[x + dx//2][y + dy//2] = 0
                visited.add((nx, ny))
                stack.append((nx, ny))
                break
        else:
            stack.pop()
    
    maze[1][1] = 0  # Start position
    maze[GRID_SIZE-2][GRID_SIZE-2] = 0  # Goal position
    return maze

# Generate a new maze each time the program runs
maze = generate_maze()
start, end = (1, 1), (GRID_SIZE - 2, GRID_SIZE - 2)
player_pos = list(start)  # Player position

# Solve the maze using DFS
solver = DFSSolver()
solution_path = solver.solve(maze, start, end)

def draw_maze():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = WHITE if maze[i][j] == 0 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw solution path
    if solution_path:
        for (x, y) in solution_path:
            pygame.draw.rect(screen, GREEN, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw player and goal
    pygame.draw.rect(screen, BLUE, (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def handle_movement(event):
    global player_pos
    x, y = player_pos
    
    if event.key == pygame.K_UP and x > 0 and maze[x-1][y] == 0:
        player_pos[0] -= 1
    elif event.key == pygame.K_DOWN and x < GRID_SIZE-1 and maze[x+1][y] == 0:
        player_pos[0] += 1
    elif event.key == pygame.K_LEFT and y > 0 and maze[x][y-1] == 0:
        player_pos[1] -= 1
    elif event.key == pygame.K_RIGHT and y < GRID_SIZE-1 and maze[x][y+1] == 0:
        player_pos[1] += 1

def main():
    running = True
    while running:
        screen.fill(WHITE)
        draw_maze()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_movement(event)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
