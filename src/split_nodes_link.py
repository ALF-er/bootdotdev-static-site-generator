from textnode import TextNode, TextType
from extract_markdown_links import extract_markdown_links

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == TextType.LINK:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link_text, link_url in links:
            parts = text.split(f"[{link_text}]({link_url})", 1)

            new_nodes.append(TextNode(parts[0], old_node.text_type))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            # NOTE: if whole old_node is link with syntax that differ from canonical
            # (ie. [_no spaces right near brackets_](_no spaces here eaither_))
            # then .split() will produce list with only one element
            text = parts[1]

        new_nodes.append(TextNode(text, old_node.text_type, old_node.url))

    return list(filter(lambda n: len(n.text) > 0 or (n.url and len(n.url) > 0), new_nodes))
