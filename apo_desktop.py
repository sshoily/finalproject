""" 
Team: Joelle Waugh, Manuel Manrique Lopez, Ricardo Rubin, (Sadia Shoily)

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
import sys
import sqlite3
import hashlib
import requests
import re
import apod_api


# Full paths of the image cache folder and database
# - The image cache directory is a subdirectory of the specified parent directory.
# - The image cache database is a sqlite database located in the image cache directory.
script_dir = os.path.dirname(os.path.abspath(__file__))
image_cache_dir = os.path.join(script_dir, 'images')
image_cache_db = os.path.join(image_cache_dir, 'image_cache.db')



def main():
    ## DO NOT CHANGE THIS FUNCTION ##
    # Get the APOD date from the command line
    apod_date = get_apod_date()    
    

    # Initialize the image cache
    init_apod_cache()

    # Add the APOD for the specified date to the cache
    apod_id = add_apod_to_cache(apod_date)
    print(apod_id)
    # Get the information for the APOD from the DB
    apod_info = get_apod_info(apod_id)

    # Set the APOD as the desktop background image
    if apod_id != 0:
        image_lib.set_desktop_background_image(apod_info['file_path'])

def get_apod_date():
    """Gets the APOD date
     
    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    date_today = date.today()
    if len(sys.argv) >= 2:
        apod_date = sys.argv[1]
        try :
            apod_date = date.fromisoformat(apod_date)
            if apod_date > date_today:
                print("Please enter a date that is more recent.") # TODO: Proper Error Message
                sys.exit(1)
                
            elif apod_date < date.fromisoformat("1995-06-16"):
                print("Please enter a date that is before 1995-06-16.") # TODO: Proper Error Message
                sys.exit(1)
            else:
                return apod_date
        except:
            print("Please enter a valid date.") # TODO: Proper Error Message
            sys.exit(1)
    else:
        return date_today
    

def init_apod_cache():
    """Initializes the image cache by:
    - Creating the image cache directory if it does not already exist,
    - Creating the image cache database if it does not already exist.
    """
    # TODO: Create the image cache directory if it does not already
    print(f"Image cache directory: {image_cache_dir}")
        # {REQ-14} {REQ-15} Create directory
    if os.path.isdir(image_cache_dir):
        print(f"image_cache_directory:{image_cache_dir} already exists.")       
    else:           
        print(f"Images cache directory:{image_cache_dir} created.")
        os.mkdir(image_cache_dir)

    # Database
    if os.path.isfile(image_cache_db):
        print(f"Images cache DB:{image_cache_db}")
        print ("Image cache DB already exists.")
    else:
        # {REQ-11}
        print(f"image_cache_db:{image_cache_db}")
        

    # TODO: Create the DB if it does not already exist
     
        con = sqlite3.connect('image_cache.db')
        cur = con.cursor()
        image_query = """
        CREATE TABLE IF NOT EXISTS Image
        (
            id          INTEGER PRIMARY KEY,
            title       TEXT NOT NULL,
            explanation TEXT NOT NULL,
            file_path   TEXT NOT NULL,
            Sha256     TEXT NOT NULL
        );
        """
        cur.execute(image_query)
        con.commit()
        con.close()
    #else:
        #print(f"Image cache database already exists.")
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
    print("APOD date:", apod_date.isoformat())
    # TODO: Download the APOD information from the NASA API
    # Hint: Use a function from apod_api.py
    apod_info = apod_api.get_apod_info(apod_date)

    # TODO: Download the APOD image
    # Hint: Use a function from image_lib.py 
    apod_image = image_lib.download_image(apod_api.get_apod_image_url(apod_info))
    respmsg = requests.get(apod_api.get_apod_image_url(apod_info))

    if respmsg.status_code == requests.codes.ok:
        content= respmsg.content

        hashvalue = hashlib.sha256(content).hexdigest()

    # TODO: Check whether the APOD already exists in the image cache
    # Hint: Use the get_apod_id_from_db() function below
    apod_id = get_apod_id_from_db(hashvalue)
    

    # TODO: Save the APOD file to the image cache directory
    # Hint: Use the determine_apod_file_path() function below to determine the image file path
    # Hint: Use a function from image_lib.py to save the image file
    if apod_id == 0:
        image_path = determine_apod_file_path(apod_info['file_path'],apod_info['file_path'])
        apod_id = add_apod_to_db(apod_info ['title'],apod_info['explanation'], image_path, hashvalue)
        image_lib.save_image_file(apod_image,image_path)
    # TODO: Add the APOD information to the DB
    # Hint: Use the add_apod_to_db() function below
    
        add_apod_to_cache(apod_date)
        return apod_id
    
    elif apod_id !=0:
        return apod_id
    return 0
    


