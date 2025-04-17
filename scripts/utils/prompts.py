import os
from .style_console_text import red, green, blue, bold, reset
from ..enums.ThingType import ThingType


def first_prompt(custom_prompt: str = None) -> None:
    """Print first prompt when script is lauched.

    Args:
        custom_prompt (str, optional): Initial prompt. Defaults to None.
    """
    # clear terminal
    os.system("cls" if os.name == "nt" else "clear")
    print(
        "\t****************************************************************************************************"
    )
    print("\t" + bold + custom_prompt + reset)
    print(
        f"\tScript works with shell languages: {blue+bold}zsh (MacOS){reset}, {blue+bold}Batch Scripting (windows){reset}"
    )
    print(
        "\t****************************************************************************************************\n"
    )

    print(
        (
            f"File name convention: use only {bold+green}lowercase{reset}  characters and {bold+green}underscores{reset} for spaces (script performs automatic correction)."
        )
    )
    print((f'Type {bold+red}"q"{reset} or {bold+red}"quit"{reset} to exit program'))
    print("")


def first_prompt__initiate_document(thing_type: ThingType) -> None:
    """Print initial prompt instructing user on how to use script.

    Args:
        thing_type (ThingType): type of object to generate: article or portfolio.
    """

    first_prompt(
        f"{bold}You are about to initiate a new {green}{thing_type}{reset} folder and respective files based on the existing template.{reset}"
    )
