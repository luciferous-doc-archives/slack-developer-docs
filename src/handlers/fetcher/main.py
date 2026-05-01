from os import environ
from urllib.parse import urlparse

from utils.http.interval_fetcher import default_fetcher
from utils.logger import create_logger, logging_function
from utils.parser import parse_sitemap_markdown

logger = create_logger(__name__)

SITEMAP_URL = "https://docs.slack.dev/llms-sitemap.md"


@logging_function(logger)
def main():
    markdown_content = default_fetcher(url=SITEMAP_URL)
    urls = parse_sitemap_markdown(markdown_content=markdown_content)
    return urls


@logging_function(logger)
def get_base_timestamp() -> str:
    return environ["BASE_TIMESTAMP"]


@logging_function(logger)
def url_to_file_path(url: str, all_urls: list[str]) -> str:
    path = urlparse(url).path[1:]

    if path.endswith(".md"):
        stem = path[:-3]
        prefix = f"/{stem}/"
        if any(urlparse(u).path.startswith(prefix) for u in all_urls):
            return f"{stem}/index.md"

    return path
