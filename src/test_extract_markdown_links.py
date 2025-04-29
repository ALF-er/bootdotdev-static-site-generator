import unittest
from extract_markdown_links import extract_markdown_links

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_basic_link(self):
        markdown = "[Link text](https://example.com)"
        expected = [("Link text", "https://example.com")]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_multiple_links(self):
        markdown = """
        # Document with multiple links

        First link: [GitHub](https://github.com)

        Second link: [Google](https://google.com)
        """
        expected = [
            ("GitHub", "https://github.com"),
            ("Google", "https://google.com")
        ]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_empty_link_text(self):
        markdown = "This is a link with empty text: [](https://example.com/empty)"
        expected = [("", "https://example.com/empty")]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_special_characters_in_url(self):
        markdown = "[Special](https://example.com/page-with_special-chars.html?param=value&other=123)"
        expected = [("Special", "https://example.com/page-with_special-chars.html?param=value&other=123")]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_quoted_url(self):
        markdown = """
        Single quotes: [Single](\'https://example.com/single\')
        Double quotes: [Double](\"https://example.com/double\")
        """
        expected = [
            ("Single", "https://example.com/single"),
            ("Double", "https://example.com/double")
        ]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_with_title(self):
        markdown = "[Link text](https://example.com \"Link title\")"
        expected = [("Link text", "https://example.com")]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_whitespace(self):
        markdown = """
        No spaces: [Link](https://example.com)
        Spaces after text: [Link ]( https://example.com )
        Spaces everywhere: [ Link text ]( https://example.com )
        """
        expected = [
            ("Link", "https://example.com"),
            ("Link", "https://example.com"),
            ("Link text", "https://example.com")
        ]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_no_links(self):
        markdown = "This is a paragraph with no links, just text."
        expected = []
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_complex_link_text(self):
        markdown = """
        [Link text with (parentheses)](https://example.com/page1)
        [Link text with [brackets]](https://example.com/page2)
        [Link text with *asterisks*](https://example.com/page3)
        """
        expected = [
            ("Link text with (parentheses)", "https://example.com/page1"),
            ("Link text with [brackets]", "https://example.com/page2"),
            ("Link text with *asterisks*", "https://example.com/page3")
        ]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_ignores_image_links(self):
        markdown = """
        This is a regular link: [Link](https://example.com)
        This is an image: ![Image](https://example.com/image.jpg)
        This is another link: [Another](https://example.com/another)
        """
        expected = [
            ("Link", "https://example.com"),
            ("Another", "https://example.com/another")
        ]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_link_with_code(self):
        markdown = "[Link with `code`](https://example.com/code)"
        expected = [("Link with `code`", "https://example.com/code")]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_email_links(self):
        markdown = "[Contact us](mailto:example@example.com)"
        expected = [("Contact us", "mailto:example@example.com")]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_relative_links(self):
        markdown = """
        [Home page](/home)
        [About page](../about)
        [Documentation](./docs/index.html)
        """
        expected = [
            ("Home page", "/home"),
            ("About page", "../about"),
            ("Documentation", "./docs/index.html")
        ]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_malformed_syntax(self):
        markdown = """
        Missing closing bracket: [Link text(https://example.com/page1)
        Missing closing parenthesis: [Link text](https://example.com/page2
        No URL: [Link text]()
        """
        expected = [("Link text", "")]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_adjacent_links(self):
        markdown = "[Link1](https://example1.com)[Link2](https://example2.com)"
        expected = [
            ("Link1", "https://example1.com"),
            ("Link2", "https://example2.com")
        ]
        self.assertEqual(extract_markdown_links(markdown), expected)

    def test_complex_mixed_content(self):
        markdown = """
        # Document with mixed content

        Here's a [link](https://example.com) and an ![image](https://example.com/image.jpg)

        This paragraph has multiple [links](https://example1.com) and more [links](https://example2.com)
        as well as multiple ![images](https://example.com/img1.jpg) and ![more images](https://example.com/img2.jpg)
        """
        expected = [
            ("link", "https://example.com"),
            ("links", "https://example1.com"),
            ("links", "https://example2.com"),
        ]
        self.assertEqual(extract_markdown_links(markdown), expected)

if __name__ == "__main__":
    unittest.main()
