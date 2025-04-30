from textnode import TextNode, TextType
from extract_markdown_images import extract_markdown_images

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == TextType.IMAGE:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image_alt, image_link in images:
            parts = text.split(f"![{image_alt}]({image_link})", 1)

            new_nodes.append(TextNode(parts[0], old_node.text_type))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            # NOTE: if whole old_node is image with syntax that differ from canonical
            # (ie. ![ spaces right near brackets ]( or spaces here either ))
            # then .split() will produce list with only one element
            text = parts[1]

        new_nodes.append(TextNode(text, old_node.text_type, old_node.url))

    return list(filter(lambda n: len(n.text) > 0 or (n.url and len(n.url) > 0), new_nodes))
