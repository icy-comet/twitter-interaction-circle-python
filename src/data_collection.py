# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# all imports
import json
import functools
from os import getenv
import tweepy
from dotenv import load_dotenv
from src.constants import *
import src.exceptions

# populate values from local environment file
load_dotenv()
BEARER_TOKEN = getenv("TWITTER_BEARER_TOKEN", None)


# API connection
auth = tweepy.OAuth2BearerHandler(BEARER_TOKEN)
api = tweepy.API(auth, wait_on_rate_limit=True)


def verify_user(screen_name: str) -> tweepy.User:
    """Verify if the given Twitter username exists.
    It also helps in getting the username casing right.

    Parameters
    ----------
    screen_name : str
        The username to verify.

    Returns
    -------
    tweepy.User
        The parsed user object returned by the Tweepy.

    Raises
    ------
    exceptions.ApiError
        if there's a problem with the API.
    """

    try:
        user = api.get_user(screen_name=screen_name, include_entities=False)
        print("verified user")
        return user
    except tweepy.TweepError as e:
        if e.args[0][0]["code"] == 50:
            raise (src.exceptions.InvalidUser(screen_name))
    except:
        raise (src.exceptions.ApiError)


def get_timeline(screen_name: str, pages_count: int) -> list[tweepy.Tweet]:
    """Fetch a list of tweets posted by the given user inclusing replies and retweets.

    Parameters
    ----------
    screen_name : str
        Twitter username to get tweets of.
    pages_count : int
        Number of pages to fetch from the Twitter API. Each page can return 200 tweets max.

    Returns
    -------
    list[tweepy.Tweet]
        List of tweets posted by the user.
    """

    res = []
    for page in tweepy.Cursor(
        api.user_timeline, screen_name=screen_name, count=200
    ).pages(pages_count):
        for tweet in page:
            res.append(tweet)
    print("fetched tweets")
    return res


def get_liked(screen_name: str, pages_count: int) -> list[tweepy.Tweet]:
    """Fetch a list of tweets liked by the given user.

    Parameters
    ----------
    screen_name : str
        Twitter username to get likes of.
    pages_count : int
        Number of pages to fetch from the Twitter API.
        Each page can return 200 tweets max.

    Returns
    -------
    list[tweepy.Tweet]
        List of tweets liked by the given user.
    """

    res = []
    for page in tweepy.Cursor(
        api.get_favorites, screen_name=screen_name, count=200
    ).pages(pages_count):
        for each_like in page:
            res.append(each_like)
    print("fetched likes")
    return res


def update_ledger(
    screen_name: str, type_: Interaction, ledger: InteractionsLedger
) -> InteractionsLedger:
    """Initialize and/or update a record for the interaction count in the passed-in ledger.

    Parameters
    ----------
    screen_name : str
        Username to update.
    type_ : Interaction
        Interaction type to increment.
    ledger : InteractionsLedger
        Existing ledger to update.

    Returns
    -------
    InteractionsLedger
        Updated ledger.
    """

    if not screen_name in ledger.keys():
        ledger.update(
            {
                screen_name: {
                    Interaction.like: 0,
                    Interaction.retweet: 0,
                    Interaction.reply: 0,
                }
            }
        )

    ledger[screen_name][type_] += 1
    return ledger


def get_interactions_ledger(
    screen_name: str, timeline: list[tweepy.Tweet], likes: list[tweepy.Tweet]
) -> InteractionsLedger:
    """Calculate the number of each interaction type with a user.

    Parameters
    ----------
    screen_name : str
        Username to analyze for.
    timeline : tweepy.Tweet
        List of all the tweets posted by the given user. Including replies and retweets.
    likes : list[tweepy.Tweet]
        List of all the tweets liked by the user.

    Returns
    -------
    InteractionsLedger
        Dictionary of users describing the count of each interaction type.
    """

    ledger: InteractionsLedger = {}
    for tweet in timeline:
        if (
            tweet.in_reply_to_screen_name
            and tweet.in_reply_to_screen_name != screen_name
        ):
            ledger = update_ledger(
                tweet.in_reply_to_screen_name, Interaction.reply, ledger
            )
        if (
            hasattr(tweet, "retweeted_status")
            and tweet.retweeted_status.user.screen_name != screen_name
        ):
            ledger = update_ledger(
                tweet.retweeted_status.user.screen_name, Interaction.retweet, ledger
            )

    print("calculated replies and retweets")

    for like in likes:
        if like.user.screen_name != screen_name:
            ledger = update_ledger(like.user.screen_name, Interaction.like, ledger)
    print("calculated likes")
    return ledger


