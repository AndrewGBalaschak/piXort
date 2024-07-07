from PIL import Image, ImageFilter
import random
import multiprocessing
import math

# Import global image variables
import globals

algorithms = ["Euclidian Distance", "Test2", "Test3"]

def palettize_helper(palette, algorithm):
    width, height = globals.sort_input.size
    original_pixels = globals.sort_input.load()
    new_pixels = []
    
    # Loop through rows
    for y in range(height):
        for x in range(width):
            # Get the original pixel color
            original_color = original_pixels[x, y]
            new_color = None
            min_distance = math.inf
            
            # Find the closest color in the palette

            # Euclidian distance
            if (algorithm == algorithms[0]):
                for candidate in palette:
                    candidate_distance = euclidian_distance(original_color, candidate)
                    if (candidate_distance < min_distance):
                        new_color = candidate
                        min_distance = candidate_distance

            
            # Add the selected color to the new image
            new_pixels.append(tuple(new_color))

    globals.sort_output = Image.new('RGB', (width, height))
    globals.sort_output.putdata(new_pixels)

    # Set the display image to reference the palettized image
    globals.display_image = globals.sort_output


def euclidian_distance(A, B):
    R1 = A[0]
    G1 = A[1]
    B1 = A[2]

    R2 = B[0]
    G2 = B[1]
    B2 = B[2]

    return math.sqrt(math.pow((A[0] - B[0]), 2)  + math.pow((A[1] - B[1]), 2) + math.pow((A[2] - B[2]), 2))