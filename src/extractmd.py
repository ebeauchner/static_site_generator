import re

#takes a block of markdown, and if there are any images formatted
#![alt_text](url), and returns a list of tuples containing all links in that block
#tuples are (alt_text,url)
def extract_markdown_images(text):
    img_tuple_list = []
    alt_text_pattern = r'!\[([^]]+)\]'
    alt_text_matches = re.findall(alt_text_pattern, text)
    link_pattern = r'\(([^)]+)\)'
    link_matches = re.findall(link_pattern, text)
    for i in range(len(alt_text_matches)):
        img_tuple_list.append((alt_text_matches[i],link_matches[i]))
    return img_tuple_list

#takes a block of markdown, and if there are any links formatted
#[alt_text](url), and returns a list of tuples containing all links in that block
#tuples are (alt_text,url)
def extract_markdown_links(text):
    link_tuple_list = []
    alt_text_pattern = r'\[([^]]+)\]'
    alt_text_matches = re.findall(alt_text_pattern, text)
    link_pattern = r'\(([^)]+)\)'
    link_matches = re.findall(link_pattern, text)
    for i in range(len(alt_text_matches)):
        link_tuple_list.append((alt_text_matches[i],link_matches[i]))
    return link_tuple_list

#splits a markdown document into a list of specific blocks
def markdown_to_block(markdown):
    markdown_blocks = markdown.split("\n\n")
    return markdown_blocks

#checks how many #'s are in the header, returns the value to account for H1-Hn
def heading_count(line, count=0):
    if not line or line[0] != '#':
        return count
    return heading_count(line[1:],count+1)

#checks that an ul is formated correctly for every line in the block
def unordered_list_check(text):
    if not text or text.strip() == '':
        return None
    lines = text.split('\n')
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and not (stripped_line.startswith('*') or stripped_line.startswith('-')):
            raise Exception(f"Invalid list line: '{line}'")
    return True

#checks that an ol is formatted correctly for every line in the block
def ordered_list_check(text):
    if not text or text.strip() == '':
        return None
    lines = text.split('\n')
    for line in lines:
        stripped_line = line.strip()
        if stripped_line and not (stripped_line[0].isnumeric() or stripped_line[1].startswith('.')):
            raise Exception(f"Invalid list line: '{line}'")
    return True

#checks the block, and returns a string containing the type of block for sorting
def block_to_block_type(raw_block):
    block = raw_block.replace("\n","")
    if block[0] == "#":
        heading_value=heading_count(block)
        if heading_value > 6:
            raise Exception('Invalid Heading Block')
        return f"Heading {heading_value} Block"
    if block[0:3] == '```':
        if block[-3:] == '```':
            return "Code Block"
        else:
            raise Exception('Invalid Code Block')
    if block[0:2] == "* " or block[0:2] == "- ":
        unordered_list_check(block)
        return "Unordered List"
    if block[0].isnumeric() and block[1] == ".":
        ordered_list_check(block)
        return "Ordered List"
    if block[0] == ">":
        return "Quote Block"
    else:
        return "Normal Paragraph"

