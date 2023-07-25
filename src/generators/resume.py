from config import settings
from generators.common import generate_dataset_of_item_files, get_all_files_from_path
from utils.template import generate_data_for_template, render_template, write_page
from utils.format import beautify_html


def generate_resume_experience(experiences):
    resume = {"resume": {"tags": [], "experiences": experiences}}

    for experience in experiences:
        if experience.get("tags"):
            for tag in experience.get("tags"):
                if tag not in resume.get("resume"):
                    resume.get("resume").get("tags").append(tag)

    resume_template = render_template("resume.j2", generate_data_for_template([resume]))

    content = {"content": resume_template}

    rendered_resume = render_template(
        "main.j2",
        generate_data_for_template([resume, content]),
    )
    write_page("/resume/index.html", beautify_html(rendered_resume))


def generate_resume():
    experiences = generate_dataset_of_item_files(
        get_all_files_from_path(f"{settings.CONTENT_PATH}/resume/experiences")
    )

    print("Generating resume ...")
    generate_resume_experience(experiences)
