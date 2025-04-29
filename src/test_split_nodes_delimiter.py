import unittest

from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextType, TextNode

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_splitting(self):
        input_nodes = [TextNode("Hello *world*!", TextType.NORMAL)]
        expected = [
            TextNode("Hello ", TextType.NORMAL),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.NORMAL)
        ]
        result = split_nodes_delimiter(input_nodes, "*", TextType.BOLD)

        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_multiple_delimiters(self):
        input_nodes = [TextNode("This is *bold* and this is *also bold*", TextType.NORMAL)]
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is ", TextType.NORMAL),
            TextNode("also bold", TextType.BOLD),
        ]
        result = split_nodes_delimiter(input_nodes, "*", TextType.BOLD)

        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_non_normal_nodes_unchanged(self):
        input_nodes = [
            TextNode("Normal text", TextType.NORMAL),
            TextNode("Bold text *with delimiters*", TextType.BOLD),
            TextNode("*More* normal text", TextType.NORMAL)
        ]
        expected = [
            TextNode("Normal text", TextType.NORMAL),
            TextNode("Bold text *with delimiters*", TextType.BOLD),
            TextNode("More", TextType.ITALIC),
            TextNode(" normal text", TextType.NORMAL)
        ]
        result = split_nodes_delimiter(input_nodes, "*", TextType.ITALIC)

        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_empty_input(self):
        input_nodes = []
        result = split_nodes_delimiter(input_nodes, "*", TextType.BOLD)
        self.assertEqual(result, [])

    def test_no_delimiters_in_text(self):
        input_nodes = [TextNode("Plain text without delimiters", TextType.NORMAL)]
        expected = [TextNode("Plain text without delimiters", TextType.NORMAL)]
        result = split_nodes_delimiter(input_nodes, "*", TextType.BOLD)

        self.assertEqual(len(result), len(expected))
        self.assertEqual(result[0].text, expected[0].text)
        self.assertEqual(result[0].text_type, expected[0].text_type)

    def test_unbalanced_delimiters(self):
        input_nodes = [TextNode("Unbalanced *delimiters", TextType.NORMAL)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(input_nodes, "*", TextType.BOLD)

        self.assertTrue("invalid markdown syntax" in str(context.exception))

    def test_different_delimiters(self):
        input_nodes = [TextNode("This is _italic_ text", TextType.NORMAL)]
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.NORMAL)
        ]
        result = split_nodes_delimiter(input_nodes, "_", TextType.ITALIC)

        self.assertEqual(len(result), len(expected))
        for i in range(len(result)):
            self.assertEqual(result[i].text, expected[i].text)
            self.assertEqual(result[i].text_type, expected[i].text_type)

    def test_multiple_node_types(self):
        input_nodes = [
            TextNode("This `is code` and ", TextType.NORMAL),
            TextNode("this is a link", TextType.LINK),
            TextNode(" and *this is bold*", TextType.NORMAL)
        ]

        # First process backticks for code
        result1 = split_nodes_delimiter(input_nodes, "`", TextType.CODE)
        expected1 = [
            TextNode("This ", TextType.NORMAL),
            TextNode("is code", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("this is a link", TextType.LINK),
            TextNode(" and *this is bold*", TextType.NORMAL)
        ]

        # Then process asterisks for bold
        result2 = split_nodes_delimiter(result1, "*", TextType.BOLD)
        expected2 = [
            TextNode("This ", TextType.NORMAL),
            TextNode("is code", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("this is a link", TextType.LINK),
            TextNode(" and ", TextType.NORMAL),
            TextNode("this is bold", TextType.BOLD),
        ]

        # Check first transformation
        self.assertEqual(len(result1), len(expected1))
        for i in range(len(result1)):
            self.assertEqual(result1[i].text, expected1[i].text)
            self.assertEqual(result1[i].text_type, expected1[i].text_type)

        # Check second transformation
        self.assertEqual(len(result2), len(expected2))
        for i in range(len(result2)):
            self.assertEqual(result2[i].text, expected2[i].text)
            self.assertEqual(result2[i].text_type, expected2[i].text_type)

if __name__ == "__main__":
    unittest.main()
