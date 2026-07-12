from textnode import TextNode, TextType
from htmlnode import LeafNode
from variables import supported_delimiters

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.PLAIN:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception(f"Unknown TextType: {text_node.text_type}")
    
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    if delimiter not in supported_delimiters:
        raise Exception(f"Delimiter '{delimiter}' is not supported. Supported delimiters are: {supported_delimiters}")
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
        elif delimiter not in old_node.text:
                new_nodes.append(old_node)
                continue
        else:
            split_texts = old_node.text.split(delimiter)
            for i in range(len(split_texts)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_texts[i], TextType.PLAIN))
                else:
                    new_nodes.append(TextNode(split_texts[i], text_type))
    return new_nodes
            
        