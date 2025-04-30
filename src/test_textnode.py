import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_create_text_node(self):
        node1 = TextNode("Hello world", TextType.TEXT)
        self.assertEqual(node1.text, "Hello world")
        self.assertEqual(node1.text_type, TextType.TEXT)
        self.assertIsNone(node1.url)

        node2 = TextNode("Important", TextType.BOLD)
        self.assertEqual(node2.text, "Important")
        self.assertEqual(node2.text_type, TextType.BOLD)

        node3 = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node3.text, "Click here")
        self.assertEqual(node3.text_type, TextType.LINK)
        self.assertEqual(node3.url, "https://example.com")

    def test_equality_comparison(self):
        node1 = TextNode("Same content", TextType.TEXT)
        node2 = TextNode("Same content", TextType.TEXT)
        self.assertEqual(node1, node2)

        node3 = TextNode("Different content", TextType.TEXT)
        self.assertNotEqual(node1, node3)

        node4 = TextNode("Same content", TextType.BOLD)
        self.assertNotEqual(node1, node4)

        node5 = TextNode("Link text", TextType.LINK, "https://example.com")
        node6 = TextNode("Link text", TextType.LINK, "https://another.com")
        self.assertNotEqual(node5, node6)

    def test_string_representation(self):
        node1 = TextNode("Test", TextType.TEXT)
        self.assertEqual(repr(node1), "TextNode(Test, text, None)")

        node2 = TextNode("def hello():", TextType.CODE)
        self.assertEqual(repr(node2), "TextNode(def hello():, code, None)")

        node3 = TextNode(
            "My Image",
            TextType.IMAGE,
            "https://example.com/image.jpg"
        )
        self.assertEqual(
            repr(node3),
            "TextNode(My Image, image, https://example.com/image.jpg)"
        )

if __name__ == "__main__":
    unittest.main()
