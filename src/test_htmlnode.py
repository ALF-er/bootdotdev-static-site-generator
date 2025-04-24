import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_valid_props(self):
        node = HTMLNode(props={"class": "container", "id": "main"})
        result = node.props_to_html()
        # Check that both properties are in the result
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
        # Check the format - should have a space at the beginning and between attributes
        self.assertTrue(result.startswith(' '))
        self.assertEqual(result, ' class="container" id="main"')

    def test_props_to_html_with_none_props(self):
        node = HTMLNode(props=None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode(props={})
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_repr_method(self):
        node = HTMLNode("div", "Hello", [HTMLNode("span")], {"class": "greeting"})
        expected = "HTMLNode(div, Hello, [HTMLNode(span, None, None, None)], {'class': 'greeting'})"
        self.assertEqual(repr(node), expected)

    def test_to_html_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
