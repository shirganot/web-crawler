from lxml import html
from lxml.cssselect import CSSSelector
from lxml.html import HtmlElement
from typing import Optional, Any
import logging
from enum import Enum


class Output(Enum):
    TEXT = "text"
    HTML_CONTENT = "html_content"
    ATTRIB = "attrib"


logger = logging.getLogger(__name__)


def parse_str_to_html(str: str) -> HtmlElement:
    return html.fromstring(str)


def find_all_html_elements(
    root_html_el: HtmlElement, css_selector: str
) -> Optional[HtmlElement]:
    try:
        sel = CSSSelector(css_selector)
        html_el = sel(root_html_el)

        return html_el
    except Exception as err:
        logger.error(
            "Something wend wrong while trying to get all html elements with"
            f" certain css selector - {err}"
        )


def find_html_element(
    root_html_el: HtmlElement, css_selector: str
) -> Optional[HtmlElement]:
    try:
        return find_all_html_elements(root_html_el, css_selector)[0]
    except Exception as err:
        logger.error(
            "Something went wrong while trying to find an html element. Maybe"
            " the data type hat was returned fro the search is invalid -"
            f" {err}"
        )


def extract_data_from_html(
    html_el: HtmlElement, output_type: str, attrib: Optional[str] = ""
) -> Optional[Any]:
    try:
        match output_type:
            case Output.TEXT.value:
                return extract_text_from_html(html_el)
            case Output.HTML_CONTENT.value:
                return extract_content_from_html(html_el)
            case Output.ATTRIB.value:
                return extract_attrib_from_html(html_el, attrib)
            case _:
                raise Exception("'output_type' value is invalid")
    except Exception as err:
        logger.error(
            "Something went wrong while extracting data from html elements -"
            f" {err}"
        )


def extract_text_from_html(html_el: HtmlElement) -> str:
    return html_el.text


def extract_attrib_from_html(html_el: HtmlElement, attrib: str) -> str:
    if not attrib:
        logger.warning("'attrib' is empty. Can't get the data")
        return ""
    return html_el.attrib[f"{attrib}"]


def extract_content_from_html(html_el: HtmlElement) -> str:
    return html_el.text_content()
