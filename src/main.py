import shutil

from config import settings
from generators.blog import generate_blog
from generators.common import add_cname_to_build
from generators.pages import generate_pages
from generators.resume import generate_resume
from utils.collection import collect_media_files, collect_static_files

if __name__ == "__main__":
    print("#", "-" * 80)
    print("Cleaning build folder ...")
    shutil.rmtree(settings.BUILD_PATH, ignore_errors=True)

    collect_media_files()
    collect_static_files()

    print("#", "-" * 80)
    print("Building site ...")

    posts = generate_blog()
    generate_pages(posts)

    print("#", "-" * 80)
    generate_resume()

    add_cname_to_build(settings.BUILD_PATH, settings.CNAME)
