import os
import subprocess
from ..utils.helpers import *
import re


# get the directory of the current script
base_dir = os.path.dirname(os.path.realpath(__file__))  # dir of current file
body_path = "./../../articles/article_tutorial/elements/body/body_en.tex"


def main():

    dir_path = os.path.join(base_dir, body_path)

    macros_to_convert = {
        r"\\myArticleSection\{(.*?)\}": "hello",
        r"\\myArticleSubsection\{(.*?)\}": "hello",
        r"\\myArticleSubsubsection\{(.*?)\}": "hello",
    }
    lista = [
        Tag_h1,
        Tag_h2

    ]


    with open(dir_path, "r", encoding="utf-8") as file:
        content = file.read()

        for key, val in macros_to_convert.items():
            matches = re.findall(key, content)
            # print(f"\n🟰  Matches for '{key}")
            # [print(match) for match in matches]
            # for match in matches:
            # content = re.sub(key,  lambda m: r'<HELLO>' + m.group(1) + '<WORLD>' ,content)

        for obj in lista:
            print(obj.latex_pttrn)
            matches = re.findall(obj.latex_pttrn, content)
            print(f"\n🟰  Matches for '{obj.__name__}")
            [print(match) for match in matches]
            content = re.sub(obj.latex_pttrn,  lambda m: obj.html_pttrn[0] + m.group(1) + obj.html_pttrn[2] ,content)



    with open("scripts/test.html", "w", encoding="utf-8") as file:
        file.write(content)


# =============================================================================
class GenericTag:
    def __init__(self, innerHTML, id, HTMLClass):
        # Initialize the attributes
        self.innerHTML = innerHTML
        self.id = id
        self.HTMLClass = HTMLClass

    def appendHTMLClass(self, newHTMLClass):
        # Method an an aditional class
        self.HTMLClass += " " + newHTMLClass
        print(f'Class {newHTMLClass} added to tag (class="{self.HTMLClass}")')


class Tag_h1(GenericTag):
    latex_pttrn = r"\\myArticleSection\{(.*?)\}"
    html_pttrn = [r"<h1>", r"(.*?)", r"</h1>"]
    def __init__(self, innerHTML, id, HTMLClass, customAttribute):
        # Call the parent class' constructor (initialize the attributes)
        super().__init__(innerHTML, id, HTMLClass)
        # Initialize additional attribute specific to CustomTag
        self.customAttribute = customAttribute

    def showCustomInfo(self):
        # Additional method specific to CustomTag
        print(f'Custom Tag with ID "{self.id}" has a custom attribute: {self.customAttribute}')


class Tag_h2(GenericTag):
    latex_pttrn = r"\\myArticleSubsection\{(.*?)\}"
    html_pttrn = [r"<h2>", r"(.*?)", r"</h2>"]
    def __init__(self, innerHTML, id, HTMLClass, customAttribute):
        # Call the parent class' constructor (initialize the attributes)
        super().__init__(innerHTML, id, HTMLClass)
        # Initialize additional attribute specific to CustomTag
        self.customAttribute = customAttribute

    def showCustomInfo(self):
        # Additional method specific to CustomTag
        print(f'Custom Tag with ID "{self.id}" has a custom attribute: {self.customAttribute}')



# Example of using the class
myTaggedContent = GenericTag("Inner contents", "testId", "testClass")

myTaggedContent.appendHTMLClass("NewClass")


# =============================================================================

if __name__ == "__main__":
    main()
