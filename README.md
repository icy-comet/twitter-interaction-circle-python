## Introduction
The script analyzes your recent public activity on Twitter and creates a beautiful image with the avatars of people you most interact with.

This is kind of a Python recreation of the popular [Node based project](https://github.com/duiker101/twitter-interaction-circles) that powers [Chirpty](https://chirpty.com).

## Example Image

![Example](example.jpg)

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

> For pinned/tested versions use requirements.pinned.txt.

### Loading API keys
The script looks for the keys in environment variables.

If using on a local machine, place the keys inside a `.env` file in the project's directory and you should be good to go. Example:

```
API_KEY=AAAAAA
API_SECRET_KEY=BBBB
```

### Customization
All the customizable variables can be changed inside `main.py` which serves as the calling point.

The script can also return a JSON list of users in each circle and/or return a base64 encoded image instead of saving it as JPEG. Configure it in `main.py`.

Note: The script, by default, fetches 3 pages of data from the Twitter API. Each page consists of 200 tweets and 20 likes. You can set it to fetch upto 3000 tweets as limited by the API.

### Run
Running would be as simple as `python main.py`.
