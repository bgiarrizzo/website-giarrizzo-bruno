import shutil

from config import settings
from generators.blog import generate_blog
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

    generate_blog()
    generate_pages()

    print("#", "-" * 80)
    generate_resume()