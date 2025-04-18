import subprocess
import os
from ..utils.style_console_text import red, green, blue, bold, reset
from functions import (
    dir_path,
    create_build_directories,
    trigger_biber,
    trigger_biblatex,
)
from parameters import (
    articles_directory,
    portfolios_directory,
    build_folder__aux_files,
    build_folder__main_output,
)


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
