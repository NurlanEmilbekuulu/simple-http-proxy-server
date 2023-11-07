import html
import re

from cachetools import LRUCache

from proxy_server.config import PROXY_HOST, PROXY_PORT

SIX_LETTER_WORD_PATTERN = re.compile(r'\b(\w{6})\b')
LINKS_PATTERN = re.compile(
    r'<a\s+href="https://news\.ycombinator\.com([^"]*)"', re.IGNORECASE)
CACHE = LRUCache(maxsize=100)


def _is_six_letter_alpha(word):
    """Check if a word is six letters long and consists of alphabetic characters."""
    return bool(SIX_LETTER_WORD_PATTERN.match(word))


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


def _unescape_href(html_content):
    """Unescape HTML href attributes."""
    href_pattern = r'href="([^"]+)"'
    hrefs = re.findall(href_pattern, html_content)
    for href in hrefs:
        decoded_href = html.unescape(href)
        html_content = html_content.replace(
            f'href="{href}"', f'href="{decoded_href}"')

    return html_content


def _replace_links(html_content):
    """Replace links in HTML with a proxy link."""
    replacement = f'<a href="http://{PROXY_HOST}:{PROXY_PORT}\\1"'
    return LINKS_PATTERN.sub(replacement, html_content)


def _modify_text_inside_tags(html_content):
    """Modify text by adding a trademark symbol to all six-letter words inside HTML tags."""
    def replace(match):
        text_inside_tags = match.group(1)
        words = text_inside_tags.split()
        modified_words = {}

        for word in words:
            if _is_six_letter_alpha(word):
                if word not in modified_words:
                    modified_word = f'{word}<sup>™</sup>'
                    text_inside_tags = text_inside_tags.replace(
                        word, modified_word)
                    modified_words[word] = modified_word

        return f'>{text_inside_tags}<'

    modified_html = re.sub(r'>([^<]+)<', replace, html_content)

    return modified_html


async def process_html_response(url, session):
    """Process HTML response, modify content and return response."""
    html_content = await _get_html_content(url, session)
    return _modify_text_inside_tags(_replace_links(_unescape_href(html_content)))
