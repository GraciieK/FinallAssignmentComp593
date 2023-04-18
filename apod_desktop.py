

""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py [apod_date]

Parameters:
  apod_date = APOD date (format: YYYY-MM-DD)
"""
from datetime import date
import os
import image_lib
import apod_api
import inspect
from sys import argv, exit
import sqlite3
import hashlib

# Global variables
image_cache_dir = None  # Full path of image cache directory
image_cache_db = None   # Full path of image cache database

def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    

    # # Get the path of the directory in which this script resides
    script_dir = get_script_dir()

    # # Initialize the image cache
    init_apod_cache(script_dir)

    # # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)

    # # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['full_path'])
        

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    
    # Complete function body
    apod_date = None

    # Checks for how many params then checks dates valid. 
    if len(argv) == 1:
        apod_date = date.today()
       
    if len(argv) >= 3:
        print('Error: To many peramitors. Please print date in YYYY-MM-DD Format.')
        exit() 

    if len(argv) == 2:
        try: 
            apod_date = date.fromisoformat(argv[1]) 
        except:
            print('Error: Not in YYYY-MM-DD format.')
            exit()
        if apod_date < date(1995,6,16):
            print('Error: APOD Date is invalid. Please provide a date between 1995-06-16 and today\'s date.')
            exit()
        elif apod_date > date.today():
            print('Error: APOD Date is invalid. Please provide a date between 1995-06-16 and today\'s date.')
            exit()   
        
    return apod_date


def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    
    ## DO NOT CHANGE THIS FUNCTION ##
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

def init_apod_cache(parent_dir):
    """Initializes the image cache by:
    - Determining the paths of the image cache directory and database,
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    
    The image cache directory is a subdirectory of the specified parent directory.
    The image cache database is a sqlite database located in the image cache directory.

    Args:
        parent_dir (str): Full path of parent directory    
    """
    
    global image_cache_dir
    global image_cache_db

    image_cache_dir = os.path.join(parent_dir, 'APODImages')
    image_cache_db = os.path.join(image_cache_dir, 'APODImage.db')

    # Checks if dir exists.
    if os.path.exists(image_cache_dir):
        print(f'Image cache directory: {image_cache_dir}')
        print('Image cahce directory already exists.')

    # Makes dir if it does not exists.
    elif os.mkdir(image_cache_dir):
        print(f'Image cache directory: {image_cache_dir}')
        print('Created APOD Image Directory.')

    # Checks if db exists.
    if os.path.exists(image_cache_db):
        print(f'Image cache DB: {image_cache_db}')
        print('Image cache DB already exists.')

    # Makes db if it does not exists.
    else:
        con = sqlite3.connect(image_cache_db)
        cur = con.cursor()
        create_apod_table = """
                CREATE TABLE IF NOT EXISTS apod_image_cache
                (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    explanation TEXT NOT NULL,
                    full_path TEXT NOT NULL,
                    sha256 TEXT NOT NULL
                );          
        """
        cur.execute(create_apod_table)
        con.commit()
        con.close()
        print('Created APOD Image Cache Database:' + image_cache_db)

    return   
    

def add_apod_to_cache(apod_date):
    """Adds the APOD image from a specified date to the image cache.
     
    The APOD information and image file is downloaded from the NASA API.
    If the APOD is not already in the DB, the image file is saved to the 
    image cache and the APOD information is added to the image cache DB.

    Args:
        apod_date (date): Date of the APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if a new APOD is added to the
        cache successfully or if the APOD already exists in the cache. Zero, if unsuccessful.
    """
    
    print(f'APOD date: {apod_date}.')

    # Downloads the APOD information from the NASA API.
    apod_info = apod_api.get_apod_info(apod_date)
    explanation = apod_info['explanation']
    title = apod_info['title']
    print(f'APOD title: {title}')

    # Downloads the APOD image.
    image_url = apod_api.get_apod_image_url(apod_info)
    print(f'APOD URL: {image_url}')
    image_data = image_lib.download_image(image_url)
    
    # Checks whether the APOD already exists in the image cache.
    sha256 = hashlib.sha256(image_data).hexdigest()
    apod_check_sha = get_apod_id_from_db(sha256)
    print(f'APOD SHA-256: {sha256}')
    
    if apod_check_sha != 0:
        print('APOD image is already in cache.')
        return apod_check_sha

    # Saves the APOD file to the image cache directory.
    elif apod_check_sha ==0:    
        print('APOD image is not already in cache.')
        image_path = determine_apod_file_path(title, image_url)
        image_lib.save_image_file(image_data, image_path)

        # Adds the APOD information to the DB.
        add_apod_id = add_apod_to_db(title, explanation, image_path, sha256)
        return add_apod_id
    
    else:
        return 0
    


def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful.  Zero, if unsuccessful       
    """
    
    # Adds Title, Explanation, File_Path, and Sha to db.
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    image_quary ="""
                INSERT INTO apod_image_cache 
                    (
                    title, 
                    explanation,
                    full_path,
                    sha256
                    )
                VALUES (?, ?, ?, ?);
                """
    apod_image_cache = (title, explanation, file_path, sha256)
    cache = cur.execute(image_quary, apod_image_cache)
    con.commit()
    con.close()
    cache_last = cache.lastrowid
    print(f'Adding APOD to image database...', end='')
    if cache_last:
        print('success.')
        return cache_last
    else:
        print('failure.')
        return 0

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    
    # Gets the apod ID from db.
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    query = f"""
            SELECT id FROM apod_image_cache 
            WHERE sha256='{image_sha256}'
            """
    cur.execute(query)
    query_results = cur.fetchone()
    con.close()

    if query_results is not None:
        return query_results[0]

    else:
        return 0

