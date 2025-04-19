import subprocess
import os
from scripts.utils.style_console_text import red, green, blue, bold, reset
from scripts.compile.functions import (
    create_build_directories, article_names, articles_dir_path, portfolio_names, portfolios_dir_path, build_message
)
from scripts.compile.proccesses import trigger_biber, trigger_lualatex

from scripts.enums.Recipe import Recipe
import argparse
from datetime import datetime


def recipe__full(args: argparse.Namespace, latex_doc_name: str):
    """Recipe for full compilation: lualatex x1, biber x1, lualatex x2

    Args:
        args (argparse.Namespace): arguments object
        latex_doc_name (str): name of main latex file to be used for compilation
    """
    thing_name = args.thing_name
    verbose_bool = args.verbose
    timer_bool = args.timer

    step_counter = 0
    time_start = datetime.now()

    time_prev, step_counter = build_message("start of compilation",step_counter, time_start, isTimer=timer_bool)
    trigger_lualatex(thing_name, latex_doc_name,  printout=verbose_bool)
    time_prev, step_counter  = build_message("end of lualatex compilation",step_counter, time_start, time_prev, isTimer=timer_bool)
    trigger_biber(thing_name, latex_doc_name,  printout=verbose_bool)
    time_prev, step_counter  = build_message("end of biber compilation", step_counter, time_start, time_prev, isTimer=timer_bool)
    trigger_lualatex(thing_name, latex_doc_name,  printout=verbose_bool)
    time_prev, step_counter  = build_message("end of lualatex compilation", step_counter, time_start, time_prev, isTimer=timer_bool)
    trigger_lualatex(thing_name,latex_doc_name, printout=verbose_bool)
    time_prev, step_counter  = build_message("end of lualatex compilation (LAST)",step_counter, time_start, time_prev, isTimer=timer_bool)


def recipe__biber(args: argparse.Namespace, latex_doc_name: str):
    """Recipe for compiling with biber x1

    Args:
        args (argparse.Namespace): arguments object
        latex_doc_name (str): name of main latex file to be used for compilation
    """
    thing_name = args.thing_name
    verbose_bool = args.verbose
    timer_bool = args.timer

    step_counter = 0
    time_start = datetime.now()

    time_prev, step_counter = build_message("start of compilation",step_counter, time_start, isTimer=timer_bool)
    trigger_biber(thing_name, latex_doc_name,  printout=verbose_bool)
    time_prev, step_counter  = build_message("end of biber compilation", step_counter, time_start, time_prev, isTimer=timer_bool)




def recipe__lualatex(args: argparse.Namespace, latex_doc_name: str):
    """Recipe for compiling with lualatex x1

    Args:
        args (argparse.Namespace): arguments object
        latex_doc_name (str): name of main latex file to be used for compilation
    """
    thing_name = args.thing_name
    verbose_bool = args.verbose
    timer_bool = args.timer

    step_counter = 0
    time_start = datetime.now()

    time_prev, step_counter = build_message("start of compilation",step_counter, time_start, isTimer=timer_bool)
    trigger_lualatex(thing_name, latex_doc_name,  printout=verbose_bool)
    time_prev, step_counter  = build_message("end of biber compilation", step_counter, time_start, time_prev, isTimer=timer_bool)
