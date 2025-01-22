import os, shutil
from mdtohtml import markdown_to_html_node, extract_title

def generate_page(from_path,template_path,dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    f = open(from_path, 'r')
    t = open(template_path, 'r')
    f_lines = f.read()
    t_lines = t.read()
    f_html = markdown_to_html_node(f_lines).to_html()
    f_title = extract_title(f_lines)
    t_title = t_lines.replace("{{ Title }}", f_title)
    t_html = t_title.replace("{{ Content }}", f_html)
    with open(dest_path, 'w') as d:
        d.write(t_html)
    f.close()
    t.close()
    d.close()

def main():
    shutil.rmtree('public')
    src = 'static'
    dest = 'public'
    shutil.copytree(src,dest)
    generate_page('content/index.md','template.html','public/index.html')

main()