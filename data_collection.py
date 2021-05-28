# all imports
import os
import exceptions
import tweepy
from dotenv import load_dotenv

# load environment variables
load_dotenv()
APP_KEY = os.environ['API_KEY']
APP_SECRET = os.environ['API_SECRET_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# API connection
auth = tweepy.OAuthHandler(APP_KEY, APP_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def verify_user(screen_name):
    try:
        user = api.get_user(screen_name=screen_name)
        print('verified user')
        return user
    except tweepy.TweepError as e:
        if e.args[0][0]['code'] == 50:
            raise(exceptions.InvalidUser(screen_name))
    except:
        raise(exceptions.ApiError)

def get_timeline(screen_name, pages):
    res = []
    for page in tweepy.Cursor(api.user_timeline, screen_name=screen_name, count=200).pages(pages):
        for tweet in page:
            res.append(tweet)
    print('fetched tweets')
    return res

def get_liked(screen_name, pages):
    res = []
    for page in tweepy.Cursor(api.favorites, screen_name=screen_name, count=200).pages(pages):
        for each_like in page:
            res.append(each_like)
    print('fetched likes')
    return res

def add_record(user_scores, screen_name, type):
    if screen_name in user_scores.keys():
        user_scores[screen_name][type] +=1
        return user_scores
    else:
        user_scores.update({screen_name: {
            'likes': 0,
            'retweets': 0,
            'replies': 0
        }})
        return user_scores

def get_scores(screen_name, pages):
    timeline = get_timeline(screen_name, pages)
    likes = get_liked(screen_name, pages)
    user_scores = {}
    for tweet in timeline:
        if tweet.in_reply_to_screen_name and tweet.in_reply_to_screen_name != screen_name:
            user_scores = add_record(user_scores, tweet.in_reply_to_screen_name, 'replies')
        if hasattr(tweet, 'retweeted_status') and tweet.retweeted_status.user.screen_name != screen_name:
            user_scores = add_record(user_scores, tweet.retweeted_status.user.screen_name, 'retweets')
    print('calculated replies and retweets')

    for like in likes:
        if like.user.screen_name != screen_name:
            user_scores = add_record(user_scores, like.user.screen_name, 'likes')
    print('calculated likes')
    return user_scores

def select_users(user_scores):
    tmp_dict = {}
    for user in user_scores:
        total = user_scores[user]['likes']*1 + user_scores[user]['replies']*1.1 + user_scores[user]['replies']*1.3
        tmp_dict.update({user: total})
    sorted_dict = dict(sorted(tmp_dict.items(), key=lambda x:x[1]))
    pairs = list(sorted_dict.items())
    selected_users = []
    for i in range(len(pairs)-1, len(pairs)-50, -1):
        try:
            selected_users.append(pairs[i])
        except:
            raise(exceptions.InactiveUser)
    print('sorted users')
    return dict(selected_users)

def get_avatar_urls(selected_users):
    users_list = [user for user in selected_users.keys()]
    res = api.lookup_users(screen_names=users_list, include_entities=False)
    avatars = {}
    for user in res:
        avatars.update({user.screen_name : user.profile_image_url_https.replace('_normal', '_400x400')})
    print('fetched all avatar urls')
    return avatars

def combine_avatars(selected_users, avatars):
    for user in selected_users:
        selected_users[user] = {
            'score' : selected_users[user],
            'avatar' : avatars[user]
        }
    print('seleted usrs updated with avatar urls')
    return selected_users

def define_layers(selected_users, layers_config):
    selected_users_list = list(selected_users.keys())
    users_in_circles = {}
    for config in layers_config:
        starting_index = config['starting_index']
        ending_index = config['ending_index']
        config.pop('starting_index')
        config.pop('ending_index')
        users = {}
        for user in selected_users:
            if selected_users_list.index(user) >= starting_index and selected_users_list.index(user) < ending_index:
                users.update({user: selected_users[user]})
            else:
                pass
        config.update({'users': users})
        users_in_circles.update({f'circle{layers_config.index(config)}': [username for username in users]}) #list comprehension
    print('defined layers')
    print('created users dict')
    return [layers_config, users_in_circles]

def get_data(screen_name, pages, layers_config):
    user = verify_user(screen_name)
    avatar_url = user.profile_image_url_https.replace('normal', '400x400')
    scores = get_scores(screen_name, pages)
    selected_users = select_users(scores)
    selected_avatars = get_avatar_urls(selected_users)
    selected_users = combine_avatars(selected_users, selected_avatars)
    layers_config, users_in_circles = define_layers(selected_users, layers_config)
    return [avatar_url, layers_config, users_in_circles]