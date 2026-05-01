from urllib.parse import urlparse

from utils.logger import create_logger, logging_function

logger = create_logger(__name__)


@logging_function(logger)
def url_to_file_path(*, url: str, all_urls: list[str]) -> str:
    path = urlparse(url).path[1:]

    if path.endswith(".md"):
        stem = path[:-3]
        prefix = f"/{stem}/"
        if any(urlparse(u).path.startswith(prefix) for u in all_urls):
            return f"{stem}/index.md"

    return path
