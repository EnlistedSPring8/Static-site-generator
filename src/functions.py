from pydoc import text

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from variables import supported_delimiters, supported_block_types
import re
from blocktype import BlockType
import os, shutil

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
    pattern = r'(?<!!)\[([^\]]+)\]\(([^)]+)\)'
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

def markdown_to_blocks(markdown: str) -> list[str]:
    # raise an exception if there is nothing noteworthy in markdown
    lines = markdown.split("\n\n")
    blocks = []
    for line in lines:
        if len(line) > 0 and not line.isspace():
            line = line.strip()
            blocks.append(line)
    return blocks

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        ## This regex matches headings from level 1 to 6, e.g., "# Heading", "## Heading", ..., "###### Heading"
        ## must have a space after the hashes to be considered a heading
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        ## This regex matches code blocks
        ## must start with ``` + \n and end with ``` to be considered a code block
        return BlockType.CODE
    elif block.startswith(">"):
        ## This regex matches quote blocks
        ## must start with > to be considered a quote block
        return BlockType.QUOTE
    elif re.match(r"^- ", block, re.MULTILINE):
        ## This regex matches unordered lists
        ## must start with - followed by a space to be considered an unordered list item
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\. ", block):
        ## This regex matches ordered lists
        ## must start with a number followed by a period and a space to be considered an ordered list item
        ## We also need to check that the numbers are in order, e.g., "1. Item", "2. Item", etc.
        line_number = 1
        for line in block.splitlines():
            if not re.match(r"^\d+\. ", line):
                return BlockType.PARAGRAPH
            current_number = int(line.split(".")[0])
            if current_number != line_number:
                return BlockType.PARAGRAPH
            line_number += 1
        return BlockType.ORDERED_LIST
    else:
        ## If none of the above patterns match, we consider it a paragraph
        return BlockType.PARAGRAPH

def block_type_to_html_node(block_type: BlockType, block: str) -> HTMLNode:
    if block_type == BlockType.HEADING:
        return ParentNode(f"h{len(block.split(' ')[0])}", text_to_children(block, block_type))   
    elif block_type == BlockType.QUOTE:
        return ParentNode("blockquote", text_to_children(block, block_type))
    elif block_type == BlockType.UNORDERED_LIST:
        unordered_list_item_leaf_nodes = []
        unordered_list_items = block.splitlines()
        for i in unordered_list_items:
            unordered_list_item_leaf_nodes.append(ParentNode("li", text_to_children(i, block_type)))
        return ParentNode("ul", unordered_list_item_leaf_nodes)
    elif block_type == BlockType.ORDERED_LIST:
        ordered_list_item_leaf_nodes = []
        ordered_list_items = block.splitlines()
        for i in ordered_list_items:
            ordered_list_item_leaf_nodes.append(ParentNode("li", text_to_children(i, block_type)))
        return ParentNode("ol", ordered_list_item_leaf_nodes)
    elif block_type == BlockType.PARAGRAPH:
        return ParentNode("p", text_to_children(block, block_type))
    else:
        # if above don't apply we will consider it not to be supported
        raise Exception(f"Block type not supported. Supported block types: {supported_block_types}")

