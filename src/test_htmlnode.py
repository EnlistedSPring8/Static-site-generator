import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def props_to_html_empty_props(self):
        node = HTMLNode(tag="div", value="Hello, World!")
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_with_props(self):
        node = HTMLNode(tag="div", value="Hello, World!", props={"class": "my-class", "id": "my-id"})
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')
    
    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello, World!", props={"class": "my-class", "id": "my-id"})
        expected_repr = "HTMLNode(tag=div, value=Hello, World!, children=[], props={'class': 'my-class', 'id': 'my-id'})"
        self.assertEqual(repr(node), expected_repr)
    
    def test_leaf_to_html_p(self):
        leaf = HTMLNode.LeafNode(tag="p", value="Hello, World!", props={"class": "my-class"})
        self.assertEqual(leaf.to_html(), '<p class="my-class">Hello, World!</p>')

    def test_leaf_to_html_no_tag(self):
        leaf = HTMLNode.LeafNode(tag=None, value="Hello, World!")
        self.assertEqual(leaf.to_html(), 'Hello, World!')
    
    def test_leaf_to_html_no_value(self):
        leaf = HTMLNode.LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            leaf.to_html()
    
    def test_leaf_repr(self):
        leaf = HTMLNode.LeafNode(tag="p", value="Hello, World!", props={"class": "my-class"})
        expected_repr = "LeafNode(tag=p, value=Hello, World!, props={'class': 'my-class'})"
        self.assertEqual(repr(leaf), expected_repr)
        
if __name__ == "__main__":
    unittest.main()