def add_apod_to_db(title, explanation, file_path, sha256):
    """Adds specified APOD information to the image cache DB.
     
    Args:
        title (str): Title of the APOD image
        explanation (str): Explanation of the APOD image
        file_path (str): Full path of the APOD image file
        sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: The ID of the newly inserted APOD record, if successful. Zero, if unsuccessful       
    """
    # TODO: Complete function body
    

    con = sqlite3.connect(image_cache_db)
    cur= con.cursor()

    apod_image_query= """
        INSERT INTO Images Cache
        (      
            title,
            explanation,
            file_path,
            Sha256,
        )
            VALUES (?,?,?,?);
    """
    new_image = (
                title,
                explanation,
                file_path,
                sha256
            )
    
    cur.execute(apod_image_query, new_image)

    cur.execute('SELECT * FROM Imagecache')

    all_image = cur.fetchall()
    print(all_image)
    con.commit()
    con.close()

    return 0
    

def get_apod_id_from_db(image_sha256):
    """Gets the record ID of the APOD in the cache having a specified SHA-256 hash value
    
    This function can be used to determine whether a specific image exists in the cache.

    Args:
        image_sha256 (str): SHA-256 hash value of APOD image

    Returns:
        int: Record ID of the APOD in the image cache DB, if it exists. Zero, if it does not.
    """
    # TODO: Complete function body
    
    #resp_msg = requests.get(image_sha256)
    
    con = sqlite3.connect(image_cache_db)
    cur =con.cursor()
    cur.execute("SELECT id FROM apod WHERE sha256 = ?", (image_sha256,))

    apod_id = cur.fetchone()
    
    con.close()
    if apod_id is not None:
        return apod_id[0]
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
    # TODO: Complete function body
    # Hint: Use regex and/or str class methods to determine the filename.
    image_file_regex = r"[^a-zA-Z0-9\s]"

    #strip down the file name to and extension
    file_extension = image_url.split('.')[-1]

    file_name =image_title.strip.replace(" "," _")

    file_name = re.sub(image_file_regex,"",file_name)

    file_path = os.path.join(image_cache_dir, f"{file_name}. {file_extension}") 
    
    return file_path
          
   


def get_apod_info(image_id):
    """Gets the title, explanation, and full path of the APOD having a specified
    ID from the DB.

    Args:
        image_id (int): ID of APOD in the DB

    Returns:
        dict: Dictionary of APOD information
    """
    # TODO: Query DB for image info
    con = sqlite3.connect('image_cache.db')
    cur = con.cursor()
    """get_apod_info_query = {
        'title': 'Title',
        'explanation' : 'Explanation',
        'file_path': 'File Path',
        'sha256': 'SHA-256'
    }"""
    get_apod_info_query = """
    CREATE TABLE apod
    (
        id          INTEGER PRIMARY KEY,
        title       TEXT NOT NULL,
        explanation TEXT NOT NULL,
        file_path   TEXT NOT NULL,
        sha256      TEXT NOT NULL,
    );
    """
    cur.excute(get_apod_info_query)

    apod_info =cur.fetchall()
    
    con.close()

    return apod_info

def get_all_apod_titles():
    """Gets a list of the titles of all APODs in the image cache

    Returns:
        list: Titles of all images in the cache
    """
    # TODO: Complete function body
    # NOTE: This function is only needed to support the APOD viewer GUI
    con = sqlite3.connect(image_cache_db)
    cur = con.cursor()

    cur.execute(f"SELECT title FROM apod")

    titles =cur.fetchall
    return titles

if __name__ == '__main__':
    main()