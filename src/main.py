from textnode import *
import os, shutil, sys
from htmlnode import markdown_to_html_node

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else './'
    src = './static'
    dst = './docs'
    if os.path.exists(f'{dst}'):
        shutil.rmtree(f'{dst}')

    static_to_public(src, dst)
    generate_pages_recursive(f'./content', f'./template.html', f'{dst}', basepath)


def static_to_public(src, dst):
    if os.path.exists(f'{dst}'):
        shutil.rmtree(f'{dst}')
    os.mkdir(f'{dst}')

    for content in os.listdir(f'{src}'):
        loc = f'{src}/{content}'
        if os.path.isfile(loc):
            shutil.copy(loc, f'{dst}')
            print(f'Copied file from {src}/{content} to {dst}/{content}')
            continue
        if not os.path.exists(f'{dst}/{content}'):
            os.mkdir(f'{dst}/{content}')
        static_to_public(f'{src}/{content}', f'{dst}/{content}')

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            line = line.replace('# ', '')
            return line.strip()
    raise Exception('No h1 header')

def generate_page(from_path, template_path, dest_path, basepath):
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
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    f = open(f'{dest_path}', 'x')
    f.write(page)
    f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.listdir(dir_path_content):
        loc = f'{dir_path_content}/{entry}'
        dst = f'{dest_dir_path}/{entry}'

        if os.path.isfile(loc):
            if entry[-2:] == 'md':
                generate_page(loc, template_path, f'{dst[:-3]}.html', basepath)
        else:
            os.mkdir(dst)
            generate_pages_recursive(loc, template_path, dst, basepath)

main()