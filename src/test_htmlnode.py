import unittest

from htmlnode import *
from mdtohtml import *

class TestHTMLNode(unittest.TestCase):
    def test_val_int(self):
        tst = HTMLNode(props={"key1":1, "key2":2}).props_to_html()
        ans = "key1=\"1\" key2=\"2\""
        self.assertEqual(tst, ans)
    def test_no_keys(self):
        tst = HTMLNode(props={}).props_to_html()
        ans = ""
        self.assertEqual(tst, ans)
    def test_case(self):
        tst = HTMLNode(props={"key1":"value1","key2":"value2"}).props_to_html()
        ans = "key1=\"value1\" key2=\"value2\""
        self.assertEqual(tst, ans)

class TestLeafNode(unittest.TestCase):
    def test_normal(self):
        tst = LeafNode("p", "hello").to_html()
        ans = "<p>hello</p>"
        self.assertEqual(tst, ans)
    def test_int(self):
        tst = LeafNode(1, "hello").to_html()
        ans = "<1>hello</1>"
        self.assertEqual(tst, ans)
    def test_None(self):
        with self.assertRaises(ValueError):
            LeafNode(None,None).to_html()

class TestParentNode(unittest.TestCase):
    def test_normal(self):
        tst = ParentNode("p",[LeafNode("p", "hello"),LeafNode("a", "click", {"href": "https://example.com"})]).to_html()
        ans = "<p><p>hello</p><a href=\"https://example.com\">click</a></p>"
        self.assertEqual(tst, ans)

class TestMarkdownToHtmlNode(unittest.TestCase):
    
    def test_normal_paragraph(self):
        tst = "This is normal text"
        a = markdown_to_html_node(tst).to_html()
        b = "<div><p>This is normal text</p></div>"
        self.assertEqual(a,b)

if __name__ == "__main__":
    unittest.main()