def filter_ledger(ledger: InteractionsLedger, needed_count: int) -> FilteredLedger:
    """Sort and pick necessary users based on their total score.

    Parameters
    ----------
    ledger : InteractionsLedger
        The complete InteractionsLedger constructed by drilling through the API data.
    needed_count : int
        Maximum number of users required to create the image. Essentially, sum of number of users in each layer.

    Returns
    -------
    FilteredLedger
        A list of dictionaries describing the username and the associated score.
    """

    tmp_arr: FilteredLedger = []
    for username in ledger:
        total = (
            ledger[username][Interaction.like]
            + (ledger[username][Interaction.retweet] * 1.1)
            + (ledger[username][Interaction.reply] * 1.3)
        )
        tmp_arr.append({"username": username, "score": total})

    tmp_arr.sort(key=lambda x: x["score"], reverse=True)

    return tmp_arr[:needed_count]


def update_ledger_avatars(filtered_ledger: FilteredLedger) -> FilteredLedger:
    """Grab the profile pic URL from Twitter API of each user in the ledger.

    Parameters
    ----------
    filtered_ledger : FilteredLedger
        A list of dictionaries describing the user. Shouldn't exceed more than 100 users to fit the Twitter API limit in current implementation.

    Returns
    -------
    FilteredLedger
        The same list passed-in updated with avatar URLs.
        Looks like this: [{"username": "", "score": 0, "avatar_url": ""}]
    """

    res = api.lookup_users(
        screen_name=[x["username"] for x in filtered_ledger], include_entities=False
    )
    avatar_ledger: AvatarLedger = {}
    for user in res:
        avatar_ledger.update(
            {
                user.screen_name: user.profile_image_url_https.replace(
                    "_normal", "_400x400"
                )
            }
        )
    print("fetched all avatar urls")

    for user in filtered_ledger:
        # handle error if we encounter a deleted account
        if not user["username"] in avatar_ledger:
            url = None
        else:
            url = avatar_ledger[user["username"]]
        user.update({"avatar_url": url})

    return filtered_ledger


def collect_data(
    screen_name: str,
    timeline_pages_count: int,
    favorites_pages_count: int,
    layer_config: LayerConfig,
) -> FilteredLedger:
    """Weave together all the helper functions to return the final ledger for creating the LayerConfig.

    Parameters
    ----------
    screen_name : str
        Twitter username to analyze.
    timeline_pages_count : int
        Number of timeline pages to fetch.
    favorites_pages_count : int
        Number of favorites/likes pages to fetch.
    layer_config : LayerConfig
        The constant part of the layer config.

    Returns
    -------
    FilteredLedger
        The final data structure to be used to build LayerConfig.
    """

    user = verify_user(screen_name)
    # Twitter API doesn't consider usernames case-sensitive
    # johndoe will match to JohnDoe and be verified by the Twitter API
    screen_name = user.screen_name

    center_user = {
        "username": screen_name,
        "avatar_url": user.profile_image_url_https.replace("normal", "400x400"),
    }

    timeline = get_timeline(screen_name, timeline_pages_count)
    likes = get_liked(screen_name, favorites_pages_count)

    data_ledger = filter_ledger(
        get_interactions_ledger(screen_name, timeline, likes),
        # sum of all users in the layer config - the central one
        functools.reduce(lambda acc, curr: acc + curr[1], layer_config, 0) - 1,
    )

    data_ledger = update_ledger_avatars(data_ledger)

    # costly operation
    # will extend be more efficient?
    data_ledger.insert(0, center_user)

    return data_ledger
