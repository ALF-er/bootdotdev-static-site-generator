import os

from extract_title import extract_title
from markdown_to_htmlnode import markdown_to_htmlnode

def generate_page(from_path, template_path, dst_path, basepath):
    print(f"Generating page from {from_path} to {dst_path} using {template_path}")

    with open(from_path) as file:
        content = file.read()
    with open(template_path) as file:
        template = file.read()

    title = extract_title(content)
    content_html = markdown_to_htmlnode(content).to_html()

    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content_html)
    html = html.replace("href=\"/", f"href=\"{basepath}")
    html = html.replace("src=\"/", f"src=\"{basepath}")

    dst_dir = os.path.dirname(dst_path)

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    with open(dst_path, "w") as file:
        print(html, file=file)
