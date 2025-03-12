from textnode import *
from blocks import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        # A string representing the HTML tag name
        self.tag = tag
        # A string representing the value of the HTML tag
        self.value = value
        # list of HTMLNode objects
        self.children = children 
        # A dictionary of key-value pairs representing the attributes of the HTML tag
        self.props = props 
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        return [f' {attr.key()}={attr.value()}' for attr in self.props].join(' ')
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError(self)
        if self.tag == None:
            return f'{self.value}'
        if self.tag == 'img':
            return f'<{self.tag} src="{self.props['src']}" alt="{self.props['alt']}">'
        if self.tag == 'a':
            return f'<{self.tag} href="{self.props['href']}">{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children: HTMLNode, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None or self.tag == '':
            raise ValueError('missing a tag')
        if self.children == None or self.children == '':
            raise ValueError('missing a children value')
        string = []
        for n in self.children:
            string.append(n.to_html())
        return f'<{self.tag}>{''.join(string)}</{self.tag}>'
    
def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type not in TextType:
        raise Exception('incorrect text type')
    elif text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode('b', text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode('i', text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode('code', text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        type = block_to_block_type(block)
        children.append(create_markdown_html_node(type, block))
    return ParentNode('div', children)

def create_markdown_html_node(type, block):
    match type:
        case BlockType.PARAGRAPH:
            block = block.replace('\n', ' ')
            nodes = text_to_textnodes(block)
            children = []
            for node in nodes:
                children.append(text_node_to_html_node(node))
            return ParentNode('p', children)
        
        case BlockType.HEADING:
            heading_lvl = f'{block.split(' ')[0]} '
            return LeafNode(f'h{heading_lvl.count('#')}', block.split(heading_lvl)[1])
        
        case BlockType.CODE:
            block = block.split("```")[1]
            block = block.strip()
            children = [LeafNode('code', block)]
            return ParentNode('pre', children)
        
        case BlockType.QUOTE:
            text = block.replace('>', '')
            return LeafNode('blockquote', text.strip())
        
        case BlockType.UNORDERED_LIST:
            items = block.split('\n')
            children = []
            for item in items:
                grandchildren = []
                text = item.split('- ', 1)[1]
                subitems = text_to_textnodes(text)
                for subitem in subitems:
                    grandchildren.append(text_node_to_html_node(subitem))
                children.append(ParentNode('li', grandchildren))
            return ParentNode('ul', children)
        
        case BlockType.ORDERED_LIST:
            items = block.split('\n')
            children = []

            for item in items:
                grandchildren = []
                text = item.split(' ', 1)[1]
                subitems = text_to_textnodes(text)
                for subitem in subitems:
                    grandchildren.append(text_node_to_html_node(subitem))
                children.append(ParentNode('li', grandchildren))
            return ParentNode('ol', children)