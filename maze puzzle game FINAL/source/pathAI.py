from games.puzzle_game import PathfindingAlgorithm

#using my abstract class to make the "AI-pathfinder"

class DFSSolver(PathfindingAlgorithm):
    def solve(self, maze, start, end):
        # Validate start and end positions
        if maze[start[0]][start[1]] == 1:
            raise ValueError("Start position is a wall")
        if maze[end[0]][end[1]] == 1:
            raise ValueError("End position is a wall")

        # Stack-based DFS
        stack = [(start, [start])]
        visited = set([start])
        rows, cols = len(maze), len(maze[0])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

        while stack:
            (x, y), path = stack.pop()
            if (x, y) == end:
                return path

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < rows and 0 <= ny < cols and
                    maze[nx][ny] == 0 and (nx, ny) not in visited):
                    stack.append(((nx, ny), path + [(nx, ny)]))
                    visited.add((nx, ny))

        return None  # No path found
    
class AIAdaptiveSystem:
    def __init__(self):
        self.performance_history = []  # Track performance metrics

    def update_performance(self, time_taken, hints_used, score, time_limit):
        # Calculate performance score (higher is better)
        if time_limit > 0:
            time_score = (time_limit - time_taken) / time_limit  # 1 if very fast, 0 if at limit
        else:
            time_score = 1  # No time limit (Easy mode)
        hint_penalty = hints_used * 0.1  # Reduce score for each hint
        performance = max(0, time_score - hint_penalty + (score / 100))
        self.performance_history.append(performance)

    def suggest_difficulty(self):
        if not self.performance_history:
            return "medium"  # Default
        avg_performance = sum(self.performance_history) / len(self.performance_history)
        if avg_performance > 0.8:
            return "hard"  # Player is doing well
        elif avg_performance < 0.4:
            return "easy"  # Player is struggling
        return "medium"  # Balanced