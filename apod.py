'''
Team: Joelle Waugh, Ricardo Rudin, Manual Manrike Lopez, Sadia Shoily

Description: Created a Gui to View  the Nasa image.

'''

from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
from PIL import ImageTk, Image
import apod_desktop
import datetime
import os
import ctypes
import matplotlib.pyplot as plt
# Initialize the image cache
apod_desktop.init_apod_cache()

script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')

# TODO: Create the GUI
root = Tk()
root.geometry('900x700')
root.minsize(600,600)
root.columnconfigure(0,weight=1)
root.rowconfigure(0, weight=1)
root.title("Astronomy Picture of the Day Viewer")



ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('Images')
root.iconbitmap(os.path.join(script_dir, 'nasa_logo_icon.ico'))

# creating the frames
frm = ttk.Frame(root)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)
frm.grid(sticky= NSEW)



Photo= ImageTk.PhotoImage(Image.open("NASA_Logo.png").resize((500,500)))

lbl_image_backg=ttk.Label(frm, image = Photo)
lbl_image_backg.grid(row=0,column=3, columnspan=2, padx=(250), pady=(10,20),sticky= N)
#frm_image_background = ttk.Frame(root)
#frm_image_background.grid(row=0, column=0)

# Create the frames
frm_input = ttk.Frame(root)
frm_input.grid(row=0, column=0, columnspan=2, pady=(20,10))

frm_images = ttk.Frame(root)
frm_images = ttk.LabelFrame(root, text="View Cached Image")
frm_images.grid(row=0, column=0, columnspan=2, pady=(10,20),padx=(0,10), sticky=SW)

frm_more_images = ttk.Frame(root)
frm_more_images = ttk.LabelFrame(root, text="Get More Images")
frm_more_images.grid(row=0, column=3, columnspan=2, pady=(10,20), padx=(0,10), sticky=SE)

#frm_image_background = ttk.Frame(root)
#frm_image_background.grid(row=0, column=0)

#TODO: Populate the user input frame with widgets
lbl_cached = ttk.Label (frm_images, text="Select Image:")
lbl_cached.grid(row=1, column=0, padx=(10,5), pady=10)
#x=[1,2,3,4,5]
#y=[1,2,3,4,5]
image_cache_dir = apod_desktop.init_apod_cache
enter_cached = ttk.Combobox(frm_images, state="readonly")
enter_cached.set("Select an image")
enter_cached.grid(row=1, column=1, padx=20, pady= 10)


enter_desktop = ttk.Button(frm_images, text="Set as Desktop")
enter_desktop.grid(row=1, column=2, padx= 10, pady=10)

lbl_dates = ttk.Label(frm_more_images, text="Select Date(YYYY-mm-dd):")
lbl_dates.grid(row=1, column=3, padx=(10,5), pady=5)

date_pat= 'y-mm-dd'
v_today =datetime.datetime.now()
enter_dates = DateEntry(frm_more_images, maxdate=v_today, date_pattern=date_pat)

enter_dates.insert(0,"")
enter_dates.grid(row=1, column=4)
print (f" Get Dates:{enter_dates.get()}")

    
enter_downloadI = ttk.Button(frm_more_images, text="Download Image")
enter_downloadI.grid(row=1, column=1, padx=10, pady= 10)

'''def handle_os_sel(event):
  lbl_cached = cbox_frmimages.get()
  photo['file'] = os.path.join(, f'{selected_pokemon}.png')
  lbl_image['image'] = photo
  button_set['state'] = "enabled"

cbox_poke.bind('<<ComboboxSelected>>', handle_os_sel)'''
#lbl_image_backg = Label (frm_image_background, image=Photo)
#lbl_image_backg.grid(row=7, column=1)

# Acciones para cada seleccion
##btn_get_info =ttk.Button(root, text="Download Image", command= terceroV3.get_apod_date)
##btn_get_info.grid(row=1, column=5)


###### Termino de insertar nuevo codigo
root.mainloop()