def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    blocks = map(lambda b: b.strip(), blocks)
    blocks = filter(lambda b: len(b) > 0, blocks)
    return list(blocks)
