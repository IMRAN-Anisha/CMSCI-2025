'''
import sys
import os
# Add the parent directory (maze_puzzle_game_FINAL) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import random
from source.UI import Button
from source.dfs_solver import DFSSolver  # Using source.dfs_solver for now
from source.constants import *

# source/pathfinding_algorithm.py
from abc import ABC, abstractmethod

#abstract class
class PathfindingAlgorithm(ABC):
    @abstractmethod
    def solve(self, maze, start, end):
        """Solve the maze and return the path from start to end."""
        pass

# Constants (override if not defined in source.constants)
GRID_SIZE = 21
CELL_SIZE = WIDTH // GRID_SIZE
YELLOW = (255, 255, 0)  # Hint color (if not in source.constants)

class PuzzleGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.font = pygame.font.Font(None, 30)  # Reduced from 36 to 30
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

    def run(self): #implements abstract method
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

        # Draw HUD with adjustments
        # Title
        title = self.font.render("Maze Adventure", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 10))
        pygame.draw.rect(self.screen, (255, 255, 255, 128), title_rect.inflate(20, 10), border_radius=5)
        self.screen.blit(title, title_rect)

        # Timer (unchanged)
        if self.timer >= 0:
            time_text = self.font.render(f"Time: {self.timer:.1f}/{self.time_limit}", True, BLACK)
            time_rect = time_text.get_rect(topright=(WIDTH - 10, 30))
            pygame.draw.rect(self.screen, (255, 255, 255, 128), time_rect.inflate(20, 10), border_radius=5)
            self.screen.blit(time_text, time_rect)

        # Instructions and Score (at the bottom)
        hint_text = self.font.render("H: Hint | S: Solution | R: Restart | Q: Quit", True, BLACK)
        hint_rect = hint_text.get_rect(bottomleft=(10, HEIGHT-10))
        
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        score_rect = score_text.get_rect(bottomleft=(hint_rect.right + 20, HEIGHT-10))  # Fixed: Use bottomleft

        # Check if the combined width exceeds the screen width
        combined_width = hint_rect.width + 20 + score_rect.width  # 20px padding between them
        if combined_width + 10 > WIDTH:  # +10 for left margin
            # Reduce font size if necessary
            font_size = self.font.get_height()
            while combined_width + 10 > WIDTH and font_size > 20:  # Don't go below size 20
                font_size -= 2
                self.font = pygame.font.Font(None, font_size)
                hint_text = self.font.render("H: Hint | S: Solution | R: Restart | Q: Quit", True, BLACK)
                hint_rect = hint_text.get_rect(bottomleft=(10, HEIGHT-10))
                score_text = self.font.render(f"Score: {self.score}", True, BLACK)
                score_rect = score_text.get_rect(bottomleft=(hint_rect.right + 20, HEIGHT-10))  # Fixed: Use bottomleft
                combined_width = hint_rect.width + 20 + score_rect.width

        # Draw hint text with background
        pygame.draw.rect(self.screen, (255, 255, 255, 128), hint_rect.inflate(20, 10), border_radius=5)
        self.screen.blit(hint_text, hint_rect)

        # Draw score text with background
        pygame.draw.rect(self.screen, (255, 255, 255, 128), score_rect.inflate(20, 10), border_radius=5)
        self.screen.blit(score_text, score_rect)

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

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Adventure")
    clock = pygame.time.Clock()
    game = PuzzleGame(screen, clock)
    game.run()

    '''
# games/puzzle_game.py
from source.base_puzzle import BasePuzzle
from source.score_manager import ScoreManager
from source.pathAI import AIAdaptiveSystem, DFSSolver
import pygame
import random

