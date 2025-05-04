import re

def extract_title(markdown):
    title = re.search(r"(?:^|\n)#\s+(.+)\s*(?:\n|$)", markdown)

    if not title:
        raise Exception("no titles in markdown")

    return title.group(1).strip(" ")
