import math, json, urllib.request
from PIL import Image, ImageDraw

# urllib setup (precaution)
opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
urllib.request.install_opener(opener)

def get_user_avatar(avatar_url):
        file, _ = urllib.request.urlretrieve(avatar_url)
        return file

def create_bg():
    mode = 'RGB'
    size = (1000, 1000)
    color = (94, 23, 235)
    bg = Image.new(mode, size, color)
    return bg

def create_mask(image):
    alpha = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([(0, 0), image.size], 0, 360, fill=255)
    return alpha

def create_image(center_avatar_url, selected_users):
    bg = create_bg()
    users_in_circle={}
    print('created background')
    gap = 10
    layers=[{'image_count': 8, 'radius': 150, 'starting_index': 0, 'ending_index': 8},
            {'image_count': 15, 'radius': 270, 'starting_index': 8, 'ending_index': 23},
            {'image_count': 26, 'radius': 380, 'starting_index': 23, 'ending_index': 60}]
    bg_w, bg_h = bg.size
    center_avatar = Image.open(get_user_avatar(center_avatar_url)).convert('RGB')
    center_avatar = center_avatar.resize((160, 160))
    bg.paste(center_avatar, ((bg_w - 160)//2, (bg_h - 160)//2), create_mask(center_avatar))
    print('pasted central avatar')
    for layer in layers:
        image_count = layer['image_count']
        gaps_count = image_count-1
        R = layer['radius']
        circuit = 2*math.pi*R
        diagonal = int((circuit - gaps_count*gap) / image_count)
        no_of_image = 0
        base_angle = 360/layer['image_count']
        users_list = []
        for user in selected_users:
            if list(selected_users.keys()).index(user) >= layer['starting_index'] and list(selected_users.keys()).index(user) < layer['ending_index']:
                users_list.append(user)
                file, _ = urllib.request.urlretrieve(selected_users[user]['avatar'])
                avatar = Image.open(file).convert('RGB')
                h = diagonal
                w = diagonal
                avatar = avatar.resize((h, w))
                angle_x = math.cos(math.radians(base_angle*no_of_image))
                angle_y = math.sin(math.radians(base_angle*no_of_image))
                x = math.ceil(R * angle_x + 445) + (layers.index(layer)*8) #offset to address circles misalignment
                y = math.ceil(R * angle_y + 445) + (layers.index(layer)*8) #offset to address circles misalignment
                bg.paste(avatar, (x, y), create_mask(avatar))
                no_of_image += 1
            else:
                pass
        users_in_circle.update({f'circle-{layers.index(layer)}': users_list})
    bg.save('interaction_circle.jpg')
    print('image created and saved')
    with open('circles.json', 'w') as f:
        json.dump(users_in_circle, f)
    print('saved the circles, too ;)')