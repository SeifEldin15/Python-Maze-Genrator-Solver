from PIL import Image
import heapq
import random
import tkinter as tk
from tkinter import filedialog

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
    if file_path:
        print("Selected image:", file_path)
        root.destroy()  # Close the Tkinter window
        # Continue with the rest of your code here
    else:
        print("No image selected.")

root = tk.Tk()
root.title("Image Browser")

browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.pack(pady=10)

root.mainloop()

def image_to_2d_list(folder_path):
    image = Image.open(folder_path)
    grayscale_image = image.convert('L')
    pixel_values = list(grayscale_image.getdata())
    width, height = grayscale_image.size
    two_d_list = [[1 if pixel == 0 else 0 for pixel in pixel_values[i:i+width]] for i in range(0, len(pixel_values), width)]
    return two_d_list

def save_maze_image(maze):
    colors = {
        0: (255, 255, 255),  # White
        1: (0, 0, 0),        # Black
        2: (255, 0, 0)       # Red
    }

    height, width = len(maze), len(maze[0])
    image = Image.new("RGB", (width, height))

    for row in range(height):
        for col in range(width):
            image.putpixel((col, row), colors[maze[row][col]])

    random_number = random.randint(1, 10000000000)  # Generate a random number between 1 and 1,000,000
    file_path = f"mazes/maze_image-{random_number}.png"
    image.save(file_path)
    return file_path

def is_valid_move(maze, row, col):
    rows, cols = len(maze), len(maze[0])
    return 0 <= row < rows and 0 <= col < cols and maze[row][col] == 0

def heuristic(position, goal):
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

def find_path(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    came_from = [[None for _ in range(cols)] for _ in range(rows)]
    
    pq = [(heuristic(start, end), 0, start)]
    heapq.heapify(pq)

    while pq:
        _, cost, current = heapq.heappop(pq)
        row, col = current

        if visited[row][col]:
            continue

        visited[row][col] = True

        if current == end:
            path = [end]
            while current != start:
                current = came_from[current[0]][current[1]]
                path.append(current)
            return path[::-1]

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if is_valid_move(maze, new_row, new_col) and not visited[new_row][new_col]:
                came_from[new_row][new_col] = (row, col)
                new_cost = cost + 1
                total_cost = new_cost + heuristic((new_row, new_col), end)
                heapq.heappush(pq, (total_cost, new_cost, (new_row, new_col)))

    return None

folder_path = 'maze.png'
result = image_to_2d_list(folder_path)
start_positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
end_position = (len(result) - 2, len(result[0]) - 2)
maze = result

for start_position in start_positions:
    if maze[start_position[0]][start_position[1]] == 0 and maze[end_position[0]][end_position[1]] == 0:
        final_path = find_path(maze, start_position, end_position)
        if final_path:
            updated_maze = [[2 if (row, col) in final_path else maze[row][col] for col in range(len(maze[0]))] for row in range(len(maze))]
            print(f"Path found from start position {start_position}")
            # print(f"Path found from start position {start_position}:")
            # for row in updated_maze:
            #     print(row)
            file_path = save_maze_image(updated_maze)
            print(f"Saved maze image as: {file_path}")
            break
else:
    print("No valid path found from any start position.")
