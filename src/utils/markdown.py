import markdown
import yaml

markdown_parser = markdown.Markdown()


def parse_yaml_header_and_markdown_body_in_file(markdown_file_path):
    with open(markdown_file_path, mode="r", encoding="utf-8") as markdown_file:
        markdown_file_content = markdown_file.read()
        markdown_file_content = markdown_file_content.split("---")

        yaml_header = yaml.load(markdown_file_content[1], Loader=yaml.FullLoader)
        markdown_body = markdown_file_content[2]

        return yaml_header, markdown_body


def convert_markdown_text_to_html(markdown_content):
    return markdown_parser.convert(
        markdown_content,
    )
