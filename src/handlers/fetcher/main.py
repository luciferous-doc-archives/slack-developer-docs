from os import environ, makedirs
from os.path import dirname

from utils.http.interval_fetcher import default_fetcher
from utils.logger import create_logger, logging_function
from utils.parser import parse_sitemap_markdown
from utils.path import url_to_file_path

logger = create_logger(__name__)

SITEMAP_URL = "https://docs.slack.dev/llms-sitemap.md"
BASE_DIR = "docs"
SKIP_URL_PREFIXES = [
    "https://docs.slack.dev/super-secret.md",
    "https://docs.slack.dev/super-secret/",
]


def _should_skip_url(url: str) -> bool:
    return any(url.startswith(prefix) for prefix in SKIP_URL_PREFIXES)


@logging_function(logger)
def main():
    base_timestamp = get_base_timestamp()
    markdown_content = default_fetcher(url=SITEMAP_URL)
    all_urls = parse_sitemap_markdown(markdown_content=markdown_content)

    filtered_urls = [url for url in all_urls if not _should_skip_url(url)]

    skipped_urls = [url for url in all_urls if _should_skip_url(url)]
    if skipped_urls:
        logger.info(f"Basic認証が必要なURLをスキップ: {len(skipped_urls)} 件")

    for url in filtered_urls:
        path = url_to_file_path(url=url, all_urls=all_urls)
        fetch_and_save(url=url, path=path, base_timestamp=base_timestamp)


@logging_function(logger)
def get_base_timestamp() -> str:
    return environ["BASE_TIMESTAMP"]


@logging_function(logger)
def fetch_and_save(*, url: str, path: str, base_timestamp: str):
    file_path = f"{BASE_DIR}/slack-developer-docs-{base_timestamp}/{path}"

    dir_path = dirname(file_path)
    makedirs(name=dir_path, exist_ok=True)

    markdown = default_fetcher(url=url)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(markdown)
