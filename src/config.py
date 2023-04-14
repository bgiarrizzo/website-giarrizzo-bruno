import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = "http://localhost:8000"

    BUILD_PATH: str = "build"
    MEDIA_PATH: str = "media"
    STATIC_PATH: str = "static"

    BLOG_PATH: str = "blog"
    RESUME_PATH: str = "resume"

    CONTENT_PATH: str = "content"
    TEMPLATE_PATH: str = "src/templates"
    LAYOUT_PATH: str = "src/templates/layouts"
    INCLUDE_PATH: str = "src/templates/layouts/includes"

    def get_working_directory(self):
        return os.getcwd()

    class Config:
        # pylint: disable=too-few-public-methods
        case_sensitive = True


settings = Settings()
