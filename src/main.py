from copy_dir_content import copy_dir_content
from generate_pages_recursive import generate_pages_recursive

def main():
    copy_dir_content("./static/", "./public/")

    generate_pages_recursive("./content/", "./template.html", "./public/")

main()
