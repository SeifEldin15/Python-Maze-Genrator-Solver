from PIL import Image

def image_to_2d_list(image_path):
    # Open the image
    image = Image.open(image_path)
    
    # Convert the image to grayscale
    grayscale_image = image.convert('L')
    
    # Get the pixel values as a list
    pixel_values = list(grayscale_image.getdata())
    
    # Get the width and height of the image
    width, height = grayscale_image.size
    
    # Convert the 1D list to a 2D list
    two_d_list = [[1 if pixel == 0 else 0 for pixel in pixel_values[i:i+width]] for i in range(0, len(pixel_values), width)]
    
    return two_d_list

# Example usage
image_path = 'maze.png'
result = image_to_2d_list(image_path)

# Print the result with commas after each ']'
with open('out.txt', 'w') as f:
    for row in result:
        print(row, end=",\n", file=f)
