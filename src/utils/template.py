from os import makedirs, path

from jinja2 import Environment, FileSystemLoader

from config import settings


def write_page(filename, content):
    makedirs(path.dirname(f"{settings.BUILD_PATH}/{filename}"), exist_ok=True)

    with open(f"{settings.BUILD_PATH}/{filename}", mode="w", encoding="utf-8") as page:
        page.write(content)


def render_template(template_name, data):
    env = Environment(loader=FileSystemLoader(settings.LAYOUT_PATH))
    template = env.get_template(template_name)
    return template.render(data)


def generate_data_for_template(datalist):
    data_for_template = {}
    site_infos = {
        "site": {
            "url": settings.BASE_URL,
            "short_url": settings.SHORT_URL,
            "description": settings.DESCRIPTION,
            "language": settings.LANGUAGE,
            "name": settings.NAME,
            "keywords": settings.KEYWORDS,
        }
    }
    data_for_template = data_for_template | site_infos
    if len(datalist) > 0:
        for data in datalist:
            data_for_template = data_for_template | data
    return data_for_template
