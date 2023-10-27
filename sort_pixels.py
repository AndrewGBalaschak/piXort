from colorsys import rgb_to_hsv, hsv_to_rgb
from PIL import Image
import random
import threading

# Import global image variables
import globals

# Sorts pixels in segments by value/lightness
def sort_value(segment_size: int, segment_random: float, segment_probability: float, is_sort: bool, is_vertical: bool):
    # Rotate 90 degrees for vertical sorting
    if(is_vertical):
        globals.original_image = globals.original_image.transpose(method=Image.Transpose.ROTATE_90)

    # Load pixel data
    globals.sorted_image = globals.original_image.copy()
    pixels = globals.sorted_image.load()

    # Get dimensions
    width, height = globals.sorted_image.size

    for y in range(height):
        row = []
        # Get current row of pixels
        for x in range(width):
            row.append(pixels[x, y])
        
        # Split row into segments
        # And sort each segment
        x = 0
        while (x < width):
            # Apply segment size randomization
            temp_segment_size = int(segment_size + ((random.random() - 0.5) * 2 * segment_random * segment_size))

            # Check if segment is to be sorted
            if (random.random() < segment_probability):
                if (is_sort):
                    row[x:x+temp_segment_size] = sorted(row[x:x+temp_segment_size])
                else:
                    copy = row[x:x+temp_segment_size].copy()
                    random.shuffle(copy)
                    row[x:x+temp_segment_size] = copy
            x = x + temp_segment_size
        
        # Write sorted data to pixel array
        for x in range(width):
            pixels[x, y] = row[x]

    # Make new image for sorted pixels
    globals.sorted_image = Image.new('RGB', (width, height))
    sorted_pixels = []
    for y in range(height):
        for x in range(width):
            sorted_pixels.append(pixels[x,y])
    globals.sorted_image.putdata(sorted_pixels)

    # Correct rotation
    if(is_vertical):
        globals.original_image = globals.original_image.transpose(method=Image.Transpose.ROTATE_270)
        globals.sorted_image = globals.sorted_image.transpose(method=Image.Transpose.ROTATE_270)

# Sorts pixels by color
def sort_hue():
    pixels = list(globals.original_image.getdata())
    pixels_hsv = [rgb_to_hsv(*pixel[:3]) for pixel in pixels]
    sorted_pixels_hsv = sorted(pixels_hsv, key=lambda x: x[0])
    sorted_pixels = [tuple(int(c * 255) for c in hsv_to_rgb(*hsv)) for hsv in sorted_pixels_hsv]

    globals.sorted_image = Image.new('Hue', globals.original_image.size)
    globals.sorted_image.putdata(sorted_pixels)

# Applies the sort and allows the sorted image to be sorted again
def apply_sort():
    if globals.sorted_image:
        globals.original_image = globals.sorted_image.copy()
        globals.sorted_image = None