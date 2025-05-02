from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_blocktype(block):
    if block[0] == "#":
        return BlockType.HEADING
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE

    lines = block.splitlines()

    if all(x[0] == ">" for x in lines):
        return BlockType.QUOTE

    if all(x[:2] == "- " for x in lines):
        return BlockType.UNORDERED_LIST

    is_ordered_list = True
    for i in range(len(lines)):
        parts = lines[i].split(". ", 1)
        if len(parts) <= 1 or not parts[0].isdigit() or int(parts[0]) != i + 1:
            is_ordered_list = False

    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
