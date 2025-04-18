# LaTeX workshop is set up to used latexmk, which automates the proccess of generating a latex document. Under the hood, it calls a latex compiler, e.g., lualatex.
# However, it might be slow, so alternatively you can use this script which calls lualatex directly.

import argparse
from ..utils.prompts import first_prompt
from ..enums.BuildMode import BuildMode
from ..utils.style_console_text import blue, reset

from .functions import (
    thing_name_list_as_string,
    deal_with_user_input,
)

from .compiler import perform_build_steps


def main():
    """Main function of script to compile an existing LaTeX document (article or portfolio) into a PDF."""

    first_prompt("Script for pdf compilation from existing document (article or portfolio)"
    )
    # Create command line argument parser
    parser = argparse.ArgumentParser(description="arTeX compilation with biblatex.")
    # Add arguments
    parser.add_argument(
        "thing_name",
        nargs="?",
        type=str,
        help=f"Document to compile. Available options: {thing_name_list_as_string}.",
        default=None,
    )
    parser.add_argument(
        "mode",
        nargs="?",
        type=str,
        help=f"Compilation mode. Available options: {", ".join([f"{blue}{e.value}{reset}" for e in BuildMode])}.",
        default=BuildMode.full.value,
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="prints compilation information to console"
    )
    parser.add_argument(
        "-t", "--timer", action="store_true", help="logs compilation duration to console"
    )
    parser.add_argument(
        "-w", "--watch", action="store_true", help="watch for changes and automatically recompile"
    )
    # Parse the arguments
    args = parser.parse_args()

    args = deal_with_user_input(args)

    perform_build_steps(args)


if __name__ == "__main__":
    main()
