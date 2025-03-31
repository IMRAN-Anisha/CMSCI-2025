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


# Button Class
class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Menu Screens
def main_menu():
    buttons = [
        Button("Play", 200, 200, 200, 50, game_mode_menu),
        Button("Quit", 200, 300, 200, 50, sys.exit)
    ]
    menu_loop(buttons)

def game_mode_menu():
    buttons = [
        Button("Mode 1", 200, 150, 200, 50, difficulty_menu),
        Button("Mode 2", 200, 250, 200, 50, difficulty_menu),
        Button("Mode 3", 200, 350, 200, 50, difficulty_menu),
        Button("Back", 200, 450, 200, 50, main_menu)
    ]
    menu_loop(buttons)

def difficulty_menu():
    buttons = [
        Button("Easy", 200, 150, 200, 50, start_game),
        Button("Medium", 200, 250, 200, 50, start_game),
        Button("Hard", 200, 350, 200, 50, start_game),
        Button("Back", 200, 450, 200, 50, game_mode_menu)
    ]
    menu_loop(buttons)

def menu_loop(buttons):
    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked(event.pos) and button.action:
                        button.action()
                        return
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

# Maze Generation
def generate_maze():
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

# Game Logic
def start_game():
    global maze, player_pos
    maze = generate_maze()
    start, end = (1, 1), (GRID_SIZE - 2, GRID_SIZE - 2)
    player_pos = list(start)
    solver = DFSSolver()
    solution_path = solver.solve(maze, start, end)
    game_loop(solution_path, end)

def game_loop(solution_path, end):
    running = True
    while running:
        screen.fill(WHITE)
        draw_maze(solution_path, end)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_movement(event)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

def draw_maze(solution_path, end):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            color = WHITE if maze[i][j] == 0 else BLACK
            pygame.draw.rect(screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if solution_path:
        for (x, y) in solution_path:
            pygame.draw.rect(screen, GREEN, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
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

if __name__ == "__main__":
    main_menu()
