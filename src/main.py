from copy_dir_content import copy_dir_content
from generate_page import generate_page

def main():
    copy_dir_content("./static/", "./public/")

    generate_page("./content/index.md", "./template.html", "./public/index.html")

main()
