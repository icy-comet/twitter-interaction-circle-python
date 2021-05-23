## Introduction
The script analyzes your recent public activity on Twitter and creates a beautiful image with the avatars of people you most interact with.

This is kind of a python recreation of the popular [Node based project](https://github.com/duiker101/twitter-interaction-circles) behind [Chirpty](https://chirpty.com).

## Example Image

![Example](circle.jpg)

## Setup
### Install Requirements
Create a virtual environment with:
```
python -m venv env
```

And then, simply run:
```
pip install -r requirements.txt
```

### Loading API keys
The script looks for the keys in environment variables.

If using on a local machine, place the keys inside a `.env` file in the project's directory and you should be good to go. Example:

```
API_KEY=AAAAAA
API_SECRET_KEY=BBBB
ACCESS_TOKEN=CCCCC
ACCESS_TOKEN_SECRET=CCCCC
```

### Limiting Analyzed Data
By default, the script fetches 1200 tweets from your timeline. To change it, change the number of pages to fetch in `get_timeline` and `get_liked` functions.

Note: Each page consists of 200 tweets.

### Run
Running would be as simple as `python main.py`.