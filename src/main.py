from functions import copy_directory, generate_page_recursive
import os, shutil
import sys

dir_path_static: str = "./static"
dir_path_public: str = "./docs"

def main() -> None:

    if len(sys.argv) > 1:
        basepath: str = sys.argv[1]
    else:
        basepath = "/"

    # Remove the directory Public and it's contents
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    # And then mkdir Public using the path of the old Public
    print("Making public directory...")
    os.mkdir(dir_path_public)

    copy_directory(dir_path_static, dir_path_public)

    generate_page_recursive("content/", "template.html", dir_path_public, basepath)


if __name__ == "__main__":
    main()