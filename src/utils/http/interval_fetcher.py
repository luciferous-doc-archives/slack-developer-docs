from datetime import datetime
from http.client import HTTPResponse
from time import sleep
from typing import Protocol
from urllib.request import urlopen

from utils.logger import create_logger, logging_function


class TypeDefinitionIntervalFetcher(Protocol):
    def __call__(self, *, url: str) -> str: ...


logger = create_logger(__name__)


def extract_charset_from_response(resp: HTTPResponse) -> str:
    """HTTPレスポンスの Content-Type ヘッダーから charset を抽出"""
    content_type = resp.headers.get("Content-Type", "")

    for part in content_type.split(";"):
        part = part.strip()
        if part.lower().startswith("charset="):
            charset = part.split("=", 1)[1].strip()
            return charset.strip("\"'")

    return "utf-8"


def make_interval_fetcher(*, sec: float) -> TypeDefinitionIntervalFetcher:
    dt_prev: datetime | None = None

    @logging_function(logger)
    def interval_fetcher(*, url: str) -> str:
        nonlocal dt_prev

        if dt_prev:
            delta = datetime.now() - dt_prev
            wait = sec - delta.total_seconds()
            if wait > 0:
                sleep(wait)
        try:
            with urlopen(url) as resp:
                resp: HTTPResponse

                body = resp.read()
                if isinstance(body, bytes):
                    charset = extract_charset_from_response(resp)
                    return body.decode(charset)
                elif isinstance(body, str):
                    return body
                else:
                    raise TypeError(f"レスポンスのタイプが不正です ({type(body)})")
        finally:
            dt_prev = datetime.now()

    return interval_fetcher


default_fetcher = make_interval_fetcher(sec=1)
