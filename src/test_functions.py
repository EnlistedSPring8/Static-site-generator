import unittest

from textnode import TextNode, TextType, Enum

from functions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestFunctions(unittest.TestCase):
    def test_text_node_to_html_node_plain(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_text_node_to_html_node_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_text_node_to_html_node_link(self):
        node = TextNode("This is a text node", TextType.LINK, url="https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.boot.dev">This is a text node</a>')

    def test_text_node_to_html_node_image(self):
        node = TextNode("This is an image", TextType.IMAGE, url="https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="https://www.boot.dev" alt="This is an image"/>')

    def test_text_node_to_html_node_unknown_type(self):
        class UnknownTextType(Enum):
            UNKNOWN = 99

        node = TextNode("This is a text node", UnknownTextType.UNKNOWN)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_split_nodes_delimiter_plain(self):
        nodes = [TextNode("This is a text node")]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 1)

    def test_split_nodes_delimiter_with_italic(self):
        nodes = [TextNode("This is _italic_ text")]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " text")
    
    def test_split_nodes_delimiter_with_bold(self):
        nodes = [TextNode("This is **bold** text")]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " text")
    
    def test_split_nodes_delimiter_with_code(self):
        nodes = [TextNode("This is `code` text")]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " text")
    
    def test_split_nodes_delimiter_with_unsupported_delimiter(self):
        nodes = [TextNode("This is a text node")]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "unsupported", TextType.ITALIC)
    
    def test_split_nodes_delimiter_with_multiple_delimiters(self):
        nodes = [TextNode("This is _italic_ and **bold** text")]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, " text")
    
    def test_extract_markdown_images(self):
        text = "This is an image ![alt text](https://www.boot.dev/image.png) in the text."
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0][0], "alt text")
        self.assertEqual(images[0][1], "https://www.boot.dev/image.png")
    
    def test_extract_markdown_links_nothing_to_extract(self):
        text = "This is a text with no links."
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)
    
    def test_extract_markdown_links(self):
        text = "This is a link [link text](https://www.boot.dev) in the text."
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0][0], "link text")
        self.assertEqual(links[0][1], "https://www.boot.dev")