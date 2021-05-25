from image import create_image
from data import get_data

screen_name = 'AniketTeredesai' #twitter username

layers_config= [{'image_count': 8, 'radius': 150, 'starting_index': 0, 'ending_index': 8},
                {'image_count': 15, 'radius': 270, 'starting_index': 8, 'ending_index': 23},
                {'image_count': 26, 'radius': 380, 'starting_index': 23, 'ending_index': 60}]

background_color = '#2978b5' #background color of the image produced

pages_to_fetch = 3 #each page consists of 200 tweets

def start(screen_name, pages, color, layers_config):
    user_avatar_url, layers_config = get_data(screen_name, pages, layers_config)
    if layers_config:
        create_image(user_avatar_url, color,  layers_config)
    else:
        print('quitting...')

start(screen_name, pages_to_fetch, background_color, layers_config)