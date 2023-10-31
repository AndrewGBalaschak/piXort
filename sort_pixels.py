import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk
from PIL import Image
import random
import numpy as np

# Import global image variables
import globals

# Sorts pixels in segments by value/lightness
def sort_value(segment_size: int, segment_random: float, segment_probability: float, orientation: str, is_sort: bool, invert_sort: bool, sort_criteria: str):
    # Rotate 90 degrees for vertical sorting
    if(orientation == 'Vertical'):
        globals.original_image = globals.original_image.transpose(method=Image.Transpose.ROTATE_90)

    # If we are being trolled
    if(segment_size==0):
        return

    # Load pixel data
    globals.sorted_image = globals.original_image.copy()
    pixels = globals.sorted_image.load()

    # Get dimensions
    width, height = globals.sorted_image.size

    # Loop through rows
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
                    if(sort_criteria == 'Hue'):
                        row[x:x+temp_segment_size] = sorted(row[x:x+temp_segment_size], key=get_hue, reverse=invert_sort)
                    elif(sort_criteria == 'Saturation'):
                        row[x:x+temp_segment_size] = sorted(row[x:x+temp_segment_size], key=get_sat, reverse=invert_sort)
                    elif(sort_criteria == 'Luminance'):
                        row[x:x+temp_segment_size] = sorted(row[x:x+temp_segment_size], key=get_lum, reverse=invert_sort)
                    elif(sort_criteria == 'Red'):
                        row[x:x+temp_segment_size] = sorted(row[x:x+temp_segment_size], key=get_red, reverse=invert_sort)
                    elif(sort_criteria == 'Green'):
                        row[x:x+temp_segment_size] = sorted(row[x:x+temp_segment_size], key=get_grn, reverse=invert_sort)
                    elif(sort_criteria == 'Blue'):
                        row[x:x+temp_segment_size] = sorted(row[x:x+temp_segment_size], key=get_blu, reverse=invert_sort)
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
    if(orientation == 'Vertical'):
        globals.original_image = globals.original_image.transpose(method=Image.Transpose.ROTATE_270)
        globals.sorted_image = globals.sorted_image.transpose(method=Image.Transpose.ROTATE_270)

# Returns the hue of a pixel
def get_hue(pixel):
    R = pixel[0] / 255
    G = pixel[1] / 255
    B = pixel[2] / 255

    max_val = max(R, G, B)
    min_val = min(R, G, B)
    hue = 0

    if(R > G and R > B):
        hue = (G - B) / (max_val - min_val)
    if(G > R and G > B):
        hue = 2 + (B - R) / (max_val - min_val)
    if(B > R and B > G):
        hue = 4 + (R - G) / (max_val - min_val)
    
    hue = hue * 60

    if(hue < 0):
        hue += 360
    
    return hue

# Returns the saturation of a pixel
def get_sat(pixel):
    R = pixel[0] / 255
    G = pixel[1] / 255
    B = pixel[2] / 255
        
    max_val = max(R, G, B)
    min_val = min(R, G, B)

    if max_val == min_val:
        return 0
    
    lum = get_lum(pixel)

    if lum <= 0.5:
        return (max_val-min_val)/(max_val+min_val)
    else:
        return (max_val-min_val)/(2.0-max_val-min_val)

# Returns the luminance of a pixel
def get_lum(pixel):
    R = pixel[0] / 255
    G = pixel[1] / 255
    B = pixel[2] / 255
    
    max_val = max(R, G, B)
    min_val = min(R, G, B)

    return (max_val + min_val) / 2

# Returns the Red of a pixel
def get_red(pixel):
    return pixel[0] / 255

# Returns the Green of a pixel
def get_grn(pixel):
    return pixel[1] / 255

# Returns the Blue of a pixel
def get_blu(pixel):
    return pixel[2] / 255

# Applies the sort and allows the sorted image to be sorted again
def apply_sort():
    if globals.sorted_image:
        globals.original_image = globals.sorted_image.copy()
        globals.sorted_image = None