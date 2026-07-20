import unittest

from textnode import TextNode, TextType, Enum

from blocktype import BlockType

from functions import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from functions import text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestFunctionsOne(unittest.TestCase):
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

    def test_extract_markdown_links_multiple(self):
        text = "This is a link [link text](https://www.boot.dev) and another link [another link](https://www.example.com) in the text."
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0][0], "link text")
        self.assertEqual(links[0][1], "https://www.boot.dev")
        self.assertEqual(links[1][0], "another link")
        self.assertEqual(links[1][1], "https://www.example.com")
    
    def test_extract_markdown_links_with_image(self):
        text = "This is a link [link text](https://www.boot.dev) and an image ![alt text](https://www.boot.dev/image.png) in the text."
        links = extract_markdown_links(text)
        images = extract_markdown_images(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0][0], "link text")
        self.assertEqual(links[0][1], "https://www.boot.dev")
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0][0], "alt text")
        self.assertEqual(images[0][1], "https://www.boot.dev/image.png")
    
    def test_extract_markdown_links_with_no_links(self):
        text = "This is a text with no links."
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)
    
    def test_extract_markdown_links_with_half_links(self):
        text = "This is a link [link text](https://www.boot.dev) and a broken link [broken link](https://www.example.com"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0][0], "link text")
        self.assertEqual(links[0][1], "https://www.boot.dev")

    def test_extract_markdown_images_with_half_images(self):
        text = "This is an image ![alt text](https://www.boot.dev/image.png) and a broken image ![broken image](https://www.example.com/image.png"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0][0], "alt text")
        self.assertEqual(images[0][1], "https://www.boot.dev/image.png")
    
    def test_extract_markdown_images_with_no_images(self):
        text = "This is a text with no images."
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.example.com)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://www.example.com"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_with_no_links(self):
        node = TextNode(
            "This is text with no links",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.PLAIN),
            ],
            new_nodes,
        )
    
    def test_split_images_with_no_images(self):
        node = TextNode(
            "This is text with no images",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.PLAIN),
            ],
            new_nodes,
        )
    
    def test_split_links_with_image(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_with_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes,
        )
    
    def test_split_links_with_image_and_no_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and no links",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and no links", TextType.PLAIN),
            ],
            new_nodes,
        )
    
    def test_split_images_with_link_and_no_images(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and no images",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and no images", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is a link [link text](https://www.boot.dev) and an image ![alt text](https://www.boot.dev/image.png) in the text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "This is a link ")
        self.assertEqual(nodes[1].text, "link text")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://www.boot.dev")
        self.assertEqual(nodes[2].text, " and an image ")
        self.assertEqual(nodes[3].text, "alt text")
        self.assertEqual(nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(nodes[3].url, "https://www.boot.dev/image.png")
        self.assertEqual(nodes[4].text, " in the text.")

    def test_text_to_textnodes_with_bold_and_italic(self):
        text = "This is **bold** and _italic_ text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " and ")
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " text.")
    
    def test_text_to_textnodes_with_code(self):
        text = "This is `code` text."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " text.")
    
    def test_text_to_textnodes_with_all(self):
        text = "This is **bold**, _italic_, `code`, a [link](https://www.boot.dev), and an ![image](https://www.boot.dev/image.png)."
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 11)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, ", ")
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, ", ")
        self.assertEqual(nodes[5].text, "code")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, ", a ")
        self.assertEqual(nodes[7].text, "link")
        self.assertEqual(nodes[7].text_type, TextType.LINK)
        self.assertEqual(nodes[7].url, "https://www.boot.dev")
        self.assertEqual(nodes[8].text, ", and an ")
        self.assertEqual(nodes[9].text, "image")
        self.assertEqual(nodes[9].text_type, TextType.IMAGE)
        self.assertEqual(nodes[9].url, "https://www.boot.dev/image.png")
        self.assertEqual(nodes[10].text, ".")

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code`here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code`here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_with_empty_lines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code`here
This is the same paragraph on a new line


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code`here\nThis is the same paragraph on a new line",
            ],
        )

    def test_markdown_to_blocks_with_no_paragraphs(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_with_only_empty_lines(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_markdown_to_blocks_with_only_whitespace_lines(self):
        md = "   \n  \n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\npython print('Hello, world!')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- This is an unordered list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. This is an ordered list item"), BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_with_invalid_block(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("   "), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("\n\n"), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_with_edge_cases(self):
        self.assertEqual(block_to_block_type("#This is not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```This is not a code block```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(">This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("-This is not an unordered list item"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.This is not an ordered list item"), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

    def test_heading_1(self):
        md = """
# This is a heading with a **bold element**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading with a <b>bold element</b></h1></div>"
        )
    def test_heading_2(self):
        md = """
## This is a heading with a **bold element**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h2>This is a heading with a <b>bold element</b></h2></div>"
        )
    
    
    def test_heading_4(self):
        md = """
#### This is a heading with a **bold element** and _italic element_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>This is a heading with a <b>bold element</b> and <i>italic element</i></h4></div>"
        )

    def test_heading_5(self):
        md = """
##### This is a heading with a **bold element** and _italic element_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h5>This is a heading with a <b>bold element</b> and <i>italic element</i></h5></div>"
        )

    def test_heading_6(self):
        md = """
###### This is a heading with a **bold element** and _italic element_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This is a heading with a <b>bold element</b> and <i>italic element</i></h6></div>"
        )
    
    def test_heading_too_much(self):
        md = """
####### This is a heading with a **bold element** and _italic element_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>####### This is a heading with a <b>bold element</b> and <i>italic element</i></p></div>"
        )

    def test_quote_block(self):
        md = """
>This is a **bold** quote with an _italian_ twist
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a <b>bold</b> quote with an <i>italian</i> twist</blockquote></div>"
        )
    
    def test_unordered_list(self):
        md = """
- Item one
- **Bold** item
- Item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one</li><li><b>Bold</b> item</li><li>Item with <code>code</code></li></ul></div>"
        )

    def test_unordered_list_with_dash_in_middle(self):
        md = """
- Item - one
- **Bold** item
- Item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item - one</li><li><b>Bold</b> item</li><li>Item with <code>code</code></li></ul></div>"
        )
    
    def test_ordered_list_with_dash_in_middle(self):
        md = """
1. Item - one
2. **Bold** item
3. Item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item - one</li><li><b>Bold</b> item</li><li>Item with <code>code</code></li></ol></div>"
        )

    def test_code_blocks_multiple_lines(self):
        md = """
```
This should remain **the same**
even with the
_inline_ stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This should remain **the same**\neven with the\n_inline_ stuff\n</code></pre></div>"
        )

    def multiple_different_blocks(self):
        md = """
# **Heading**

- Item - list
- _italic_ item
- `code item`

```
**code** stuff
to check
that everything works
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1><b>Heading</b></h1><ul><li>Item - list</li><li><i>italic</i> item</li><li><code>code item</code></li></ul><pre><code>**code** stuff\nto check\nthat everything works\n</code></pre></div>"
        )


