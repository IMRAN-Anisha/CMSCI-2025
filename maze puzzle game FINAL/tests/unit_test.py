import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to sys.path to import game modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from games.puzzle_game import PuzzleGame
from source.path_levels import *
from source.score_manager import ScoreManager
from source.dfs_solver import DFSSolver
from source.pathAI import AIAdaptiveSystem

class TestPuzzleGame(unittest.TestCase):
    def setUp(self):
        # Mock Pygame dependencies to avoid initializing a display
        self.pygame_mock = MagicMock()
        self.pygame_display_mock = MagicMock()
        self.pygame_time_mock = MagicMock()
        self.pygame_event_mock = MagicMock()

        # Patch Pygame modules
        self.pygame_patch = patch.multiple('pygame',
            display=self.pygame_display_mock,
            time=self.pygame_time_mock,
            event=self.pygame_event_mock,
            font=MagicMock(),
            QUIT=MagicMock(),
            KEYDOWN=MagicMock(),
            MOUSEBUTTONDOWN=MagicMock(),
            K_UP=MagicMock(),
            K_DOWN=MagicMock(),
            K_LEFT=MagicMock(),
            K_RIGHT=MagicMock(),
            K_h=MagicMock(),
            K_s=MagicMock(),
            K_r=MagicMock(),
            K_q=MagicMock(),
            Q=MagicMock()
        )
        self.pygame_patch.start()

        # Create mock screen and clock
        self.screen = MagicMock()
        self.clock = MagicMock()
        self.clock.tick.return_value = 60  # Mock clock tick for 60 FPS

        # Initialize PuzzleGame
        self.game = PuzzleGame(self.screen, self.clock)

    def tearDown(self):
        self.pygame_patch.stop()

    def test_generate_puzzle(self):
        """Test that generate_puzzle creates a solvable maze."""
        self.game.start = (1, 1)
        self.game.end = (self.game.GRID_SIZE - 2, self.game.GRID_SIZE - 2)
        self.game.generate_puzzle()
        self.assertIsNotNone(self.game.maze)
        self.assertEqual(self.game.maze[1][1], 0)  # Start position is a path
        self.assertEqual(self.game.maze[self.game.GRID_SIZE-2][self.game.GRID_SIZE-2], 0)  # End position is a path
        self.assertIsNotNone(self.game.solution_path)  # Solution path exists

    def test_handle_movement_valid(self):
        """Test player movement to a valid position."""
        self.game.generate_puzzle()
        self.game.player_pos = [1, 1]
        self.game.maze[1][2] = 0  # Ensure right position is a path
        event = MagicMock()
        event.key = self.game.K_RIGHT
        self.game.handle_movement(event)
        self.assertEqual(self.game.player_pos, [1, 2])
        self.assertEqual(self.game.score_manager.get_score(), 1)

    def test_handle_movement_invalid_wall(self):
        """Test player movement into a wall."""
        self.game.generate_puzzle()
        self.game.player_pos = [1, 1]
        self.game.maze[1][2] = 1  # Right position is a wall
        event = MagicMock()
        event.key = self.game.K_RIGHT
        self.game.handle_movement(event)
        self.assertEqual(self.game.player_pos, [1, 1])  # Position unchanged
        self.assertEqual(self.game.score_manager.get_score(), 0)

    def test_handle_key_hint(self):
        """Test hint toggle and score deduction."""
        self.game.generate_puzzle()
        event = MagicMock()
        event.key = self.game.K_h
        self.game.handle_key(event)
        self.assertTrue(self.game.show_hint)
        self.assertEqual(self.game.score_manager.get_score(), -5)  # Hint deducts 5 points

class TestScoreManager(unittest.TestCase):
    def setUp(self):
        self.score_manager = ScoreManager()

    def test_add_points(self):
        """Test adding points to score."""
        self.score_manager.add_points(10)
        self.assertEqual(self.score_manager.get_score(), 10)

    def test_deduct_points(self):
        """Test deducting points, ensuring score doesn't go below 0."""
        self.score_manager.add_points(5)
        self.score_manager.deduct_points(10)
        self.assertEqual(self.score_manager.get_score(), 0)

    def test_reset_score(self):
        """Test resetting the score."""
        self.score_manager.add_points(20)
        self.score_manager.reset()
        self.assertEqual(self.score_manager.get_score(), 0)

