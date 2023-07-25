from config import settings
from generators.common import generate_dataset_of_item_files, get_all_files_from_path
from utils.template import generate_data_for_template, render_template, write_page
from utils.format import beautify_html


def generate_page(page, blog_posts=None):
    data = {"page": page, "posts": blog_posts}

    page_template = render_template("page.j2", generate_data_for_template([data]))

    content = {"content": page_template}

    rendered_page = render_template(
        "main.j2", generate_data_for_template([data, content])
    )
    write_page(f"{page['permalink']}/index.html", beautify_html(rendered_page))


def generate_pages(posts):
    pages_files = get_all_files_from_path(f"{settings.CONTENT_PATH}/pages")
    pages = generate_dataset_of_item_files(pages_files)

    print("#", "-" * 80)
    print("Generating pages ...")
    for page in pages:
        if len(page.get("permalink")) == 0:
            print("Generating page with empty permalink: Home ? ...")
        else:
            print(f"Generating page: {page['permalink']} ...")
        generate_page(page, posts)
