from enum import Enum

class TextType(Enum):
    PLAIN = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text: str, text_type: TextType = TextType.PLAIN, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False    
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"