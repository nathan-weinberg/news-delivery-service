# news-delivery-service

## Purpose
See [here](https://nathanweinberg.me/assets/blog/navigating_news.html) for a writeup on why I created this

## Prerequisites
You will need a YouTube API key. To obtain one, follow Google's documentation on the matter: https://developers.google.com/youtube/v3/getting-started

## Setup
Create a file named "config.yaml" based off "config.yaml.example" with the following fields filled in:
- **recipients:**: Email addresses of recipients
- **sender_email:**: Email address of sender
- **sender_password:**: Email password of sender
- **smtp_host**: SMTP host of sender's email
- **youtube_api_key**: Your YouTube API Key

Ensure your "config.yaml" file is in the same directory as "main.py"

### Packages
- [PyYAML](https://pyyaml.org/) for parsing config YAML
- [Jinja2](https://jinja.palletsprojects.com/en/2.10.x/) for generating HTML
- [google-api-python-client](https://github.com/googleapis/google-api-python-client) for interacting with the YouTube v3 API

To install packages run:

`$ pip install -r requirements.txt`

It is recommended you do this within a virtual environment.

## Usage
To run:
- `$ ./main.py` if `/usr/bin/python3` is a valid path
- `$ python3 main.py` otherwise

## Notes
Email code is tailored to specific email servers - it may require modification to work with your setup.
