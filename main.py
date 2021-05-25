from image import create_image
from data import get_data

screen_name = 'AniketTeredesai'

def start(screen_name):
    user_avatar_url, layers_config = get_data(screen_name)
    if layers_config:
        create_image(user_avatar_url, layers_config)
    else:
        print('quitting...')

start(screen_name)