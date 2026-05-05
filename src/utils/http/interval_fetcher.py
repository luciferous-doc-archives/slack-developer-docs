from datetime import datetime
from time import sleep
from typing import Protocol

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, RequestException, Timeout

from utils.logger import create_logger, logging_function


class TypeDefinitionIntervalFetcher(Protocol):
    def __call__(self, *, url: str) -> str: ...


class RetryableHTTPError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(message)


logger = create_logger(__name__)

# コネクションプーリング設定付きセッションの初期化
_session = requests.Session()
_adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10)
_session.mount("http://", _adapter)
_session.mount("https://", _adapter)


def extract_charset_from_response(resp: requests.Response) -> str:
    """requests レスポンスの Content-Type ヘッダーから charset を抽出"""
    content_type = resp.headers.get("Content-Type", "")

    for part in content_type.split(";"):
        part = part.strip()
        if part.lower().startswith("charset="):
            charset = part.split("=", 1)[1].strip()
            return charset.strip("\"'")

    return "utf-8"


def make_interval_fetcher(
    *,
    sec: float,
    max_retries: int = 5,
    initial_backoff: float = 1.0,
) -> TypeDefinitionIntervalFetcher:
    dt_prev: datetime | None = None

    @logging_function(logger)
    def interval_fetcher(*, url: str) -> str:
        nonlocal dt_prev

        for attempt in range(max_retries):
            try:
                if attempt == 0 and dt_prev:
                    delta = datetime.now() - dt_prev
                    wait = sec - delta.total_seconds()
                    if wait > 0:
                        sleep(wait)

                resp = _session.get(url)

                # リトライ対象HTTPエラーをチェック
                if resp.status_code >= 500 or resp.status_code == 429:
                    raise RetryableHTTPError(
                        resp.status_code,
                        f"HTTP {resp.status_code} リトライ可能エラー",
                    )

                resp.raise_for_status()

                body = resp.content
                if isinstance(body, bytes):
                    charset = extract_charset_from_response(resp)
                    result = body.decode(charset)
                elif isinstance(body, str):
                    result = body
                else:
                    raise TypeError(f"レスポンスのタイプが不正です ({type(body)})")

                dt_prev = datetime.now()
                return result

            except (ConnectionError, Timeout, RetryableHTTPError) as e:
                if attempt < max_retries - 1:
                    wait_time = initial_backoff * (2**attempt)
                    logger.info(
                        f"リトライ対象エラー発生。{wait_time}秒待機後にリトライします",
                        extra={
                            "attempt": attempt + 1,
                            "max_retries": max_retries,
                            "error": str(e),
                            "wait_time": wait_time,
                        },
                    )
                    sleep(wait_time)
                else:
                    raise RequestException(
                        f"{max_retries}回のリトライ後も失敗しました (最後のエラー: {e})"
                    ) from e
            except Exception:
                raise

    return interval_fetcher


default_fetcher = make_interval_fetcher(sec=1, max_retries=5, initial_backoff=1.0)
