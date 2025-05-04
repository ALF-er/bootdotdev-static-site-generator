import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_basic_h1(self):
        markdown = "# This is a title"
        self.assertEqual(extract_title(markdown), "This is a title")

    def test_title_with_spaces(self):
        markdown = "#    Title with spaces    "
        self.assertEqual(extract_title(markdown), "Title with spaces")

    def test_multiple_headings(self):
        markdown = "# First heading\n\nSome content\n\n## Second heading"
        self.assertEqual(extract_title(markdown), "First heading")

    def test_heading_not_at_beginning(self):
        markdown = "Some text before\n\n# The title\n\nMore text"
        self.assertEqual(extract_title(markdown), "The title")

    def test_heading_with_special_chars(self):
        markdown = "# Title with: special! characters?"
        self.assertEqual(extract_title(markdown), "Title with: special! characters?")

    def test_heading_with_hash(self):
        markdown = "# Title with # symbol"
        self.assertEqual(extract_title(markdown), "Title with # symbol")

    def test_no_heading(self):
        markdown = "This is a document with no headings"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no titles in markdown")

    def test_empty_string(self):
        markdown = ""
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "no titles in markdown")

    def test_heading_with_markdown_formatting(self):
        markdown = "# Title with *italic* and **bold**"
        self.assertEqual(extract_title(markdown), "Title with *italic* and **bold**")

if __name__ == "__main__":
    unittest.main()
