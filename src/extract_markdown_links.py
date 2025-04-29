import re

def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[\s*(\S?.*?\S?)\s*\]\s*\(\s*(?:\'|\")?(.*?)(?:\'|\")?\s*(?:".*?")?\s*\)', text)