class PuzzleGame(BasePuzzle):
    GRID_SIZE = 21
    CELL_SIZE = 800 // GRID_SIZE  # Assuming WIDTH = 800 from constants

    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        # Private variables with double underscore
        self.__maze = None
        self.__player_pos = [1, 1]
        self.__score_manager = ScoreManager()
        self.__timer = 0
        self.__show_hint = False
        self.__show_solution = False
        self.__current_difficulty = None
        self.__time_limit = 60  # Default, overridden by subclasses
        self.__start = (1, 1)
        self.__end = (self.GRID_SIZE - 2, self.GRID_SIZE - 2)
        self.__solution_path = None
        self.__ai_system = AIAdaptiveSystem()
        self.__solver = DFSSolver()
        self.__font = pygame.font.Font(None, 36)

    # Getters
    def get_maze(self):
        """Returns the current maze grid."""
        return self.__maze

    def get_player_pos(self):
        """Returns the player's current position as [x, y]."""
        return self.__player_pos

    def get_score(self):
        """Returns the player's current score."""
        return self.__score_manager.get_score()

    def get_timer(self):
        """Returns the current timer value in seconds."""
        return self.__timer

    def is_hint_shown(self):
        """Returns True if the hint is currently shown."""
        return self.__show_hint

    def is_solution_shown(self):
        """Returns True if the solution path is currently shown."""
        return self.__show_solution

    def get_current_difficulty(self):
        """Returns the current difficulty level."""
        return self.__current_difficulty

    def get_time_limit(self):
        """Returns the time limit for the current game."""
        return self.__time_limit

    def get_start(self):
        """Returns the start position as (x, y)."""
        return self.__start

    def get_end(self):
        """Returns the end position as (x, y)."""
        return self.__end

    def get_solution_path(self):
        """Returns the solution path as a list of (x, y) coordinates."""
        return self.__solution_path

    # Setters
    def set_maze(self, maze):
        """Sets the maze grid."""
        self.__maze = maze

    def set_player_pos(self, new_pos):
        """Sets the player's position to new_pos [x, y] after validation."""
        self.__player_pos = new_pos

    def set_timer(self, value):
        """Sets the timer value, ensuring it's non-negative in timed mode."""
        if value < 0 and self.get_time_limit() >= 0:
            raise ValueError("Timer cannot be negative in timed mode")
        self.__timer = value

    def set_hint_shown(self, value):
        """Sets whether the hint is shown."""
        self.__show_hint = value

    def set_solution_shown(self, value):
        """Sets whether the solution path is shown."""
        self.__show_solution = value

    def set_current_difficulty(self, difficulty):
        """Sets the current difficulty level."""
        self.__current_difficulty = difficulty

    def set_time_limit(self, time_limit):
        """Sets the time limit for the game."""
        self.__time_limit = time_limit

    def set_start(self, start):
        """Sets the start position."""
        self.__start = start

    def set_end(self, end):
        """Sets the end position."""
        self.__end = end

    def set_solution_path(self, path):
        """Sets the solution path."""
        self.__solution_path = path

    def generate_puzzle(self):
        """Generates a maze using a simplified DFS algorithm."""
        # Initialize maze with walls
        maze = [[1 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        # Stack for DFS
        stack = [(1, 1)]
        maze[1][1] = 0  # Start position
        visited = {(1, 1)}

        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Right, Down, Left, Up

        while stack:
            x, y = stack[-1]
            # Get unvisited neighbors (2 cells away to create walls)
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (1 <= nx < self.GRID_SIZE - 1 and 1 <= ny < self.GRID_SIZE - 1 and
                        (nx, ny) not in visited):
                    neighbors.append((nx, ny))

            if neighbors:
                # Choose a random neighbor
                nx, ny = random.choice(neighbors)
                # Carve a path
                maze[nx][ny] = 0
                maze[x + (nx - x) // 2][y + (ny - y) // 2] = 0  # Clear the wall between
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        # Ensure start and end are open
        maze[1][1] = 0
        maze[self.GRID_SIZE - 2][self.GRID_SIZE - 2] = 0
        self.set_maze(maze)
        self.set_start((1, 1))
        self.set_end((self.GRID_SIZE - 2, self.GRID_SIZE - 2))
        self.set_solution_path(self.__solver.solve(self.get_maze(), self.get_start(), self.get_end()))

    def handle_movement(self, event):
        """Handles player movement based on arrow key input."""
        x, y = self.get_player_pos()
        new_x, new_y = x, y
        if event.key == pygame.K_UP:
            new_x -= 1
        elif event.key == pygame.K_DOWN:
            new_x += 1
        elif event.key == pygame.K_LEFT:
            new_y -= 1
        elif event.key == pygame.K_RIGHT:
            new_y += 1

        maze = self.get_maze()
        if (0 <= new_x < self.GRID_SIZE and 0 <= new_y < self.GRID_SIZE and
                maze[new_x][new_y] == 0):
            self.set_player_pos([new_x, new_y])
            self.__score_manager.add_points(1)

    def handle_key(self, event):
        """Handles key presses for movement, hints, and other actions."""
        if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
            self.handle_movement(event)
        elif event.key == pygame.K_h:
            self.set_hint_shown(not self.is_hint_shown())
            if self.is_hint_shown():
                self.__score_manager.deduct_points(5)
        elif event.key == pygame.K_s:
            self.set_solution_shown(not self.is_solution_shown())
            if self.is_solution_shown():
                self.__score_manager.deduct_points(10)
        elif event.key == pygame.K_r:
            self.start_game(self.get_current_difficulty())
        elif event.key in (pygame.K_q, pygame.K_Q):
            self.quit_game(return_to_menu=True)

    def game_loop(self):
        """Main game loop handling events, updates, and rendering."""
        self.set_timer(0 if self.get_time_limit() >= 0 else -1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    self.handle_key(event)
                    if event.key in (pygame.K_q, pygame.K_Q):
                        return True

            if self.get_time_limit() >= 0:
                self.set_timer(self.get_timer() + self.clock.get_time() / 1000)
                if self.get_timer() > self.get_time_limit():
                    self.loss_screen()
                    return True

            player_x, player_y = self.get_player_pos()
            if (player_x, player_y) == self.get_end():
                self.victory_screen()
                return True

            self.draw()
            self.clock.tick(60)

    def draw(self):
        """Draws the game state, including the maze, player, goal, hints, and HUD."""
        self.screen.fill((0, 0, 0))  # Black background

        # Draw the maze
        maze = self.get_maze()
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                color = (255, 255, 255) if maze[i][j] == 1 else (0, 0, 0)  # White walls, black paths
                pygame.draw.rect(self.screen, color, (j * self.CELL_SIZE, i * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw the solution path if shown
        if self.is_solution_shown() and self.get_solution_path():
            for x, y in self.get_solution_path():
                pygame.draw.rect(self.screen, (0, 255, 0), (y * self.CELL_SIZE, x * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw the hint if shown
        if self.is_hint_shown() and self.get_solution_path():
            # Show the next step after the player's current position
            player_x, player_y = self.get_player_pos()
            for x, y in self.get_solution_path():
                if x == player_x and y == player_y:
                    break
            # Find the next position in the path
            idx = self.get_solution_path().index((player_x, player_y))
            if idx + 1 < len(self.get_solution_path()):
                next_x, next_y = self.get_solution_path()[idx + 1]
                pygame.draw.rect(self.screen, (255, 255, 0), (next_y * self.CELL_SIZE, next_x * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw the player (blue square)
        player_x, player_y = self.get_player_pos()
        pygame.draw.rect(self.screen, (0, 0, 255), (player_y * self.CELL_SIZE, player_x * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw the goal (red square)
        end_x, end_y = self.get_end()
        pygame.draw.rect(self.screen, (255, 0, 0), (end_y * self.CELL_SIZE, end_x * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw the HUD (score and timer)
        score_text = self.__font.render(f"Score: {self.get_score()}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        if self.get_time_limit() >= 0:
            time_remaining = max(0, self.get_time_limit() - self.get_timer())
            timer_text = self.__font.render(f"Time: {int(time_remaining)}", True, (255, 255, 255))
            self.screen.blit(timer_text, (self.screen.get_width() - 150, 10))

        pygame.display.flip()

    def start_game(self, difficulty):
        """Starts a new game with the specified difficulty."""
        self.set_current_difficulty(difficulty)
        self.set_timer(0 if self.get_time_limit() >= 0 else -1)
        self.generate_puzzle()
        self.set_player_pos([1, 1])
        self.set_solution_shown(False)
        self.set_hint_shown(False)
        self.__score_manager.reset()
        return self.game_loop()

    def victory_screen(self):
        """Displays the victory screen and updates AI performance."""
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("You Win!", True, (0, 255, 0))
        score_text = font.render(f"Final Score: {self.get_score()}", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, self.screen.get_height() // 2 + 10))
        pygame.display.flip()
        pygame.time.wait(2000)  # Display for 2 seconds

        # Update AI performance
        hints_used = 1 if self.is_hint_shown() else 0
        self.__ai_system.update_performance(
            time_taken=self.get_timer(),
            hints_used=hints_used,
            score=self.get_score(),
            time_limit=self.get_time_limit()
        )
        # Suggest new difficulty for next game
        suggested_difficulty = self.__ai_system.suggest_difficulty()
        self.set_current_difficulty(suggested_difficulty)

    def loss_screen(self):
        """Displays the loss screen and updates AI performance."""
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("Time's Up! You Lose!", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {self.get_score()}", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, self.screen.get_height() // 2 + 10))
        pygame.display.flip()
        pygame.time.wait(2000)  # Display for 2 seconds

        # Update AI performance
        hints_used = 1 if self.is_hint_shown() else 0
        self.__ai_system.update_performance(
            time_taken=self.get_timer(),
            hints_used=hints_used,
            score=self.get_score(),
            time_limit=self.get_time_limit()
        )
        # Suggest new difficulty for next game
        suggested_difficulty = self.__ai_system.suggest_difficulty()
        self.set_current_difficulty(suggested_difficulty)