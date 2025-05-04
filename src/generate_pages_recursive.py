import os

from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dst_dir_path, basepath):
    dir_items = os.listdir(dir_path_content)

    for item in dir_items:
        item_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dst_dir_path, item)

        if os.path.isfile(item_path) and item[-3:] == ".md":
            generate_page(item_path, template_path, dst_path[:-3] + ".html", basepath)
        elif os.path.isdir(item_path):
            generate_pages_recursive(item_path, template_path, dst_path, basepath)
