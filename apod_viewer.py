from tkinter import *
from tkinter import ttk
import inspect
import os
import apod_desktop
import ctypes
from tkcalendar import Calendar, DateEntry
import image_lib

# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
apod_desktop.init_apod_cache(script_dir)

# TODO: Create the GUI
root = Tk()
root.title('Astronomy Picture of the Day Viewer')
root.geometry('600x400')
root.minsize(1000, 700)

# Set The Window Icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
icon_path = os.path.join(script_dir, 'nasa.ico')
root.iconbitmap(icon_path)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


#ADD Frames To Window.
frame = ttk.Frame(root)
frm_top = ttk.Frame(root)
frm_top.grid(row=0, column=0, columnspan=2, pady=(20, 10))

cach_frame = ttk.LabelFrame(root, text='View Cached Image')
cach_frame.grid(row=0, column=0, padx=(20, 10), pady=(10, 20), sticky=SW)

dwnld_frame = ttk.LabelFrame(root, text='Get More Images')
dwnld_frame.grid(row=0, column=1, padx=(20, 10), pady=(10, 20), sticky=SW)

# Add The Image To The Frame

img_nasa = PhotoImage(file=os.path.join(script_dir,'default.png'))
lbl_img_nasa = ttk.Label(frm_top, image=img_nasa)
lbl_img_nasa.grid(row=0, column=0)

# Add The Images To Pull-Down Menu 
apod_titles = apod_desktop.get_all_apod_titles()
cbox_image_select = ttk.Combobox(cach_frame, values=apod_titles, state='readonly')
cbox_image_select.set('Select an Image')
cbox_image_select.grid(row=0, column=1, padx=10, pady=10, sticky=SW)

# Add Dates To Pull-Down Menu 

cal = DateEntry(root, selectmode='day')
cal = ttk.Combobox(dwnld_frame, values=cal)
cal.set('Select Date')
cal.grid(row=0, column=1, padx=10, pady=10, sticky=SW)



# Add Widgets To Window.

lbl_name = ttk.Label(cach_frame, text='Select Image:')
lbl_name.grid(row=0, column=0, padx=(10, 5), pady=10)

dwnld_name = ttk.Label(dwnld_frame, text='Select Date')
dwnld_name.grid(row=0, column=0, padx=(10, 5), pady=10)

def set_background():

    image_background = image_lib.set_desktop_background_image(script_path)
    return image_background

def save_image():
    save_apod = image_lib.save_image_file(script_path)
    return save_apod


def handle_set_image_sel(event):

    # Get The Name Of The Selected Image
    image_name = cbox_image_select.get()

    # Download And Save The Artwork For The Selected Pokemon
    global image_path
    image_path = image_lib.download_image(image_name)

    # Display The Pokemon Artwork
    if image_path is not None:
        img_nasa['file'] = image_path
    # Allows Use Of Button    
    btn_get_download(['!disabled'])

cbox_image_select.bind('<<ComboboxSelected>>', handle_set_image_sel)

# Add Buttons To Window.
btn_get_download = ttk.Button(dwnld_frame, text='Download Image', command=save_image)
btn_get_download.grid(row=0, column=2, padx=10, pady=10)

btn_get_set = ttk.Button(cach_frame, text='Set as Desktop', command=set_background, )
btn_get_set.grid(row=0, column=2, padx=10, pady=10)








root.mainloop()