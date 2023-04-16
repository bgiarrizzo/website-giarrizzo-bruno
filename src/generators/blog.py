from slugify import slugify

from config import settings
from generators.common import generate_dataset_of_item_files, get_all_files_from_path
from utils.template import generate_data_for_template, render_template, write_page


def extract_date_and_slugify_title_of_blog_post(post_list):
    for post in post_list:
        if post.get("publish_date"):
            post["short_date"] = post.get("publish_date").strftime("%d-%b-%Y")
            post["year"] = post.get("publish_date").year
        if post.get("title"):
            post["slug"] = slugify(post.get("title"))
    return post_list


def generate_rss_feed(posts: list):
    posts_data = {"posts": posts}
    rendered_rss_feed = render_template(
        "blog_feed_rss.j2", generate_data_for_template([posts_data])
    )
    write_page("blog/feed.xml", rendered_rss_feed)


def generate_blog_post(post_data):
    post = {"post": post_data}

    blog_post_template = render_template(
        "blog_post.j2", generate_data_for_template([post])
    )

    content = {"content": blog_post_template}

    rendered_page = render_template(
        "main.j2", generate_data_for_template([post, content])
    )
    write_page(f"blog/{post_data['slug']}/index.html", rendered_page)


def generate_blog_page_list(posts_data):
    posts = {"posts": posts_data}

    blog_post_list_template = render_template(
        "blog_post_list.j2", generate_data_for_template([posts])
    )

    content = {"content": blog_post_list_template}

    rendered_page = render_template(
        "main.j2", generate_data_for_template([posts, content])
    )
    write_page("blog/index.html", rendered_page)


def generate_blog():
    posts = extract_date_and_slugify_title_of_blog_post(
        generate_dataset_of_item_files(
            get_all_files_from_path(f"{settings.CONTENT_PATH}/blog_posts")
        )
    )

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

    return posts
