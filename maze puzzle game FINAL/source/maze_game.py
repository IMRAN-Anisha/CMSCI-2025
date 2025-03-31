import pygame
import random
import sys
from source.UI import Button
from source.dfs_solver import DFSSolver
from source.constants import *

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]  # 1 represents walls
        self.visited = set()

    def generate_maze(self, x=1, y=1):
        self.maze[y][x] = 0  # Mark as path (0 represents open space)
        self.visited.add((x, y))
        
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (1 <= nx < self.width-1 and 1 <= ny < self.height-1) and (nx, ny) not in self.visited:
                self.maze[y + dy // 2][x + dx // 2] = 0  # Remove wall between cells
                self.generate_maze(nx, ny)  # Recursive call

    def get_maze(self):
        return self.maze

class MazeGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True

    def run(self):
        self.show_game_mode_menu()

    def show_game_mode_menu(self):
        buttons = [
            Button("Mode 1", 200, 150, 200, 50, BLUE, GRAY, self.show_difficulty_menu),
            Button("Mode 2", 200, 250, 200, 50, BLUE, GRAY, self.show_difficulty_menu),
            Button("Mode 3", 200, 350, 200, 50, BLUE, GRAY, self.show_difficulty_menu),
            Button("Back", 200, 450, 200, 50, BLUE, GRAY, self.back_to_menu)
        ]
        self.menu_loop(buttons)

    def show_difficulty_menu(self):
        buttons = [
            Button("Easy", 200, 150, 200, 50, BLUE, GRAY, lambda: self.start_game("Easy")),
            Button("Medium", 200, 250, 200, 50, BLUE, GRAY, lambda: self.start_game("Medium")),
            Button("Hard", 200, 350, 200, 50, BLUE, GRAY, lambda: self.start_game("Hard")),
            Button("Back", 200, 450, 200, 50, BLUE, GRAY, self.show_game_mode_menu)
        ]
        self.menu_loop(buttons)

    def menu_loop(self, buttons):
        while self.running:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for button in buttons:
                    if button.is_clicked(event) and button.action:
                        button.action()
                        return
            for button in buttons:
                button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def back_to_menu(self):
        self.running = False  # Return to main menu

    def start_game(self, difficulty):
        generator = MazeGenerator(GRID_SIZE, GRID_SIZE)
        generator.generate_maze()  # Generate the maze starting at (1, 1)
        maze = generator.get_maze()
        start, end = (1, 1), (GRID_SIZE - 2, GRID_SIZE - 2)
        self.player_pos = list(start)
        solver = DFSSolver()
        solution_path = solver.solve(maze, start, end)
        self.game_loop(maze, solution_path, end)

    def game_loop(self, maze, solution_path, end):
        while self.running:
            self.screen.fill(WHITE)
            self.draw_maze(maze, solution_path, end)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()  # Fully exit on window close
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:  # Quit on Q key press only when in game
                        pygame.quit()
                        sys.exit()
                    self.handle_movement(event, maze)
            pygame.display.flip()
            self.clock.tick(60)

    def draw_maze(self, maze, solution_path, end):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                color = WHITE if maze[i][j] == 0 else BLACK
                pygame.draw.rect(self.screen, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        if solution_path:
            for (x, y) in solution_path:
                pygame.draw.rect(self.screen, GREEN, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, BLUE, (self.player_pos[1] * CELL_SIZE, self.player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, RED, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def handle_movement(self, event, maze):
        x, y = self.player_pos
        if event.key == pygame.K_UP and x > 0 and maze[x-1][y] == 0:
            self.player_pos[0] -= 1
        elif event.key == pygame.K_DOWN and x < GRID_SIZE-1 and maze[x+1][y] == 0:
            self.player_pos[0] += 1
        elif event.key == pygame.K_LEFT and y > 0 and maze[x][y-1] == 0:
            self.player_pos[1] -= 1
        elif event.key == pygame.K_RIGHT and y < GRID_SIZE-1 and maze[x][y+1] == 0:
            self.player_pos[1] += 1