import unittest

from enum import Enum
from textnode_to_htmlnode import textnode_to_htmlnode
from textnode import TextType, TextNode

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_normal_text_node(self):
        text_node = TextNode("Regular text", TextType.TEXT)
        html_node = textnode_to_htmlnode(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Regular text")

    def test_bold_text_node(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = textnode_to_htmlnode(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_text_node(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = textnode_to_htmlnode(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code_text_node(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = textnode_to_htmlnode(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")

    def test_link_text_node(self):
        text_node = TextNode("Link text", TextType.LINK, "https://example.com")
        html_node = textnode_to_htmlnode(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props["href"], "https://example.com")

    def test_image_text_node(self):
        text_node = TextNode("Image alt text", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = textnode_to_htmlnode(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://example.com/image.jpg")
        self.assertEqual(html_node.props["alt"], "Image alt text")

    def test_unknown_text_node_type(self):
        class MockTextType(Enum):
            UNKNOWN = 99

        text_node = TextNode("Unknown type", MockTextType.UNKNOWN)
        with self.assertRaises(Exception) as context:
            textnode_to_htmlnode(text_node)

        self.assertEqual(str(context.exception), "unknown type of text node")

if __name__ == "__main__":
    unittest.main()
