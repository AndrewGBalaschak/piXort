import sort_pixels
import globals
from PIL import Image, ImageTk
import time


# This basically makes sure that threads spawned for multiprocessing don't run the code again
if __name__ == '__main__':
    globals.original_image = Image.open('examples\image2.png')
    globals.sort_input = globals.original_image.copy()

    #Get basic details about the image
    print(globals.original_image.format)
    print(globals.original_image.mode)
    print(globals.original_image.size)

    # Start timer
    start = time.time()

    # Sort the image and display
    sort_pixels.get_segments(50, 0.0, 'Horizontal', False)
    sort_pixels.sort_pixels(True, 'Luminance', 1.0)
    sort_pixels.apply_sort()

    end = time.time()
    print("Time to sort:", end - start)

    # sort_pixels.get_segments(5, 1, 0.1, 'Vertical')
    # sort_pixels.sort_pixels(False, 'Saturation')

    # globals.sorted_image.show()
    # globals.sorted_image.save('examples\image1-sorted-2.png')