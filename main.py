import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import threading

# Import my sorting functions
import sort_pixels

# Import global image variables 
import globals

def clear(event = None):
    globals.original_image = None
    globals.sorted_image = None
    globals.display_image = None
    update_display()

# Open a file dialog to load a file
def open_file_dialog(event = None):
    file_path = filedialog.askopenfilename(filetypes=[('Image files', '*.png *.jpg *.jpeg *.bmp *.gif *.ppm *.pgm *.pbm')])
    
    if file_path:
        # Load the selected image using Pillow
        globals.original_image = Image.open(file_path)

        # Clear any old image
        globals.sorted_image = None
        update_display()

# Opens a file dialog to save a file
def save_file_dialog(event = None):
    if globals.sorted_image:
        save_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
        if save_path:
            globals.sorted_image.save(save_path)

# Updates the image displayed in the GUI
def update_display():
    if globals.sorted_image:
        globals.display_image = globals.sorted_image.copy()

    elif globals.original_image:
        globals.display_image = globals.original_image.copy()

    else:
        globals.display_image = globals.empty_image.copy()

    if globals.display_image:
        globals.display_image.thumbnail(globals.thumb_size)
        display_image_tk = ImageTk.PhotoImage(globals.display_image)
        display_label.config(image=display_image_tk)
        display_label.image = display_image_tk


#################### ---------- MAIN WINDOW ---------- ####################
# Load the default image
globals.empty_image = Image.open('images/empty.png')

# Create the main tkinter window
root = ThemedTk(theme='equilux', themebg=True)
root.title('piXort')
root.minsize(600, 600)
root.resizable(False, False)

# Load app icon
icon = tk.PhotoImage(file='images/icon.png')
root.iconphoto(True, icon)
root.iconwindow()

# About popup window
def about_window():
    about = tk.Toplevel(root)
    about.title('About')
    root.minsize(300, 200)
    root.resizable(False, False)

    body = ttk.Label(about, text="piXort written by Andrew Balaschak\n(C) 2023")
    body.pack()


#################### ---------- MENU BAR ---------- ####################
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=False)
filemenu.add_command(label='New', command=clear, accelerator="Ctrl+N")
filemenu.add_command(label='Open', command=open_file_dialog, accelerator="Ctrl+O")
filemenu.add_command(label='Save', command=save_file_dialog, accelerator="Ctrl+S")
filemenu.add_separator()
filemenu.add_command(label='Exit', command=root.quit)
menubar.add_cascade(label='File', menu=filemenu)
'''
helpmenu = tk.Menu(menubar, tearoff=False)
helpmenu.add_command(label='Help')
helpmenu.add_command(label='About...', command=about_window)
menubar.add_cascade(label='Help', menu=helpmenu)
'''
root.config(menu=menubar)

# Keyboard shortcuts
root.bind('<Control-n>', clear)
root.bind('<Control-o>', open_file_dialog)
root.bind('<Control-s>', save_file_dialog)


#################### ---------- BASIC / ADVANCED TABS ---------- ####################
# Create basic and advanced feature tabs
tabControl = ttk.Notebook(root)
tab_basic = ttk.Frame(tabControl)
tab_advan = ttk.Frame(tabControl)

tabControl.add(tab_basic, text ='Basic', sticky='NSEW')
tabControl.add(tab_advan, text ='Advanced', sticky='NSEW')
tabControl.grid(row=0, column=0, sticky='NSEW')

tab_basic.grid_rowconfigure(0, weight=1)
tab_basic.grid_rowconfigure(1, weight=1)
tab_basic.grid_columnconfigure(0, weight=1)
tab_basic.grid_columnconfigure(1, weight=1)


#################### ---------- SEGMENT OPTIONS ---------- ####################
# Frame for segment config
segments_frame = ttk.Frame(tab_basic)
segments_frame.grid(row=0, column=0)

segments_frame.grid_rowconfigure(0, weight=1)
segments_frame.grid_columnconfigure(0, weight=1)
segments_frame.grid_columnconfigure(1, weight=1)
segments_frame.grid_columnconfigure(2, weight=1)

# Segments header
segment_header = ttk.Label(segments_frame, text='Segments', font=("TkDefaultFont",24))
segment_header.grid(row=0, column=0, columnspan=3)

# Create a text box for segment size
segment_size_label = ttk.Label(segments_frame, text='Size')
segment_size_entry = ttk.Entry(segments_frame)
segment_size_entry.insert(0, '256')      # Set default value
segment_size_label.grid(row=1, column=0, sticky='E')
segment_size_entry.grid(row=1, column=1, sticky='W')

# Create a slider for segment random size
def update_random_label(value):
    segment_random_scale_readout['text'] = str(round(float(value), 2))
segment_random_label = ttk.Label(segments_frame, text='Random Size')
segment_random_scale = ttk.Scale(segments_frame, from_=0, to=1, orient='horizontal', length=100, value=0, command=update_random_label)
segment_random_label.grid(row=2, column=0, sticky='E')
segment_random_scale.grid(row=2, column=1, sticky='W')
segment_random_scale_readout = ttk.Label(segments_frame, width=5, text=str(round(segment_random_scale.get())))
segment_random_scale_readout.grid(row=2, column=2, sticky='W')

# Create a slider for segment sort probability
def update_probability_label(value):
    segment_probability_readout['text'] = str(round(float(value), 2))

