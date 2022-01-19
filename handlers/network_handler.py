import requests
from urllib.parse import urlparse
from exceptions import TooManyRequestsError
import logging
from typing import Any, Dict
import sys

logger = logging.getLogger(__name__)


def request_html_page(url: str) -> Any:
    headers = {
        "Content-Type": "text/html",
        "Accept": "text/html",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.5",
        "Dnt": 1,
        "Referer": "https://www.google.com",
        "Accept-Encoding": "gzip, deflate",
    }
    return request(url, headers)


def request(url: str, headers: Dict = {}) -> Any:
    try:
        res = requests.get(url, headers)
        if res.status_code == 429:
            raise TooManyRequestsError()
        return res
    except TooManyRequestsError:
        logger.error(
            "We are sending too much requests to this domain -"
            f" {urlparse(url).netloc}. Maybe there is a problem with the"
            " treading"
        )
    except Exception as err:
        logger.error(f"Something went wrong during I/O operation - {err}")
        sys.exit()


def is_absolute_url(url: str) -> bool:
    return bool(urlparse(url).netloc)


def get_absolute_url(url: str, domain: str) -> str:
    if not is_absolute_url(url):
        return f"{domain}{url}"
    return url
