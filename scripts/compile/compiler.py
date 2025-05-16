import subprocess
import os
import scripts.utils.style_console_text as sty
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

        print(f"\n🏗️  RECIPE FOR BUILD: {sty.magenta+sty.bold}{args.recipe}{sty.reset}\n")
        # use dispatch to call the correct recipe instead of match case to be compatible with python <3.10
        recipe_dispatch = {
            Recipe.full.value: recipe__full,
            Recipe.lualatex.value: recipe__lualatex,
            Recipe.biber.value: recipe__biber,
        }

        if args.recipe in recipe_dispatch:
            recipe_dispatch[args.recipe](args, latex_doc_name)
        else:
            print(f"{sty.red}CHOSEN COMPILATION RECIPE ({args.recipe}) DOES NOT EXIST{sty.reset}")
            exit()

        print(f"\n✅ {sty.green}Compilation in {sty.bold}{args.recipe}{sty.reset}{sty.green} recipe finished for {sty.bold}{args.thing_name}{sty.reset} \n")

    except subprocess.CalledProcessError as e:
        print("Compilation log:")
        print(e.stdout)
        print(e.stderr)
        print(f"{sty.red}Compilation failed{sty.reset}")
