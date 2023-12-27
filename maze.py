import tkinter as tk
import random

# Time complexity: O(rows * cols)
def generate_maze(rows, cols):
    maze = [['1' for _ in range(cols)] for _ in range(rows)]

    # Time complexity: O(rows * cols)
    def dfs(row, col):
        maze[row][col] = '0'

        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        # Time complexity: O(1)
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            # Time complexity: O(1)
            if 0 <= new_row < rows and 0 <= new_col < cols and maze[new_row][new_col] == '1':
                maze[(row + new_row) // 2][(col + new_col) // 2] = '0'
                dfs(new_row, new_col)

    start_row, start_col = 0, 0
    dfs(start_row, start_col)

    return maze

# Time complexity: O(rows * cols)
def print_maze(maze):
    for row in maze:
        # Time complexity: O(cols)
        print(" ".join(row))
    print()

# Time complexity: O(rows * cols)
def solve_maze(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]

    # Time complexity: O(rows * cols)
    def dfs(row, col, path):
        # Time complexity: O(1)
        if row < 0 or row >= rows or col < 0 or col >= cols or maze[row][col] == '1' or visited[row][col]:
            return False

        visited[row][col] = True
        path.append((row, col))

        # Time complexity: O(1)
        if (row, col) == end:
            return True

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        # Time complexity: O(1)
        for dr, dc in directions:
            # Time complexity: O(rows * cols)
            if dfs(row + dr, col + dc, path):
                return True

        path.pop()  # Remove the current cell from the path if it does not lead to the destination
        return False

    start_row, start_col = start
    end_row, end_col = end
    path = []
    # Time complexity: O(rows * cols)
    if dfs(start_row, start_col, path):
        return path
    else:
        return None

class MazeSolverGUI:
    def __init__(self, master, rows, cols):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.maze = generate_maze(rows, cols)
        print_maze(self.maze)

        self.canvas = tk.Canvas(master, width=cols*30, height=rows*30)
        self.canvas.pack()

        self.draw_maze()

        self.solve_button = tk.Button(master, text="Solve Maze", command=self.solve_and_draw_path)
        self.solve_button.pack()

        self.solution_label = tk.Label(master, text="")
        self.solution_label.pack()

    def draw_maze(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                cell_color = "black" if self.maze[row][col] == '1' else "white"
                self.canvas.create_rectangle(col * 30, row * 30, (col + 1) * 30, (row + 1) * 30, fill=cell_color)
                if (row, col) == (0, 0):
                    self.canvas.create_text(col * 30 + 15, row * 30 + 15, text="Start", fill="blue")
                elif (row, col) == (self.rows - 1, self.cols - 1):
                    self.canvas.create_text(col * 30 + 15, row * 30 + 15, text="End", fill="red")

    def draw_path(self, path):
        for row, col in path:
            self.canvas.create_rectangle(col * 30, row * 30, (col + 1) * 30, (row + 1) * 30, fill="green")
            if (row, col) == (0, 0):
                self.canvas.create_text(col * 30 + 15, row * 30 + 15, text="Start", fill="blue")
            elif (row, col) == (self.rows - 1, self.cols - 1):
                self.canvas.create_text(col * 30 + 15, row * 30 + 15, text="End", fill="red")

    def draw_path_animation(self, path, index):
        if index < len(path):
            row, col = path[index]
            self.canvas.create_rectangle(col * 30, row * 30, (col + 1) * 30, (row + 1) * 30, fill="green")
            
            if (row, col) == (0, 0):
                self.canvas.create_text(col * 30 + 15, row * 30 + 15, text="Start", fill="blue")
            elif (row, col) == (self.rows - 1, self.cols - 1):
                self.canvas.create_text(col * 30 + 15, row * 30 + 15, text="End", fill="red")

            self.master.after(100, lambda: self.draw_path_animation(path, index + 1))
        else:
            self.solution_label.config(text="Path found!")

    def solve_and_draw_path(self):
        start_point = (0, 0)
        end_point = (self.rows - 1, self.cols - 1)

        path = solve_maze(self.maze, start_point, end_point)

        if path:
            # self.draw_path(path)
            # self.solution_label.config(text="Path found!")
            self.draw_path_animation(path, 0)
        else:
            self.solution_label.config(text="No solution found.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Maze Solver GUI")

    rows, cols = 20, 20 

    if (rows % 2 == 0):
        rows += 1

    if (cols % 2 == 0):
        cols += 1

    app = MazeSolverGUI(root, rows, cols)

    root.mainloop()