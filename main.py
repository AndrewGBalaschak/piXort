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

# This basically makes sure that threads spawned for multiprocessing don't generate extra UI windows
if __name__ == '__main__':
    # Clears the image onscreen
    def clear(event = None):
        globals.original_image = None
        globals.sort_input = None
        globals.sort_output = None
        globals.display_image = None
        update_display()

    # Resets any sorting and brings back the original image
    def reset(event = None):
        if globals.original_image:
            globals.display_image = globals.original_image
            update_display()

    # Pop off the undo stack and push onto redo stack
    def undo(event = None):
        if len(globals.undo_stack) > 0:
            globals.redo_stack.append(globals.display_image.copy())
            globals.display_image = globals.undo_stack.pop()

            update_display()

        else:
            print('Nothing to undo!')

    # Pop off the redo stack and push onto undo stack
    def redo(event = None):
        if len(globals.redo_stack) > 0:
            globals.undo_stack.append(globals.display_image.copy())
            globals.display_image = globals.redo_stack.pop()

            update_display()

        else:
            print('Nothing to redo!')

    # Undoes all transformations and revents to the original image
    def reset(event = None):
        if globals.original_image:
            globals.display_image = globals.original_image
            globals.sort_input = globals.original_image.copy()
            globals.display_image = globals.original_image
            
            # Clear any old images
            globals.undo_stack.clear()
            globals.redo_stack.clear()
            globals.sort_output = None
            update_display()

    # Open a file dialog to load a file
    def open_file_dialog(event = None):
        file_path = filedialog.askopenfilename(filetypes=[('Image files', '*.png *.jpg *.jpeg *.bmp *.gif *.ppm *.pgm *.pbm')])
        
        if file_path:
            # Load the selected image using Pillow
            globals.original_image = Image.open(file_path)
            reset()

    # Opens a file dialog to save the image that is currently on screen
    def save_file_dialog(event = None):
        if globals.display_image:
            save_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
            if save_path:
                globals.display_image.save(save_path)

    # Updates the image displayed in the GUI
    def update_display():
        if not globals.display_image:
            globals.display_image = globals.empty_image

        # Copy the image to be displayed into the thumbnail buffer
        globals.display_image_thumb = globals.display_image.copy()

        # Create the thumbnail for display
        globals.display_image_thumb.thumbnail(globals.thumb_size)

        # Create a TKinter object for display
        display_image_tk = ImageTk.PhotoImage(globals.display_image_thumb)

        # Update the display label to hold the objcet
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
        about.minsize(300, 200)
        about.resizable(False, False)

        body = ttk.Label(about, text='piXort is a Free and Open-Source Software (FOSS) pixel sorting program written in Python. For more details see the LICENSE file.\n\n(c) Andrew Balaschak 2023', anchor=tk.CENTER, justify=tk.CENTER, wraplength=180)
        body.pack(fill=tk.BOTH, expand=True)



    #################### ---------- MENU BAR ---------- ####################
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=False)
    file_menu.add_command(label='New', command=clear, accelerator='Ctrl+N')
    file_menu.add_command(label='Open', command=open_file_dialog, accelerator='Ctrl+O')
    file_menu.add_command(label='Save', command=save_file_dialog, accelerator='Ctrl+S')
    file_menu.add_separator()
    file_menu.add_command(label='Exit', command=root.quit)
    menubar.add_cascade(label='File', menu=file_menu)

    edit_menu = tk.Menu(menubar, tearoff=False)
    edit_menu.add_command(label='Undo', command=undo, accelerator='Ctrl+Z')
    edit_menu.add_command(label='Redo', command=redo, accelerator='Ctrl+Y')
    edit_menu.add_separator()
    edit_menu.add_command(label='Reset', command=reset, accelerator='Ctrl+R')
    menubar.add_cascade(label='Edit', menu=edit_menu)

    help_menu = tk.Menu(menubar, tearoff=False)
    help_menu.add_command(label='Help')
    help_menu.add_command(label='About...', command=about_window)
    menubar.add_cascade(label='Help', menu=help_menu)

    root.config(menu=menubar)

    # Keyboard shortcuts
    root.bind('<Control-n>', clear)
    root.bind('<Control-o>', open_file_dialog)
    root.bind('<Control-s>', save_file_dialog)
    root.bind('<Control-z>', undo)
    root.bind('<Control-y>', redo)
    root.bind('<Control-r>', reset)



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
    segments_frame = ttk.Frame(tab_basic, relief=tk.SUNKEN, padding=(5,5,5,5))
    segments_frame.grid(row=0, column=0, sticky='EW')

    segments_frame.grid_rowconfigure(0, weight=1)
    segments_frame.grid_columnconfigure(0, weight=1)
    segments_frame.grid_columnconfigure(1, weight=1)
    segments_frame.grid_columnconfigure(2, weight=1)

    def update_segments_visibility():
        # If edge detection is on
        if (segment_edge_detect_var.get()):
            segment_size_label['state'] = 'disabled'
            segment_size_entry['state'] = 'disabled'
            segment_random_scale['state'] = 'disabled'
            segment_random_label['state'] = 'disabled'
            segment_random_scale_readout['state'] = 'disabled'
            threading.Thread(target=update_display_edges).start()
        else:
            segment_size_label['state'] = 'enabled'
            segment_size_entry['state'] = 'enabled'
            segment_random_scale['state'] = 'enabled'
            segment_random_label['state'] = 'enabled'
            segment_random_scale_readout['state'] = 'enabled'
            update_display()

    # Segments header
    segment_header = ttk.Label(segments_frame, text='Segments', font=('TkDefaultFont',24))
    segment_header.grid(row=0, column=0, columnspan=3)

    # Create checkbutton for edge detection
    segment_edge_detect_var = tk.BooleanVar(value=False)
    segment_edge_detect_label = ttk.Label(segments_frame, text='Edge Detection')
    segment_edge_detect_check = ttk.Checkbutton(segments_frame, variable=segment_edge_detect_var, command=update_segments_visibility)
    segment_edge_detect_label.grid(row=1, column=0, sticky='E')
    segment_edge_detect_check.grid(row=1, column=1, sticky='W')

    # Create a slider for edge detection threshold
    def update_edge_detect_label(value):
        segment_edge_thresh_readout['text'] = str(round(float(value)*100)) + '%'

    segment_edge_thresh_label = ttk.Label(segments_frame, text='Edge Threshold')
    segment_edge_thresh_scale = ttk.Scale(segments_frame, from_=0, to=1, orient='horizontal', length=100, value=0.5, command=lambda x:[update_edge_detect_label(x)])
    segment_edge_thresh_scale.bind("<ButtonRelease-1>", lambda x:[threading.Thread(target=update_display_edges).start()])
    segment_edge_thresh_label.grid(row=2, column=0, sticky='E')
    segment_edge_thresh_scale.grid(row=2, column=1, sticky='W')
    segment_edge_thresh_readout = ttk.Label(segments_frame, width=5, text=str(round(float(segment_edge_thresh_scale.get()), 2)))
    segment_edge_thresh_readout.grid(row=2, column=2, sticky='W')
    update_edge_detect_label(segment_edge_thresh_scale.get())

    # Create separator
    sort_separator =  ttk.Separator(segments_frame, orient='horizontal')
    sort_separator.grid(row=3, column=0, columnspan=3, sticky='EW')

    # Create a text box for segment size
    segment_size_label = ttk.Label(segments_frame, text='Length (Pixels)')
    segment_size_entry = ttk.Entry(segments_frame, width=10)
    segment_size_entry.insert(0, '256')      # Set default value
    segment_size_label.grid(row=4, column=0, sticky='E')
    segment_size_entry.grid(row=4, column=1, sticky='W')

    # Create a slider for segment random size
    def update_random_label(value):
        segment_random_scale_readout['text'] = str(round(float(value)*100)) + '%'
        
    segment_random_label = ttk.Label(segments_frame, text='Random Length Multiplier')
    segment_random_scale = ttk.Scale(segments_frame, from_=0, to=1, orient='horizontal', length=100, value=0, command=update_random_label)
    segment_random_label.grid(row=5, column=0, sticky='E')
    segment_random_scale.grid(row=5, column=1, sticky='W')
    segment_random_scale_readout = ttk.Label(segments_frame, width=5, text=str(round(segment_random_scale.get())))
    segment_random_scale_readout.grid(row=5, column=2, sticky='W')
    update_random_label(segment_random_scale.get())

    # Create separator
    sort_separator =  ttk.Separator(segments_frame, orient='horizontal')
    sort_separator.grid(row=6, column=0, columnspan=3, sticky='EW')

    # Create a slider for segment sort probability
    def update_probability_label(value):
        segment_probability_readout['text'] = str(round(float(value)*100)) + '%'

    segment_probability_label = ttk.Label(segments_frame, text='Effect Probability')
    segment_probability_scale = ttk.Scale(segments_frame, from_=0, to=1, orient='horizontal', length=100, value=1, command=update_probability_label)
    segment_probability_label.grid(row=7, column=0, sticky='E')
    segment_probability_scale.grid(row=7, column=1, sticky='W')
    segment_probability_readout = ttk.Label(segments_frame, width=5, text=str(round(float(segment_probability_scale.get()), 2)))
    segment_probability_readout.grid(row=7, column=2, sticky='W')
    update_probability_label(segment_probability_scale.get())

    # Create separator
    sort_separator =  ttk.Separator(segments_frame, orient='horizontal')
    sort_separator.grid(row=8, column=0, columnspan=3, sticky='EW')

    # Create radio buttons for segment orientation
    segment_orientation_label = ttk.Label(segments_frame, text='Orientation:')
    segment_orientation_label.grid(row=9, column=0, rowspan=2, sticky='E')

    segment_orientation_var = tk.StringVar(value='Horizontal')
    segment_orientation_hori = ttk.Radiobutton(segments_frame, text='Horizontal', variable=segment_orientation_var, value='Horizontal')
    segment_orientation_vert = ttk.Radiobutton(segments_frame, text='Vertical', variable=segment_orientation_var, value='Vertical')
    segment_orientation_hori.grid(row=9, column=1, sticky='W')
    segment_orientation_vert.grid(row=10, column=1, sticky='W')



    #################### ---------- SORT OPTIONS ---------- ####################
    # Frame for sort config
    sort_frame = ttk.Frame(tab_basic, relief=tk.SUNKEN, padding=(5,5,5,5))
    sort_frame.grid(row=1, column=0, sticky='EW')

    sort_frame.grid_rowconfigure(0, weight=1)
    sort_frame.grid_columnconfigure(0, weight=1)
    sort_frame.grid_columnconfigure(1, weight=1)
    sort_frame.grid_columnconfigure(2, weight=1)

    # Sort header
    sort_header = ttk.Label(sort_frame, text='Pixel Sorting', font=('TkDefaultFont',24))
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
    sort_separator.grid(row=7, column=0, columnspan=4, sticky='EW')

    # Create radio buttons for sort direction
    sort_direction_label = ttk.Label(sort_frame, text='Sort Direction:')
    sort_direction_label.grid(row=8, column=0, rowspan=2, sticky='E')

    sort_direction_var = tk.BooleanVar()
    sort_direction_low = ttk.Radiobutton(sort_frame, text='Standard', variable=sort_direction_var, value=False)
    sort_direction_high = ttk.Radiobutton(sort_frame, text='Inverted', variable=sort_direction_var, value=True)
    sort_direction_low.grid(row=8, column=1, sticky='W')
    sort_direction_high.grid(row=9, column=1, sticky='W')



    #################### ---------- PIXEL DRIFT OPTIONS ---------- ####################
    # Frame for segment config
    drift_frame = ttk.Frame(tab_basic, relief=tk.SUNKEN, padding=(5,5,5,5))
    drift_frame.grid(row=2, column=0, sticky='EW')

    drift_frame.grid_rowconfigure(0, weight=1)
    drift_frame.grid_columnconfigure(0, weight=1)
    drift_frame.grid_columnconfigure(1, weight=1)
    drift_frame.grid_columnconfigure(2, weight=1)

    # Drift header
    drift_header = ttk.Label(drift_frame, text='Pixel Drift', font=('TkDefaultFont',24))
    drift_header.grid(row=0, column=0, columnspan=3)

    # Create a text box for drift iterations
    drift_iter_label = ttk.Label(drift_frame, text='Iterations')
    drift_iter_entry = ttk.Entry(drift_frame)
    drift_iter_entry.insert(0, '16')      # Set default value
    drift_iter_label.grid(row=1, column=0, sticky='E')
    drift_iter_entry.grid(row=1, column=1, sticky='W')

    # Create a slider for drift probability
    def update_drift_probability(value):
        drift_probability_scale_readout['text'] = str(round(float(value) * 100)) + '%'
        
    drift_probability_label = ttk.Label(drift_frame, text='Pixel Drift Probability')
    drift_probability_scale = ttk.Scale(drift_frame, from_=0, to=1, orient='horizontal', length=100, value=0.5, command=update_drift_probability)
    drift_probability_label.grid(row=2, column=0, sticky='E')
    drift_probability_scale.grid(row=2, column=1, sticky='W')
    drift_probability_scale_readout = ttk.Label(drift_frame, width=5, text=str(round(drift_probability_scale.get())))
    drift_probability_scale_readout.grid(row=2, column=2, sticky='W')
    update_drift_probability('0.5')

    drift_max_label = ttk.Label(drift_frame, text='Maximum Drift')
    drift_max_check = ttk.Checkbutton(drift_frame)
    drift_max_label.grid(row=3, column=0, sticky='E')
    drift_max_check.grid(row=3, column=1, sticky='W')


    #################### ---------- PROGRESS BAR ---------- ####################
    pb = ttk.Progressbar(root, mode='indeterminate')



    #################### ---------- RENDER FRAME ---------- ####################
    # Frame for render buttons
    render_frame = ttk.Frame(root)
    render_frame.grid(row=2, column=0, sticky='NSEW')

    # Displays edges
    def update_display_edges():
        if segment_edge_detect_var.get() and globals.sort_input:
            # Display progress bar
            pb.grid(row=2, column=2, sticky='EW', padx=100)
            pb.start(25)

            sort_pixels.get_edges(segment_edge_thresh_scale.get())

            # Hide progress bar
            pb.stop()
            pb.grid_forget()

            # Copy the edges into the thumbnail buffer
            globals.display_image_thumb = globals.edges.copy()

            # Create the thumbnail for display
            globals.display_image_thumb.thumbnail(globals.thumb_size)

            # Create a TKinter object for display
            display_image_tk = ImageTk.PhotoImage(globals.display_image_thumb)

            # Update the display label to hold the objcet
            display_label.config(image=display_image_tk)
            display_label.image = display_image_tk

    # Sorts image based on parameters
    def sort():
        if globals.sort_input:
            # Display progress bar
            pb.grid(row=2, column=2, sticky='EW', padx=100)
            pb.start(25)

            # Disable buttons
            sort_button['state'] = 'disabled'
            shuffle_button['state'] = 'disabled'
            apply_button['state'] = 'disabled'

            # Perform computation
            if not globals.edges and segment_edge_detect_var.get():
                sort_pixels.get_edges(segment_edge_thresh_scale.get())
            sort_pixels.get_segments(int(segment_size_entry.get()), segment_random_scale.get(), segment_orientation_var.get(), segment_edge_detect_var.get())
            sort_pixels.sort_pixels(sort_direction_var.get(), sort_criteria_var.get(), segment_probability_scale.get())

            # Enable buttons
            sort_button['state'] = 'normal'
            shuffle_button['state'] = 'normal'
            apply_button['state'] = 'normal'

            # Hide progress bar
            pb.stop()
            pb.grid_forget()

            update_display()

    def drift():
        if globals.sort_input:
            # Display progress bar
            pb.grid(row=2, column=2, sticky='EW', padx=100)
            pb.start(25)

            # Disable buttons
            sort_button['state'] = 'disabled'
            shuffle_button['state'] = 'disabled'
            apply_button['state'] = 'disabled'

            # Perform computation
            if not globals.edges and segment_edge_detect_var.get():
                sort_pixels.get_edges(segment_edge_thresh_scale.get())
            sort_pixels.get_segments(int(segment_size_entry.get()), segment_random_scale.get(), segment_orientation_var.get(), segment_edge_detect_var.get())
            sort_pixels.drift_pixels(int(drift_iter_entry.get()), drift_probability_scale.get(), segment_probability_scale.get())

            # Enable buttons
            sort_button['state'] = 'normal'
            shuffle_button['state'] = 'normal'
            apply_button['state'] = 'normal'

            # Hide progress bar
            pb.stop()
            pb.grid_forget()

            update_display()

    # Create buttons for rendering
    sort_button = ttk.Button(render_frame, text='Preview Sort', width=20, command=lambda:[threading.Thread(target=sort).start()])
    shuffle_button = ttk.Button(render_frame, text='Preview Drift', width=20, command=lambda:[threading.Thread(target=drift).start()])
    apply_button = ttk.Button(render_frame, text='Apply', width=44, command=sort_pixels.apply_sort)
    sort_button.grid(row=0, column=0)
    shuffle_button.grid(row=0, column=1)
    apply_button.grid(row=1, column=0, columnspan=2)



    #################### ---------- IMAGE ---------- ####################
    display_label = ttk.Label(root)
    display_label.grid(row=0, column=2, rowspan=1, sticky='NSEW')



    update_display()
    root.mainloop()