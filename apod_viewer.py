from tkinter import *
from tkinter import ttk
import inspect
import os
import apod_desktop
import image_lib
import ctypes
import sqlite3
from tkcalendar import *
from PIL import Image, ImageTk
import datetime


# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
apod_desktop.init_apod_cache(script_dir)

# TODO: Create the GUI
root = Tk()
root.title('Astronomy Picture of the Day Viewer')
root.geometry('800x600')
root.minsize(800, 600)
root.resizable(True, True)
root.columnconfigure(1, weight=1)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set The Window Icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.ApodImageViewer')
icon_path = os.path.join(script_dir, 'nasa.ico')
root.iconbitmap(icon_path)


#ADD Frames To Window.
frame = ttk.Frame(root)
frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=NSEW)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

cach_frame = ttk.LabelFrame(root, text='View Cached Image')
cach_frame.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)


dwnld_frame = ttk.LabelFrame(root, text='Get More Images')
dwnld_frame.grid(row=1, column=1, padx=10, pady=10, sticky=NSEW)


# Add The Image To The Frame
nasa_icon_path = ImageTk.PhotoImage(Image.open(os.path.join(script_dir,'nasa_icon.png')))
lbl_img_nasa = ttk.Label(frame, image=nasa_icon_path)
lbl_img_nasa.grid(row=0, column=0)

# Add The Images To Pull-Down Menu 
apod_titles = apod_desktop.get_all_apod_titles()
cbox_image_select = ttk.Combobox(cach_frame, values=apod_titles, state='readonly')
cbox_image_select.set('Select an Image')
cbox_image_select.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

# Add Dates To Pull-Down Menu 
cal_apod = DateEntry(dwnld_frame, date_pattern='yyyy-mm-dd', mindate=datetime.date(1995,6,16), maxdate=datetime.date.today())
cal_apod.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)


# Add explanation to frame.
explanation_text = ttk.Label(frame, text=None, wraplength=1000)
explanation_text.grid(row=1, column=0, padx=10, pady=10, sticky=S)

# Add Widgets To Window.

lbl_name = ttk.Label(cach_frame, text='Select Image:')
lbl_name.grid(row=0, column=0, padx=10, pady=10)

dwnld_name = ttk.Label(dwnld_frame, text='Select Date')
dwnld_name.grid(row=0, column=0, padx=10, pady=10)

def set_background():
    image_lib.set_desktop_background_image(full_path) 

def handle_set_image_sel(event):

    # Get The Name Of The Selected Image
    image_name = cbox_image_select.get()
    # Get the file path and explanation from the title.
    database = apod_desktop.image_cache_db
    con = sqlite3.connect(database)
    cur = con.cursor()
    query = """
            SELECT full_path, explanation FROM apod_image_cache 
            WHERE title =?
            """
    cur.execute(query, (image_name,))
    query_results = cur.fetchone()
    con.close()
    
    global full_path
    full_path = query_results[0]
    explanation = query_results[1]


    set_image(full_path, explanation, image_name)
   
cbox_image_select.bind('<<ComboboxSelected>>', handle_set_image_sel)
    

def get_apod_date():
    apod_date = cal_apod.get_date().strftime('%Y-%m-%d')

    apod_info = apod_desktop.add_apod_to_cache(apod_date)
    apod_dict = apod_desktop.get_apod_info(apod_info)

    global full_path
    full_path = apod_dict['full_path']
    explanation = apod_dict['explanation']
    title = apod_dict['title']
    apod_titles.append(title)
    cbox_image_select['values'] = apod_titles

    set_image(full_path, explanation, title)


def set_image(path, explanation, title):


    global full_path
    main_image = Image.open(path)
    main_image.thumbnail((1000, 700))
    apod_image = ImageTk.PhotoImage(main_image)
    lbl_img_nasa.configure(image=apod_image)
    lbl_img_nasa.image = apod_image
    explanation_text.configure(text=explanation)
    

    if title is not None:
        cbox_image_select.set(title)


# Add Buttons To Window.
btn_get_download = ttk.Button(dwnld_frame, text='Download Image', command=get_apod_date)
btn_get_download.grid(row=0, column=2, padx=10, pady=10)

btn_get_set = ttk.Button(cach_frame, text='Set as Desktop', command=set_background)
btn_get_set.grid(row=0, column=2, padx=10, pady=10)


root.mainloop()