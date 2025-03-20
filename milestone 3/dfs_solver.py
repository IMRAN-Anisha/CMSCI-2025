import random

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

# generate a maze using DFS-based random traversal
def generate_maze(width, height):
    # Initialize maze with walls ('#')
    maze = [['#' for _ in range(width)] for _ in range(height)]
    start = (1, 1)  # Set starting point
    stack = [start]  # Stack for DFS traversal
    visited = set([start])  # Keep track of visited cells

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while stack:
        x, y = stack[-1]  #current position
        random.shuffle(directions)  # Shuffle direction
        for dx, dy in directions:
            nx, ny = x + dx, y + dy  # new position
            
            # Check if new position is inside maze bounds and not visited
            if 1 <= nx < height-1 and 1 <= ny < width-1 and (nx, ny) not in visited:
                maze[nx][ny] = '.'  # Mark cell as a path
                maze[x + dx//2][y + dy//2] = '.'  # Remove wall between cells
                visited.add((nx, ny))  # Mark as visited
                stack.append((nx, ny))  # Push to stack for further exploration
                break
        else:
            stack.pop()  # Backtrack if no unvisited neighbors
    
    # Set start and end points in the maze
    maze[1][1] = 'S'  # Start position
    maze[height-2][width-2] = 'E'  # End position
    return maze

#Solving the maze using DFS
def dfs_solve_maze(maze, start, end):
    stack = [(start, [start])]  # Stack stores (position, path taken)
    visited = set()  # Track visited positions
    
    while stack:
        (x, y), path = stack.pop()  # Pop current position and path
        if (x, y) == end:
            return path  # Return solution path if goal is reached
        
        if (x, y) in visited:
            continue  # Skip if already visited
        visited.add((x, y))  # Mark as visited
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if maze[nx][ny] in {'.', 'E'} and (nx, ny) not in visited:
                stack.append(((nx, ny), path + [(nx, ny)]))  # Push new position to stack
    return None  # Return None if no path is found

# Function to print the maze with optional path visualization
def print_maze(maze, path=None):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if path and (i, j) in path:
                print('*', end=' ') 
            else:
                print(cell, end=' ')  # Print maze cell
        print()

# Main execution block - trial and error section
if __name__ == "__main__":
    width, height = 21, 21  # Define maze dimensions
    maze = generate_maze(width, height)  # Generate maze
    start, end = (1, 1), (height-2, width-2)  # Define start and end positions
    path = dfs_solve_maze(maze, start, end)  # Solve maze using DFS
    print_maze(maze, path)  # Print maze with solution path