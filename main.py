import json
from image_creation import create_image
from data_collection import get_data
# from encoding import encode

screen_name = 'AniketTeredesai' #twitter username

layers_config= [{'radius': 150, 'starting_index': 0, 'ending_index': 8},
                {'radius': 270, 'starting_index': 8, 'ending_index': 23},
                {'radius': 380, 'starting_index': 23, 'ending_index': 60}]

background_color = '#2978b5' #background color of the image produced

pages_to_fetch = 3 #each page consists of 200 tweets and 20 likes

def start(screen_name, pages, color, layers_config):
    api_data = get_data(screen_name, pages, layers_config)
    if api_data:
        user_avatar_url, layers_config, users_in_circles = api_data
        image = create_image(user_avatar_url, color, layers_config)
        with open(f'{screen_name}_circles.json', 'w') as f:
            json.dump(users_in_circles, f)
        print('users list saved as json')
        image.save(f'{screen_name}_interaction_circle.jpg')
        # base64_image = encode(image)
    else:
        print('Above error occurred. quitting...')

start(screen_name, pages_to_fetch, background_color, layers_config)