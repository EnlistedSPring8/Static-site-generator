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
    
if __name__ == "__main__":
    unittest.main()