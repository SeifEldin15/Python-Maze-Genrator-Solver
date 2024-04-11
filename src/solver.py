from PIL import Image
import heapq

# Function to save the maze as an image
def save_maze_image(maze, file_path):
    colors = {
        0: (255, 255, 255),  # White
        1: (0, 0, 0),        # Black
        2: (255, 0, 0)       # Red
    }

    height, width = len(maze), len(maze[0])
    image = Image.new("RGB", (width, height))

    # Fill the image with colors based on the maze
    for row in range(height):
        for col in range(width):
            image.putpixel((col, row), colors[maze[row][col]])

    # Save the image to the specified file path
    image.save(file_path)

# Function to check if a move is valid
def is_valid_move(maze, row, col):
    rows, cols = len(maze), len(maze[0])
    return 0 <= row < rows and 0 <= col < cols and maze[row][col] == 0

# Heuristic function for A* algorithm (Manhattan distance)
def heuristic(position, goal):
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

# A* algorithm to find the path in the maze
def find_path(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # Priority queue for A* algorithm (heuristic cost, position)
    pq = [(heuristic(start, end), start)]
    heapq.heapify(pq)

    # A* algorithm loop
    while pq:
        current_cost, current = heapq.heappop(pq)
        row, col = current

        # If the goal is reached, reconstruct the path
        if current == end:
            path = [end]
            while current != start:
                current = visited[current[0]][current[1]]
                path.append(current)
            return path[::-1]

        # Possible directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Check if the move is valid and not visited
            if is_valid_move(maze, new_row, new_col) and not visited[new_row][new_col]:
                visited[new_row][new_col] = current
                cost = heuristic((new_row, new_col), end)
                heapq.heappush(pq, (cost, (new_row, new_col)))

    # If no path is found
    return None

# Example maze
maze = open('out.txt', 'r') # stopped here check this

rows, cols = len(maze), len(maze[0])

start_position = (1, 1)  # Example start position
end_position = (rows - 2, cols - 2)  # Example end position

# Find the path using A* algorithm
final_path = find_path(maze, start_position, end_position)

# Display the original and updated maze (if a path is found)
if final_path:
    updated_maze = [[2 if (row, col) in final_path else maze[row][col] for col in range(cols)] for row in range(rows)]

    print("Original Maze:")
    for row in maze:
        print(row)

    print("\nUpdated Maze with Path:")
    for row in updated_maze:
        print(row)
else:
    print("No path found.")

# Save the maze image with the path (if a path is found)
if final_path:
    save_maze_image(updated_maze, "maze_image.png")
else:
    print("No path found.")

