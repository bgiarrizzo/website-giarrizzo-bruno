from os import path, walk
from datetime import date
from slugify import slugify

from config import settings
from utils.markdown import (
    convert_markdown_text_to_html,
    parse_yaml_header_and_markdown_body_in_file,
)
from utils.template import generate_data_for_template, render_template, write_page


def extract_year_from_blog_post(blog_post):
    return blog_post["date"].year

def get_all_blog_posts_files_from_content_path(content_path) -> list:
    blog_post_files = []
    path_to_blog_posts = f"{content_path}/blog_posts"
    for root, dirs, files in walk(path_to_blog_posts):
        for file in sorted(files):
            blog_post_files.append(path.join(root, file))
    return blog_post_files


def generate_dataset_of_blog_posts(blog_posts_files) -> list:
    posts = []
    for blog_post_file in blog_posts_files:
        yaml_header, markdown_body = parse_yaml_header_and_markdown_body_in_file(
            blog_post_file
        )
        post = yaml_header | {"body": convert_markdown_text_to_html(markdown_body)}
        post["slug"] = slugify(post["title"])
        post["year"] = extract_year_from_blog_post(post)
        posts.append(post)
    return posts


def generate_rss_feed(posts: list):
    posts_data = {"posts": posts}
    rendered_rss_feed = render_template(
        "blog_feed_rss.j2", generate_data_for_template([posts_data])
    )
    write_page("blog/feed.xml", rendered_rss_feed)


def generate_blog_post(post):
    post_data = {"post": post}

    blog_post_template = render_template(
        "blog_post.j2", generate_data_for_template([post_data])
    )

    content = {"content": blog_post_template}

    rendered_page = render_template(
        "main.j2", generate_data_for_template([post_data, content])
    )
    write_page(f"blog/{post['slug']}/index.html", rendered_page)


def generate_blog_page_list(posts):
    posts_data = {"posts": posts}

    blog_post_list_template = render_template(
        "blog_post_list.j2", generate_data_for_template([posts_data])
    )

    content = {"content": blog_post_list_template}

    rendered_page = render_template(
        "main.j2", generate_data_for_template([posts_data, content])
    )
    write_page("blog/index.html", rendered_page)


def generate_blog():
    blog_posts_files = get_all_blog_posts_files_from_content_path(settings.CONTENT_PATH)
    posts = generate_dataset_of_blog_posts(blog_posts_files)

    print("#", "-" * 80)
    print("Generating blog ...")

    print("Generating RSS feed ...")
    generate_rss_feed(posts)

    print("Generating blog page list ...")
    generate_blog_page_list(posts)

    print("Generating blog posts ...")
    for post in posts:
        print(f"Generating blog post: {post['title']}")
        generate_blog_post(post)
