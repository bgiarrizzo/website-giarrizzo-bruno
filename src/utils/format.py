from bs4 import BeautifulSoup


def beautify_html(content):
    return BeautifulSoup(content, "html.parser").prettify()


def beautify_xml(content):
    return BeautifulSoup(content, features="xml").prettify()
