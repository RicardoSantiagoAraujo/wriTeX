import os
import scripts.utils.style_console_text as sty
from scripts.enums.ThingType import ThingType
import shutil


def first_prompt(custom_prompt: str = None) -> None:
    """Print first prompt when script is lauched.

    Args:
        custom_prompt (str, optional): Initial prompt. Defaults to None.
    """
    # clear terminal
    os.system("cls" if os.name == "nt" else "clear")
    # get width of console in characters
    console_w = shutil.get_terminal_size().columns
    print(f"\t{'*' * (console_w - 8*2)}")
    print(f"\t{sty.bold}{sty.blue}{custom_prompt.center(console_w - 8*2)}{sty.reset}")
    print(f"\t{'*' * (console_w - 8*2)}\n")
    print(
        f"\t{f'Script works with shell languages: {sty.blue+sty.bold}zsh (MacOS){sty.reset}, {sty.blue+sty.bold}Batch Scripting (windows){sty.reset}'}"
    )

    print(
        (
            f"\tFile name convention: use only {sty.bold+sty.green}lowercase{sty.reset}  characters and {sty.bold+sty.green}underscores{sty.reset} for spaces (script performs automatic correction)."
        )
    )
    print((f'\tType {sty.bold+sty.red}"q"{sty.reset} or {sty.bold+sty.red}"quit"{sty.reset} to exit program'))
    print(f"\t{'_' * (console_w - 8*2)}\n")


def first_prompt__initiate_document(thing_type: ThingType) -> None:
    """Print initial prompt instructing user on how to use script.

    Args:
        thing_type (ThingType): type of object to generate: article or portfolio.
    """

    first_prompt(
        f"{sty.bold}You are about to initiate a new {sty.green}{thing_type}{sty.reset} folder and respective files based on the existing template.{sty.reset}"
    )
