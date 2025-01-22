import unittest

from textnode import TextNode, text_node_to_html_node, TextType
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq_different_type(self):
        node = TextNode("Hello", TextType.ITALIC)
        node2 = TextNode("World", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_text_node_to_html_node(self):
        text = TextNode("Hello, world!", TextType.TEXT)
        html = text_node_to_html_node(text)
        self.assertEqual(html.to_html(), "Hello, world!")
        text = TextNode("Bold text", TextType.BOLD)
        html = text_node_to_html_node(text)
        self.assertEqual(html.to_html(), "<b>Bold text</b>")
        text = TextNode("Link Text",TextType.LINK, "http://www.example.com")
        html = text_node_to_html_node(text)
        self.assertEqual(html.to_html(), "<a href=\"http://www.example.com\">Link Text</a>")

class TextSplitDelim(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        split_node = split_nodes_delimiter([node],"", TextType.BOLD)
        split_node2 = split_nodes_delimiter([node2],"", TextType.BOLD)
        self.assertEqual(split_node, split_node2)
        node = TextNode("This is a **text** node", TextType.TEXT)
        node2 = TextNode("This is a **text** node", TextType.TEXT)
        split_node = split_nodes_delimiter([node],"**", TextType.BOLD)
        split_node2 = split_nodes_delimiter([node2],"**", TextType.BOLD)
        self.assertEqual(split_node, split_node2)

class TextSplit(unittest.TestCase):
    def test_text_to_textnodes(self):
        # Test 1: Plain text only
        text = "Hello world"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "Hello world")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

        # Test 2: Bold text
        text = "Hello **world**"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "world")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)

        # Test 3: Empty string
        text = ""
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)



if __name__ == "__main__":
    unittest.main()

