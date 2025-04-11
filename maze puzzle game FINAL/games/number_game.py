import sys
import os
# Add the parent directory (maze_puzzle_game_FINAL) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import random
from source.UI import Button
from source.constants import *

class SudokuGame:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.number_font = pygame.font.Font(None, 40)
        self.grid = [[0] * NUMBER_GRID_SIZE for _ in range(NUMBER_GRID_SIZE)]
        self.original = [[0] * NUMBER_GRID_SIZE for _ in range(NUMBER_GRID_SIZE)]
        self.solution = [[0] * NUMBER_GRID_SIZE for _ in range(NUMBER_GRID_SIZE)]
        self.selected = None
        self.show_solution = False
        self.timer = 0
        self.solved = False
        self.current_difficulty = None  # Store the current difficulty

    def run(self):
        while self.running:
            # Start directly with the difficulty menu
            difficulty = self.difficulty_menu()
            if difficulty is None:  # Player chose to go back or quit
                break  # Return to main menu in main.py
            # Start the game with the selected difficulty
            self.start_game(difficulty)
        return True  # Signal to return to main menu

    def generate_puzzle(self, difficulty):
        self.grid = [[0] * NUMBER_GRID_SIZE for _ in range(NUMBER_GRID_SIZE)]
        self.solve(self.grid)
        self.solution = [row[:] for row in self.grid]
        self.original = [row[:] for row in self.grid]
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
            title = self.font.render("Sudoku Adventure", True, WHITE)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game(return_to_menu=True)
                    return None  # Signal to return to main menu
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.is_clicked(event):
                            return button.action()  # Return the action result (difficulty string or None)
            
            for button in buttons:
                button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        return None  # Return to main menu if loop exits

    def start_game(self, difficulty):
        self.current_difficulty = difficulty  # Store the difficulty
        self.generate_puzzle(difficulty)
        self.selected = None
        self.show_solution = False
        self.timer = 0
        self.solved = False
        return self.game_loop()

    def quit_game(self, return_to_menu=False):
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
                    self.quit_game(return_to_menu=True)
                    return True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event)
            
            self.timer += 1/60
            self.draw()
            result = self.check_win()
            if result:
                if result == "win":
                    return self.victory_screen()
                elif result == "loss":
                    return self.loss_screen()
            pygame.display.flip()
            self.clock.tick(60)
        return True

    def handle_click(self, pos):
        x = (pos[0] - GRID_OFFSET_X) // NUMBER_CELL_SIZE
        y = (pos[1] - GRID_OFFSET_Y) // NUMBER_CELL_SIZE
        if 0 <= x < 9 and 0 <= y < 9 and self.original[y][x] == 0:
            self.selected = (y, x)
        else:
            self.selected = None

    # below is option one, if you want to input the correct number only,
    # this does not allow you to enter the wrong number.
    ''' 
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
    '''
    # below is the code if you want to be able to put any number, by removing the self.is_valid()
    def handle_key(self, event):
        if self.selected:
            if event.key in range(pygame.K_0, pygame.K_9 + 1):
                num = event.key - pygame.K_0
                if num == 0:  # Allow erasing with 0
                    self.grid[self.selected[0]][self.selected[1]] = 0
                elif num >= 1 and num <= 9:  # Allow any number 1-9
                    self.grid[self.selected[0]][self.selected[1]] = num
            elif event.key == pygame.K_BACKSPACE:
                self.grid[self.selected[0]][self.selected[1]] = 0
        if event.key == pygame.K_s:
            self.show_solution = not self.show_solution
        elif event.key == pygame.K_r:
            self.start_game(self.current_difficulty)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:  # Quit the game when Q is pressed
                self.quit_game(return_to_menu=True)
                return True

    def draw(self):
        title = self.font.render("Sudoku Adventure", True, WHITE)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        pygame.draw.rect(self.screen, LIGHT_GRAY, 
                        (GRID_OFFSET_X, GRID_OFFSET_Y, NUMBER_GRID_SIZE * NUMBER_CELL_SIZE, NUMBER_GRID_SIZE * NUMBER_CELL_SIZE))
        for i in range(NUMBER_GRID_SIZE + 1):
            thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK, 
                           (GRID_OFFSET_X, GRID_OFFSET_Y + i * NUMBER_CELL_SIZE),
                           (GRID_OFFSET_X + NUMBER_GRID_SIZE * NUMBER_CELL_SIZE, GRID_OFFSET_Y + i * NUMBER_CELL_SIZE), thickness)
            pygame.draw.line(self.screen, BLACK,
                           (GRID_OFFSET_X + i * NUMBER_CELL_SIZE, GRID_OFFSET_Y),
                           (GRID_OFFSET_X + i * NUMBER_CELL_SIZE, GRID_OFFSET_Y + NUMBER_GRID_SIZE * NUMBER_CELL_SIZE), thickness)
        for i in range(NUMBER_GRID_SIZE):
            for j in range(NUMBER_GRID_SIZE):
                if self.show_solution and self.grid[i][j] == 0:
                    text = self.number_font.render(str(self.solution[i][j]), True, YELLOW)
                    text_rect = text.get_rect(center=(GRID_OFFSET_X + j * NUMBER_CELL_SIZE + NUMBER_CELL_SIZE//2,
                                                    GRID_OFFSET_Y + i * NUMBER_CELL_SIZE + NUMBER_CELL_SIZE//2))
                    self.screen.blit(text, text_rect)
                elif self.grid[i][j] != 0:
                    color = BLUE if self.original[i][j] != 0 else GREEN
                    text = self.number_font.render(str(self.grid[i][j]), True, color)
                    text_rect = text.get_rect(center=(GRID_OFFSET_X + j * NUMBER_CELL_SIZE + NUMBER_CELL_SIZE//2,
                                                    GRID_OFFSET_Y + i * NUMBER_CELL_SIZE + NUMBER_CELL_SIZE//2))
                    self.screen.blit(text, text_rect)
        if self.selected:
            pygame.draw.rect(self.screen, RED,
                           (GRID_OFFSET_X + self.selected[1] * NUMBER_CELL_SIZE,
                            GRID_OFFSET_Y + self.selected[0] * NUMBER_CELL_SIZE,
                            NUMBER_CELL_SIZE, NUMBER_CELL_SIZE), 2)
        time_text = self.font.render(f"Time: {self.timer:.1f}", True, WHITE)
        self.screen.blit(time_text, (10, HEIGHT - 40))
        hint_text = self.font.render("S: Solution | R: Restart | 0-9: Input | Q: Quit", True, WHITE)
        self.screen.blit(hint_text, (10, HEIGHT - 70))

    def check_win(self):
        # Check if the grid is completely filled
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return False  # Grid isn't fully filled yet
        
        # Grid is filled, compare with the solution
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != self.solution[i][j]:
                    return "loss"  # Grid is filled but incorrect
        return "win"  # Grid is filled and matches the solution

    def victory_screen(self):
        while self.running:
            self.screen.fill(BLACK)
            victory_text = self.font.render("Congratulations! You Solved It!", True, WHITE)
            time_text = self.font.render(f"Time: {self.timer:.1f}", True, WHITE)
            replay = Button("Play Again", 200, 300, 200, 50, BLUE, GRAY, lambda: self.start_game(self.current_difficulty))
            menu = Button("Main Menu", 200, 400, 200, 50, BLUE, GRAY, lambda: True)

            self.screen.blit(victory_text, (WIDTH//2 - victory_text.get_width()//2, 100))
            self.screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 200))
            replay.draw(self.screen)
            menu.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
            loss_text = self.font.render("Sorry, That's Incorrect!", True, WHITE)
            time_text = self.font.render(f"Time: {self.timer:.1f}", True, WHITE)
            replay = Button("Try Again", 200, 300, 200, 50, BLUE, GRAY, lambda: self.start_game(self.current_difficulty))
            menu = Button("Main Menu", 200, 400, 200, 50, BLUE, GRAY, lambda: True)

            self.screen.blit(loss_text, (WIDTH//2 - loss_text.get_width()//2, 100))
            self.screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 200))
            replay.draw(self.screen)
            menu.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
    pygame.display.set_caption("Sudoku Adventure")
    clock = pygame.time.Clock()
    game = SudokuGame(screen, clock)
    game.run()