from source.pathfinding_algorithm import PathfindingAlgorithm

#using my abstract class to make the "AI-pathfinder"
class AIAdaptiveSystem:
    def update_performance(self, time_taken, hints_used, score, time_limit):
        pass  # Placeholder

    def suggest_difficulty(self):
        return "medium"  # Default suggestion

class DFSSolver:
    def solve(self, maze, start, end):
        # Simple DFS to find a path (placeholder)
        def is_valid(x, y):
            return (0 <= x < len(maze) and 0 <= y < len(maze[0]) and
                    maze[x][y] == 0)

        stack = [(start, [start])]
        visited = set([start])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while stack:
            (x, y), path = stack.pop()
            if (x, y) == end:
                return path

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if is_valid(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append(((nx, ny), path + [(nx, ny)]))
        return None  # No path found