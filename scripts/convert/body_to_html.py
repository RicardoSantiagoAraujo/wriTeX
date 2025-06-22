import os
import subprocess
from ..utils.helpers import *
import re
from scripts.classes.tags.GenericTag import GenericTag
from scripts.classes.tags.Tag_h1 import Tag_h1
from scripts.classes.tags.Tag_h2 import Tag_h2

# get the directory of the current script
base_dir = os.path.dirname(os.path.realpath(__file__))  # dir of current file
body_path = "./../../articles/wrtx_article_tutorial/elements/body/body_en.tex"
destination_path = "scripts/convert/test.html"

def main():
    dir_path = os.path.join(base_dir, body_path)

    list_tags_to_convert = [Tag_h1, Tag_h2]

    with open(dir_path, "r", encoding="utf-8") as file:
        content = file.read()

        for obj in list_tags_to_convert:
            print(obj.latex_pttrn)
            matches = re.findall(obj.latex_pttrn, content)
            print(f"\n🟰  Matches for '{obj.__name__}")
            [print(match) for match in matches]
            content = re.sub(
                obj.latex_pttrn,
                lambda m: obj.html_pttrn[0] + m.group(1) + obj.html_pttrn[2],
                content,
            )

    with open(destination_path, "w", encoding="utf-8") as file:
        file.write(content)






if __name__ == "__main__":
    main()
