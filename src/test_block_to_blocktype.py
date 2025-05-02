import unittest

from block_to_blocktype import block_to_blocktype, BlockType

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        # Test single-level heading
        self.assertEqual(block_to_blocktype("# Heading 1"), BlockType.HEADING)
        # Test multi-level heading
        self.assertEqual(block_to_blocktype("### Heading 3"), BlockType.HEADING)
        # Test heading with additional content
        self.assertEqual(block_to_blocktype("# Heading with **bold** and *italic*"), BlockType.HEADING)

    def test_code_block(self):
        # Test simple code block
        code_block = "```\nprint('Hello World')\n```"
        self.assertEqual(block_to_blocktype(code_block), BlockType.CODE)

        # Test code block with language specified
        code_block_with_lang = "```python\ndef hello():\n    print('Hello World')\n```"
        self.assertEqual(block_to_blocktype(code_block_with_lang), BlockType.CODE)

        # Test code block with multiple lines
        multi_line_code = "```\nline 1\nline 2\nline 3\n```"
        self.assertEqual(block_to_blocktype(multi_line_code), BlockType.CODE)

    def test_quote(self):
        # Test single line quote
        self.assertEqual(block_to_blocktype("> This is a quote"), BlockType.QUOTE)

        # Test multi-line quote
        multi_line_quote = "> Line 1\n> Line 2\n> Line 3"
        self.assertEqual(block_to_blocktype(multi_line_quote), BlockType.QUOTE)

        # Test nested quote
        nested_quote = "> Outer quote\n> > Inner quote"
        self.assertEqual(block_to_blocktype(nested_quote), BlockType.QUOTE)

    def test_unordered_list(self):
        # Test single item list
        self.assertEqual(block_to_blocktype("- Item 1"), BlockType.UNORDERED_LIST)

        # Test multi-item list
        multi_item_list = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_blocktype(multi_item_list), BlockType.UNORDERED_LIST)

        # Test list with nested content
        nested_list = "- Item 1\n- Item 2 with **bold** text\n- Item 3 with *italic* text"
        self.assertEqual(block_to_blocktype(nested_list), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        # Test single item ordered list
        self.assertEqual(block_to_blocktype("1. Item 1"), BlockType.ORDERED_LIST)

        # Test multi-item ordered list
        multi_item_list = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_blocktype(multi_item_list), BlockType.ORDERED_LIST)

        # Test ordered list with nested content
        nested_list = "1. Item 1\n2. Item 2 with **bold** text\n3. Item 3 with *italic* text"
        self.assertEqual(block_to_blocktype(nested_list), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        # Test simple paragraph
        self.assertEqual(block_to_blocktype("This is a paragraph"), BlockType.PARAGRAPH)

        # Test multi-line paragraph
        multi_line = "Line 1\nLine 2\nLine 3"
        self.assertEqual(block_to_blocktype(multi_line), BlockType.PARAGRAPH)

        # Test paragraph with markdown formatting
        formatted = "This is a paragraph with **bold** and *italic* text, and a [link](https://example.com)"
        self.assertEqual(block_to_blocktype(formatted), BlockType.PARAGRAPH)

    def test_edge_cases(self):
        # Test malformed ordered list (wrong numbering)
        wrong_numbering = "1. Item 1\n3. Item 2\n4. Item 3"
        self.assertEqual(block_to_blocktype(wrong_numbering), BlockType.PARAGRAPH)

        # Test malformed unordered list (missing space after dash)
        wrong_unordered = "-Item 1\n-Item 2\n-Item 3"
        self.assertEqual(block_to_blocktype(wrong_unordered), BlockType.PARAGRAPH)

        # Test mixed list (should be classified as paragraph)
        mixed_list = "1. Item 1\n- Item 2\n3. Item 3"
        self.assertEqual(block_to_blocktype(mixed_list), BlockType.PARAGRAPH)

        # Test empty string (might cause an index error if not handled)
        try:
            block_to_blocktype("")
            self.fail("Empty string should raise an IndexError")
        except IndexError:
            pass

if __name__ == "__main__":
    unittest.main()
