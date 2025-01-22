from enum import Enum
from htmlnode import LeafNode, ParentNode

class TextType(Enum):
	TEXT = "normal" 
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

#
class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		if not isinstance(other, TextNode):
			return False
		return (self.text == other.text 
				and self.text_type == other.text_type 
				and self.url == other.url)
		
	def __repr__(self):
		if self.url is None:
			return "\nTextNode(\"" + str(self.text) + "\", " + str(self.text_type) + ")"
		else:
			return "\nTextNode(\"" + str(self.text) + "\", " + str(self.text_type) + ", \"" + str(self.url) + "\")"

#based on the text_type of the textnode inputted, it returns a LeafNode object with the HTML tag, value, and properties
def text_node_to_html_node(textnode_to_conv):
	if not isinstance(textnode_to_conv, TextNode):
		raise Exception("Value must be class TextNode")
	match (textnode_to_conv.text_type):
		case (TextType.TEXT):
			leafnode_conv = LeafNode(None,value=textnode_to_conv.text)
			return leafnode_conv
		case (TextType.BOLD):
			leafnode_conv = LeafNode("b",textnode_to_conv.text)
			return leafnode_conv
		case (TextType.ITALIC):
			leafnode_conv = LeafNode("i",textnode_to_conv.text)
			return leafnode_conv
		case (TextType.CODE):
			leafnode_conv = ParentNode("pre",[LeafNode("code",textnode_to_conv.text)])
			return leafnode_conv
		case (TextType.LINK):
			leafnode_conv = LeafNode("a",textnode_to_conv.text,{"href":textnode_to_conv.url})
			return leafnode_conv
		case (TextType.IMAGE):
			leafnode_conv = LeafNode("img","", {"src":textnode_to_conv.url,"alt":textnode_to_conv.text})
			return leafnode_conv			
		case _:
			raise Exception("Invalid text_type")
			