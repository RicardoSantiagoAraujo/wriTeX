import subprocess
import os
from scripts.utils.style_console_text import red, green, blue, bold, reset
from scripts.compile.functions import (
    create_build_directories, article_names, articles_dir_path, portfolio_names, portfolios_dir_path, build_message, get_build_directory, get_name_of_latex_main_file
)
from .parameters import (
    articles_directory,
    portfolios_directory,
    build_folder__aux_files,
    build_folder__main_output,
)
from scripts.compile.recipes import recipe__biber, recipe__full, recipe__lualatex
from scripts.enums.Recipe import Recipe
import argparse
from datetime import datetime


def perform_build_steps(args: argparse.Namespace):
    """Compile a LaTeX document (article or portfolio) with lualaTeX.

    Args:
        args (argparse.Namespace): namespace with arguments parsed via command line.
    """

    build_directory = get_build_directory(args)
    latex_doc_name = get_name_of_latex_main_file(args)

    try:
        # print( os.path.join(dir_path, thing_name + ".tex"))
        # CHANGE DIRECTORY TO THING'S
        os.chdir(build_directory)
        # CREATE BUILD FOLDERS IF IT DOES NOT EXIST
        create_build_directories()

        print(f"\n🏗️  RECIPE FOR BUILD: {blue}{args.recipe}{reset}\n")
        match args.recipe:
            case Recipe.full.value :
                recipe__full(args, latex_doc_name)
            case Recipe.lualatex.value:
                recipe__lualatex(args, latex_doc_name)
            case Recipe.biber.value :
                recipe__biber(args, latex_doc_name)
            case _:
                print(f"{red}CHOSEN COMPILATION RECIPE ({args.recipe}) DOES NOT EXIST {reset}")
                exit()

        print(f"\n✅ {green}Compilation in {bold}{args.recipe}{reset}{green} recipe finished for {bold}{args.thing_name}{reset} \n")

    except subprocess.CalledProcessError as e:
        print("Compilation log:")
        print(e.stdout)
        print(e.stderr)
        print(f"{red}Compilation failed{reset}")
