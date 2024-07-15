from PIL import Image, ImageFilter
import random
import multiprocessing
import math

# Import global image variables
import globals

algorithms = ['Euclidian Distance', 'Red Distance', 'Green Distance', 'Blue Distance']

dithering_options = ['None', 'Floyd-Steinberg', 'Quick']

def palettize_helper(palette, algorithm, dithering, dithering_strength):
    width, height = globals.input_image.size
    original_pixels = globals.input_image.copy()
    original_pixels = original_pixels.load()
    new_pixels = []
    
    # Loop through rows
    for y in range(height):
        for x in range(width):
            # Get the original pixel color
            original_color = original_pixels[x, y]
            new_color = None
            min_distance = math.inf
            
            # Find the closest color in the palette
            for candidate in palette:
                # Euclidian distance
                if (algorithm == algorithms[0]):
                    candidate_distance = euclidian_distance(original_color, candidate)
                
                # Only Red
                elif (algorithm == algorithms[1]):
                    candidate_distance = red_distance(original_color, candidate)

                # Only Green
                elif (algorithm == algorithms[2]):
                    candidate_distance = green_distance(original_color, candidate)

                # Only Blue
                elif (algorithm == algorithms[3]):
                    candidate_distance = blue_distance(original_color, candidate) 

                if (candidate_distance < min_distance):
                    new_color = candidate
                    min_distance = candidate_distance

            # Apply dithering

            # Floyd-Steinberg
            if (dithering == dithering_options[1]):
                quantization_error = tuple(map(lambda i, j: i - j, original_color, new_color))

                if x < width - 1:
                    original_pixels[x + 1, y    ] = tuple(map(lambda i, j: i + j, original_pixels[x + 1, y    ], tuple([int(i * 7/16 * dithering_strength) for i in quantization_error])))
                if x > 0 and y < height - 1:
                    original_pixels[x - 1, y + 1] = tuple(map(lambda i, j: i + j, original_pixels[x - 1, y + 1], tuple([int(i * 3/16 * dithering_strength) for i in quantization_error])))
                if y < height - 1:
                    original_pixels[x    , y + 1] = tuple(map(lambda i, j: i + j, original_pixels[x    , y + 1], tuple([int(i * 5/16 * dithering_strength) for i in quantization_error])))
                if x < width - 1 and y < height - 1:
                    original_pixels[x + 1, y + 1] = tuple(map(lambda i, j: i + j, original_pixels[x + 1, y + 1], tuple([int(i * 1/16 * dithering_strength) for i in quantization_error])))

            if (dithering == dithering_options[2]):
                quantization_error = tuple(map(lambda i, j: i - j, original_color, new_color))

                if x < width - 1:
                    original_pixels[x + 1, y    ] = tuple(map(lambda i, j: i + j, original_pixels[x + 1, y    ], tuple([int(i * 1/2 * dithering_strength) for i in quantization_error])))



            # Add the selected color to the new image
            new_pixels.append(tuple(new_color))

    globals.output_image = Image.new('RGB', (width, height))
    globals.output_image.putdata(new_pixels)

    # Set the display image to reference the palettized image
    globals.display_image = globals.output_image


def euclidian_distance(A, B):

    return math.pow((A[0] - B[0]), 2)  + math.pow((A[1] - B[1]), 2) + math.pow((A[2] - B[2]), 2)

def red_distance(A, B):
    return math.pow((A[0] - B[0]), 2)

def green_distance(A, B):
    return math.pow((A[1] - B[1]), 2)

def blue_distance(A, B):
    return math.pow((A[2] - B[2]), 2)