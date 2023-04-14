from os import path, walk

from config import settings
from utils.markdown import (
    convert_markdown_text_to_html,
    parse_yaml_header_and_markdown_body_in_file,
)
from utils.template import generate_data_for_template, render_template, write_page


def get_all_pages_from_content_path(content_path) -> list:
    pages_files = []
    path_to_pages = f"{content_path}/pages"
    for root, dirs, files in walk(path_to_pages):
        for file in sorted(files):
            pages_files.append(path.join(root, file))
    return pages_files


def generate_dataset_of_pages(pages_files) -> list:
    pages = []
    for page_file in pages_files:
        yaml_header, markdown_body = parse_yaml_header_and_markdown_body_in_file(
            page_file
        )
        page = yaml_header | {"body": convert_markdown_text_to_html(markdown_body)}
        pages.append(page)
    return pages


def generate_page(page):
    page_data = {"page": page}

    page_template = render_template("page.j2", generate_data_for_template([page_data]))

    content = {"content": page_template}

    rendered_page = render_template(
        "main.j2", generate_data_for_template([page_data, content])
    )
    write_page(f"{page['permalink']}/index.html", rendered_page)


def generate_pages():
    pages_files = get_all_pages_from_content_path(settings.CONTENT_PATH)
    pages = generate_dataset_of_pages(pages_files)

    print("#", "-" * 80)
    print("Generating pages ...")
    for page in pages:
        if len(page.get("permalink")) == 0:
            print("Generating page with empty permalink: Home ? ...")
        else:
            print(f"Generating page: {page['permalink']} ...")
        generate_page(page)
