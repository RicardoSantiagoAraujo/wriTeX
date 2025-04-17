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

# build folders for main pdf output AND all auxiliary files relative to script location
build_folder__main_output = "auxiliary_files"
build_folder__aux_files = "auxiliary_files"

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

    args.thing_name = deal_with_user_input(args.thing_name)

    thing_name = args.thing_name
    global dir_path

    if thing_name in article_names:
        dir_path = articles_dir_path
    elif thing_name in portfolio_names:
        dir_path = portfolios_dir_path

    perform_build_steps(thing_name)


def deal_with_user_input(thing_name_from_cmd_line: str) -> str:
    """Manage user input by first checking whether it was passed directly in the terminal or must be collected with the input() command.
    Additionally, perform tests for availability, quit commands and index inputs.

    Args:
        thing_name_from_cmd_line (str): user input thing (target document) as passed through the command line; may be empty in which case input is collected with the input() command

    Returns:
        str: _description_
    """
    keep_asking = True
    while keep_asking == True:
        # If no thing name has been provided in the command line directly, request it from the user
        if thing_name_from_cmd_line == None:
            art_names = list_existing_things(articles_dir_path, header_message="Articles:")
            prt_names = list_existing_things(
                portfolios_dir_path, header_message="Portfolio versions:", cnt_start=len(art_names)
            )
            all_names = art_names + prt_names
            indexes = list(range(1, len(all_names) + 1))
            choice = input(f"Which do you want to compile? ({blue}choose from options above{reset}): ")
            #  if user passed an instruction to quit the program:
            if choice in ["q", "quit"]:
                print(f"\n💀💀💀 {red}Program quit without compiling anything.{reset}")
                exit()
            # if user picked a valid index (number):
            elif choice.isdigit() and int(choice) in indexes:
                thing_name = all_names[int(choice) - 1]
            # if user wrote the article name directly and it is valid:
            elif choice in thing_names:
                thing_name = choice
            # if invalid choice (non existing name or index):
            else:
                print(f"\n\n\n{red}Invalid choice{reset}, pick from options:\n")
                continue

            print(f"You have chosen to compile {blue}{thing_name}{reset}\n...")
            keep_asking = False


        # If thing name has been provided...
        # ...but it does not actually exist:
        elif thing_name_from_cmd_line not in thing_names:
            print(f"\n\n\n{red}thing_name{reset} does not exist, pick from options:\n")
            # Restart proccess
            thing_name = None
        # ...and it exists:
        else:
            # Exit loop
            thing_name = thing_name_from_cmd_line
            print(f"You have chosen to compile {blue}{thing_name_from_cmd_line}{reset}\n...")
            keep_asking = False

    return thing_name


def perform_build_steps(thing_name: str):
    """Compile a LaTeX document (article or portfolio) with lualaTeX.

    Args:
        thing_name (str): name of an existing LaTeX document to compile.
    """
    try:
        # print( os.path.join(dir_path, thing_name + ".tex"))
        # CHANGE DIRECTORY TO THING'S
        os.chdir(os.path.join(dir_path, thing_name))
        # CREATE BUILD FOLDERS IF IT DOES NOT EXIST
        create_build_directories()

        trigger_biblatex(thing_name, printout=False)
        trigger_biber(thing_name, printout=False)
        trigger_biblatex(thing_name, printout=False)
        trigger_biblatex(thing_name, printout=False)

        print(f"\n{green}Compilation finished{reset}")

    except subprocess.CalledProcessError as e:
        print("Compilation log:")
        print(e.stdout)
        print(e.stderr)
        print(f"{red}Compilation failed{reset}")




def create_build_directories() -> None:
    """
    Create required build directories if they do not exist yet
    """
    if not os.path.exists(build_folder__main_output):
        os.makedirs(build_folder__main_output)
    if not os.path.exists(build_folder__aux_files):
        os.makedirs(build_folder__aux_files)

def trigger_biber(thing_name : str, printout:bool = True) -> None :
    """Trigger biber

    Args:
        thing_name (str): _description_
        printout (bool, optional): _description_. Defaults to True.
    """
    result =  subprocess.run(
    ["biber", os.path.join(build_folder__aux_files, f"{'document'}")])

    if printout:
        print(result.stdout)
    print(f"{blue}trigger_biber : DONE{reset}")



def trigger_biblatex(thing_name : str, printout:bool = True) -> None :
    """Trigger biblatex compilation

    Args:
        thing_name (str): _description_
        printout (bool, optional): _description_. Defaults to True.
    """
    result = subprocess.run(
        [
            "lualatex",
            "--interaction=nonstopmode",
            f"--job-name={thing_name}", # output file(s) name
            f"--output-directory={build_folder__main_output}", # output directory of pdf file
            f"--aux-directory={build_folder__aux_files}",  # output directory of all other auxiliary files
            f"{'portfolio_document'}.tex",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    if printout:
        print(result.stdout)
    print(f"{blue}trigger_biblatex : DONE{reset}")


if __name__ == "__main__":
    main()
