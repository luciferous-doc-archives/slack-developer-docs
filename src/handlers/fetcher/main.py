from os import environ, makedirs
from os.path import dirname
from urllib.parse import urlparse

from utils.http.interval_fetcher import default_fetcher
from utils.logger import create_logger, logging_function
from utils.parser import parse_sitemap_markdown

logger = create_logger(__name__)

SITEMAP_URL = "https://docs.slack.dev/llms-sitemap.md"
BASE_DIR = "docs"


@logging_function(logger)
def main():
    base_timestamp = get_base_timestamp()
    markdown_content = default_fetcher(url=SITEMAP_URL)
    all_urls = parse_sitemap_markdown(markdown_content=markdown_content)
    for url in all_urls:
        path = url_to_file_path(url=url, all_urls=all_urls)
        fetch_and_save(url=url, path=path, base_timestamp=base_timestamp)


@logging_function(logger)
def get_base_timestamp() -> str:
    return environ["BASE_TIMESTAMP"]


@logging_function(logger)
def url_to_file_path(*, url: str, all_urls: list[str]) -> str:
    path = urlparse(url).path[1:]

    if path.endswith(".md"):
        stem = path[:-3]
        prefix = f"/{stem}/"
        if any(urlparse(u).path.startswith(prefix) for u in all_urls):
            return f"{stem}/index.md"

    return path


@logging_function(logger)
def fetch_and_save(*, url: str, path: str, base_timestamp: str):
    file_path = f"{BASE_DIR}/slack-developer-docs-{base_timestamp}/{path}"

    dir_path = dirname(file_path)
    makedirs(name=dir_path, exist_ok=True)

    markdown = default_fetcher(url=url)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown)
