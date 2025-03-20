class DFSSolver:
    def __init__(self):
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up

    def solve(self, maze, start, end):
        stack = [(*start, [start])]  # (x, y, path)
        visited = set()

        while stack:
            x, y, path = stack.pop()
            if (x, y) == end:
                return path  #wroking path
            
            if (x, y) in visited:
                continue
            visited.add((x, y))

            for dx, dy in self.directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
                    stack.append((nx, ny, path + [(nx, ny)]))

        return None  # No path found
