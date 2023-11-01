from aiohttp import ClientSession, web

from proxy_server.config import TARGET_URL
from proxy_server.utils import process_html_response


async def handle_http_request(request):
    async with ClientSession() as session:
        url = f"{TARGET_URL}{request.path_qs[1:]}"
        if 'text/html' in request.headers.get('Accept', ''):
            modified_content = await process_html_response(url, session)
            return web.Response(text=modified_content, content_type='text/html')
        else:
            return web.HTTPFound(url)
