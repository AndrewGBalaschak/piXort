import sort_pixels
import globals
from PIL import Image, ImageTk

globals.original_image = Image.open('examples\image2.png')
globals.sort_input = globals.original_image.copy()

#Get basic details about the image
print(globals.original_image.format)
print(globals.original_image.mode)
print(globals.original_image.size)

# Sort the image and display
sort_pixels.get_segments(50, 0.5, 1, 'Horizontal', True, 0.8)
sort_pixels.sort_pixels(True, 'Luminance')
sort_pixels.apply_sort()

# sort_pixels.get_segments(5, 1, 0.1, 'Vertical')
# sort_pixels.sort_pixels(False, 'Saturation')

globals.sort_input.show()
# globals.sorted_image.save('examples\image1-sorted-2.png')