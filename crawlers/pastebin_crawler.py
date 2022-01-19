from db.db import DB
from .crawler import WebCrawler
import logging
from handlers import html_parser
from handlers.load_files_helper import get_json_file
from handlers.job_handler import JobHandler
from handlers.html_parser import HtmlElement
from typing import Dict, Optional, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

logger = logging.getLogger(__name__)


class PastebinCrawler(WebCrawler):
    _PASTEBIN_CONFIG_PATH = "configs/pastebin_config"

    def __init__(self, db: DB):
        self.config = get_json_file(PastebinCrawler._PASTEBIN_CONFIG_PATH)

        super().__init__(
            db,
            root_url=f'{self.config["DOMAIN"]}{self.config["ROOT_URL_PATH"]}',
            domain=self.config["DOMAIN"],
        )

        self.scraping_job_handler = JobHandler(
            interval_amount=self.config["INTERVAL_AMOUNT"],
            interval_units=self.config["INTERVAL_UNITS"],
        )

    def process(self) -> None:
        logger.info("Fetching new data from pastebin")
        self.append_new_links()
        links_data = self.get_links_data()
        self.db.insert_many(links_data)
        self.scraping_job_handler.schedule_a_job(self.process)

    def append_new_links(self) -> None:
        root_page_html = self.get_page_as_html_el(self.root_url)
        all_a_tags = html_parser.find_all_html_elements(
            root_html_el=root_page_html,
            css_selector=self.config["links_list_css_selector"],
        )

        for a_tag in all_a_tags:
            relative_path = html_parser.extract_attrib_from_html(a_tag, "href")
            if relative_path not in self.visited:
                self.to_be_visited.add(relative_path)

    def get_links_data(self) -> Optional[List[Dict[str, Any]]]:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.get_link_data, link)
                for link in self.to_be_visited
            ]

            try:
                links_data = [f.result() for f in as_completed(futures)]
                return links_data

            except Exception as err:
                logger.error(
                    "Sometihng went wrong while requesting web pages in"
                    f" threads - {err}"
                )
                sys.exit()
            finally:
                self.to_be_visited.clear()

    def get_link_data(self, link: str) -> Dict[str, Any]:
        link_html = self.get_page_as_html_el(link)
        link_id = link[1:] if link[0] == "/" else link
        link_data = self.extract_data(link_html, id=link_id)
        self.visited.add(link)
        return link_data

    def extract_data(
        self, root_html_el: HtmlElement, id: Optional[str]
    ) -> Dict[str, str]:
        model = {}
        data_modal_config = self.config["data_model_to_extract"]
        for key, config_data in data_modal_config.items():
            curr_html_el = html_parser.find_html_element(
                root_html_el=root_html_el,
                css_selector=config_data["css_selector"],
            )
            data = html_parser.extract_data_from_html(
                html_el=curr_html_el,
                output_type=config_data["output_type"],
                attrib=config_data.get("attrib", ""),
            )
            model[key] = data
        if id:
            model["id"] = id
        return model
