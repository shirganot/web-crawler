from abc import ABC, abstractmethod
from db.db import DB
from handlers.network_handler import get_absolute_url, request_html_page
from handlers import html_parser
import logging
from typing import Optional
import sys


logger = logging.getLogger(__name__)


class WebCrawler(ABC):
    def __init__(
        self,
        db: DB,
        root_url: str,
        domain: str,
    ):
        self.root_url = root_url
        self.domain = domain
        self.db = db
        self.visited = set()
        self.to_be_visited = set()

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def append_new_links(self):
        pass

    @abstractmethod
    def extract_data(self, html_el: html_parser.HtmlElement):
        pass

    @abstractmethod
    def get_links_data(self):
        pass

    def get_page_as_html_el(
        self, url: str
    ) -> Optional[html_parser.HtmlElement]:
        try:
            absolute_url = get_absolute_url(url, self.domain)
            res = request_html_page(absolute_url)
            return html_parser.parse_str_to_html(res.text)
        except Exception as err:
            logger.error(
                "Sometihng went wrong while requesting web page as html -"
                f" {err}"
            )
            sys.exit()
