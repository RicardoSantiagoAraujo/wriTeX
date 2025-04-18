
import os
import argparse
from datetime import datetime
from ..utils.helpers import list_existing_things
from ..utils.style_console_text import red, green, blue, bold, reset
from ..enums.ThingType import ThingType
import enum
from .parameters import (
    articles_directory,
    portfolios_directory,
    build_folder__aux_files,
    build_folder__main_output,
)
from ..enums.BuildMode import BuildMode


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


def deal_with_user_input(args__cmd_line: argparse.Namespace) -> argparse.Namespace:
    """Manage user arguments passed through the command line, and collect missing ones through the input() command.
    Additionally, perform tests for availability, quit commands and index inputs.

    Args:
        args__cmd_line (argparse.Namespace): user passed arguments through the command line

    Returns:
        argparse.Namespace: Validated and updated arguments
    """

    # If something has been provided in the command line as first argument but it is the build mode:
    if args__cmd_line.thing_name in [e.value for e in BuildMode]:
        # Pass it to the right arg and empty the thing_name arg
        args__cmd_line.mode = args__cmd_line.thing_name
        args__cmd_line.thing_name = None


    # get and test user input thing (target document) as passed through the command line; may be empty in which case input is collected with the input() command
    thing_name_from_cmd_line = args__cmd_line.thing_name

    keep_asking = True
    while keep_asking == True:
        # If no thing name has been provided in the command line directly, request it from the user
        if thing_name_from_cmd_line == None:
            art_names = list_existing_things(
                articles_dir_path, header_message="Articles:"
            )
            prt_names = list_existing_things(
                portfolios_dir_path,
                header_message="Portfolio versions:",
                cnt_start=len(art_names),
            )
            all_names = art_names + prt_names
            indexes = list(range(1, len(all_names) + 1))
            choice = input(
                f"Which do you want to compile? ({blue}choose from options above{reset}): "
            )
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
            print(
                f"You have chosen to compile {blue}{thing_name_from_cmd_line}{reset}\n..."
            )
            keep_asking = False

    args__cmd_line.thing_name = thing_name
    return args__cmd_line



def create_build_directories() -> None:
    """
    Create required build directories if they do not exist yet
    """
    if not os.path.exists(build_folder__main_output):
        os.makedirs(build_folder__main_output)
    if not os.path.exists(build_folder__aux_files):
        os.makedirs(build_folder__aux_files)


def build_message(msg: str, counter: int,time_start : datetime, time_prev: datetime | None = None, isTimer: bool = True) -> datetime:
    counter+=1
    print(f"{blue}{msg}{reset} (step {counter})")
    if isTimer:
        time_now = datetime.now()
        delta_start = time_now - time_start
        print(f"\t⏲ {"Elapsed time since beginning:":<30} {green}{round(delta_start.total_seconds(), 2)}{reset} seconds")
        if time_prev != None:
            delta_prev = time_now - time_prev
            print(f"\t⏲ {"Elapsed time since prev. step:":<30} {green}{round(delta_prev.total_seconds(), 2)}{reset} seconds")
        return (time_now, counter)
    return (None, counter)