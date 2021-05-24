# all imports
import os
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
        return user
    except tweepy.TweepError as e:
        if e.args[0][0]['code'] == 50:
            print('User Not Found')
            return None
    except:
        print("couldn't connect to the api and verify the screen_name")
        return None

def get_timeline(screen_name):
    res = []
    for page in tweepy.Cursor(api.user_timeline, screen_name=screen_name, count=200).pages(6): #fetches 1200 tweets
        for tweet in page:
            res.append(tweet)
    print('Fetched the entire timeline')
    return res

def get_liked(screen_name):
    res = []
    for page in tweepy.Cursor(api.favorites, screen_name=screen_name, count=200).pages(6):
        for each_like in page:
            res.append(each_like)
    print('Fetched all likes')
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

def get_scores(screen_name):
    timeline = get_timeline(screen_name)
    likes = get_liked(screen_name)
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
        selected_users.append(pairs[i])
    print('sorted dict according to the total')
    return dict(selected_users)

def get_selected_avatars(selected_users):
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
    print('avatar urls added to the selected users dictionary')
    return selected_users

def get_data(screen_name):
    user = verify_user(screen_name)
    if user != None:
        avatar_url = user.profile_image_url_https.replace('normal', '400x400')
        scores = get_scores(screen_name)
        selected_users = select_users(scores)
        selected_avatars = get_selected_avatars(selected_users)
        selected_users = combine_avatars(selected_users, selected_avatars)
        return [avatar_url, selected_users]
    else:
        return None