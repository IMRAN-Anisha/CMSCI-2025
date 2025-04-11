from source.base_puzzle import BasePuzzle
from source.score_manager import ScoreManager
from source.pathAI import AIAdaptiveSystem, DFSSolver
import pygame
import random
import pygame
import random

class PuzzleGame(BasePuzzle):
    # Maze size and rendering constants
    GRID_SIZE = 21  # Default 21x21 maze grid
    CELL_SIZE = 800 // GRID_SIZE  # Cell size in pixels (800px screen / 21)

    def __init__(self, screen, clock):
        # Initialize base class (assumes BasePuzzle handles screen/clock)
        super().__init__(screen, clock)
        # Game state variables
        self.__maze = None  # Maze grid, set by generate_puzzle
        self.__player_pos = [1, 1]  # Player's starting position [x, y]
        self.__score_manager = ScoreManager()  # Tracks score
        self.__timer = 0  # Elapsed time in seconds
        self.__show_hint = False  # Whether hint is visible
        self.__show_solution = False  # Whether solution path is visible
        self.__current_difficulty = None  # Current difficulty (e.g., 'easy')
        self.__time_limit = 60  # Default time limit (seconds)
        self.__start = (1, 1)  # Maze start position
        self.__end = (self.GRID_SIZE - 2, self.GRID_SIZE - 2)  # Maze end position
        self.__solution_path = None  # List of (x, y) for solution path
        self.__ai_system = AIAdaptiveSystem()  # AI for difficulty adjustment
        self.__solver = DFSSolver()  # Solver for solution path
        self.__font = pygame.font.Font(None, 28)  # Font for HUD text
        self.__button_font = pygame.font.Font(None, 36)  # Font for buttons
        # Movement timing for holding keys
        self.__last_move_time = 0  # Time of last move (seconds)
        self.__move_delay = 0.1  # Delay between moves when holding keys

    ### Getters (unchanged)
    def get_maze(self):
        """Returns the maze grid."""
        return self.__maze

    def get_player_pos(self):
        """Returns player's position as [x, y]."""
        return self.__player_pos

    def get_score(self):
        """Returns current score."""
        return self.__score_manager.get_score()

    def get_timer(self):
        """Returns elapsed time in seconds."""
        return self.__timer

    def is_hint_shown(self):
        """Returns True if hint is shown."""
        return self.__show_hint

    def is_solution_shown(self):
        """Returns True if solution path is shown."""
        return self.__show_solution

    def get_current_difficulty(self):
        """Returns current difficulty level."""
        return self.__current_difficulty

    def get_time_limit(self):
        """Returns time limit in seconds."""
        return self.__time_limit

    def get_start(self):
        """Returns start position as (x, y)."""
        return self.__start

    def get_end(self):
        """Returns end position as (x, y)."""
        return self.__end

    def get_solution_path(self):
        """Returns solution path as list of (x, y)."""
        return self.__solution_path

    ### Setters
    def set_maze(self, maze):
        """Sets the maze grid."""
        self.__maze = maze

    def set_player_pos(self, new_pos):
        """Sets player's position to [x, y]."""
        self.__player_pos = new_pos

    def set_timer(self, value):
        """Sets timer value, ensures non-negative in timed mode."""
        if value < 0 and self.get_time_limit() >= 0:
            raise ValueError("Timer cannot be negative in timed mode")
        self.__timer = value

    def set_hint_shown(self, value):
        """Sets whether hint is shown."""
        self.__show_hint = value

    def set_solution_shown(self, value):
        """Sets whether solution path is shown."""
        self.__show_solution = value

    def set_current_difficulty(self, difficulty):
        """Sets difficulty level."""
        self.__current_difficulty = difficulty

    def set_time_limit(self, time_limit):
        """Sets time limit for the game."""
        #print("Setting time limit to:", time_limit)  # Debug where it’s changed
        self.__time_limit = time_limit

    def set_start(self, start):
        """Sets start position."""
        self.__start = start

    def set_end(self, end):
        """Sets end position."""
        self.__end = end

    def set_solution_path(self, path):
        """Sets solution path."""
        self.__solution_path = path

    def generate_puzzle(self):
        """Generates a maze using depth-first search."""
        # Create maze filled with walls (1 = wall)
        maze = [[1 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        # Start at (1, 1) and track visited cells
        stack = [(1, 1)]
        maze[1][1] = 0  # Set start as path (0 = path)
        visited = {(1, 1)}

        # Directions to carve paths (2 cells away to leave walls)
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Right, Down, Left, Up

        # Carve paths randomly
        while stack:
            x, y = stack[-1]
            # Find unvisited neighbors
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (1 <= nx < self.GRID_SIZE - 1 and 1 <= ny < self.GRID_SIZE - 1 and
                        (nx, ny) not in visited):
                    neighbors.append((nx, ny))

            if neighbors:
                # Carve path to a random neighbor
                nx, ny = random.choice(neighbors)
                maze[nx][ny] = 0  # Set neighbor as path
                maze[x + (nx - x) // 2][y + (ny - y) // 2] = 0  # Clear wall between
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()  # Backtrack if no neighbors

        # Ensure start and end are paths
        maze[1][1] = 0
        maze[self.GRID_SIZE - 2][self.GRID_SIZE - 2] = 0
        self.set_maze(maze)
        self.set_start((1, 1))
        self.set_end((self.GRID_SIZE - 2, self.GRID_SIZE - 2))
        # Generate solution path
        self.set_solution_path(self.__solver.solve(self.get_maze(), self.get_start(), self.get_end()))

    def handle_movement(self, direction):
        """Moves player in the given direction if valid."""
        # Get current position
        x, y = self.get_player_pos()
        new_x, new_y = x, y
        # Adjust position based on direction
        if direction == 'up':
            new_x -= 1
        elif direction == 'down':
            new_x += 1
        elif direction == 'left':
            new_y -= 1
        elif direction == 'right':
            new_y += 1

        # Move if new position is valid (not a wall)
        maze = self.get_maze()
        if (0 <= new_x < self.GRID_SIZE and 0 <= new_y < self.GRID_SIZE and
                maze[new_x][new_y] == 0):
            self.set_player_pos([new_x, new_y])
            self.__score_manager.add_points(1)  # Add point for move

    def handle_key(self, event):
        """Handles non-movement key presses."""
        # Toggle hint
        if event.key == pygame.K_h:
            self.set_hint_shown(not self.is_hint_shown())
            if self.is_hint_shown():
                self.__score_manager.deduct_points(5)  # Hint penalty
        # Toggle solution
        elif event.key == pygame.K_s:
            self.set_solution_shown(not self.is_solution_shown())
            if self.is_solution_shown():
                self.__score_manager.deduct_points(10)  # Solution penalty
        # Restart game
        elif event.key == pygame.K_r:
            self.start_game(self.get_current_difficulty())
        # Quit to menu
        elif event.key == pygame.K_q:
            self.quit_game(return_to_menu=True)

    def draw(self):
        """Draws maze, player, goal, and HUD."""
        # Clear screen with black background
        self.screen.fill((0, 0, 0))

        # Draw maze (white walls, black paths)
        maze = self.get_maze()
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                color = (255, 255, 255) if maze[i][j] == 1 else (0, 0, 0)
                pygame.draw.rect(self.screen, color, (j * self.CELL_SIZE, i * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw solution path (green) if shown
        if self.is_solution_shown() and self.get_solution_path():
            for x, y in self.get_solution_path():
                pygame.draw.rect(self.screen, (0, 255, 0), (y * self.CELL_SIZE, x * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw hint (yellow next step) if shown
        if self.is_hint_shown() and self.get_solution_path():
            player_x, player_y = self.get_player_pos()
            for x, y in self.get_solution_path():
                if x == player_x and y == player_y:
                    break
            idx = self.get_solution_path().index((player_x, player_y))
            if idx + 1 < len(self.get_solution_path()):
                next_x, next_y = self.get_solution_path()[idx + 1]
                pygame.draw.rect(self.screen, (255, 255, 0), (next_y * self.CELL_SIZE, next_x * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw player (blue)
        player_x, player_y = self.get_player_pos()
        pygame.draw.rect(self.screen, (0, 0, 255), (player_y * self.CELL_SIZE, player_x * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw goal (red)
        end_x, end_y = self.get_end()
        pygame.draw.rect(self.screen, (255, 0, 0), (end_y * self.CELL_SIZE, end_x * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

        # Draw HUD
        # Score at top-left (blue text, white background)
        score_text = self.__font.render(f"Score: {self.get_score()}", True, (0, 0, 193))
        score_pos = (10, 10)
        pygame.draw.rect(self.screen, (255, 255, 255), (score_pos[0] - 5, score_pos[1] - 5, score_text.get_width() + 10, score_text.get_height() + 10))
        self.screen.blit(score_text, score_pos)

        # Timer at top-right (if timed mode, blue text, white background)
        if self.get_time_limit() >= 0:
            time_remaining = max(0, self.get_time_limit() - self.get_timer())
            timer_text = self.__font.render(f"Time: {int(time_remaining)}", True, (0, 0, 193))
            timer_pos = (self.screen.get_width() - 150, 10)
            pygame.draw.rect(self.screen, (255, 255, 255), (timer_pos[0] - 5, timer_pos[1] - 5, timer_text.get_width() + 10, timer_text.get_height() + 10))
            self.screen.blit(timer_text, timer_pos)

        # Controls hint at bottom-left (blue text, white background)
        hint_text = self.__font.render("H: Hint | S: Solution | R: Restart | Q: Quit", True, (0, 0, 193))
        hint_pos = (10, self.screen.get_height() - 30)
        pygame.draw.rect(self.screen, (255, 255, 255), (hint_pos[0] - 5, hint_pos[1] - 5, hint_text.get_width() + 10, hint_text.get_height() + 10))
        self.screen.blit(hint_text, hint_pos)

        # Update display
        pygame.display.flip()

    def start_game(self, difficulty):
        """Starts a new game with given difficulty."""
        # Reset game state
        self.set_current_difficulty(difficulty)
        # Explicitly set time limit based on difficulty to override any resets
        if difficulty == "easy":
            self.set_time_limit(-1)  # No timer for Easy
        elif difficulty == "medium":
            self.set_time_limit(120)  # 120 seconds for Medium
        elif difficulty == "hard":
            self.set_time_limit(60)  # 60 seconds for Hard
        else:
            self.set_time_limit(60)  # Default fallback
        #print("Start game - Difficulty:", difficulty, "Time limit:", self.get_time_limit())  # Debug
        self.set_timer(0 if self.get_time_limit() >= 0 else -1)  # Reset timer
        self.generate_puzzle()
        self.set_player_pos([1, 1])
        self.set_solution_shown(False)
        self.set_hint_shown(False)
        self.__score_manager.reset()
        self.__last_move_time = 0  # Reset movement timer
        return self.run()

    def run(self):
        """Main game loop."""
        # Initialize timer
        self.set_timer(0 if self.get_time_limit() >= 0 else -1)
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Exit game
                if event.type == pygame.KEYDOWN:
                    self.handle_key(event)
                    if event.key == pygame.K_q:
                        return "menu"  # Return to menu

            # Handle continuous movement
            current_time = pygame.time.get_ticks() / 1000
            if current_time - self.__last_move_time >= self.__move_delay:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]:
                    self.handle_movement('up')
                    self.__last_move_time = current_time
                elif keys[pygame.K_DOWN]:
                    self.handle_movement('down')
                    self.__last_move_time = current_time
                elif keys[pygame.K_LEFT]:
                    self.handle_movement('left')
                    self.__last_move_time = current_time
                elif keys[pygame.K_RIGHT]:
                    self.handle_movement('right')
                    self.__last_move_time = current_time

            # Update timer
            if self.get_time_limit() >= 0:
                delta_time = self.clock.get_time() / 1000
                self.set_timer(self.get_timer() + delta_time)
                if self.get_timer() > self.get_time_limit():
                    result = self.loss_screen()
                    if result == "play_again":
                        return "menu"  # Return to difficulty selection
                    return True

            # Check for victory
            player_x, player_y = self.get_player_pos()
            if (player_x, player_y) == self.get_end():
                result = self.victory_screen()
                if result == "play_again":
                    return "menu"  # Return to difficulty selection
                return True

            # Draw and update
            self.draw()
            self.clock.tick(60)

    def victory_screen(self):
        """Displays victory screen with play again button."""
        # Clear screen
        self.screen.fill((0, 0, 0))
        # Show win message and score
        font = pygame.font.Font(None, 50)
        text = font.render("You Win!", True, (0, 255, 0))
        score_text = font.render(f"Final Score: {self.get_score()}", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - 100))
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, self.screen.get_height() // 2 - 40))

        # Draw play again button
        button_text = self.__button_font.render("Play Again", True, (255, 255, 255))
        button_rect = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 20, 200, 50)
        pygame.draw.rect(self.screen, (0, 100, 200), button_rect)  # Blue button
        button_text_pos = (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2)
        self.screen.blit(button_text, button_text_pos)

        pygame.display.flip()

        # Update AI with performance
        hints_used = 1 if self.is_hint_shown() else 0
        self.__ai_system.update_performance(
            time_taken=self.get_timer(),
            hints_used=hints_used,
            score=self.get_score(),
            time_limit=self.get_time_limit()
        )
        suggested_difficulty = self.__ai_system.suggest_difficulty()
        self.set_current_difficulty(suggested_difficulty)

        # Handle button clicks
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return "play_again"  # Return to difficulty selection
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return "menu"  # Quit to menu

    def loss_screen(self):
        """Displays loss screen with play again button."""
        # Clear screen
        self.screen.fill((0, 0, 0))
        # Show loss message and score
        font = pygame.font.Font(None, 50)
        text = font.render("Time's Up! You Lose!", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {self.get_score()}", True, (255, 255, 255))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - 100))
        self.screen.blit(score_text, (self.screen.get_width() // 2 - score_text.get_width() // 2, self.screen.get_height() // 2 - 40))

        # Draw play again button
        button_text = self.__button_font.render("Play Again", True, (255, 255, 255))
        button_rect = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2 + 20, 200, 50)
        pygame.draw.rect(self.screen, (0, 100, 200), button_rect)  # Blue button
        button_text_pos = (button_rect.centerx - button_text.get_width() // 2, button_rect.centery - button_text.get_height() // 2)
        self.screen.blit(button_text, button_text_pos)

        pygame.display.flip()

        # Update AI with performance
        hints_used = 1 if self.is_hint_shown() else 0
        self.__ai_system.update_performance(
            time_taken=self.get_timer(),
            hints_used=hints_used,
            score=self.get_score(),
            time_limit=self.get_time_limit()
        )
        suggested_difficulty = self.__ai_system.suggest_difficulty()
        self.set_current_difficulty(suggested_difficulty)

        # Handle button clicks
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return "play_again"  # Return to difficulty selection
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return "menu"  # Quit to menu