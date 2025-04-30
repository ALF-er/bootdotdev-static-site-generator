import unittest

from split_nodes_link import split_nodes_link
from textnode import TextType, TextNode

class TestSplitNodesLink(unittest.TestCase):
    def test_no_links(self):
        input_nodes = [
            TextNode("This is a paragraph with no links.", TextType.TEXT)
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "This is a paragraph with no links.")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertIsNone(result[0].url)

    def test_single_link(self):
        input_nodes = [
            TextNode("Here is a [link](https://example.com)", TextType.TEXT)
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 2)

        # First part: text before link
        self.assertEqual(result[0].text, "Here is a ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertIsNone(result[0].url)

        # Second part: the link
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com")

    def test_multiple_links(self):
        input_nodes = [
            TextNode(
                "First [link](https://example.com/first) and second [link](https://example.com/second)",
                TextType.TEXT
            )
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 4)

        # First part: text before first link
        self.assertEqual(result[0].text, "First ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        # Second part: first link
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com/first")

        # Third part: text between links
        self.assertEqual(result[2].text, " and second ")
        self.assertEqual(result[2].text_type, TextType.TEXT)

        # Fourth part: second link
        self.assertEqual(result[3].text, "link")
        self.assertEqual(result[3].text_type, TextType.LINK)
        self.assertEqual(result[3].url, "https://example.com/second")

    def test_link_at_beginning(self):
        input_nodes = [
            TextNode("[First link](https://example.com/first) followed by text", TextType.TEXT)
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 2)

        # Second part: the link
        self.assertEqual(result[0].text, "First link")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "https://example.com/first")

        # Third part: text after link
        self.assertEqual(result[1].text, " followed by text")
        self.assertEqual(result[1].text_type, TextType.TEXT)

    def test_link_at_end(self):
        input_nodes = [
            TextNode("Text followed by [last link](https://example.com/last)", TextType.TEXT)
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 2)

        # First part: text before link
        self.assertEqual(result[0].text, "Text followed by ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        # Second part: the link
        self.assertEqual(result[1].text, "last link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com/last")

    def test_empty_link_text(self):
        input_nodes = [
            TextNode("Link with no text: [](https://example.com/empty)", TextType.TEXT)
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 2)

        # First part: text before link
        self.assertEqual(result[0].text, "Link with no text: ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        # Second part: the link
        self.assertEqual(result[1].text, "")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com/empty")

    def test_special_characters_in_url(self):
        input_nodes = [
            TextNode(
                "Special URL: [Special](https://example.com/page-with_special-chars.html?param=value&other=123)",
                TextType.TEXT
            )
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 2)

        # Second part: the link
        self.assertEqual(result[1].text, "Special")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com/page-with_special-chars.html?param=value&other=123")

    def test_multiple_nodes(self):
        input_nodes = [
            TextNode("First node with [link1](https://example.com/link1)", TextType.TEXT),
            TextNode("Second node without links", TextType.BOLD),
            TextNode("Third node with [link2](https://example.com/link2)", TextType.ITALIC)
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 5)

        # First node, first part
        self.assertEqual(result[0].text, "First node with ")
        self.assertEqual(result[0].text_type, TextType.TEXT)

        # First node, second part (link)
        self.assertEqual(result[1].text, "link1")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com/link1")

        # Second node
        self.assertEqual(result[2].text, "Second node without links")
        self.assertEqual(result[2].text_type, TextType.BOLD)

        # Third node, first part
        self.assertEqual(result[3].text, "Third node with ")
        self.assertEqual(result[3].text_type, TextType.ITALIC)

        # Third node, second part (link)
        self.assertEqual(result[4].text, "link2")
        self.assertEqual(result[4].text_type, TextType.LINK)
        self.assertEqual(result[4].url, "https://example.com/link2")

    def test_preservation_of_text_type(self):
        input_nodes = [
            TextNode("Bold text with [link](https://example.com/link)", TextType.BOLD)
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 2)

        # Text before link
        self.assertEqual(result[0].text, "Bold text with ")
        self.assertEqual(result[0].text_type, TextType.BOLD)

        # The link
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)

    def test_empty_nodes_filtered_out(self):
        input_nodes = [
            TextNode("[Link only](https://example.com/only)", TextType.TEXT),
            TextNode("[](https://example.com/empty-text)", TextType.TEXT)
        ]
        result = split_nodes_link(input_nodes)

        # Should have 2 nodes (the links) since the text nodes before and after are empty
        self.assertEqual(len(result), 2)

        # First link
        self.assertEqual(result[0].text, "Link only")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "https://example.com/only")

        # Second link with empty text
        self.assertEqual(result[1].text, "")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com/empty-text")

    def test_complex_link_text(self):
        input_nodes = [
            TextNode("Link with [*formatted* text](https://example.com/formatted)", TextType.TEXT)
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 2)

        # The link part
        self.assertEqual(result[1].text, "*formatted* text")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com/formatted")

    def test_image_vs_link(self):
        input_nodes = [
            TextNode("A [link](https://example.com/link) and an ![image](https://example.com/image.jpg)", TextType.TEXT)
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 3)

        # First part: text before link
        self.assertEqual(result[0].text, "A ")

        # Second part: the link
        self.assertEqual(result[1].text, "link")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example.com/link")

        # Third part: text after link including the image markdown
        self.assertEqual(result[2].text, " and an ![image](https://example.com/image.jpg)")

    def test_adjacent_links(self):
        input_nodes = [
            TextNode("[Link1](https://example1.com)[Link2](https://example2.com)", TextType.TEXT)
        ]
        result = split_nodes_link(input_nodes)

        self.assertEqual(len(result), 2)

        # First link
        self.assertEqual(result[0].text, "Link1")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "https://example1.com")

        # Second link
        self.assertEqual(result[1].text, "Link2")
        self.assertEqual(result[1].text_type, TextType.LINK)
        self.assertEqual(result[1].url, "https://example2.com")

    def test_empty_url(self):
        input_nodes = [
            TextNode("[Text with no URL]()", TextType.TEXT)
        ]
        result = split_nodes_link(input_nodes)

        # Function should still create a link node even with empty URL
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Text with no URL")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "")

    def test_filter_behavior(self):
        input_nodes = [
            TextNode("[Empty text](https://example.com)", TextType.TEXT),
            TextNode("[Text with empty URL]()", TextType.TEXT),
            TextNode("", TextType.TEXT),  # Empty node
            TextNode("", TextType.LINK, "https://example.com")  # Empty text but has URL
        ]
        result = split_nodes_link(input_nodes)

        # Should keep nodes with text or with URLs
        self.assertEqual(len(result), 3)

        # First link
        self.assertEqual(result[0].text, "Empty text")
        self.assertEqual(result[0].text_type, TextType.LINK)
        self.assertEqual(result[0].url, "https://example.com")

        self.assertEqual(result[2].text, "")
        self.assertEqual(result[2].text_type, TextType.LINK)
        self.assertEqual(result[2].url, "https://example.com")

if __name__ == "__main__":
    unittest.main()
