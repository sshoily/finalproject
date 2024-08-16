"""Sadia Shoily

Description: GUI to view and manage NASA's Astronomy Picture of the Day (APOD).
"""

from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from PIL import ImageTk, Image
import apod_desktop
import datetime
import os
import ctypes

# Initialize the image cache directory for APOD images
apod_desktop.init_apod_cache()

# Define directories
script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')

# Create the main root window
root = Tk()
root.geometry('900x700')
root.minsize(600, 600)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.title("Astronomy Picture of the Day Viewer")

# Set application icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Images')
root.iconbitmap(os.path.join(script_dir, 'nasa_logo_icon.ico'))

# Create the main frame
main_frame = ttk.Frame(root)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)
main_frame.grid(sticky=NSEW)

# Load and display NASA logo image
photo = ImageTk.PhotoImage(Image.open("NASA_Logo.png").resize((500, 500)))
lbl_image_background = ttk.Label(main_frame, image=photo)
lbl_image_background.grid(row=0, column=3, columnspan=2, padx=250, pady=(10, 20), sticky=N)

# Create frames for image display and user inputs
frm_input = ttk.Frame(root)
frm_input.grid(row=0, column=0, columnspan=2, pady=(20, 10))

frm_images = ttk.LabelFrame(root, text="View Cached Image")
frm_images.grid(row=0, column=0, columnspan=2, pady=(10, 20), padx=(0, 10), sticky=SW)

frm_more_images = ttk.LabelFrame(root, text="Get More Images")
frm_more_images.grid(row=0, column=3, columnspan=2, pady=(10, 20), padx=(0, 10), sticky=SE)

# Populate 'View Cached Image' frame with widgets
lbl_cached = ttk.Label(frm_images, text="Select Image:")
lbl_cached.grid(row=1, column=0, padx=(10, 5), pady=10)

# Combo box to select cached images
image_cache_dir = apod_desktop.init_apod_cache
enter_cached = ttk.Combobox(frm_images, state="readonly")
enter_cached.set("Select an image")
enter_cached.grid(row=1, column=1, padx=20, pady=10)

# Button to set selected image as desktop wallpaper
enter_desktop = ttk.Button(frm_images, text="Set as Desktop")
enter_desktop.grid(row=1, column=2, padx=10, pady=10)

# Populate 'Get More Images' frame with widgets
lbl_dates = ttk.Label(frm_more_images, text="Select Date (YYYY-mm-dd):")
lbl_dates.grid(row=1, column=3, padx=(10, 5), pady=5)

# DateEntry widget for selecting a date
date_pattern = 'y-mm-dd'
current_date = datetime.datetime.now()
enter_dates = DateEntry(frm_more_images, maxdate=current_date, date_pattern=date_pattern)

enter_dates.insert(0, "")
enter_dates.grid(row=1, column=4)
print(f"Get Dates: {enter_dates.get()}")

# Button to download image from the selected date
enter_downloadI = ttk.Button(frm_more_images, text="Download Image")
enter_downloadI.grid(row=1, column=1, padx=10, pady=10)

# Main event loop
root.mainloop()
