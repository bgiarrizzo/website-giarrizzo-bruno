from bs4 import BeautifulSoup
from prettierfier import prettify_html, prettify_xml


def beautify_html(content):
    htmlsouped = BeautifulSoup(content, "html.parser").prettify()
    return prettify_html(html_string=htmlsouped)


def beautify_xml(content):
    xml_souped = BeautifulSoup(content, "xml").prettify()
    return prettify_xml(xml_string=xml_souped)
