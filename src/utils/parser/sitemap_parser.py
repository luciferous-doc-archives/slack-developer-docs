import re
from typing import Protocol

from utils.logger import create_logger, logging_function

logger = create_logger(__name__)

_URL_PATTERN = re.compile(r"^https://docs\.slack\.dev/[a-z0-9/_.-]+\.md$")


class TypeDefinitionSitemapParser(Protocol):
    def __call__(self, *, markdown_content: str) -> list[str]: ...


def _validate_slack_doc_url(url: str) -> bool:
    return bool(_URL_PATTERN.match(url))


def make_sitemap_parser() -> TypeDefinitionSitemapParser:
    @logging_function(logger)
    def parse_sitemap_markdown(*, markdown_content: str) -> list[str]:
        urls: list[str] = []
        skipped: list[str] = []

        for line in markdown_content.splitlines():
            stripped = line.strip()
            if not stripped.startswith("- https://"):
                continue

            url = stripped[2:]
            if _validate_slack_doc_url(url):
                urls.append(url)
            else:
                skipped.append(url)

        if skipped:
            logger.warning(
                f"無効な URL をフィルタリング: {len(skipped)} 件",
                data={"skipped_count": len(skipped), "examples": skipped[:5]},
            )

        return urls

    return parse_sitemap_markdown


default_parser = make_sitemap_parser()
