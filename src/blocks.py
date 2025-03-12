from nodes import *
from textnode import TextType, TextNode
from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered'
    ORDERED_LIST = 'ordered'

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    strip_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped != '':
            strip_blocks.append(stripped)
    return strip_blocks

def block_to_block_type(block):
    lines = block.split('\n')

    # Heading
    if re.findall(r"^#{1,6} .*", block) != []:
        return BlockType.HEADING
    # Code
    elif re.findall(r"^`{3}[\s\S]*`{3}$", block) != []:
        return BlockType.CODE
    # Quote
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    # Unordered List
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    # Ordered List
    if len(lines) > 0:
        expect_num = 1
        for line in lines:
            if not line.startswith(f"{expect_num}. "):
                break
            expect_num += 1
        else:
            return BlockType.ORDERED_LIST
    # Paragraph
    return BlockType.PARAGRAPH
    