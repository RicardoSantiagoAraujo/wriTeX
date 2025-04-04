# Script to automatically create and cleanup new article files and folder from template
import os
import glob
import sys

# Add parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, parent_dir)

import scripts.init_helpers as h

# CONSTANTS
portfolio_template_string = "portfolio_template" # change here if the name of the template changes


def main():
    ### MAIN PROGRAM ###
    # get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Print initial prompt
    h.initial_prompt("Portfolio")
    # Get list of existing articles
    version_names =h.list_existing_things(dir_path)
    # ask user for desired name for the new article
    new_portfolio_name = h.request_name("Portfolio", version_names)

    #### Creating new portfolio version folder/files:
    # create portfolio version unless user quits
    new_folder = h.create_new_folder_with_files(new_portfolio_name, portfolio_template_string, dir_path)

    #### Cleaning up files in folder:

    # Remove template build folder and files
    h.delete_build(new_folder)
    h.print_progress_msg(f'Removed old build folder {h.bold+h.green}{h.build_folder}{h.reset} from new portfolio')

    # Remove template markdown auxiliary files
    h.delete_md_aux(new_folder)
    h.print_progress_msg(f'Removed old {h.bold+h.green}_markdown{h.reset} folder from new portfolio ')

    # Print success message
    h.final_message("Portfolio", new_portfolio_name)


###############################################################################
###############################################################################
###############################################################################



if __name__ == "__main__":
    main()