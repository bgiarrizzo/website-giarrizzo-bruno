from os import path, walk

from utils.markdown import (
    convert_markdown_text_to_html,
    parse_yaml_header_and_markdown_body_in_file,
)


def extract_year_from_item(item):
    return item.get("date").year


def add_cname_to_build(path_to_build, cname):
    with open(path.join(path_to_build, "CNAME"), "w") as f:
        f.write(cname)


def get_all_files_from_path(target_path) -> list:
    files_list = []
    for root, dirs, files in walk(target_path):
        for file in sorted(files):
            files_list.append(path.join(root, file))
    return files_list


def generate_dataset_of_item_files(item_files) -> list:
    items = []
    for item_file in item_files:
        yaml_header, markdown_body = parse_yaml_header_and_markdown_body_in_file(
            item_file
        )
        item = yaml_header | {"body": convert_markdown_text_to_html(markdown_body)}
        items.append(item)
    return items