def determine_apod_file_path(image_title, image_url):
    """Determines the path at which a newly downloaded APOD image must be 
    saved in the image cache. 
    
    The image file name is constructed as follows:
    - The file extension is taken from the image URL
    - The file name is taken from the image title, where:
        - Leading and trailing spaces are removed
        - Inner spaces are replaced with underscores
        - Characters other than letters, numbers, and underscores are removed

    For example, suppose:
    - The image cache directory path is 'C:\\temp\\APOD'
    - The image URL is 'https://apod.nasa.gov/apod/image/2205/NGC3521LRGBHaAPOD-20.jpg'
    - The image title is ' NGC #3521: Galaxy in a Bubble '

    The image path will be 'C:\\temp\\APOD\\NGC_3521_Galaxy_in_a_Bubble.jpg'

    Args:
        image_title (str): APOD title
        image_url (str): APOD image URL
    
    Returns:
        str: Full path at which the APOD image file must be saved in the image cache directory
    """
    
    # Changed the title of the file_name to specifications.
    global file_path

    image_extention = os.path.splitext(image_url)[1]
    image_title = image_title.strip().replace(' ', '_')
    image_title = ''.join(i for i in image_title if i.isalnum() or i == '_')
    file_name = image_title + image_extention
    file_path = os.path.join(image_cache_dir, file_name)
   
    return file_path

def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    
    # Querys DB for image info.
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    apod_dict = f"""SELECT title, explanation, full_path FROM apod_image_cache WHERE id='{image_id}'"""
    cur.execute(apod_dict)
    query_results = cur.fetchone()
    con.close()

    # Puts information into a dictionary.
    apod_info_dict = {
        'title': query_results[0], 
        'explanation': query_results[1],
        'full_path': query_results[2]
    }

    return apod_info_dict

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    
    # Lists all apod titles for GUI.
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()
    apod_query_title = """ SELECT title FROM apod_image_cache"""
    cur.execute(apod_query_title)
    query_title_results = [row[0] for row in cur.fetchall()]
    con.close()

    if query_title_results is not None:
        return query_title_results
    
    return None

if __name__ == '__main__':
    main()