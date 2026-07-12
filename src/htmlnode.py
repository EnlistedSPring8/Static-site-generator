class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses must implement the to_html method.")
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return f" {props_str}"
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):

        def __init__(self, tag: str, value: str, props: dict[str, str] = None):
            super().__init__(tag=tag, value=value, props=props)
        
        def to_html(self) -> str:
            if self.value is None:
                raise ValueError("LeafNode must have a value.")
            if self.tag is None:
                return self.value
            if self.tag == "img":
                return f'<{self.tag}{self.props_to_html()}/>'
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
        def __repr__(self):
            return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag=tag, children=children, props=props)
    
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if self.children is None or self.children == []:
            raise ValueError("ParentNode must have children.")
        children_html = "".join(
            child.to_html() for child in self.children
        )
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"