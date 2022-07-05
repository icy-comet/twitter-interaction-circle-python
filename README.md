## Introduction
Analyze your Twitter public activity and get to know the people you most interact with.

The more you interact with someone, the closer they are in your Twitter circle. Visualize this with an image that you can show-off and a detailed JSON list describing the same.

This is kind of a Python-recreation of the popular [JS-based project](https://github.com/duiker101/twitter-interaction-circles) that powers [Chirpty](https://chirpty.com).

> The user should have atleast one Twitter interaction for this package to work.

## Sample Image

<img src="sample.jpg" width="500" align="center">

## Requirements
- Create a virtual environment and activate it.
  ```bash
  # linux
  python -m venv venv
  source ./venv/bin/activate
  ```
  ```powershell
  # windows
  py -m venv venv
  .\venv\Scripts\activate
  ```
- And then, simply run:
  ```bash
  pip install -r requirements.txt
  ```
  > For pinned/tested versions use requirements.pinned.txt.

## Twitter API Authentication
The package uses OAuth 2.0 App Auth with Twitter API v1.1 and needs a `TWITTER_BEARER_TOKEN` in the system's environment varibales. You can generate one in Twitter's Developer Dashboard.

If using on a local machine, place the keys inside a `.env` file in the project's directory and you should be good to go. Example:

```toml
TWITTER_BEARER_TOKEN=xxxxxx
```

## Customization
`main.py` file serves as the entry point for the package. All the customizable variables have been listed under the `Config` class inside this file.

> Why create this as a package?
> So that a frontend can be adapted around it. I, myself, host a public web-frontend for this package.

## Debugging
Pass `debug=True` to the main function inside the `main.py`. That uses dumped online data in subsequent runs instead of calling the API and uses a dummy avatar image instead of downloading the avatars off of the internet.