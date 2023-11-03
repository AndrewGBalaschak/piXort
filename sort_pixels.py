from PIL import Image, ImageFilter
import random

# Import global image variables
import globals

segments = []               # Stores the segments of an image
segments_mask = []          # Mask of whether a segment gets processed or not
segment_orientation = ''    # Stores orientation of segments

def get_edges(edge_threshold: float):
    # Load pixel data
    edges = globals.sort_input.copy()
    edges = edges.convert('L')

    # Apply edge detection
    edges = edges.filter(ImageFilter.FIND_EDGES)
    pixels = edges.load()

    # Get dimensions
    width, height = edges.size

    # Loop through rows
    for y in range(height):
        # Get current row of pixels
        for x in range(width):
            temp = pixels[x, y]
            if temp > (255 * edge_threshold):
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0

    # edges.show()
    globals.edges = edges.copy()

# Computes the segments array, segment mask, and sets the segments orientation
def get_segments(segment_size: int, segment_random: float, segment_probability: float, orientation: str, detect_edges: bool, edge_threshold: float):
    # If we are being trolled
    if(segment_size==0):
        return
    
    # Clear old segments
    segments.clear()
    segments_mask.clear()
    
    # Use global segment orientation
    global segment_orientation

    # Rotate 90 degrees for vertical segments
    if(orientation == 'Vertical'):
        globals.sort_input = globals.sort_input.transpose(method=Image.Transpose.ROTATE_90)
        global edges
        edges = edges.transpose(method=Image.Transpose.ROTATE_90)
        segment_orientation = 'Vertical'
    else:
        segment_orientation = 'Horizontal'

    # Load pixel data
    globals.sort_output = globals.sort_input.copy()
    pixels = globals.sort_output.load()

    # Get dimensions
    width, height = globals.sort_output.size

    # If we are using random segments
    if not detect_edges:
        for y in range(height):
            row = []
            # Get current row of pixels
            for x in range(width):
                row.append(pixels[x, y])
            
            # Split row into segments
            x = 0

            while (x < width):
                # Apply segment size randomization
                temp_segment_size = int(segment_size + ((random.random() - 0.5) * 2 * segment_random * segment_size))

                # Add the segment to the segments array
                segments.append(row[x:x+temp_segment_size].copy())

                # Check if segment is to be processed, add to segments mask array
                segments_mask.append(random.random() <= segment_probability)
                
                # Move to next segment
                x = x + temp_segment_size

    # If we are using edge detection
    else:
        # Load edge data
        if not globals.edges:
            get_edges(edge_threshold)

        edges = globals.edges.load()

        for y in range(height):
            row = []
            # Get current row of pixels
            for x in range(width):
                row.append(pixels[x, y])
            
            # Split row into segments
            x = 0
            last_x = 0
            last_edge = edges[0, y]

            while (x < width):
                # If we are at an edge or at the end
                if edges[x, y] != last_edge:
                    # Add the edge to segments
                    segments.append(row[last_x:x])

                    # Check if segment is to be processed, add to segments mask array
                    segments_mask.append(random.random() <= segment_probability)
                    
                    last_edge = edges[x, y]
                    last_x = x
                    x = x + 1
                # If we are not at an edge
                else:
                    x = x + 1
            
            # Add any remainder
            segments.append(row[last_x:x])

            # Check if segment is to be processed, add to segments mask array
            segments_mask.append(random.random() <= segment_probability)


    # Correct rotation
    if(segment_orientation == 'Vertical'):
        globals.sort_input = globals.sort_input.transpose(method=Image.Transpose.ROTATE_270)
        # edges = edges.transpose(method=Image.Transpose.ROTATE_270)

# Sorts pixels in segments by sort criteria
def sort_pixels(invert_sort: bool, sort_criteria: str):
    # Loop through segments
    for i in range(len(segments)):
        # Check if segment is to be processed
        if (segments_mask[i]):
            if(sort_criteria == 'Hue'):
                segments[i] = sorted(segments[i], key=get_hue, reverse=invert_sort)
            elif(sort_criteria == 'Saturation'):
                segments[i] = sorted(segments[i], key=get_sat, reverse=invert_sort)
            elif(sort_criteria == 'Luminance'):
                segments[i] = sorted(segments[i], key=get_lum, reverse=invert_sort)
            elif(sort_criteria == 'Red'):
                segments[i] = sorted(segments[i], key=get_red, reverse=invert_sort)
            elif(sort_criteria == 'Green'):
                segments[i] = sorted(segments[i], key=get_grn, reverse=invert_sort)
            elif(sort_criteria == 'Blue'):
                segments[i] = sorted(segments[i], key=get_blu, reverse=invert_sort)
    
    # Get dimensions for output
    width, height = globals.sort_input.size

    # Make new image for sorted pixels
    if(segment_orientation == 'Horizontal'):
        globals.sort_output = Image.new('RGB', (width, height))
    elif(segment_orientation == 'Vertical'):
        globals.sort_output = Image.new('RGB', (height, width))

    # Write segments to array of pixels
    pixels = []
    for segment in segments:
        for pixel in segment:
            pixels.append(pixel)

    globals.sort_output.putdata(pixels)

    # Correct rotation
    if(segment_orientation == 'Vertical'):
        globals.sort_output = globals.sort_output.transpose(method=Image.Transpose.ROTATE_270)

    # Set the display image to reference the sorted image
    globals.display_image = globals.sort_output

def drift_pixels(drift_iterations: int, drift_probability: float):
    # Loop through segments
    for i in range(len(segments)):
        # Check if segment is to be processed
        if (segments_mask[i]):
            # For each iteration
            for _ in range(drift_iterations):
                # For each pixel in the segment
                for j in range(len(segments[i]) - 1):
                    if(random.random() < drift_probability):
                        temp_pixel = segments[i][j]
                        segments[i][j] = segments[i][j+1]
                        segments[i][j+1] = temp_pixel

    # Get dimensions for output
    width, height = globals.sort_input.size

    # Make new image for sorted pixels
    if(segment_orientation == 'Horizontal'):
        globals.sort_output = Image.new('RGB', (width, height))
    elif(segment_orientation == 'Vertical'):
        globals.sort_output = Image.new('RGB', (height, width))

    # Write segments to array of pixels
    pixels = []
    for segment in segments:
        for pixel in segment:
            pixels.append(pixel)

    globals.sort_output.putdata(pixels)

    # Correct rotation
    if(segment_orientation == 'Vertical'):
        globals.sort_output = globals.sort_output.transpose(method=Image.Transpose.ROTATE_270)

    # Set the display image to reference the sorted image
    globals.display_image = globals.sort_output

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
    if globals.display_image:
        # Add most recent image to the undo array
        globals.undo_stack.append(globals.sort_input.copy())

        # If we have more than the allowed undo levels, remove the oldest
        while(len(globals.undo_stack) > globals.undo_levels):
            del globals.undo_stack[0]

        # Clear the redo stack
        globals.redo_stack.clear()

        # Copy the buffer referenced by the display to the input buffer
        globals.sort_input = globals.display_image.copy()

        # Clear the output buffer
        globals.sort_output = None