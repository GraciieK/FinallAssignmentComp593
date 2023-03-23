import requests


'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
# NASA API KEY 3CGbIof8JmN09qviOquCUSy8oVEpHqmsMpeEyo3G
#?  https://api.nasa.gov/planetary/apod?api_key=3CGbIof8JmN09qviOquCUSy8oVEpHqmsMpeEyo3G  



def main():
    # TODO: Add code to test the functions in this module
    
    get_apod_info()
    
    return






def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    apod_image_url = f'https://api.nasa.gov/planetary/apod'
    api_params = {'date': '1994-09-26',
                  'thumbs': 'True',
                  'api_key': '3CGbIof8JmN09qviOquCUSy8oVEpHqmsMpeEyo3G'}
    

    resp_msg = requests.get(api_params, params=api_params)
    body_dict = resp_msg.text
    
    if resp_msg.status_code == requests.codes.ok:
        print('Sucesss')
        return body_dict
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
    return

if __name__ == '__main__':
    main()