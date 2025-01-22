from textnode import TextType, TextNode
from extractmd import extract_markdown_images,extract_markdown_links
import re

#uses a delimiter and text_type to split a single line of text into a list with correct text_type
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_node_list = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            split_node_list.append(old_node)
            continue
            
        # If no delimiter is found, keep the node as-is
        if delimiter not in old_node.text:
            split_node_list.append(old_node)
            continue
            
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 != 1:
            raise Exception("Invalid markdown syntax")
            
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                node = TextNode(parts[i], TextType.TEXT)
            else:
                node = TextNode(parts[i], text_type)
            split_node_list.append(node)
            
    return split_node_list

def split_nodes_image(old_nodes):
    split_node_list = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            split_node_list.append(old_node)
            continue

        pattern = r'!\[(.*?)\]\((.*?)\)'
        last_end = 0
        text = old_node.text
        for match in re.finditer(pattern, text):
            # Add any text that came before this match
            if match.start() > last_end:
                split_node_list.append(TextNode(text[last_end:match.start()], TextType.TEXT))
            
            # Add the image node
            image_text = match.group(1)  # The text inside []
            image_url = match.group(2)   # The url inside ()
            split_node_list.append(TextNode(image_text, TextType.IMAGE, image_url))
            
            last_end = match.end()
        
        # Add any remaining text after the last match
        if last_end < len(text):
            split_node_list.append(TextNode(text[last_end:], TextType.TEXT))

    return split_node_list

#input a list of nodes as TextType.TEXT, and split out the Links the parts in another list
def split_nodes_link(old_nodes):
    split_node_list = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            split_node_list.append(old_node)
            continue

        # Pattern for [text](url) but not ![text](url)
        pattern = r'(?<!!)(\[(.*?)\]\((.*?)\))'
        # (?<!!) = negative lookbehind for !
        # \[(.*?)\] = capture text inside []
        # \((.*?)\) = capture url inside ()
        
        last_end = 0
        text = old_node.text
        for match in re.finditer(pattern, text):
            # Add any text that came before this match
            if match.start() > last_end:
                split_node_list.append(TextNode(text[last_end:match.start()], TextType.TEXT))
            
            # Add the link node
            link_text = match.group(2)  # The text inside []
            link_url = match.group(3)   # The url inside ()
            split_node_list.append(TextNode(link_text, TextType.LINK, link_url))
            
            last_end = match.end()
        
        # Add any remaining text after the last match
        if last_end < len(text):
            split_node_list.append(TextNode(text[last_end:], TextType.TEXT))

    return split_node_list

def text_to_textnodes(text):
    if not text:
        return [TextNode("", TextType.TEXT)]
    text_to_convert = TextNode(text,TextType.TEXT,None)
    image_list = split_nodes_image([text_to_convert])
    link_list = split_nodes_link(image_list)
    bold_list = split_nodes_delimiter(link_list,"**",TextType.BOLD)
    italic_list = split_nodes_delimiter(bold_list,"*",TextType.ITALIC)
    code_list = split_nodes_delimiter(italic_list,"`",TextType.CODE)
    return code_list

