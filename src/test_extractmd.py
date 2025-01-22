import unittest

from extractmd import extract_markdown_images,extract_markdown_links

class TestLinkExtract(unittest.TestCase):
    def test_normal(self):
        tst = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        ans = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(tst, ans)
    def test_notequal(self):
        tst = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        ans = [("[to boot dev]", "(https://www.boot.dev)"), ("[to youtube]", "(https://www.youtube.com/@bootdotdev)")]
        self.assertNotEqual(tst,ans)
    def test_no_link(self):
        tst = extract_markdown_images("This is text with a rick roll")
        ans = []
        self.assertEqual(tst, ans)
        
        import unittest

def heading_count(block):
    """
    Counts the number of '#' characters at the start of `block`.
    For example: heading_count("### My Heading") -> 3
    """
    count = 0
    for char in block:
        if char == '#':
            count += 1
        else:
            break
    return count

def unordered_list_check(block):

    for line in block.split('\n'):
        if line.strip() and not (line.strip().startswith('*') or line.strip().startswith('-')):
            raise Exception("Invalid Unordered List")

def ordered_list_check(block):
    for line in block.split('\n'):
        line = line.strip()
        if line:
            if not (line[0].isdigit() and line[1] == '.'):
                raise Exception("Invalid Ordered List")

def block_to_block_type(block):
    if block[0] == "#":
        heading_value = heading_count(block)
        if heading_value > 6:
            raise Exception('Invalid Heading Block')
        return f"Heading {heading_value} Block"
    if block[0:3] == '```':
        if block[-3:] == '```':
            return "Code Block"
        else:
            raise Exception('Invalid Code Block')
    if block[0] == "*" or block[0] == "-":
        unordered_list_check(block)
        return "Unordered List"
    if block[0].isnumeric() and block[1] == ".":
        ordered_list_check(block)
        return "Ordered List"
    else:
        return "Normal Paragraph"


class TestBlockToBlockType(unittest.TestCase):

    def test_heading_level_1(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "Heading 1 Block")
    
    def test_heading_level_3(self):
        self.assertEqual(block_to_block_type("### Heading 3"), "Heading 3 Block")

    def test_heading_level_6(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), "Heading 6 Block")

    def test_invalid_heading_level_7(self):
        with self.assertRaises(Exception) as context:
            block_to_block_type("####### Heading 7")
        self.assertIn("Invalid Heading Block", str(context.exception))

    def test_valid_code_block(self):
        code_block = """```
def hello_world():
    print("Hello, World!")
```"""
        self.assertEqual(block_to_block_type(code_block), "Code Block")

    def test_invalid_code_block(self):
        code_block = """```
def hello_world():
    print("Hello, World!")"""
        with self.assertRaises(Exception) as context:
            block_to_block_type(code_block)
        self.assertIn("Invalid Code Block", str(context.exception))

    def test_unordered_list_asterisk(self):
        ul_block = """* item1
* item2
* item3"""
        self.assertEqual(block_to_block_type(ul_block), "Unordered List")

    def test_unordered_list_hyphen(self):
        ul_block = """- item1
- item2
- item3"""
        self.assertEqual(block_to_block_type(ul_block), "Unordered List")

    def test_invalid_unordered_list(self):
        ul_block = """- item1
x item2
- item3"""
        with self.assertRaises(Exception) as context:
            block_to_block_type(ul_block)
        self.assertIn("Invalid Unordered List", str(context.exception))

    def test_valid_ordered_list(self):
        ol_block = """1. item1
2. item2
3. item3"""
        self.assertEqual(block_to_block_type(ol_block), "Ordered List")

    def test_invalid_ordered_list(self):
        ol_block = """1. item1
2: item2
3. item3"""
        with self.assertRaises(Exception) as context:
            block_to_block_type(ol_block)
        self.assertIn("Invalid Ordered List", str(context.exception))

    def test_normal_paragraph(self):
        paragraph = "This is just a normal paragraph without any special markers."
        self.assertEqual(block_to_block_type(paragraph), "Normal Paragraph")

    def test_empty_string(self):
        with self.assertRaises(IndexError):
            block_to_block_type("")

if __name__ == "__main__":
    unittest.main()

