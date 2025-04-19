# Script to automatically create and cleanup new article files and folder from template
import os
from scripts.utils.helpers import *
from scripts.utils.prompts import first_prompt__initiate_document
from scripts.utils.style_console_text import red, green, blue, bold, reset
from scripts.enums.ThingType import ThingType

# CONSTANTS
article_template_string = (
    "article_template"  # change here if the name of the template changes
)
articles_directory = "./../../articles/"  # relative to script location
biblatex_filepath = "../../articles_common_files/biblatex_files/myArticles.bib"  # change here if the name of the template changes
# biblatex entries: update if the myarticle type is updated in settings
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
    ### MAIN PROGRAM ###
    # Print initial prompt
    first_prompt__initiate_document(ThingType("Article").value)
    # Get list of existing articles
    article_names = list_existing_things(
        dir_path, header_message="Articles names already in use:"
    )
    # ask user for desired name for the new article
    new_article_name = request_name(ThingType("Article").value, article_names)

    #### Creating new article folder/files:
    # create article unless user quits
    new_folder = create_new_folder_with_files(
        new_article_name, article_template_string, dir_path
    )

    #### Cleaning up files in folder:
    # Rename template latex file with new filename
    rename_file(new_folder, article_template_string, new_article_name)
    print_progress_msg(
        f"Renamed files inside new folder as {bold+green}{new_article_name}{reset}"
    )

    # Remove template build folder and files
    delete_build(new_folder)
    print_progress_msg(
        f"Removed old build folder {bold+green}{build_folder}{reset} from new article"
    )

    # Remove template markdown auxiliary files
    delete_md_aux(new_folder)
    print_progress_msg(
        f"Removed old {bold+green}_markdown{reset} folder from new article "
    )

    # Remove template expanded files
    delete_expanded(ThingType("Article").value, new_folder)
    print_progress_msg(
        f"Removed old {bold+green}expanded{reset} file from new article "
    )

    # Replace template article name
    replace_string_in_tex_file(
        new_folder, "document.tex", article_template_string, new_article_name
    )
    replace_string_in_tex_file(
        new_folder,
        f"{new_article_name}.tex",
        article_template_string,
        new_article_name,
    )
    print_progress_msg(
        f"Replaced old string {bold+green}{article_template_string}{reset} with {bold+green}{new_article_name}{reset} "
    )

    print("\n🙂 New article folder and files successfully generated 🙂")

    ###########################################################################
    # Give user option to generate new bib entry
    create_new_bib_entry(new_article_name, article_template_string, new_folder)

    # Print success message
    final_message(ThingType("Article").value, new_article_name)


###############################################################################
###############################################################################
###############################################################################

### USED FUNCTIONS ###


def update_biblatex_file(new_article_name: str) -> None:
    print(f"{blue}English (en) version by default 🇬🇧🇬🇧🇬🇧{reset}")
    # Open the file in append mode ('a') so that new content is added at the end
    rel_path = os.path.join(
        base_dir, biblatex_filepath
    )  # path relative to script folder
    with open(rel_path, "a", encoding="utf-8") as file:
        new_entry = f"""
        \n\n@myarticle{{myarticle:{new_article_name}:en,"""
        for i, field in enumerate(biblatex_fields):
            # print current index
            print(f"{i+1} out of {len(biblatex_fields)}")
            # Request input
            val = input(
                f"Value for {green}{bold}{field}{reset} ? You may leave it empty: "
            )
            # append field line
            new_entry += f"\n\t{field}={{{val}}},"
        # close entry
        new_entry += f"\n}}"
        # write to file
        file.write(new_entry)
        print(f"\n Text has been appended to {blue}{biblatex_filepath}{reset}.")
        print(f"\n You may change file manually.")
        print(f"\n {bold}LaTeX Workshop{reset} may instantly pop up an error message.")


def create_new_bib_entry(
    new_thing_name: str, old_thing_name: str, new_folder: str
) -> None:
    print("\n\n📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚📚")
    print(
        f"Would you also like to create a new {blue}biblatex{reset} entry for {green+bold}{new_thing_name}{reset} ?"
    )
    is_create_new_bib = input("(y/N) :").lower()
    if is_create_new_bib.lower().strip() in ["y", "yes"]:
        update_biblatex_file(new_thing_name)
        replace_string_in_tex_file(
            new_folder, f"{new_thing_name}.tex", old_thing_name, new_thing_name
        )
        print_progress_msg(
            f"Replaced old string {bold+green}{old_thing_name}{reset} with {bold+green}{new_thing_name}{reset} for bibliography"
        )

    else:
        print(
            f"\n You will have to manually create a new bib entry in {green}{biblatex_filepath}{reset}.\n"
        )


if __name__ == "__main__":
    main()
