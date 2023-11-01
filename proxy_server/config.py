import os
import re

from dotenv import load_dotenv

load_dotenv()

PROXY_HOST = os.getenv('PROXY_HOST', 'http://127.0.0.1')

PROXY_PORT = os.getenv('PROXY_PORT', 9097)

TARGET_URL = os.getenv('TARGET_URL', 'https://news.ycombinator.com/')
