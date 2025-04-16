# LaTeX workshop is set up to used latexmk, which automates the proccess of generating a latex document. Under the hood, it calls a latex compiler, e.g., lualatex.
# However, it might be slow, so alternatively you can use this script which calls lualatex directly.

import subprocess
import os
import argparse
from ..utils.helpers import list_existing_things
from ..utils.prompts import first_prompt
from ..utils.style_console_text import red, green, blue, bold, reset
from ..enums.ThingType import ThingType
import enum
import sys

articles_directory = "./../../articles/"  # relative to script location
portfolios_directory = "./../../portfolios/versions/"  # relative to script location

build_folder = "auxiliary_files"  # relative to script location

# get the directory of the current script
base_dir = os.path.dirname(os.path.realpath(__file__))  # dir of current file
articles_dir_path = os.path.join(base_dir, articles_directory)
portfolios_dir_path = os.path.join(base_dir, portfolios_directory)


article_names = list_existing_things(articles_dir_path, print_list=False)
portfolio_names = list_existing_things(portfolios_dir_path, print_list=False)
thing_names = article_names + portfolio_names


def list_as_string(list: list[any]) -> str:
    return ", ".join([f"{blue}{e}{reset}" for e in list])


def enum_list_as_string(enumName: enum.Enum) -> str:
    return ", ".join([f"{blue}{e.value}{reset}" for e in enumName])


article_list_as_string = list_as_string(article_names)
portfolio_list_as_string = list_as_string(article_names)
thing_name_list_as_string = list_as_string(thing_names)
thing_type_list_as_string = enum_list_as_string(ThingType)


def main():
    """Main function of script to compile an existing LaTeX document (article or portfolio) into a PDF."""

    first_prompt("Script for pdf compilation from existing document (article or portfolio)")
    # Create command line argument parser
    parser = argparse.ArgumentParser(description="arTeX compilation with biblatex.")
    # Add arguments
    parser.add_argument(
        "thing_name", nargs="?", type=str, help=f"available options: {thing_name_list_as_string}", default=None
    )
    # parser.add_argument('thing_type', type=str, help=f"available options: {thing_type_list_as_string}")
    parser.add_argument("--biber", type=bool, help="Whether to run biber too", default=True)
    # Parse the arguments
    args = parser.parse_args()
    keep_asking = True
    while keep_asking == True:
        # If not thing name as been provided in the command line directly, request it from the user
        if args.thing_name == None:
            art_names = list_existing_things(articles_dir_path, header_message="Articles:")
            prt_names = list_existing_things(
                portfolios_dir_path, header_message="Portfolio versions:", cnt_start=len(art_names)
            )
            all_names = art_names + prt_names
            indexes = list(range(1, len(all_names) + 1))
            choice = input(f"Which do you want to compile? ({blue}choose from options above{reset}): ")

            # if used picked a number:
            if choice.isdigit() and int(choice) in indexes:
                thing_name = all_names[int(choice) - 1]
            # if used wrote the article name:
            else:
                thing_name = choice
                # Store it in the command line object
            args.thing_name = thing_name
            print(f"You have chosen to compile {blue}{thing_name}{reset}\n...")

        # check if chosen thing actually exists:
        if args.thing_name in ["q", "quit"]:
            print(f"\n💀💀💀 {red}Program quit without compiling anything.{reset}")
            exit()
        elif args.thing_name not in thing_names:
            print(f"\n\n\n{red}Invalid thing_name{reset}, pick from options:\n")
            # Restart proccess
            args.thing_name = None
        else:
            keep_asking = False

    thing_name = args.thing_name
    global dir_path

    if thing_name in article_names:
        dir_path = articles_dir_path
    elif thing_name in portfolio_names:
        dir_path = portfolios_dir_path

    compile_with_lualatex(thing_name)


def compile_with_lualatex(thing_name: str):
    """Compile a LaTeX document (article or portfolio) with lualaTeX.

    Args:
        thing_name (str): name of an existing LaTeX document to compile.
    """
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
            text=True,
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Compilation failed:")
        print(e.stdout)
        print(e.stderr)


if __name__ == "__main__":

    main()
