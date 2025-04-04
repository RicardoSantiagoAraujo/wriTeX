# Script to automatically create and cleanup new article files and folder from template
import os
import sys

# Add parent directory to the system path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import scripts.init_helpers as h

# CONSTANTS
article_template_string = "article_template" # change here if the name of the template changes
biblatex_filepath = "../articles_common_files/biblatex_files/myArticles.bib" # change here if the name of the template changes
# biblatex entries: update if the myarticle type is updated in settings
biblatex_fields=[
    "title", "shorttitle", "subtitle", "url", "doi", "abstract", "author", "translator", "illustrator", "reviewer", "thank", "month", "year", "note", "pages", "file", "language", "targetPublication", "audienceLevel", "wordMin", "wordMax", "charMin", "charMax", "keywords", "discipline", "copyright", "mainSource"
]



def main():
    ### MAIN PROGRAM ###
    # get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Print initial prompt
    h.initial_prompt("article")
    # Get list of existing articles
    article_names =h.list_existing_things(dir_path)
    # ask user for desired name for the new article
    new_article_name = h.request_name("Article", article_names)

    #### Creating new article folder/files:
    # create article unless user quits
    new_folder = h.create_new_folder_with_files(new_article_name, article_template_string, dir_path)

    #### Cleaning up files in folder:
    # Rename template latex file with new filename
    h.rename_file(new_folder, article_template_string, new_article_name)
    h.print_progress_msg(f'Renamed files inside new folder as {h.bold+h.green}{new_article_name}{h.reset}')

    # Remove template build folder and files
    h.delete_build(new_folder)
    h.print_progress_msg(f'Removed old build folder {h.bold+h.green}{h.build_folder}{h.reset} from new article')

    # Remove template markdown auxiliary files
    h.delete_md_aux(new_folder)
    h.print_progress_msg(f'Removed old {h.bold+h.green}_markdown{h.reset} folder from new article ')


    # Replace template article name
    h.replace_string_in_tex_file(f"{new_folder}/document.tex", article_template_string, new_article_name)
    h.replace_string_in_tex_file(f"{new_folder}/{new_article_name}.tex", article_template_string, new_article_name)
    h.print_progress_msg(f'Replaced old string {h.bold+h.green}{article_template_string}{h.reset} with {h.bold+h.green}{new_article_name}{h.reset} ')

    print("\n🙂 New article folder and files successfully generated 🙂")

    ###########################################################################
    # Give user option to generate new bib entry
    create_new_bib_entry(new_article_name, article_template_string ,new_folder)

    # Print success message
    h.final_message("Article", new_article_name)


###############################################################################
###############################################################################
###############################################################################

### USED FUNCTIONS ###


def update_biblatex_file(new_article_name):
    print(f"English (en) version by default 🇬🇧")
    # Open the file in append mode ('a') so that new content is added at the end
    with open(biblatex_filepath, 'a', encoding='utf-8') as file:
        new_entry =f"""
        \n\n@myarticle{{myarticle:{new_article_name}:en,"""
        for i, field in enumerate(biblatex_fields):
            # print current index
            print(f'{i+1} out of {len(biblatex_fields)}')
            # Request input
            val = input(f"Value for {h.green}{h.bold}{field}{h.reset} ? You may leave it empty: " )
            # append field line
            new_entry += f'\n\t{field}={{{val}}},'
        # close entry
        new_entry += f"\n}}"
        # write to file
        file.write(new_entry)
        print(f"\n Text has been appended to {h.blue}{biblatex_filepath}{h.reset}.")
        print(f"\n You may change file manually.")
        print(f"\n {h.bold}LaTeX Workshop{h.reset} may instantly pop up an error message.")



def create_new_bib_entry(new_thing_name, old_thing_name, new_folder):
        print(f'\n\n Would you also like to create a new {h.blue}biblatex{h.reset} entry for {h.green+h.bold}{new_thing_name}{h.reset} ?')
        is_create_new_bib = input("(y/N) :").lower()
        if is_create_new_bib.lower().strip() in ["y","yes"]:
            update_biblatex_file(new_thing_name)
            h.replace_string_in_tex_file(f"{new_folder}/{new_thing_name}.tex", old_thing_name, new_thing_name)
        else:
            print(f'\n You will have to manually create a new bib entry in {h.green}{biblatex_filepath}{h.reset}.\n')



if __name__ == "__main__":
    main()