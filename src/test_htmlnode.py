import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        props = {"href": "https://www.google.com",
                 "target": "_blank",
                 }
        node = HTMLNode("h1", 'test_value', None, props)

    def test_neq(self):
        props = {"href": "https://www.google.com",
                 "target": "_blank",
                 }
        node = HTMLNode("p", 'test_value', None, None)

    def test_url(self):
        props = {"href": "https://www.google.com",
                 "target": "_blank",
                 }
        node = HTMLNode(None, 'test_value', None, props)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_hl(self):
        node = LeafNode("hl", "Hello, world!")
        self.assertEqual(node.to_html(), "<hl>Hello, world!</hl>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertNotEqual(node.to_html(), "<p>Hello, world!</p>")

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_mult_parents(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent2_node = ParentNode("div", [child_node])
        parent_node = ParentNode("div", [child_node, parent2_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><div><span><b>grandchild</b></span></div></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            html
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
            html
        )

if __name__ == "__main__":
    unittest.main()