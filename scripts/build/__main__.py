# LaTeX workshop is set up to used latexmk, which automates the proccess of generating a latex document. Under the hood, it calls a latex compiler, e.g., lualatex.
# However, it might be slow, so alternatively you can use this script which calls lualatex directly.

import argparse
from ..utils.prompts import first_prompt
from .functions import (
    thing_name_list_as_string,
    deal_with_user_input,
    perform_build_steps,
)


def main():
    """Main function of script to compile an existing LaTeX document (article or portfolio) into a PDF."""

    first_prompt(
        "Script for pdf compilation from existing document (article or portfolio)"
    )
    # Create command line argument parser
    parser = argparse.ArgumentParser(description="arTeX compilation with biblatex.")
    # Add arguments
    parser.add_argument(
        "thing_name",
        nargs="?",
        type=str,
        help=f"available options: {thing_name_list_as_string}",
        default=None,
    )
    # parser.add_argument('thing_type', type=str, help=f"available options: {thing_type_list_as_string}")
    parser.add_argument(
        "--biber", type=bool, help="Whether to run biber too", default=True
    )
    # Parse the arguments
    args = parser.parse_args()

    args.thing_name = deal_with_user_input(args.thing_name)

    thing_name = args.thing_name

    perform_build_steps(thing_name)


if __name__ == "__main__":
    main()
