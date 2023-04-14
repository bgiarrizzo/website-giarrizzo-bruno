from os import path, walk

from config import settings
from utils.markdown import (
    convert_markdown_text_to_html,
    parse_yaml_header_and_markdown_body_in_file,
)
from utils.template import generate_data_for_template, render_template, write_page


def get_all_resume_experiences_from_content_path(content_path) -> list:
    resume_experiences_files = []
    path_to_resume_experiences = f"{content_path}/resume/experiences"
    for root, dirs, files in walk(path_to_resume_experiences):
        for file in sorted(files):
            resume_experiences_files.append(path.join(root, file))
    return resume_experiences_files

def generate_dataset_of_resume_experiences(resume_experiences_files) -> list:
    resume_experiences = []
    for resume_experience_file in resume_experiences_files:
        yaml_header, markdown_body = parse_yaml_header_and_markdown_body_in_file(
            resume_experience_file
        )
        resume_experience = yaml_header | {"body": convert_markdown_text_to_html(markdown_body)}
        resume_experiences.append(resume_experience)
    return resume_experiences


def generate_resume_experience(resume_experience):
    resume_experience_data = {"experiences": resume_experience}

    resume_experience_template = render_template("resume.j2", generate_data_for_template([resume_experience_data]))

    content = {"content": resume_experience_template}

    rendered_resume = render_template(
        "main.j2", generate_data_for_template([resume_experience_data, content])
    )
    write_page("/resume/index.html", rendered_resume)


def generate_resume():
    resume_experience_files = get_all_resume_experiences_from_content_path(settings.CONTENT_PATH)
    resume_experiences = generate_dataset_of_resume_experiences(resume_experience_files)

    print("Generating resume ...")
    generate_resume_experience(resume_experiences)
