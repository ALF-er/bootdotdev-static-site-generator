import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_parent_node_with_children(self):
        leaf1 = LeafNode("p", "First paragraph")
        leaf2 = LeafNode("p", "Second paragraph")
        parent = ParentNode("div", [leaf1, leaf2])
        expected = "<div><p>First paragraph</p><p>Second paragraph</p></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_parent_node_with_props(self):
        leaf = LeafNode("span", "Hello world")
        parent = ParentNode("div", [leaf], {"class": "container", "id": "main"})
        html = parent.to_html()
        self.assertTrue(html.startswith("<div "))
        self.assertTrue(html.endswith("</div>"))
        self.assertIn('class="container"', html)
        self.assertIn('id="main"', html)
        self.assertIn("<span>Hello world</span>", html)
        self.assertEqual(html, '<div class="container" id="main"><span>Hello world</span></div>')

    def test_parent_node_with_nested_children(self):
        inner_leaf = LeafNode("b", "Bold text")
        inner_parent = ParentNode("p", [inner_leaf])
        outer_parent = ParentNode("div", [inner_parent])
        expected = "<div><p><b>Bold text</b></p></div>"
        self.assertEqual(outer_parent.to_html(), expected)

    def test_parent_node_with_none_tag(self):
        leaf = LeafNode("p", "Paragraph")
        parent = ParentNode(None, [leaf])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "ParentNode.tag is mandatory")

    def test_parent_node_with_none_children(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertEqual(str(context.exception), "ParentNode.children is mandatory")

    def test_parent_node_with_empty_children_list(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_repr_method(self):
        leaf = LeafNode("p", "Paragraph")
        parent = ParentNode("div", [leaf], {"class": "container"})
        # Note: The actual string representation depends on how LeafNode.__repr__ is implemented
        self.assertTrue(repr(parent).startswith("ParentNode(div, ["))
        self.assertTrue(repr(parent).endswith("], {'class': 'container'})"))

if __name__ == "__main__":
    unittest.main()
