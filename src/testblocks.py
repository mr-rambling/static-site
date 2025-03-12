import unittest
from textnode import TextType, TextNode
from blocks import *
import re

class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
                        [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],blocks
        )
    
    def test_block_block_heading(self):
        md = '## Heading 2'
        type = block_to_block_type(md)
        self.assertEqual(BlockType.HEADING, type)    

    def test_block_block_code(self):
        md = '``` Heading 2```'
        type = block_to_block_type(md)
        self.assertEqual(BlockType.CODE, type)
        
    def test_block_block_quote(self):
        md = '''>## Heading 2
> Quote 2'''
        type = block_to_block_type(md)
        self.assertEqual(BlockType.QUOTE, type)
         
    def test_block_block_unordered(self):
        md = '''- ## Heading 2
- Heading 3'''
        type = block_to_block_type(md)
        self.assertEqual(BlockType.UNORDERED_LIST, type)
        
    def test_block_block_ordered(self):
        md = """1. ## Heading 2
2. Heading 3
3. new heading"""
        type = block_to_block_type(md)
        self.assertEqual(BlockType.ORDERED_LIST, type)