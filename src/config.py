import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_URL: str = "https://www.bruno-giarrizzo.fr"
    CNAME: str = "www.bruno-giarrizzo.fr"

    BUILD_PATH: str = "docs"
    MEDIA_PATH: str = "media"
    STATIC_PATH: str = "static"

    BLOG_PATH: str = "blog"
    RESUME_PATH: str = "resume"

    CONTENT_PATH: str = "content"
    TEMPLATE_PATH: str = "src/templates"
    LAYOUT_PATH: str = "src/templates/layouts"
    INCLUDE_PATH: str = "src/templates/layouts/includes"

    NAME: str = "Bruno Giarrizzo"
    SHORT_URL: str = "bruno-giarrizzo.fr"
    DESCRIPTION: str = "Freelance Developer, DevOps, Ethical Hacker"
    KEYWORDS: list = [
        "Bruno",
        "Giarrizzo",
        "Bruno Giarrizzo",
        "Freelance",
        "Developer",
        "DevOps",
        "Ethical Hacker",
        "Ethical",
        "Hacker",
        "Django",
        "Python",
        "Swift",
        "Ansible",
        "Terraform",
        "Kubernetes",
        "Infra as Code",
    ]
    LANGUAGE: str = "en"

    def get_working_directory(self):
        return os.getcwd()

    class Config:
        # pylint: disable=too-few-public-methods
        case_sensitive = True


settings = Settings()
