import re

from parentnode import ParentNode
from textnode import TextNode, TextType
from markdown_to_blocks import markdown_to_blocks
from block_to_blocktype import block_to_blocktype, BlockType
from text_to_textnodes import text_to_textnodes
from textnode_to_htmlnode import textnode_to_htmlnode

def block_to_quote_htmlnode(block):
    block = re.sub(r"^>\s*", "", block, flags=re.MULTILINE)
    textnodes = text_to_textnodes(block)
    children = list(map(textnode_to_htmlnode, textnodes))
    return ParentNode("blockquote", children)

def block_to_heading_htmlnode(block):
    hash_count = max(len(block) - len(block.lstrip("#")), 6)
    textnodes = text_to_textnodes(block.lstrip("# "))
    children = list(map(textnode_to_htmlnode, textnodes))
    return ParentNode(f"h{hash_count}", children)

def block_to_ul_htmlnode(block):
    lines = block.splitlines()
    children = []
    for line in lines:
        line_textnodes = text_to_textnodes(line.lstrip("- "))
        line_htmlnodes = list(map(textnode_to_htmlnode, line_textnodes))
        children.append(ParentNode("li", line_htmlnodes))
    return ParentNode("ul", children)

def block_to_ol_htmlnode(block):
    lines = block.splitlines()
    children = []
    for line in lines:
        line_textnodes = text_to_textnodes(line.lstrip("1234567890. "))
        line_htmlnodes = list(map(textnode_to_htmlnode, line_textnodes))
        children.append(ParentNode("li", line_htmlnodes))
    return ParentNode("ol", children)

def block_to_paragraph_htmlnode(block):
    textnodes = text_to_textnodes(block)
    children = list(map(textnode_to_htmlnode, textnodes))
    return ParentNode("p", children)

def block_to_code_htmlnode(block):
    textnode = TextNode(block.strip("` \n"), TextType.CODE)
    children = [textnode_to_htmlnode(textnode)]
    return ParentNode("pre", children)

def block_to_htmlnode(block):
    blocktype = block_to_blocktype(block)

    match blocktype:
        case BlockType.QUOTE:
            return block_to_quote_htmlnode(block)
        case BlockType.HEADING:
            return block_to_heading_htmlnode(block)
        case BlockType.UNORDERED_LIST:
            return block_to_ul_htmlnode(block)
        case BlockType.ORDERED_LIST:
            return block_to_ol_htmlnode(block)
        case BlockType.PARAGRAPH:
            return block_to_paragraph_htmlnode(block)
        case BlockType.CODE:
            return block_to_code_htmlnode(block)

def markdown_to_htmlnode(markdown):
    blocks = markdown_to_blocks(markdown)
    blocknodes = list(map(block_to_htmlnode, blocks))

    return ParentNode("div", blocknodes)
