from source.base_puzzle import BasePuzzle
from source.score_manager import ScoreManager
from source.pathAI import AIAdaptiveSystem, DFSSolver
import pygame
import random

class PuzzleGame(BasePuzzle):
    GRID_SIZE = 21
    CELL_SIZE = 800 // GRID_SIZE  

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
        self.__font = pygame.font.Font(None, 28)

    ### Getters
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

    ### Setters
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
        elif event.key == pygame.K_q:
            self.quit_game(return_to_menu=True)

    def draw(self):
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

        # Draw the HUD (score, timer, and hint text)
        score_text = self.__font.render(f"Score: {self.get_score()}", True, (0,0,193))  
        self.screen.blit(score_text, (10, 10))

        # Debug time limit
        print("Time limit:", self.get_time_limit(), "Timer:", self.get_timer())

        # Draw timer with (0, 0, 193) text and white background
        if self.get_time_limit() >= 0:
            time_remaining = max(0, self.get_time_limit() - self.get_timer())
            timer_text = self.__font.render(f"Time: {int(time_remaining)}", True, (0, 0, 193))  # Blue text
            timer_pos = (self.screen.get_width() - 150, 10)
            # Draw white background for timer
            pygame.draw.rect(self.screen, (255, 255, 255), (timer_pos[0] - 5, timer_pos[1] - 5, timer_text.get_width() + 10, timer_text.get_height() + 10))
            self.screen.blit(timer_text, timer_pos)
            print("Timer rendering: Time", int(time_remaining))

        # Draw the hint text (controls instruction)
        hint_text = self.__font.render("H: Hint | S: Solution | R: Restart | Q: Quit", True, (0,0,193))  
        self.screen.blit(hint_text, (10, self.screen.get_height() - 30))  # Position at bottom-left

        pygame.display.flip()

    def start_game(self, difficulty):
        """Starts a new game with the specified difficulty."""
        self.set_current_difficulty(difficulty)
        self.set_time_limit(60)  # Ensure timed mode
        self.set_timer(0)  # Reset timer
        self.generate_puzzle()
        self.set_player_pos([1, 1])
        self.set_solution_shown(False)
        self.set_hint_shown(False)
        self.__score_manager.reset()
        return self.run()

    def run(self):
        """Main game loop implementing the abstract run method from BasePuzzle."""
        self.set_timer(0 if self.get_time_limit() >= 0 else -1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    self.handle_key(event)
                    if event.key == pygame.K_q:
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
        self.__ai_system.update_performance(time_taken=self.get_timer(),
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
