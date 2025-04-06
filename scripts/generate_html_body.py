import os
import subprocess
import helpers as h

# get the directory of the current script
base_dir = os.path.dirname(os.path.realpath(__file__))  # dir of current file
body_path = "./../articles/article_tutorial/elements/body/body_en.tex"

dir_path = os.path.join(base_dir, body_path)


with open(dir_path, 'r', encoding='utf-8') as file:
    content = file.read()
    print(content)