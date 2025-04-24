import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_node_with_props(self):
        node = LeafNode("span", "Styled text", {"class": "highlight", "id": "intro"})
        html = node.to_html()
        self.assertTrue(html.startswith("<span "))
        self.assertTrue(html.endswith("</span>"))
        self.assertIn('class="highlight"', html)
        self.assertIn('id="intro"', html)
        self.assertIn(">Styled text<", html)
        self.assertEqual(html, '<span class="highlight" id="intro">Styled text</span>')

    def test_leaf_node_with_none_value(self):
        node = LeafNode("div", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "LeafNode must have value")

    def test_repr_method(self):
        node = LeafNode("p", "Hello", {"class": "greeting"})
        expected = "LeafNode(p, Hello, {'class': 'greeting'})"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
