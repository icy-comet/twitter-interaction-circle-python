![Example](circle.jpg)

## Introduction
A python recreation of the popular [Node based project](https://github.com/duiker101/twitter-interaction-circles) behind Chirpty.

It analyzes your timeline to find people you most interact with.

## Setup
### Install Requirements
After creating a virtual environment, simply run:
```
pip install -r requirements.txt
```

### Loading API keys
The script looks for them in environment variables.

If using on a local machine, place the keys inside a `.env` file in the project's directory and you should be good to go. Example:

```
API_KEY=AAAAAA
API_SECRET_KEY=BBBB
ACCESS_TOKEN=CCCCC
ACCESS_TOKEN_SECRET=CCCCC
```

### Limiting Data
By default, the script fetches 1200 tweets from your timeline. To change it, change the number of pages to fetch in `Cursor.pages()`.

Note: Each page consists of 200 tweets.

### Run
Running would be as simple as `python main.py`.