from textnode import *
import os, shutil
from htmlnode import markdown_to_html_node

def main():
    src = './static'
    dst = './public'
    if os.path.exists(f'{dst}'):
        shutil.rmtree(f'{dst}')

    static_to_public(src, dst)
    generate_page('./content/index.md', './template.html', './public/index.html')


def static_to_public(src, dst):
    if os.path.exists(f'{dst}'):
        shutil.rmtree(f'{dst}')
    os.mkdir(f'{dst}')

    log = []
    for content in os.listdir(f'{src}'):
        loc = f'{src}/{content}'
        if os.path.isfile(loc):
            shutil.copy(loc, f'{dst}')
            log.append((f'{src}/{content}', f'{dst}/{content}'))
            continue
        if not os.path.exists(f'{dst}/{content}'):
            os.mkdir(f'{dst}/{content}')
        log.append(static_to_public(f'{src}/{content}', f'{dst}/{content}'))
    return log 

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            line = line.replace('# ', '')
            return line.strip()
    raise Exception('No h1 header')

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path)
    markdown = f.read()
    f.close()

    f = open(template_path)
    template = f.read()
    f.close()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace('{{ Title }}', title)
    page = page.replace('{{ Content }}', content)

    f = open(f'{dest_path}', 'x')
    f.write(page)
    f.close()


main()