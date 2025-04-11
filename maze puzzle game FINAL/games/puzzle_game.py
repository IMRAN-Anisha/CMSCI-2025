import sys
import os
# Add the parent directory (maze_puzzle_game_FINAL) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import random
from source.UI import Button
from source.dfs_solver import DFSSolver  # Using source.dfs_solver for now
from source.constants import *

# Constants (override if not defined in source.constants)
GRID_SIZE = 21
CELL_SIZE = WIDTH // GRID_SIZE
YELLOW = (255, 255, 0)  # Hint color (if not in source.constants)

class PuzzleGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.maze = None
        self.player_pos = [1, 1]
        self.start = (1, 1)
        self.end = (GRID_SIZE - 2, GRID_SIZE - 2)
        self.solution_path = None
        self.show_solution = False
        self.show_hint = False
        self.score = 0
        self.timer = 0
        self.time_limit = None  # Will be set based on difficulty
        self.current_difficulty = None

    def run(self):
        while self.running:
            # Start with the difficulty menu
            difficulty = self.difficulty_menu()
            if difficulty is None:  # Player chose to go back or quit
                break  # Return to main menu in main.py
            # Start the game with the selected difficulty
            self.start_game(difficulty)
        return True  # Signal to return to main menu

    def difficulty_menu(self):
        buttons = [
            Button("Easy", 200, 150, 200, 50, BLUE, GRAY, lambda: "easy"),
            Button("Medium", 200, 250, 200, 50, BLUE, GRAY, lambda: "medium"),
            Button("Hard", 200, 350, 200, 50, BLUE, GRAY, lambda: "hard"),
            Button("Back", 200, 450, 200, 50, BLUE, GRAY, lambda: None)  # Return to main menu
        ]
        return self.menu_loop(buttons)

    def menu_loop(self, buttons):
        while self.running:
            self.screen.fill(BLACK)
            title = self.font.render("Maze Adventure", True, WHITE)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected in menu_loop")
                    self.quit_game(return_to_menu=True)
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_Q):
                        print("Q key pressed in menu_loop - quitting")
                        self.quit_game(return_to_menu=True)
                        return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.is_clicked(event):
                            return button.action()
            
            for button in buttons:
                button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        return None

    def generate_maze(self):
        self.maze = [[1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        stack = [self.start]
        visited = set([self.start])
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            x, y = stack[-1]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 1 <= nx < GRID_SIZE-1 and 1 <= ny < GRID_SIZE-1 and (nx, ny) not in visited:
                    self.maze[nx][ny] = 0
                    self.maze[x + dx//2][y + dy//2] = 0
                    visited.add((nx, ny))
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()
        
        self.maze[1][1] = 0
        self.maze[GRID_SIZE-2][GRID_SIZE-2] = 0
        solver = DFSSolver()
        self.solution_path = solver.solve(self.maze, self.start, self.end)

    def start_game(self, difficulty):
        self.current_difficulty = difficulty
        # Set time limit based on difficulty
        difficulty_settings = {
            "easy": {"time_limit": -1},  # No timer
            "medium": {"time_limit": 120},  # 120 seconds
            "hard": {"time_limit": 60}  # 60 seconds
        }
        settings = difficulty_settings[difficulty]
        self.time_limit = settings["time_limit"]
        self.timer = 0 if self.time_limit >= 0 else -1  # Timer only for Medium and Hard
        # Generate the maze
        self.generate_maze()
        # Reset player state
        self.player_pos = [1, 1]
        self.show_solution = False
        self.show_hint = False
        self.score = 0
        return self.game_loop()

    def quit_game(self, return_to_menu=False):
        print(f"quit_game called with return_to_menu={return_to_menu}, setting running to False")
        self.running = False
        if not return_to_menu:
            pygame.quit()
            sys.exit()
        return True

    def game_loop(self):
        while self.running:
            self.screen.fill(BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected in game_loop")
                    self.quit_game(return_to_menu=True)
                    return True
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event)
            
            if self.timer >= 0:  # Timer active
                self.timer += 1/60
                if self.timer >= self.time_limit:
                    return self.loss_screen()  # Player ran out of time
            
            self.draw_game()
            if tuple(self.player_pos) == self.end:
                return self.victory_screen()
            pygame.display.flip()
            self.clock.tick(60)
        return True

    def handle_key(self, event):
        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            self.handle_movement(event)
        elif event.key == pygame.K_h:
            self.show_hint = not self.show_hint
            if self.show_hint:
                self.score -= 5
        elif event.key == pygame.K_s:
            self.show_solution = not self.show_solution
            if self.show_solution:
                self.score -= 10
        elif event.key == pygame.K_r:
            self.start_game(self.current_difficulty)
        elif event.key in (pygame.K_q, pygame.K_Q):
            print("Q key pressed in game_loop - quitting")
            self.quit_game(return_to_menu=True)

    def handle_movement(self, event):
        x, y = self.player_pos
        new_x, new_y = x, y
        if event.key == pygame.K_UP and x > 0:
            new_x -= 1
        elif event.key == pygame.K_DOWN and x < GRID_SIZE-1:
            new_x += 1
        elif event.key == pygame.K_LEFT and y > 0:
            new_y -= 1
        elif event.key == pygame.K_RIGHT and y < GRID_SIZE-1:
            new_y += 1
        
        if self.maze[new_x][new_y] == 0:
            self.player_pos = [new_x, new_y]
            self.score += 1

    def draw_game(self):
        # Draw maze
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(self.screen, WHITE, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw solution or hint
        if self.show_solution and self.solution_path:
            for x, y in self.solution_path:
                pygame.draw.rect(self.screen, GREEN, (y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        elif self.show_hint and self.solution_path:
            next_step = self.solution_path[1] if len(self.solution_path) > 1 else self.solution_path[0]
            pygame.draw.rect(self.screen, YELLOW, (next_step[1]*CELL_SIZE, next_step[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw player and goal
        pygame.draw.rect(self.screen, BLUE, (self.player_pos[1]*CELL_SIZE, self.player_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, RED, (self.end[1]*CELL_SIZE, self.end[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw HUD
        title = self.font.render("Maze Adventure", True, WHITE)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 50))
        if self.timer >= 0:
            time_text = self.font.render(f"Time: {self.timer:.1f}/{self.time_limit}", True, WHITE)
            self.screen.blit(time_text, (10, 80))
        hint_text = self.font.render("H: Hint | S: Solution | R: Restart | Q: Quit", True, WHITE)
        self.screen.blit(hint_text, (10, HEIGHT-40))

    def victory_screen(self):
        while self.running:
            self.screen.fill(BLACK)
            victory_text = self.font.render("Congratulations! You Won!", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            time_text = self.font.render(f"Time: {self.timer:.1f}" if self.timer >= 0 else "Time: N/A", True, WHITE)
            replay = Button("Play Again", 200, 300, 200, 50, BLUE, GRAY, lambda: self.start_game(self.current_difficulty))
            menu = Button("Main Menu", 200, 400, 200, 50, BLUE, GRAY, lambda: True)

            self.screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, 100))
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))
            self.screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 250))
            replay.draw(self.screen)
            menu.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected in victory_screen")
                    self.quit_game(return_to_menu=True)
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_Q):
                        print("Q key pressed in victory_screen - quitting")
                        self.quit_game(return_to_menu=True)
                        return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.is_clicked(event):
                        replay.action()
                        return False
                    if menu.is_clicked(event):
                        return menu.action()
            
            pygame.display.flip()
            self.clock.tick(60)
        return True

    def loss_screen(self):
        while self.running:
            self.screen.fill(BLACK)
            loss_text = self.font.render("Time's Up! You Got Lost!", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            time_text = self.font.render(f"Time: {self.timer:.1f}", True, WHITE)
            replay = Button("Try Again", 200, 300, 200, 50, BLUE, GRAY, lambda: self.start_game(self.current_difficulty))
            menu = Button("Main Menu", 200, 400, 200, 50, BLUE, GRAY, lambda: True)

            self.screen.blit(loss_text, (WIDTH//2 - loss_text.get_width()//2, 100))
            self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))
            self.screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 250))
            replay.draw(self.screen)
            menu.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quit event detected in loss_screen")
                    self.quit_game(return_to_menu=True)
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_Q):
                        print("Q key pressed in loss_screen - quitting")
                        self.quit_game(return_to_menu=True)
                        return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.is_clicked(event):
                        replay.action()
                        return False
                    if menu.is_clicked(event):
                        return menu.action()
            
            pygame.display.flip()
            self.clock.tick(60)
        return True

#testing 
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Adventure")
    clock = pygame.time.Clock()
    game = PuzzleGame(screen, clock)
    game.run()