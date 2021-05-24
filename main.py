from image import create_image
from data import get_data

screen_name = 'AniketTeredesai'

def start(screen_name):
    user_avatar_url, data = get_data(screen_name)
    if data:
        create_image(user_avatar_url, selected_users=data)
    else:
        print('quitting...')

start(screen_name)