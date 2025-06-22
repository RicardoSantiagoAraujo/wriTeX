# Script to automatically create and cleanup new article files and folder from template
import os
from scripts.utils.helpers import *
from scripts.utils.prompts import first_prompt__initiate_document
from scripts.utils.style_console_text import red, green, blue, bold, reset
from scripts.enums.ThingType import ThingType

# CONSTANTS
wrtx_portfolio_template_string = "wrtx_portfolio_template"  # change here if the name of the template changes
portfolio_versions_directory = "./../../portfolios/versions/"  # relative to script location

# get the directory of the current script
base_dir = os.path.dirname(os.path.realpath(__file__))  # dir of current file
dir_path = os.path.join(base_dir, portfolio_versions_directory)


def main():
    """Main function to initialise an empty portfolio version."""
    ### MAIN PROGRAM ###
    # Print initial prompt
    first_prompt__initiate_document(ThingType("Portfolio"))
    # Get list of existing articles
    version_names = list_existing_things(dir_path, header_message="Portfolio names already in use:")
    # ask user for desired name for the new article
    new_portfolio_name = request_name(ThingType("Portfolio"), version_names)

    #### Creating new portfolio version folder/files:
    # create portfolio version unless user quits
    new_folder = create_new_folder_with_files(new_portfolio_name, wrtx_portfolio_template_string, dir_path)

    #### Cleaning up files in folder:

    # Remove template build folder and files
    delete_build(new_folder)
    print_progress_msg(f"Removed old build folder {sty.bold+sty.green}{build_folder}{sty.reset} from new portfolio")

    # Remove template markdown auxiliary files
    delete_md_aux(new_folder)
    print_progress_msg(f"Removed old {sty.bold+sty.green}_markdown{sty.reset} folder from new portfolio ")

    # Print success message
    final_message(ThingType("Portfolio"), new_portfolio_name)


###############################################################################
###############################################################################
###############################################################################


if __name__ == "__main__":
    main()
