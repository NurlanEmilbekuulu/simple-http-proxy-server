# Simple HTTP Proxy Server

This project is a simple HTTP proxy server implemented using Python and aiohttp. The proxy server serves the content of Hacker News pages locally, with a modification of adding a trademark symbol "™" to every six-letter word on the pages.

## Features

- Proxy serves the content of Hacker News pages.
- Modifies the text on the pages by adding a trademark symbol "™" after every six-letter word.
- Dockerized for easy setup and execution.

## Pre-requisites

- Python 3.9+
- Docker

## Setup and Running

### With Docker

1. Ensure Docker is installed on your machine.
2. Build the Docker image:

```bash
docker build -t simple-proxy .
```

3. Run the Docker container:

```bash
docker run -d -p 9097:9097 simple-proxy
```

The proxy server will now be running at `http://127.0.0.1:9097`.

### Without Docker

1. Clone the repository.
2. Navigate to the project directory.
3. Install the necessary dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

4. Run the server:

```bash
python -m proxy_server.app
```

The proxy server will now be running at `http://127.0.0.1:9097`.

### Usage

Navigate to `http://127.0.0.1:9097` in your web browser to view the proxied content of Hacker News. The URL path and query parameters will be forwarded to Hacker News, and the content will be modified as per the project's specification before being displayed.

### Customization

You can customize the proxy server by modifying the environment variables in a `.env` file in the project root, or by directly modifying the `config.py` file. The configurable variables are:

- `PROXY_HOST`: Host on which the proxy server runs. Default is `http://127.0.0.1`.
- `PROXY_PORT`: Port on which the proxy server runs. Default is `9097`.
- `TARGET_URL`: URL of Hacker News. Default is `https://news.ycombinator.com/`.
