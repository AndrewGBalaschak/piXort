import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Import my sorting functions
import sort_pixels

# Import global image variables
import globals

# Open a file dialog to load a file
def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.ppm *.pgm *.pbm")])
    
    if file_path:
        # Load the selected image using Pillow
        globals.original_image = Image.open(file_path)

        # Clear any old image
        globals.sorted_image = None
        update_display()

# Opens a file dialog to save a file
def save_file_dialog():
    if globals.sorted_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            globals.sorted_image.save(save_path)

# Updates the image displayed in the GUI
def update_display():
    if globals.sorted_image:
        globals.display_image = globals.sorted_image.copy()

    elif globals.original_image:
        globals.display_image = globals.original_image.copy()

    if globals.display_image:
        globals.display_image.thumbnail(globals.thumb_size)
        display_image_tk = ImageTk.PhotoImage(globals.display_image)
        display_label.config(image=display_image_tk)
        display_label.image = display_image_tk

# Create the main tkinter window
root = tk.Tk()
root.title("piXort")
root.minsize(600, 600)
root.resizable(False, False)

# Create buttons for open and save
open_button = tk.Button(root, text="Open Image", command=open_file_dialog)
save_button = tk.Button(root, text="Save Sorted Image", command=save_file_dialog)

# Create buttons for sort, shuffle, and apply
sort_button = tk.Button(root, text="Sort", command=lambda:[sort_pixels.sort_value(int(segment_size_entry.get()), segment_random_scale.get(), segment_probability_scale.get(), True, sorting_direction_var.get()), update_display()])
shuffle_button = tk.Button(root, text="Shuffle", command=lambda:[sort_pixels.sort_value(int(segment_size_entry.get()), segment_random_scale.get(), segment_probability_scale.get(), False, sorting_direction_var.get()), update_display()])
apply_button = tk.Button(root, text="Apply", command=sort_pixels.apply_sort)

# Create a text box for segment size
segment_size_label = tk.Label(root, text="Segment Size")
segment_size_entry = tk.Entry(root)
segment_size_entry.insert(0, "50")      # Set default value

# Create a slider for segment random size
segment_random_label = tk.Label(root, text="Segment Random Size")
segment_random_scale = tk.Scale(root, from_=0, to=1, orient="horizontal", resolution=0.01)
segment_random_scale.set(0)             # Set default value

# Create a slider for segment sort probability
segment_probability_label = tk.Label(root, text="Segment Sort Probability")
segment_probability_scale = tk.Scale(root, from_=0, to=1, orient="horizontal", resolution=0.01)
segment_probability_scale.set(1)        # Set default value

# Create a checkbox for sorting direction
sorting_direction_var = tk.BooleanVar()
sorting_direction_checkbox = tk.Checkbutton(root, text="Vertical Sorting", variable=sorting_direction_var)

# Create labels for image display
display_label = tk.Label(root)

# Arrange elements using the grid geometry manager
open_button.grid(row=0, column=0, columnspan=2)
root.grid_columnconfigure(0, weight=1)  # Center column 0 horizontally
root.grid_columnconfigure(1, weight=1)  # Center column 1 horizontally
segment_size_label.grid(row=1, column=0)
segment_size_entry.grid(row=1, column=1)
segment_random_label.grid(row=2, column=0)
segment_random_scale.grid(row=2, column=1)
segment_probability_label.grid(row=3, column=0)
segment_probability_scale.grid(row=3, column=1)
sorting_direction_checkbox.grid(row=4, column=0, columnspan=2)
sort_button.grid(row=5, column=0)
shuffle_button.grid(row=6, column=0)
apply_button.grid(row=5, column=1, rowspan=2)
save_button.grid(row=7, column=0, columnspan=2)

# Display image
display_label.grid(row=8, column=0, columnspan=2)

'''
# Pack UI OLD
open_button.pack()
save_button.pack()
sort_button.pack()
apply_button.pack()
segment_size_label.pack()
segment_size_entry.pack()
segment_random_label.pack()
segment_random_scale.pack()
sorting_direction_checkbox.pack()
display_label.pack()
'''




root.mainloop()