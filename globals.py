original_image = None       # Stores the original image, is never modified
undo_stack = []             # Stores multiple levels of undo
redo_stack = []             # Stores multiple levels of redo
input_image = None          # Stores the input to the processing algorithm
output_image = None         # Stores the output from the processing algorithm
resized_image = None        # Stores the output from the resize operation
edges = None                # Stores detected edges for display
display_image_thumb = None  # Stores the image displayed on screen in thumbnail size
empty_image = None          # Stores the empty image used when no image is loaded

display_image = None        # Stores a reference to the image that is displayed, does NOT contain a unique image

thumb_size = (1024,1024)    # Thumbnail size

undo_levels = 16             # Undo levels