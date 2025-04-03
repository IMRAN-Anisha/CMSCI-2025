import pygame
import sys
import random
from source.constants import WIDTH,HEIGHT,WHITE,BLACK,GRAY,BLUE,RED,GREEN,YELLOW,LIGHT_GRAY,GRID_SIZE,CELL_SIZE,GRID_WIDTH, GRID_OFFSET_X, GRID_OFFSET_Y

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Adventure")
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

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class SudokuGame:
    def __init__(self):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.number_font = pygame.font.Font(None, 40)
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.original = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.solution = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.selected = None
        self.show_solution = False
        self.timer = 0
        self.solved = False

    def generate_puzzle(self, difficulty):
        # Generate full grid
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.solve(self.grid)
        self.solution = [row[:] for row in self.grid]  # Store solution
        
        # Copy to original
        self.original = [row[:] for row in self.grid]
        
        # Remove numbers based on difficulty
        cells_to_remove = {"easy": 30, "medium": 40, "hard": 50}[difficulty]
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        for i, j in cells[:cells_to_remove]:
            self.grid[i][j] = 0
            self.original[i][j] = 0

    def solve(self, grid):
        empty = self.find_empty(grid)
        if not empty:
            return True
        row, col = empty
        
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for num in numbers:
            if self.is_valid(grid, num, (row, col)):
                grid[row][col] = num
                if self.solve(grid):
                    return True
                grid[row][col] = 0
        return False

    def find_empty(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, grid, num, pos):
        for x in range(9):
            if grid[pos[0]][x] == num and pos[1] != x:
                return False
        for x in range(9):
            if grid[x][pos[1]] == num and pos[0] != x:
                return False
        box_x, box_y = pos[1] // 3, pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if grid[i][j] == num and (i, j) != pos:
                    return False
        return True

    def main_menu(self):
        buttons = [
            Button("Play", 200, 250, 200, 50, BLUE, GRAY, self.difficulty_menu),
            Button("Quit", 200, 350, 200, 50, BLUE, GRAY, sys.exit)
        ]
        self.menu_loop(buttons)

    def difficulty_menu(self):
        buttons = [
            Button("Easy", 200, 150, 200, 50, BLUE, GRAY, lambda: self.start_game("easy")),
            Button("Medium", 200, 250, 200, 50, BLUE, GRAY, lambda: self.start_game("medium")),
            Button("Hard", 200, 350, 200, 50, BLUE, GRAY, lambda: self.start_game("hard")),
            Button("Back", 200, 450, 200, 50, BLUE, GRAY, self.main_menu)
        ]
        self.menu_loop(buttons)

    def menu_loop(self, buttons):
        while self.running:
            self.screen.fill(BLACK)
            title = self.font.render("Sudoku Adventure", True, WHITE)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.is_clicked(event):
                            button.action()
                            return
            
            for button in buttons:
                button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

    def start_game(self, difficulty):
        self.generate_puzzle(difficulty)
        self.selected = None
        self.show_solution = False
        self.timer = 0
        self.solved = False
        self.game_loop()

    def quit_game(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def game_loop(self):
        while self.running:
            self.screen.fill(BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event)
            
            self.timer += 1/60
            self.draw()
            if self.check_win():
                self.victory_screen()
                return
            pygame.display.flip()
            self.clock.tick(60)

    def handle_click(self, pos):
        x = (pos[0] - GRID_OFFSET_X) // CELL_SIZE
        y = (pos[1] - GRID_OFFSET_Y) // CELL_SIZE
        if 0 <= x < 9 and 0 <= y < 9 and self.original[y][x] == 0:
            self.selected = (y, x)
        else:
            self.selected = None

    def handle_key(self, event):
        if self.selected:
            if event.key in range(pygame.K_0, pygame.K_9 + 1):
                num = event.key - pygame.K_0
                if num == 0 or self.is_valid(self.grid, num, self.selected):
                    self.grid[self.selected[0]][self.selected[1]] = num
            elif event.key == pygame.K_BACKSPACE:
                self.grid[self.selected[0]][self.selected[1]] = 0
        if event.key == pygame.K_s:
            self.show_solution = not self.show_solution
        elif event.key == pygame.K_r:
            self.start_game("medium")

    def draw(self):
        # Draw title
        title = self.font.render("Sudoku Adventure", True, WHITE)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        # Draw grid background
        pygame.draw.rect(self.screen, LIGHT_GRAY, 
                        (GRID_OFFSET_X, GRID_OFFSET_Y, GRID_WIDTH, GRID_WIDTH))

        # Draw grid lines
        for i in range(GRID_SIZE + 1):
            thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK, 
                           (GRID_OFFSET_X, GRID_OFFSET_Y + i * CELL_SIZE),
                           (GRID_OFFSET_X + GRID_WIDTH, GRID_OFFSET_Y + i * CELL_SIZE), thickness)
            pygame.draw.line(self.screen, BLACK,
                           (GRID_OFFSET_X + i * CELL_SIZE, GRID_OFFSET_Y),
                           (GRID_OFFSET_X + i * CELL_SIZE, GRID_OFFSET_Y + GRID_WIDTH), thickness)

        # Draw numbers
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.show_solution and self.grid[i][j] == 0:
                    text = self.number_font.render(str(self.solution[i][j]), True, YELLOW)
                    text_rect = text.get_rect(center=(GRID_OFFSET_X + j * CELL_SIZE + CELL_SIZE//2,
                                                    GRID_OFFSET_Y + i * CELL_SIZE + CELL_SIZE//2))
                    self.screen.blit(text, text_rect)
                elif self.grid[i][j] != 0:
                    color = BLUE if self.original[i][j] != 0 else GREEN
                    text = self.number_font.render(str(self.grid[i][j]), True, color)
                    text_rect = text.get_rect(center=(GRID_OFFSET_X + j * CELL_SIZE + CELL_SIZE//2,
                                                    GRID_OFFSET_Y + i * CELL_SIZE + CELL_SIZE//2))
                    self.screen.blit(text, text_rect)

        # Draw selection
        if self.selected:
            pygame.draw.rect(self.screen, RED,
                           (GRID_OFFSET_X + self.selected[1] * CELL_SIZE,
                            GRID_OFFSET_Y + self.selected[0] * CELL_SIZE,
                            CELL_SIZE, CELL_SIZE), 2)

        # Draw HUD
        time_text = self.font.render(f"Time: {self.timer:.1f}", True, WHITE)
        self.screen.blit(time_text, (10, HEIGHT - 40))
        hint_text = self.font.render("S: Solution | R: Restart | 0-9: Input", True, WHITE)
        self.screen.blit(hint_text, (10, HEIGHT - 70))

    def check_win(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0 or not self.is_valid(self.grid, self.grid[i][j], (i, j)):
                    return False
        return True

    def victory_screen(self):
        while self.running:
            self.screen.fill(BLACK)
            victory_text = self.font.render("Congratulations! You Solved It!", True, WHITE)
            time_text = self.font.render(f"Time: {self.timer:.1f}", True, WHITE)
            replay = Button("Play Again", 200, 300, 200, 50, BLUE, GRAY, lambda: self.start_game("medium"))
            menu = Button("Main Menu", 200, 400, 200, 50, BLUE, GRAY, self.main_menu)

            self.screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, 100))
            self.screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 200))
            replay.draw(self.screen)
            menu.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay.is_clicked(event):
                        replay.action()
                        return
                    if menu.is_clicked(event):
                        menu.action()
                        return
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = SudokuGame()
    game.main_menu()