class TestDFSSolver(unittest.TestCase):
    def setUp(self):
        self.solver = DFSSolver()

    def test_solve_simple_maze(self):
        """Test DFS solver on a simple 3x3 maze."""
        maze = [
            [1, 1, 1],
            [1, 0, 0],
            [1, 0, 0]
        ]
        start = (1, 1)
        end = (2, 2)
        path = self.solver.solve(maze, start, end)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], end)

    def test_solve_no_path(self):
        """Test DFS solver when no path exists."""
        maze = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]
        start = (1, 1)
        end = (2, 2)
        path = self.solver.solve(maze, start, end)
        self.assertIsNone(path)

    def test_invalid_start_position(self):
        """Test DFS solver with invalid start position (wall)."""
        maze = [
            [1, 1, 1],
            [1, 0, 0],
            [1, 0, 0]
        ]
        start = (0, 0)  # Wall
        end = (2, 2)
        with self.assertRaises(ValueError):
            self.solver.solve(maze, start, end)

class TestAIAdaptiveSystem(unittest.TestCase):
    def setUp(self):
        self.ai_system = AIAdaptiveSystem()

    def test_update_performance(self):
        """Test updating performance history."""
        self.ai_system.update_performance(time_taken=30, hints_used=1, score=10, time_limit=60)
        self.assertEqual(len(self.ai_system.performance_history), 1)
        expected_performance = max(0, (60 - 30) / 60 - (1 * 0.1) + (10 / 100))  # (time_score - hint_penalty + score/100)
        self.assertAlmostEqual(self.ai_system.performance_history[0], expected_performance)

    def test_suggest_difficulty_high_performance(self):
        """Test suggesting difficulty for high performance."""
        self.ai_system.performance_history = [0.9]  # High performance
        difficulty = self.ai_system.suggest_difficulty()
        self.assertEqual(difficulty, "hard")

    def test_suggest_difficulty_low_performance(self):
        """Test suggesting difficulty for low performance."""
        self.ai_system.performance_history = [0.3]  # Low performance
        difficulty = self.ai_system.suggest_difficulty()
        self.assertEqual(difficulty, "easy")

class TestDifficultySubclasses(unittest.TestCase):
    def setUp(self):
        self.pygame_mock = MagicMock()
        self.pygame_display_mock = MagicMock()
        self.pygame_time_mock = MagicMock()
        self.pygame_event_mock = MagicMock()
        self.pygame_patch = patch.multiple('pygame',
            display=self.pygame_display_mock,
            time=self.pygame_time_mock,
            event=self.pygame_event_mock,
            font=MagicMock(),
            QUIT=MagicMock(),
            KEYDOWN=MagicMock(),
            MOUSEBUTTONDOWN=MagicMock()
        )
        self.pygame_patch.start()
        self.screen = MagicMock()
        self.clock = MagicMock()

    def tearDown(self):
        self.pygame_patch.stop()

    def test_easy_maze_settings(self):
        """Test EasyMaze settings."""
        game = EasyMaze(self.screen, self.clock)
        self.assertEqual(game.GRID_SIZE, 15)
        self.assertEqual(game.time_limit, -1)  # No timer

    def test_medium_maze_settings(self):
        """Test MediumMaze settings."""
        game = MediumMaze(self.screen, self.clock)
        self.assertEqual(game.GRID_SIZE, 21)
        self.assertEqual(game.time_limit, 120)

    def test_hard_maze_settings(self):
        """Test HardMaze settings."""
        game = HardMaze(self.screen, self.clock)
        self.assertEqual(game.GRID_SIZE, 25)
        self.assertEqual(game.time_limit, 60)

if __name__ == '__main__':
    unittest.main()