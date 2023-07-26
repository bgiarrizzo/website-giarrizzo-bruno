from config import settings
from generators.common import generate_dataset_of_item_files, get_all_files_from_path
from utils.format import beautify_html
from utils.template import generate_data_for_template, render_template, write_page


def generate_resume_head(dataset: list, resume: dict):
    for head in dataset:
        if head.get("tags"):
            for tag in head.get("tags"):
                if tag not in resume.get("resume").get("tags"):
                    resume.get("resume").get("tags").append(tag)

    resume["resume"]["head"] = dataset[0].get("body")

    return resume


def generate_resume_experience(
    dataset: list,
    resume: dict,
):
    for experience in dataset:
        if experience.get("tags"):
            for tag in experience.get("tags"):
                if tag not in resume.get("resume"):
                    resume.get("resume").get("tags").append(tag)

    resume["resume"]["experiences"] = dataset

    return resume


def generate_resume_education(dataset: list, resume: dict):
    for education in dataset:
        if education.get("tags"):
            for tag in education.get("tags"):
                if tag not in resume.get("resume").get("tags"):
                    resume.get("resume").get("tags").append(tag)

    resume["resume"]["educations"] = dataset

    return resume


def generate_resume():
    print("Generating resume ...")

    resume = {
        "resume": {
            "tags": [],
        }
    }

    head_dataset = generate_dataset_of_item_files(
        get_all_files_from_path(f"{settings.CONTENT_PATH}/resume/head")
    )
    experiences_dataset = generate_dataset_of_item_files(
        get_all_files_from_path(f"{settings.CONTENT_PATH}/resume/experiences")
    )
    educations_dataset = generate_dataset_of_item_files(
        get_all_files_from_path(f"{settings.CONTENT_PATH}/resume/educations")
    )

    print("Generating header ...")
    resume = resume | generate_resume_head(dataset=head_dataset, resume=resume)

    print("Generating education part ...")
    resume = resume | generate_resume_education(
        dataset=educations_dataset, resume=resume
    )

    print("Generating experience part ...")
    resume = resume | generate_resume_experience(
        dataset=experiences_dataset, resume=resume
    )

    print("Generating resume page ...")
    resume_template = render_template("resume.j2", generate_data_for_template([resume]))

    content = {"content": resume_template}

    rendered_resume = render_template(
        "main.j2",
        generate_data_for_template([resume, content]),
    )
    write_page("/resume/index.html", beautify_html(rendered_resume))
