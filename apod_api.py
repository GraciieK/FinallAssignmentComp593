import requests
import json


'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''

apod_date = '2022-01-10'

def main():

    info = get_apod_info(apod_date)
    print(get_apod_image_url(info))
    

def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    apod_info_url = f'https://api.nasa.gov/planetary/apod'
    api_params = {
                'date': apod_date,
                'thumbs': 'True',
                'api_key': '3CGbIof8JmN09qviOquCUSy8oVEpHqmsMpeEyo3G'
            }
    resp_msg = requests.get(apod_info_url, params=api_params)
    apod_info_dict = resp_msg.json()
    
    if resp_msg.status_code == requests.codes.ok:
        print('Sucesss')
        return apod_info_dict
    else:
        print('Failed')
        print(f'{resp_msg.status_code} ({resp_msg.reason})')
        print(f'Error: {resp_msg.text}')
    return 



def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info from API

    Returns:
        str: APOD image URL
    """

    if apod_info_dict['media_type'] == 'image':
        apod_image_url = apod_info_dict['hdurl']
        return apod_image_url
    elif apod_info_dict['media_type'] == 'video':
        apod_image_url = apod_info_dict['thumbnail_url']
        return apod_image_url
 

if __name__ == '__main__':
    main()