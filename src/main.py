from src.textnode import TextNode, TextType
def main() -> None:
    TextNode1 = TextNode("Hello, World!", TextType.BOLD, "https://www.boot.dev")
    print(TextNode1)

if __name__ == "__main__":
    main()