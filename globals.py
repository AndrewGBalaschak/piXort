original_image = None       # Stores the original image, is never modified
undo_stack = []             # Stores multiple levels of undo
redo_stack = []             # Stores multiple levels of redo
sort_input = None           # Stores the input to the storting algorithm
sort_output = None          # Stores the output from the sorting algorithm
display_image_thumb = None  # Stores the image displayed on screen in thumbnail size
empty_image = None          # Stores the empty image used when no image is loaded

display_image = None        # Stores a reference to the image that is displayed

thumb_size = (512,512)      # Thumbnail size

undo_levels = 5             # Undo levels