segment_probability_label = ttk.Label(segments_frame, text='Effect Probability')
segment_probability_scale = ttk.Scale(segments_frame, from_=0, to=1, orient='horizontal', length=100, value=1, command=update_probability_label)
segment_probability_label.grid(row=3, column=0, sticky='E')
segment_probability_scale.grid(row=3, column=1, sticky='W')
segment_probability_readout = ttk.Label(segments_frame, width=5, text=str(round(float(segment_probability_scale.get()), 2)))
segment_probability_readout.grid(row=3, column=2, sticky='W')

# Create radio buttons for segment orientation
seg_orientation_label = ttk.Label(segments_frame, text='Orientation:')
seg_orientation_label.grid(row=4, column=0, rowspan=2, sticky='E')

seg_orientation_var = tk.StringVar(value='Horizontal')
seg_orientation_hori = ttk.Radiobutton(segments_frame, text='Horizontal', variable=seg_orientation_var, value='Horizontal')
seg_orientation_vert = ttk.Radiobutton(segments_frame, text='Vertical', variable=seg_orientation_var, value='Vertical')
seg_orientation_hori.grid(row=4, column=1, sticky='W')
seg_orientation_vert.grid(row=5, column=1, sticky='W')


#################### ---------- SORT OPTIONS ---------- ####################
# Frame for sort config
sort_frame = ttk.Frame(tab_basic)
sort_frame.grid(row=1, column=0)

sort_frame.grid_rowconfigure(0, weight=1)
sort_frame.grid_columnconfigure(0, weight=1)
sort_frame.grid_columnconfigure(1, weight=1)
sort_frame.grid_columnconfigure(2, weight=1)

# Sort header
sort_header = ttk.Label(sort_frame, text='Sorting', font=("TkDefaultFont",24))
sort_header.grid(row=0, column=0, columnspan=3)

# Create radio buttons for sort criteria
seg_direction_label = ttk.Label(sort_frame, text='Sort By:')
seg_direction_label.grid(row=1, column=0, rowspan=6, sticky='E')

sort_criteria_var = tk.StringVar(value='Luminance')
sort_criteria_hue = ttk.Radiobutton(sort_frame, text='Hue', variable=sort_criteria_var, value='Hue')
sort_criteria_sat = ttk.Radiobutton(sort_frame, text='Saturation', variable=sort_criteria_var, value='Saturation')
sort_criteria_lum = ttk.Radiobutton(sort_frame, text='Luminance', variable=sort_criteria_var, value='Luminance')
sort_criteria_red = ttk.Radiobutton(sort_frame, text='Red', variable=sort_criteria_var, value='Red')
sort_criteria_grn = ttk.Radiobutton(sort_frame, text='Green', variable=sort_criteria_var, value='Green')
sort_criteria_blu = ttk.Radiobutton(sort_frame, text='Blue', variable=sort_criteria_var, value='Blue')

sort_criteria_hue.grid(row=1, column=1, sticky='W')
sort_criteria_sat.grid(row=2, column=1, sticky='W')
sort_criteria_lum.grid(row=3, column=1, sticky='W')
sort_criteria_red.grid(row=4, column=1, sticky='W')
sort_criteria_grn.grid(row=5, column=1, sticky='W')
sort_criteria_blu.grid(row=6, column=1, sticky='W')

# Create separator
sort_separator =  ttk.Separator(sort_frame, orient='horizontal')
sort_separator.grid(row=7, column=0, columnspan=2, sticky='EW')

# Create radio buttons for sort direction
sort_direction_label = ttk.Label(sort_frame, text='Sort Direction:')
sort_direction_label.grid(row=8, column=0, rowspan=2, sticky='E')

sort_direction_var = tk.BooleanVar()
sort_direction_low = ttk.Radiobutton(sort_frame, text='Low to High', variable=sort_direction_var, value=False)
sort_direction_high = ttk.Radiobutton(sort_frame, text='High to Low', variable=sort_direction_var, value=True)
sort_direction_low.grid(row=8, column=1, sticky='W')
sort_direction_high.grid(row=9, column=1, sticky='W')


#################### ---------- RENDER FRAME ---------- ####################
# Frame for render buttons
render_frame = ttk.Frame(root)
render_frame.grid(row=2, column=0, sticky='NSEW')

# Create buttons for rendering
sort_button = ttk.Button(render_frame, text='Sort', width=20, command=lambda:[sort_pixels.sort_value(int(segment_size_entry.get()), segment_random_scale.get(), segment_probability_scale.get(), seg_orientation_var.get(), True, sort_direction_var.get(), sort_criteria_var.get()), update_display()])
shuffle_button = ttk.Button(render_frame, text='Shuffle', width=20, command=lambda:[sort_pixels.sort_value(int(segment_size_entry.get()), segment_random_scale.get(), segment_probability_scale.get(), seg_orientation_var.get(), False, sort_direction_var.get(), sort_criteria_var.get()), update_display()])
apply_button = ttk.Button(render_frame, text='Apply', width=44, command=sort_pixels.apply_sort)
sort_button.grid(row=0, column=0)
shuffle_button.grid(row=0, column=1)
apply_button.grid(row=1, column=0, columnspan=2)


#################### ---------- IMAGE ---------- ####################
display_label = ttk.Label(root)
display_label.grid(row=0, column=2, rowspan=1, sticky='NSEW')


#################### ---------- PROGRESS ---------- ####################
# progress_bar = ttk.Progressbar(root, mode='determinate')
# progress_bar.grid(row=1, column=2, sticky='EW')

update_display()
root.mainloop()