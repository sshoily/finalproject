"""Sadia Shoily

Library of useful functions for working with images and setting desktop background.
"""

import requests
import ctypes
import apod_api
import apod_desktop
import os
from PIL import Image

def main():
    """Main function to test the functionality of the module."""
    # Get APOD date and info
    date = apod_desktop.get_apod_date()
    info = apod_api.get_apod_info(date)

    # Fetch the image URL
    apod_url = apod_api.get_apod_image_url(info)

    # Download and save the image
    image_data = download_image(apod_url)
    if image_data:
        image_path = "NASA_Logo.png"
        save_image_file(image_data, image_path)
        set_desktop_background_image(image_path)

def download_image(image_url):
    """
    Downloads an image from the specified URL without saving it to disk.
    
    Args:
        image_url (str): URL of the image to be downloaded.
    
    Returns:
        bytes: Binary data of the image if successful, else None.
    """
    print(f'Downloading image from {image_url}...', end='')
    
    # Perform the HTTP request to download the image
    response = requests.get(image_url)

    if response.status_code == requests.codes.ok:
        print('success')
        image_data = response.content
        
        # Check image size and scale it
        with Image.open("NASA_Logo.png") as img:
            size = img.size
            scale_image(size)
        
        return image_data
    else:
        print(f'failure\nResponse code: {response.status_code} ({response.reason})')
        return None

def save_image_file(image_data, image_path):
    """
    Saves binary image data as a file on the disk.
    
    Args:
        image_data (bytes): The image data to save.
        image_path (str): The file path where the image should be saved.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        print(f"Saving image file as {image_path}...", end='')
        with open(image_path, 'wb') as file:
            file.write(image_data)
        print("success")
        return True
    except Exception as e:
        print(f"failure\nError: {e}")
        return False

def set_desktop_background_image(image_path):
    """
    Sets the desktop wallpaper to a specified image file.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    print(f"Setting desktop to {image_path}...", end='')
    SPI_SETDESKWALLPAPER = 20
    image_path = os.path.abspath(image_path)

    try:
        # Set desktop wallpaper using Windows API
        if ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3):
            print("success")

            # Check image size and scale if needed
            with Image.open(image_path) as img:
                size = img.size
                scale_image(size)
            
            return True
    except Exception as e:
        print(f"failure\nError: {e}")
        return False

def scale_image(image_size, max_size=(800, 600)):
    """
    Calculates and returns the dimensions of the image scaled to a 
    maximum width and height, while maintaining its aspect ratio.
    
    Args:
        image_size (tuple[int, int]): Original image size in pixels (width, height).
        max_size (tuple[int, int], optional): Maximum allowed size for the image (default is 800x600).
    
    Returns:
        tuple[int, int]: Scaled image size in pixels (width, height).
    """
    resize_ratio = min(max_size[0] / image_size[0], max_size[1] / image_size[1])
    new_size = (int(image_size[0] * resize_ratio), int(image_size[1] * resize_ratio))
    return new_size

if __name__ == '__main__':
    main()
