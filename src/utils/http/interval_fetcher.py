from urllib.request import urlopen
from utils.logger import create_logger, logging_function
from http.client import HTTPResponse
from datetime import datetime
from typing import Protocol
from time import sleep


class TypeDefinitionIntervalFetcher(Protocol):
    def __call__(self, *, url: str) -> str: ...


logger = create_logger(__name__)


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
                    return body.decode()
                elif isinstance(body, str):
                    return body
                else:
                    raise TypeError(f"レスポンスのタイプが不正です ({type(body)})")
        finally:
            dt_prev = datetime.now()

    return interval_fetcher


default_fetcher = make_interval_fetcher(sec=1)
