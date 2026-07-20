import unittest

from functions import markdown_to_html_node, extract_title, text_to_children
from blocktype import BlockType

class TestFunctionsTwo(unittest.TestCase):
    def test_multiple_different_blocks(self):
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
    
    def test_empty_md(self):
        md = ""
        self.assertRaises(TypeError, markdown_to_html_node(md))
    
    def test_extract_title(self):
        md = "# Title"
        title = extract_title(md)
        self.assertEqual(
            title,
            "Title"
        )

    def test_extract_title_error(self):
        md = " Title"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_single_digit_item(self):
        result = markdown_to_html_node("1. Gandalf")
        self.assertEqual(
            result.to_html(),
            "<div><ol><li>Gandalf</li></ol></div>"
        )

    def test_double_digit_item(self):
        result = markdown_to_html_node("""
1. Gandalf
2. Galadriel
3. Gandalf
4. Galadriel
5. Gandalf
6. Galadriel
7. Gandalf
8. Galadriel
9. Gandalf
10. Galadriel
""")
        self.assertEqual(
            result.to_html(),
            "<div><ol><li>Gandalf</li><li>Galadriel</li><li>Gandalf</li><li>Galadriel</li><li>Gandalf</li><li>Galadriel</li><li>Gandalf</li><li>Galadriel</li><li>Gandalf</li><li>Galadriel</li></ol></div>"
        )
    
    def test_link_in_unordered_list(self):
        md = "- [Link text Here](https://link-url-here.org)"
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            '<div><ul><li><a href="https://link-url-here.org">Link text Here</a></li></ul></div>'
        )