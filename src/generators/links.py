from slugify import slugify

from config import settings
from generators.common import generate_dataset_of_item_files, get_all_files_from_path
from utils.format import beautify_html, beautify_xml
from utils.template import generate_data_for_template, render_template, write_page


def extract_date_and_slugify_title_of_link(link_list):
    for link in link_list:
        if link.get("publish_date"):
            link["condensed_date"] = link.get("publish_date").strftime("%Y%m%d")
            link["short_date"] = link.get("publish_date").strftime("%d-%b-%Y")
            link["month"] = link.get("publish_date").strftime("%B")
            link["year"] = link.get("publish_date").year
        if link.get("title"):
            link["slug"] = slugify(link.get("title"))
        if link.get("slug") and link.get("publish_date"):
            link["id"] = f"{link.get('condensed_date')}-{link.get('slug')}"
    return link_list


def generate_rss_feed(links: list):
    links_data = {"links": links}
    rendered_rss_feed = render_template(
        "links_feed_rss.j2", generate_data_for_template([links_data])
    )
    write_page("links/feed.xml", beautify_xml(rendered_rss_feed))


def generate_link(link_data):
    link = {"link": link_data}

    link_template = render_template(
        "links_post.j2", generate_data_for_template([link])
    )

    content = {"content": link_template}

    rendered_page = render_template(
        "main.j2", generate_data_for_template([link, content])
    )
    write_page(f"links/{link_data['id']}/index.html", beautify_html(rendered_page))


def generate_link_page_list(links_data):
    links = {"all_links": links_data}

    link_list_template = render_template(
        "links_list.j2", generate_data_for_template([links])
    )

    content = {"content": link_list_template}

    rendered_page = render_template(
        "main.j2", generate_data_for_template([links, content])
    )
    write_page("links/index.html", beautify_html(rendered_page))


def generate_links():
    links = extract_date_and_slugify_title_of_link(
        generate_dataset_of_item_files(
            get_all_files_from_path(f"{settings.CONTENT_PATH}/links")
        )
    )

    print("#", "-" * 80)
    print("Generating links ...")

    print("Generating RSS feed ...")
    generate_rss_feed(links)

    print("Generating link list ...")
    generate_link_page_list(links)

    print("Generating links ...")
    for link in links:
        print(f"Generating link: {link.get('title')}")
        generate_link(link)

    return links
