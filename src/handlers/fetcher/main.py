from os import environ

from utils.http.interval_fetcher import default_fetcher
from utils.logger import create_logger, logging_function
from utils.parser import default_parser

logger = create_logger(__name__)

SITEMAP_URL = "https://docs.slack.dev/llms-sitemap.md"


@logging_function(logger)
def main():
    markdown_content = default_fetcher(url=SITEMAP_URL)
    urls = default_parser(markdown_content=markdown_content)
    return urls


@logging_function(logger)
def get_base_timestamp() -> str:
    return environ["BASE_TIMESTAMP"]
