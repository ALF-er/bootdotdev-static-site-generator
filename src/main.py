import sys

from copy_dir_content import copy_dir_content
from generate_pages_recursive import generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_dir_content("./static/", "./docs/")

    generate_pages_recursive("./content/", "./template.html", "./docs/", basepath)

main()
