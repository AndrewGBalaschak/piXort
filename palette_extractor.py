from PIL import Image
import json
import os

def get_unique_colors(image_path):
    colors = []

    # Open an image file
    image = Image.open(image_path)
    image = image.convert(mode='RGB')

    # Get dimensions
    width, height = image.size

    # Load image pixels
    image = image.load()

    # Loop through rows
    for y in range(height):
        # Get current row of pixels
        for x in range(width):
            colors.append(image[x, y])

    unique_colors = list(set(colors))
    
    return unique_colors

def save_colors_to_json(colors, output_file):
    with open(output_file, 'w') as f:
        json.dump(colors, f, indent=4)

if __name__ == "__main__":
    image_path = 'images/atari.png'
    
    unique_colors = get_unique_colors(image_path)
    
    # Save colors to JSON file
    basename = os.path.splitext(os.path.basename(image_path))[0]
    output_file = basename + '_palette.txt'
    with open(output_file, 'w') as f:
        for color in unique_colors:
            print("[{}, {}, {}],".format(color[0], color[1], color[2]), file = f)
    
    print(f"Unique colors extracted from '{image_path}' and saved to '{output_file}'.")