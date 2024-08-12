'''
Team: Joelle Waugh, Manuel Manrique Lopez, Ricardo Rubin, Sadia Shoily

Library of useful functions for working with images.
'''
import requests
import ctypes
import apod_api
import apod_desktop
import os
from PIL import Image
def main():
    # TODO: Add code to test the functions in this module 
    date = apod_desktop.get_apod_date()
    info = apod_api.get_apod_info(date)
    APOD_URL = apod_api.get_apod_image_url(info)
    bind = download_image(APOD_URL)
    save_image_file(bind,"NASA_Logo.png")
    set_desktop_background_image("NASA_logo.png")
    

def download_image(image_url):
    """Downloads an image from a specified URL.

    DOES NOT SAVE THE IMAGE FILE TO DISK.

    Args:
        image_url (str): URL of image

    Returns:
        bytes: Binary image data, if succcessful. None, if unsuccessful.
    """
    # TODO: Complete function body
    print(f'Downloading image from {image_url}...', end='')
    resp_msg = requests.get(image_url)

    # Check if the image was retrieved successfully
    if resp_msg.status_code == requests.codes.ok:
        binData = resp_msg.content
        with Image.open("NASA_logo.png") as img:
            size = img.size
            scale_image(size)
        print('success')
        return binData
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})') 
    return None

def save_image_file(image_data, image_path):
    """Saves image data as a file on disk.
    
    DOES NOT DOWNLOAD THE IMAGE.

    Args:
        image_data (bytes): Binary image data
        image_path (str): Path to save image file

    Returns:
        bool: True, if succcessful. False, if unsuccessful
    """
    # TODO: Complete function body
    try:
        print(f"Saving image file as {image_path}...", end='')
        with open(image_path, 'wb') as file:
            file.write(image_data)
        print("success")
        return True
    except:
        print("failure")
        return False
    

def set_desktop_background_image(image_path):
    """Sets the desktop background image to a specific image.

    Args:
        image_path (str): Path of image file

    Returns:
        bytes: True, if succcessful. False, if unsuccessful        
    """
    # TODO: Complete function body
    print(f"Setting desktop to {image_path}...", end='')
    SPI_SETDESKWALLPAPER = 20
    image_path = os.path.abspath(image_path)
    try:
        if ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3):
            with Image.open(image_path) as img:
                size =img.size
                scale_image(size)
            print("success")
            return True
    except:
        print("failure")
        return False

    

def scale_image(image_size, max_size=(800, 600)):
    """Calculates the dimensions of an image scaled to a maximum width
    and/or height while maintaining the aspect ratio  

    Args:
        image_size (tuple[int, int]): Original image size in pixels (width, height) 
        max_size (tuple[int, int], optional): Maximum image size in pixels (width, height). Defaults to (800, 600).

    Returns:
        tuple[int, int]: Scaled image size in pixels (width, height)
    """
    ## DO NOT CHANGE THIS FUNCTION ##
    # NOTE: This function is only needed to support the APOD viewer GUI
    resize_ratio = min(max_size[0] / image_size[0], max_size[1] / image_size[1])
    new_size = (int(image_size[0] * resize_ratio), int(image_size[1] * resize_ratio))
    return new_size

if __name__ == '__main__':
    main()