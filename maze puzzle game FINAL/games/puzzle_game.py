import pygame
import sys
import random
from dfs_solver import DFSSolver

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 21
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)    # Player
RED = (255, 0, 0)     # Goal
GREEN = (0, 255, 0)   # Solution Path
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0) # Hint color

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Adventure")
clock = pygame.time.Clock()

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Game:
    def __init__(self):
        self.maze = None
        self.player_pos = [1, 1]
        self.start = (1, 1)
        self.end = (GRID_SIZE - 2, GRID_SIZE - 2)
        self.solution_path = None
        self.show_solution = False
        self.show_hint = False
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.timer = 0

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

    def main_menu(self):
        buttons = [
            Button("Play", 200, 200, 200, 50, BLUE, GRAY, self.game_mode_menu),
            Button("Quit", 200, 300, 200, 50, BLUE, GRAY, sys.exit)
        ]
        self.menu_loop(buttons)

    def game_mode_menu(self):
        buttons = [
            Button("Normal", 200, 150, 200, 50, BLUE, GRAY, lambda: self.start_game(1)),
            Button("Timed", 200, 250, 200, 50, BLUE, GRAY, lambda: self.start_game(2)),
            Button("Challenge", 200, 350, 200, 50, BLUE, GRAY, lambda: self.start_game(3)),
            Button("Back", 200, 450, 200, 50, BLUE, GRAY, self.main_menu)
        ]
        self.menu_loop(buttons)

    def menu_loop(self, buttons):
        while True:
            screen.fill(BLACK)
            title = self.font.render("Maze Adventure", True, WHITE)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.is_clicked(event.pos) and button.action:
                            button.action()
                            return
            
            for button in buttons:
                button.draw(screen)
            pygame.display.flip()
            clock.tick(60)

    def start_game(self, mode):
        self.generate_maze()
        self.player_pos = [1, 1]
        self.score = 0
        self.timer = 0 if mode == 2 else -1  # Timed mode only
        self.show_solution = False
        self.show_hint = False
        self.game_loop(mode)

    def game_loop(self, mode):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
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
                        self.start_game(mode)  # Restart

            self.draw_game()
            if self.timer >= 0:  # Timed mode
                self.timer += 1/60  # Increment by frame time
            
            # Check win condition
            if tuple(self.player_pos) == self.end:
                self.victory_screen(mode)
                return
                
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()

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
        screen.fill(BLACK)
        # Draw maze
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.maze[i][j] == 1:
                    pygame.draw.rect(screen, WHITE, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw solution or hint
        if self.show_solution and self.solution_path:
            for x, y in self.solution_path:
                pygame.draw.rect(screen, GREEN, (y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        elif self.show_hint and self.solution_path:
            next_step = self.solution_path[1] if len(self.solution_path) > 1 else self.solution_path[0]
            pygame.draw.rect(screen, YELLOW, (next_step[1]*CELL_SIZE, next_step[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw player and goal
        pygame.draw.rect(screen, BLUE, (self.player_pos[1]*CELL_SIZE, self.player_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (self.end[1]*CELL_SIZE, self.end[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw HUD
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        if self.timer >= 0:
            time_text = self.font.render(f"Time: {self.timer:.1f}", True, WHITE)
            screen.blit(time_text, (10, 40))
        hint_text = self.font.render("H: Hint | S: Solution | R: Restart", True, WHITE)
        screen.blit(hint_text, (10, HEIGHT-40))

    def victory_screen(self, mode):
        while True:
            screen.fill(BLACK)
            victory_text = self.font.render("Congratulations! You Won!", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            time_text = self.font.render(f"Time: {self.timer:.1f}" if self.timer >= 0 else "Time: N/A", True, WHITE)
            replay = Button("Play Again", 200, 300, 200, 50, BLUE, GRAY, lambda: self.start_game(mode))
            menu = Button("Main Menu", 200, 400, 200, 50, BLUE, GRAY, self.main_menu)

            screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, 100))
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))
            screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 250))
            replay.draw(screen)
            menu.draw(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.is_clicked(event.pos):
                        replay.action()
                        return
                    if menu.is_clicked(event.pos):
                        menu.action()
                        return
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.main_menu()