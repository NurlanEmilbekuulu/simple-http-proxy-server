from aiohttp import web

from proxy_server.config import PROXY_PORT
from proxy_server.handlers import handle_http_request


def main():
    app = web.Application()
    app.router.add_get('/{tail:.*}', handle_http_request)
    web.run_app(app, port=PROXY_PORT)


if __name__ == "__main__":
    main()
