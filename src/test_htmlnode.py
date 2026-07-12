import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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
        leaf = LeafNode(tag="p", value="Hello, World!", props={"class": "my-class"})
        self.assertEqual(leaf.to_html(), '<p class="my-class">Hello, World!</p>')

    def test_leaf_to_html_no_tag(self):
        leaf = LeafNode(tag=None, value="Hello, World!")
        self.assertEqual(leaf.to_html(), 'Hello, World!')
    
    def test_leaf_to_html_no_value(self):
        leaf = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            leaf.to_html()
    
    def test_leaf_repr(self):
        leaf = LeafNode(tag="p", value="Hello, World!", props={"class": "my-class"})
        expected_repr = "LeafNode(tag=p, value=Hello, World!, props={'class': 'my-class'})"
        self.assertEqual(repr(leaf), expected_repr)
    
    def test_parent_to_html(self):
        child1 = LeafNode(tag="p", value="Child 1")
        child2 = LeafNode(tag="p", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "my-class"})
        self.assertEqual(parent.to_html(), '<div class="my-class"><p>Child 1</p><p>Child 2</p></div>')
    
    def test_to_html_with_grandchildren(self):
        grandchild1 = LeafNode(tag="span", value="Grandchild 1")
        grandchild2 = LeafNode(tag="span", value="Grandchild 2")
        child1 = ParentNode(tag="div", children=[grandchild1])
        child2 = ParentNode(tag="div", children=[grandchild2])
        parent = ParentNode(tag="section", children=[child1, child2])
        self.assertEqual(parent.to_html(), '<section><div><span>Grandchild 1</span></div><div><span>Grandchild 2</span></div></section>')

    def test_parent_to_html_no_tag(self):
        child1 = LeafNode(tag="p", value="Child 1")
        child2 = LeafNode(tag="p", value="Child 2")
        parent = ParentNode(tag=None, children=[child1, child2])
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_parent_to_html_no_children(self):
        parent = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            parent.to_html()
    
    def test_parent_repr(self):
        child1 = LeafNode(tag="p", value="Child 1")
        child2 = LeafNode(tag="p", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2], props={"class": "my-class"})
        expected_repr = "ParentNode(tag=div, children=[LeafNode(tag=p, value=Child 1, props={}), LeafNode(tag=p, value=Child 2, props={})], props={'class': 'my-class'})"
        self.assertEqual(repr(parent), expected_repr)

    def test_parent_to_html_with_nested_children(self):
        grandchild1 = LeafNode(tag="span", value="Grandchild 1")
        grandchild2 = LeafNode(tag="span", value="Grandchild 2")
        child1 = ParentNode(tag="div", children=[grandchild1])
        child2 = ParentNode(tag="div", children=[grandchild2])
        parent = ParentNode(tag="section", children=[child1, child2], props={"class": "my-class"})
        self.assertEqual(parent.to_html(), '<section class="my-class"><div><span>Grandchild 1</span></div><div><span>Grandchild 2</span></div></section>')

if __name__ == "__main__":
    unittest.main()