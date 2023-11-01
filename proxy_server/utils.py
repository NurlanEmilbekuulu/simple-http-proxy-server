import re
from urllib.parse import urljoin, urlparse, urlunparse

from bs4 import BeautifulSoup, NavigableString
from cachetools import LRUCache

from proxy_server.config import PROXY_HOST, PROXY_PORT, TARGET_URL

SIX_LETTER_WORD_PATTERN = re.compile(r'\b(\w{6})\b')
CACHE = LRUCache(maxsize=100)


def modify_text(text):
    """Modify text by adding trademark symbol to six-letter words."""
    return SIX_LETTER_WORD_PATTERN.sub(r'\1<sup>™</sup>', text)


async def fetch_html(url, session):
    """Fetch HTML content asynchronously."""
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.text()


async def get_html_content(url, session):
    """Get HTML content either from cache or by fetching it."""
    if url in CACHE:
        return CACHE[url]
    html_content = await fetch_html(url, session)
    CACHE[url] = html_content
    return html_content


def modify_text_in_soup(soup):
    """Modify text by adding trademark symbol to six-letter words in HTML soup."""
    body_text_nodes = soup.body.find_all(string=True) if soup.body else []
    for text_node in body_text_nodes:
        if isinstance(text_node, NavigableString):
            parent_tag = text_node.parent
            if parent_tag.name != 'a' and len(text_node.string) >= 6:
                text_node.replace_with(BeautifulSoup(
                    modify_text(text_node), 'html.parser'))


def rewrite_links_in_soup(soup):
    """Rewrite links in HTML soup to go through the proxy."""
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href.startswith(TARGET_URL):
            parsed_href = urlparse(href)
            path_query = urlunparse(
                ('', '', parsed_href.path, '', parsed_href.query, ''))
            a_tag['href'] = urljoin(
                f'{PROXY_HOST}:{PROXY_PORT}', path_query)


async def process_html_response(url, session):
    """Process HTML response, modify content and return response."""
    html_content = await get_html_content(url, session)
    soup = BeautifulSoup(html_content, 'lxml')
    modify_text_in_soup(soup)
    rewrite_links_in_soup(soup)
    return soup.prettify(formatter="html")
