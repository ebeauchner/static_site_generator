from extractmd import markdown_to_block, block_to_block_type, heading_count
from textnode import ParentNode, LeafNode, text_node_to_html_node
from splitnodes import TextNode, TextType, text_to_textnodes

#Creates a Parent Node with div tag and children equating the markdown input
def markdown_to_html_node(markdown):
    div_node = ParentNode("div",[])
    blocks = markdown_to_block(markdown)
    for block in blocks:
        block_textnodes = text_to_textnodes(block)
        for textnode in block_textnodes:
            if textnode.text_type is TextType.TEXT:
                leafnode = text_to_children(textnode.text)
            else:   
                leafnode = text_node_to_html_node(textnode)
            div_node.children.append(leafnode)
    return div_node


#This covers special blocks that are not covered in TextType.TYPE
def text_to_children(text):
    type_of_block = block_to_block_type(text)
    if type_of_block[0:7] == "Heading":
        heading_value = heading_count(text)
        return LeafNode(f"h{heading_value}", text[heading_value+1:])
    if type_of_block == "Unordered List":
        ul_node = ParentNode("ul",[])
        split_text = text.split("\n")
        for each_text in split_text:
            list_node = LeafNode("li",each_text[2:])
            ul_node.children.append(list_node)
        return ul_node
    if type_of_block == "Ordered List":
        ol_node = ParentNode("ol",[])
        split_text = text.split("\n")
        for each_text in split_text:
            list_node = LeafNode("li",each_text[3:])
            ol_node.children.append(list_node)
        return ol_node
    if type_of_block == "Normal Paragraph":
        return LeafNode("p",text)
    if type_of_block == "Quote Block":
        return LeafNode("blockquote", text.replace(">",""))
    else:
        raise Exception("Invalid text")
