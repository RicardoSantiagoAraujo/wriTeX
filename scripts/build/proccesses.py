import subprocess
import os
from ..utils.style_console_text import red, green, blue, bold, reset
from .parameters import (
    build_folder__aux_files,
    build_folder__main_output,
)
from datetime import datetime


def trigger_biber(thing_name: str, latex_doc_name:str,  printout: bool = True) -> None:
    """Trigger biber

    Args:
        thing_name (str): name of document to compile.
        latex_doc_name (str): filename of document's main tex file.
        printout (bool, optional): Whether to print log to console or not. Defaults to True.
    """
    print(f"\n{blue}trigger_biber ...{reset}")
    result = subprocess.run(
        ["biber", os.path.join(build_folder__aux_files, f"{latex_doc_name}")],
         capture_output=True, text=True
    )

    if printout:
        print(result.stdout)


def trigger_lualatex(thing_name: str, latex_doc_name: str, printout: bool = True) -> None:
    """Trigger biblatex compilation

    Args:
        thing_name (str): name of document to compile.
        latex_doc_name (str): filename of document's main tex file.
        printout (bool, optional): Whether to print log to console or not. Defaults to True.
    """
    print(f"\n{blue}trigger_lualatex ...{reset}")
    result = subprocess.run(
        [
            "lualatex",
            "--interaction=nonstopmode",
            f"--job-name={thing_name}",  # output file(s) name
            f"--output-directory={build_folder__main_output}",  # output directory of pdf file
            f"--aux-directory={build_folder__aux_files}",  # output directory of all other auxiliary files
            f"{latex_doc_name}.tex",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    if printout:
        print(result.stdout)
