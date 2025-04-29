import re

def extract_markdown_images(text):
    return re.findall(r'!\[\s*(\S?.*?\S?)\s*\]\s*\(\s*(?:\'|\")?(.*?)(?:\'|\")?\s*(?:".*?")?\s*\)', text)
