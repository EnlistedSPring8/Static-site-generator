from functions import copy_directory, generate_page_recursive
import os, shutil

dir_path_static = "./static"
dir_path_public = "./public"

def main() -> None:
    # Remove the directory Public and it's contents
    print("Deleting public directory...")
    shutil.rmtree(dir_path_public)
    # And then mkdir Public using the path of the old Public
    print("Making public directory...")
    os.mkdir(dir_path_public)

    copy_directory(dir_path_static, dir_path_public)

    generate_page_recursive("content/", "template.html", "public/")


if __name__ == "__main__":
    main()