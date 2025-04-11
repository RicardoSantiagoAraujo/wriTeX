# LaTeX workshop is set up to used latexmk, which automates the proccess of generating a latex document. Under the hood, it calls a latex compiler, e.g., lualatex.
# However, it might be slow, so alternatively you can use this script which calls lualatex directly.

import subprocess
import os
import argparse
from ..utils.helpers import *
from ..utils.style_console_text import red, green, blue, bold, reset
from ..enums.ThingType import ThingType


articles_directory = "./../../articles/"  # relative to script location
portfolios_directory = "./../../portfolios/versions/"  # relative to script location

build_folder = "auxiliary_files"  # relative to script location

# get the directory of the current script
base_dir = os.path.dirname(os.path.realpath(__file__))  # dir of current file
articles_dir_path = os.path.join(base_dir, articles_directory)
portfolios_dir_path = os.path.join(base_dir, portfolios_directory)




def main(args):
    thing_type = args.thing_type.lower()
    global dir_path
    
    if thing_type == ThingType.Article.value.lower():
        dir_path = articles_dir_path
    elif thing_type == ThingType.Portfolio.value.lower():
        dir_path = portfolios_dir_path
    else:
        exit()
        print("Invalid type")

    list_existing_things(dir_path)
    choice = input(f"Which {thing_type}? ")

    compile_with_lualatex(choice)



def compile_with_lualatex(thing_name:str):
    try:
        # print( os.path.join(dir_path, thing_name + ".tex"))
        # CHANGE DIRECTORY TO THING'S
        os.chdir(os.path.join(dir_path, thing_name))
        # CREATE BUILD FOLDER IF IT DOES NOT EXIST
        if not os.path.exists(build_folder):
            os.makedirs(build_folder)
        result = subprocess.run(
            ["lualatex", "-interaction=nonstopmode", f"-output-directory={build_folder}", "document.tex"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Compilation failed:")
        print(e.stdout)
        print(e.stderr)

thing_type_list_as_string = ', '.join([f'{blue}{e.value}{reset}' for e in ThingType])

if __name__ == "__main__":
    # Create command line argument parser
    parser = argparse.ArgumentParser(description="arTeX compilation with biblatex.")
    # Add arguments
    parser.add_argument('thing_type', type=str, help=f"available options: {thing_type_list_as_string}")
    parser.add_argument('--biber', type=bool, help='Your age', default=True)

    # Parse the arguments
    args = parser.parse_args()

    if args.thing_type.lower() not in [e.value.lower() for e in ThingType]:
        print(f'Invalid thing_type, pick from: {thing_type_list_as_string}')
        exit()    
        
    main(args)
