import unittest

from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_simple_blocks(self):
        text = "This is the first paragraph.\n\nThis is the second paragraph."
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "This is the first paragraph.")
        self.assertEqual(blocks[1], "This is the second paragraph.")

    def test_multiple_blocks(self):
        text = "First block.\n\nSecond block.\n\nThird block.\n\nFourth block."
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[0], "First block.")
        self.assertEqual(blocks[1], "Second block.")
        self.assertEqual(blocks[2], "Third block.")
        self.assertEqual(blocks[3], "Fourth block.")

    def test_strip_whitespace(self):
        text = "  Block with leading spaces.  \n\n\tBlock with leading tab.\t"
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "Block with leading spaces.")
        self.assertEqual(blocks[1], "Block with leading tab.")

    def test_filter_empty_blocks(self):
        text = "First block.\n\n\n\nSecond block.\n\n\n\n\nThird block."
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "First block.")
        self.assertEqual(blocks[1], "Second block.")
        self.assertEqual(blocks[2], "Third block.")

    def test_empty_input(self):
        text = ""
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 0)

    def test_only_whitespace(self):
        text = "   \n\n   \t   \n\n   "
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 0)

    def test_single_block(self):
        text = "This is a single block with no paragraph breaks."
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0], "This is a single block with no paragraph breaks.")

    def test_preserve_single_newlines(self):
        text = "This has a single\nline break which should not split.\n\nThis is the second paragraph."
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "This has a single\nline break which should not split.")
        self.assertEqual(blocks[1], "This is the second paragraph.")

    def test_markdown_code_block(self):
        text = "Text before.\n\n```\ncode block\nwith multiple\nlines\n```\n\nText after."
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "Text before.")
        self.assertEqual(blocks[1], "```\ncode block\nwith multiple\nlines\n```")
        self.assertEqual(blocks[2], "Text after.")

    def test_markdown_list(self):
        text = "# Heading\n\n- Item 1\n- Item 2\n- Item 3\n\nParagraph after list."
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "- Item 1\n- Item 2\n- Item 3")
        self.assertEqual(blocks[2], "Paragraph after list.")

if __name__ == "__main__":
    unittest.main()
