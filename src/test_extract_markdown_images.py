import unittest
from extract_markdown_images import extract_markdown_images

class TestExtractMarkdownImages(unittest.TestCase):
    def test_basic_image(self):
        markdown = "![Alt text](https://example.com/image.jpg)"
        expected = [("Alt text", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_multiple_images(self):
        markdown = """
        # Document with multiple images

        First image: ![First](https://example.com/first.jpg)

        Second image: ![Second](https://example.com/second.png)
        """
        expected = [
            ("First", "https://example.com/first.jpg"),
            ("Second", "https://example.com/second.png")
        ]
        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_empty_alt_text(self):
        markdown = "This is an image with empty alt text: ![](https://example.com/empty.jpg)"
        expected = [("", "https://example.com/empty.jpg")]
        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_special_characters_in_url(self):
        markdown = "![Special](https://example.com/image-with_special-chars.jpg?param=value&other=123)"
        expected = [("Special", "https://example.com/image-with_special-chars.jpg?param=value&other=123")]
        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_quoted_url(self):
        markdown = """
        Single quotes: ![Single](\'https://example.com/single.jpg\')
        Double quotes: ![Double](\"https://example.com/double.jpg\")
        """
        expected = [
            ("Single", "https://example.com/single.jpg"),
            ("Double", "https://example.com/double.jpg")
        ]
        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_with_title(self):
        markdown = "![Alt text](https://example.com/image.jpg \"Image title\")"
        expected = [("Alt text", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_whitespace(self):
        markdown = """
        No spaces: ![Alt](https://example.com/image.jpg)
        Spaces after alt: ![Alt ]( https://example.com/image.jpg )
        Spaces everywhere: ![ Alt text ]( https://example.com/image.jpg )
        """
        expected = [
            ("Alt", "https://example.com/image.jpg"),
            ("Alt", "https://example.com/image.jpg"),
            ("Alt text", "https://example.com/image.jpg")
        ]
        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_no_images(self):
        markdown = "This is a paragraph with no images, just text."
        expected = []
        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_complex_alt_text(self):
        markdown = """
        ![Alt text with (parentheses)](https://example.com/image1.jpg)
        ![Alt text with [brackets]](https://example.com/image2.jpg)
        ![Alt text with *asterisks*](https://example.com/image3.jpg)
        """
        expected = [
            ("Alt text with (parentheses)", "https://example.com/image1.jpg"),
            ("Alt text with [brackets]", "https://example.com/image2.jpg"),
            ("Alt text with *asterisks*", "https://example.com/image3.jpg")
        ]
        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_ignore_links(self):
        markdown = """
        This is a paragraph with an ![image](https://example.com/image.jpg) in the middle.

        This is a link [not an image](https://example.com)
        """
        expected = [("image", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(markdown), expected)

    def test_malformed_syntax(self):
        markdown = """
        Missing closing bracket: ![Alt text(https://example.com/image1.jpg)
        Missing closing parenthesis: ![Alt text](https://example.com/image2.jpg
        No URL: ![Alt text]()
        """
        expected = [("Alt text", "")]
        self.assertEqual(extract_markdown_images(markdown), expected)

if __name__ == "__main__":
    unittest.main()
