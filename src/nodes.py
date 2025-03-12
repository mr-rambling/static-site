from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise Exception('invalid Markdown syntax')
        else:
            strings = node.text.split(delimiter)
            for ind in range(len(strings)):
                if ind % 2 != 0:
                    new_nodes.append(TextNode(strings[ind], text_type))
                else:
                    new_nodes.append(TextNode(strings[ind], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        text = node.text
        if images == []:
            new_nodes.append(node)
            continue
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            else:
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = sections[1]
        if text != '' and images != []:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        text = node.text
        if links == []:
            new_nodes.append(node)
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != '':
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            else:
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = sections[1]
        if text != '' and links != []:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes