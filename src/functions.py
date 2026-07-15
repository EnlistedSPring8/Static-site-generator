from pydoc import text

from textnode import TextNode, TextType
from htmlnode import LeafNode
from variables import supported_delimiters
import re

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
            
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r'[^!]\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
        else:
            images = extract_markdown_images(old_node.text)
            if not images:
                new_nodes.append(old_node)
                continue
            last_index = 0
            for alt_text, url in images:
                start_index = old_node.text.find(f"![{alt_text}]({url})", last_index)
                if start_index > last_index:
                    new_nodes.append(TextNode(old_node.text[last_index:start_index], TextType.PLAIN))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))
                last_index = start_index + len(f"![{alt_text}]({url})")
            if last_index < len(old_node.text):
                new_nodes.append(TextNode(old_node.text[last_index:], TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN:
            new_nodes.append(old_node)
        else:
            links = extract_markdown_links(old_node.text)
            if not links:
                new_nodes.append(old_node)
                continue
            last_index = 0
            for link_text, url in links:
                start_index = old_node.text.find(f"[{link_text}]({url})", last_index)
                if start_index > last_index:
                    new_nodes.append(TextNode(old_node.text[last_index:start_index], TextType.PLAIN))
                new_nodes.append(TextNode(link_text, TextType.LINK, url=url))
                last_index = start_index + len(f"[{link_text}]({url})")
            if last_index < len(old_node.text):
                new_nodes.append(TextNode(old_node.text[last_index:], TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes