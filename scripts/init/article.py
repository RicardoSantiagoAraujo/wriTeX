# Script to automatically create and cleanup new article files and folder from template
import os
from scripts.utils.helpers import *
from scripts.utils.prompts import first_prompt__initiate_document
import scripts.utils.style_console_text as sty
from scripts.enums.ThingType import ThingType

# CONSTANTS
wrtx_article_template_string = "wrtx_article_template"  # change here if the name of the template changes
articles_directory = "./../../articles/"  # relative to script location
biblatex_filepath = (
    "../../articles_common_files/biblatex_files/wrtxArticles.bib"  # change here if the name of the template changes
)
# biblatex entries: update if the wrtxarticle type is updated in settings
biblatex_fields = [
    "title",
    "shorttitle",
    "subtitle",
    "url",
    "doi",
    "abstract",
    "author",
    "translator",
    "illustrator",
    "reviewer",
    "thank",
    "month",
    "year",
    "note",
    "pages",
    "file",
    "language",
    "targetPublication",
    "audienceLevel",
    "wordMin",
    "wordMax",
    "charMin",
    "charMax",
    "keywords",
    "discipline",
    "copyright",
    "mainSource",
]

# get the directory of the current script
base_dir = os.path.dirname(os.path.realpath(__file__))  # dir of current file
dir_path = os.path.join(base_dir, articles_directory)


def main():
    """Main function to initialise an empty article and optionally create a bib entry for it."""
    ### MAIN PROGRAM ###
    # Print initial prompt
    first_prompt__initiate_document(ThingType("Article").value)
    # Get list of existing articles
    article_names = list_existing_things(dir_path, header_message="Articles names already in use:")
    # ask user for desired name for the new article
    new_article_name = request_name(ThingType("Article").value, article_names)

    #### Creating new article folder/files:
    # create article unless user quits
    new_folder = create_new_folder_with_files(new_article_name, wrtx_article_template_string, dir_path)

    #### Cleaning up files in folder:
    # Rename template latex file with new filename
    rename_file(new_folder, wrtx_article_template_string, new_article_name)
    print_progress_msg(f"Renamed files inside new folder as {sty.bold+sty.green}{new_article_name}{sty.reset}")

    # Remove template build folder and files
    delete_build(new_folder)
    print_progress_msg(f"Removed old build folder {sty.bold+sty.green}{build_folder}{sty.reset} from new article")

    # Remove template markdown auxiliary files
    delete_md_aux(new_folder)
    print_progress_msg(f"Removed old {sty.bold+sty.green}_markdown{sty.reset} folder from new article ")

    # Remove template expanded files
    delete_expanded(ThingType("Article").value, new_folder)
    print_progress_msg(f"Removed old {sty.bold+sty.green}expanded{sty.reset} file from new article ")

    # Replace template article name
    replace_string_in_tex_file(new_folder, "document.tex", wrtx_article_template_string, new_article_name)
    replace_string_in_tex_file(
        new_folder,
        f"{new_article_name}.tex",
        wrtx_article_template_string,
        new_article_name,
    )
    print_progress_msg(
        f"Replaced old string {sty.bold+sty.green}{wrtx_article_template_string}{sty.reset} with {sty.bold+sty.green}{new_article_name}{sty.reset} "
    )

    print("\n🙂 New article folder and files successfully generated 🙂")

    ###########################################################################
    # Give user option to generate new bib entry
    create_new_bib_entry(new_article_name, wrtx_article_template_string, new_folder)

    # Print success message
    final_message(ThingType("Article").value, new_article_name)


###############################################################################
###############################################################################
###############################################################################

### USED FUNCTIONS ###


def update_biblatex_file(new_article_name: str) -> None:
    """Add new entry for initialised article into the bibliography .bib file by collecting entry fields from the user.

    Args:
        new_article_name (str): name of the initialised article to be used in bib.
    """

    print(f"{sty.blue}English (en) version by default 🇬🇧🇬🇧🇬🇧{sty.reset}")
    # Open the file in append mode ('a') so that new content is added at the end
    rel_path = os.path.join(base_dir, biblatex_filepath)  # path relative to script folder
    with open(rel_path, "a", encoding="utf-8") as file:
        new_entry = f"""
        \n\n@wrtxarticle{{wrtxarticle:{new_article_name}:en,"""
        for i, field in enumerate(biblatex_fields):
            # print current index
            print(f"{i+1} out of {len(biblatex_fields)}")
            # Request input
            val = input(f"Value for {sty.green}{sty.bold}{field}{sty.reset} ? You may leave it empty: ")
            # append field line
            new_entry += f"\n\t{field}={{{val}}},"
        # close entry
        new_entry += f"\n}}"
        # write to file
        file.write(new_entry)
        print(f"\n Text has been appended to {sty.blue}{biblatex_filepath}{sty.reset}.")
        print(f"\n You may change file manually.")
        print(f"\n {sty.bold}LaTeX Workshop{sty.reset} may instantly pop up an error message.")


def create_new_bib_entry(new_thing_name: str, old_thing_name: str, new_folder: str) -> None:
    """Prompt for the optional creation of a new bibliography entry for the initialised article.

    Args:
        new_thing_name (str): name of the initialised article to be used in bib.
        old_thing_name (str): name of the reference article to be used as base for new entry.
        new_folder (str): folder containing the new article.
    """

    print("\n\n📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚")
    print(
        f"Would you also like to create a new {sty.blue}biblatex{sty.reset} entry for {sty.green+sty.bold}{new_thing_name}{sty.reset} ?"
    )
    is_create_new_bib = input("(y/N) :").lower()
    if is_create_new_bib.lower().strip() in ["y", "yes"]:
        update_biblatex_file(new_thing_name)
        replace_string_in_tex_file(new_folder, f"{new_thing_name}.tex", old_thing_name, new_thing_name)
        print_progress_msg(
            f"Replaced old string {sty.bold+sty.green}{old_thing_name}{sty.reset} with {sty.bold+sty.green}{new_thing_name}{sty.reset} for bibliography"
        )

    else:
        print(f"\n You will have to manually create a new bib entry in {sty.green}{biblatex_filepath}{sty.reset}.\n")


if __name__ == "__main__":
    main()
