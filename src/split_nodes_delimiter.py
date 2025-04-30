from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            parts = old_node.text.split(delimiter)

            if len(parts) % 2 == 0:
                # TODO: improve message
                raise Exception("invalid markdown syntax")

            for i in range(len(parts)):
                if len(parts[i]) > 0:
                    new_nodes.append(TextNode(parts[i], TextType.TEXT if i % 2 == 0 else text_type))
        else:
            new_nodes.append(old_node)

    return new_nodes