def text_to_children(text: str, block_type: BlockType) -> list[HTMLNode]:
    # code blocks taken care off separately
    # need to take whiteline away
    text = text.strip()
    text_nodes = []

    # header (take the "#xx "away)
    if block_type == BlockType.HEADING:
        text_clean = text.split(re.match(r"^#{1,6} ", text).group())
        text_nodes = text_to_textnodes(text_clean[1])

    # quote (remember to take last > out if it exists)
    elif block_type == BlockType.QUOTE:
        text_lines = text.splitlines()
        cleaned_text_lines = []
        for line in text_lines:
            cleaned_line = line.split(">")
            cleaned_line = cleaned_line[1].strip()
            cleaned_text_lines.append(cleaned_line)

        text_clean = "\n".join(cleaned_text_lines)
        text_nodes.extend(text_to_textnodes(text_clean))

    # unordered list (take "- " away)
    elif block_type == BlockType.UNORDERED_LIST:
        text_clean = text.split("- ", 1)
        for i in text_clean:
            if len(i) != 0:
                text_nodes.extend(text_to_textnodes(i))
            else:
                continue

    # ordered list (take "1. , 2. , etc. away")
    elif block_type == BlockType.ORDERED_LIST:
        lines = text.splitlines()
        for line in lines:
           splitted_line = re.split(r"^\d+. ", line, 1)
           text_nodes.extend(text_to_textnodes(splitted_line[1]))
    
    # If no other block type matches it must be paragraph (error should have happened earlier)
    else:
        splitted_text = text.split("\n")
        joined_text = " ".join(splitted_text)
        text_nodes.extend(text_to_textnodes(joined_text))
    
    # Turning TextNodes to HTMLNodes
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_html_node(markdown: str) -> HTMLNode:
    # split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    # loop over each block
    html_nodes = []
    for block in blocks:
        #determine block type
        # convert block to html node based on block type
        block_type = block_to_block_type(block)

        # determine value or children values in the block_html_node
        if block_type == BlockType.CODE:
            block_text = block.split("```")
            block_text = re.split(r"^\n", block_text[1])
            code_text_node = TextNode(block_text[1], TextType.CODE)
            code_html_child_node = [text_node_to_html_node(code_text_node)]
            code_html_parent_node = ParentNode("pre", code_html_child_node)
            html_nodes.append(code_html_parent_node)
        else:
            html_nodes.append(block_type_to_html_node(block_type, block))

    
    return ParentNode("div", html_nodes)


def copy_directory(from_path: str, dst_path: str) -> None:

    # Make sure the path is valid using os.path.exists
    if not os.path.exists(from_path) or not os.path.exists(dst_path):
        raise Exception("Given paths should be valid paths!")

    # Make a list of the directory or file -names
    to_be_copied_paths = os.listdir(from_path)

    # Loop through the list of the item names
    for path_name in to_be_copied_paths:
        
        # Make a path from the path_name
        path = os.path.join(from_path, path_name)
        
        # if the item in from_path is a file we should copy the file to the destination path
        if os.path.isfile(path):
            
            print(f"copied path: {path}")
            shutil.copy(path, dst_path)
        
        # Or if it is a directory we should make a recursive call to the directory
        elif os.path.isdir(path):

            print(f"copied path: {path}")
            new_dir_path = os.path.join(dst_path, path_name)
            os.mkdir(new_dir_path)
            copy_directory(path, new_dir_path)


def extract_title(markdown: str):
    if re.match(r"^# ", markdown) == None:
        raise Exception("Title should be h1")
    unsure_title = markdown.split("# ")
    true_title = unsure_title[1].split("\n")
    return true_title[0]


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file and store it (also close it)
    from_path_f = open(from_path)
    from_path_md = from_path_f.read()
    from_path_f.close()
    
    # Read the template html file and store it (also close it)
    template_path_f = open(template_path)
    template_path_html = template_path_f.read()
    template_path_f.close()
    
    # Transform the markdown file to html string
    from_path_html = markdown_to_html_node(from_path_md).to_html()

    title = extract_title(from_path_md)

    template_path_html = template_path_html.replace("{{ Title }}", title)

    template_path_html = template_path_html.replace("{{ Content }}", from_path_html)

    dir_name = os.path.dirname(dest_path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)
    
    dest_path_f = open(dest_path, "w")

    dest_path_f.write(template_path_html)

    dest_path_f.close()

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    
    if not os.path.exists(dir_path_content) or not os.path.exists(template_path):
        raise Exception("Given paths should be valid paths!")

    path_names = os.listdir(dir_path_content)

    for path_name in path_names:

        # Make a path from the path_name
        path = os.path.join(dir_path_content, path_name)
        path_parts = os.path.split(path)
        # Check for a .md file
        print(path_parts[1])
        if ".md" in path_parts[1]:
            rel_dir_path = os.path.relpath(path, dir_path_content)
            new_dest_path = os.path.join(dest_dir_path, rel_dir_path)
            new_dest_path = str(new_dest_path).replace(".md", ".html")
            generate_page(path, template_path, new_dest_path)
        elif os.path.isdir(path):
            rel_dir_path = os.path.relpath(path, dir_path_content)
            new_dest_path = os.path.join(dest_dir_path, rel_dir_path)
            generate_page_recursive(path, template_path, new_dest_path)
        