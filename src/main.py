import os
import shutil

def main():
    src = "/Users/ericbeauchner/workspace/github.com/ebeauchner/static_site_generator/static"
    dest = "/Users/ericbeauchner/workspace/github.com/ebeauchner/static_site_generator/public"
    shutil.copytree(src,dest,dirs_exist_ok=True)


main()
