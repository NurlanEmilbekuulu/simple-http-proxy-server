import re

from bs4 import BeautifulSoup
from cachetools import LRUCache

from proxy_server.config import PROXY_HOST, PROXY_PORT

SIX_LETTER_WORD_PATTERN = re.compile(r'\b(\w{6})\b')
CACHE = LRUCache(maxsize=100)


async def _fetch_html(url, session):
    """Fetch HTML content asynchronously."""
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.text()


async def _get_html_content(url, session):
    """Get HTML content either from cache or by fetching it."""
    if url in CACHE:
        return CACHE[url]
    html_content = await _fetch_html(url, session)
    CACHE[url] = html_content
    return html_content


def modify_links(soup: BeautifulSoup):
    """Replace links in HTML with a proxy link."""
    for anchor_tag in soup.find_all('a', href=lambda href: href and href.startswith('https://news.ycombinator.com')):
        anchor_tag['href'] = anchor_tag['href'].replace(
            'https://news.ycombinator.com', f'{PROXY_HOST}:{PROXY_PORT}')

    return soup


def add_trademark(soup: BeautifulSoup):
    """Modify text by adding a trademark symbol to all six-letter words in text."""
    for element in soup.find_all(string=True):
        element.replace_with(SIX_LETTER_WORD_PATTERN.sub(r'\1™', str(element)))
    return soup


async def process_html_response(url, session):
    """Process HTML response, modify content and return response."""
    html_content = await _get_html_content(url, session)
    soup = BeautifulSoup(html_content, 'html.parser')
    return str(modify_links(add_trademark(soup)))
