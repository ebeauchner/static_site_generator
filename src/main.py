import os
import shutil

def main():
    src = "/Users/ericbeauchner/workspace/github.com/ebeauchner/static_site_generator/static"
    dest = "/Users/ericbeauchner/workspace/github.com/ebeauchner/static_site_generator/public"
    shutil.copytree(src,dest,dirs_exist_ok=True)

def generate_page(from_path,template_path,dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    open


main()
