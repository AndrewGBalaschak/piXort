import sort_pixels
import globals
from PIL import Image, ImageTk

globals.original_image = Image.open('images\image1.png')

#Get basic details about the image
print(globals.original_image.format)
print(globals.original_image.mode)
print(globals.original_image.size)

# Sort the image and display
sort_pixels.sort_value(50, 0.5, 0.25, 'Horizontal', True, False, 'Hue')
sort_pixels.apply_sort()
sort_pixels.sort_value(5, 1, 0.1, 'Vertical', True, False, 'Saturation')
globals.sorted_image.show()
# globals.sorted_image.save('images\image1-sorted-2.png')