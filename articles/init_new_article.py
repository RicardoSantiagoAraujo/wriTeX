# Script to automatically create and cleanup new article files and folder from template
import os
import glob

# CONSTANTS
article_template_string = "article_template" # change here if the name of the template changes
build_folder = 'auxiliary_files' # folder name where the LaTeX build compilation outputs are placed
biblatex_filepath = "../articles_common_files/biblatex_files/myArticles.bib" # change here if the name of the template changes
# biblatex entries: update if the myarticle type is updated in settings
biblatex_fields=[
    "title", "shorttitle", "subtitle", "url", "doi", "abstract", "author", "translator", "illustrator", "reviewer", "thank", "month", "year", "note", "pages", "file", "language", "targetPublication", "audienceLevel", "wordMin", "wordMax", "charMin", "charMax", "keywords", "discipline", "copyright", "mainSource"
]

### Pimping up the console output
bold = '\033[1m' # to make console text bold
reset = '\033[0m'  # to revert o normal
# Color codes
red = '\033[31m'
green = '\033[32m'
blue = '\033[34m'

def main():
    ### MAIN PROGRAM ###
    # get the directory of the current script
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Print initial prompt
    initial_prompt()
    # Get list of existing articles
    article_names =list_existing_articles(dir_path)
    # ask user for desired name for the new article
    new_article_name = request_article_name(article_names)

    #### Creating new article folder/files:
    # create article unless user quits
    new_folder = create_new_folder_with_files(new_article_name, dir_path)

    #### Cleaning up files in folder:
    # Rename template latex file with new filename
    old_path = new_folder + f"/{article_template_string}.tex"
    new_path = new_folder + "/" + new_article_name + ".tex"
    if os.name == 'posix': # if Unix-like OS (e.g., Linux, MacOS)
        os.system("mv " + old_path + " " +  new_path)
    elif os.name == 'nt': # if Windows OS
        os.system("move " + old_path + " " +  new_path)



    # Remove template auxiliary folder and files
    if os.name == 'posix': # if Unix-like OS (e.g., Linux, MacOS)
        os.system("rm -r " +  new_folder + f'/{build_folder}/*')
    elif os.name == 'nt': # if Windows OS 
        os.system("del /S /Q " +  new_folder + f'\\{build_folder}\\* > NUL') # delete files
        os.system("rmdir /S /Q " + new_folder + f'\\{build_folder}') # delete directories


    # Remove template markdown auxiliary files
    # Create the path for the target folder using a wildcard
    pattern = os.path.join(new_folder, "_markdown*")
    # Use glob to find all directories that partially match "_markdown"
    matching_dirs = glob.glob(pattern)
    # Iterate over the matching directories and delete them
    for dir_path in matching_dirs:
        if os.name == 'posix': # if Unix-like OS (e.g., Linux, MacOS)
            os.system("rm -r " +  dir_path)
        elif os.name == 'nt': # if Windows OS 
            os.system("del /S /Q " +  dir_path + f' > NUL') # delete files
            os.system("rmdir /S /Q " + dir_path) # delete directories


    # Replace template article name
    replace_string_in_tex_file(f"{new_folder}/document.tex", article_template_string, new_article_name)
    print(f'\n\n You can now edit the files directly in the {new_article_name} folder')


    print(f'\n\n Would you also like to create a new {blue}biblatex{reset} entry for {green+bold}{new_article_name}{reset} ?')
    is_create_new_bib = input("(y/N) :").lower()
    if is_create_new_bib.lower().strip() in ["y","yes"]:
        update_biblatex_file(new_article_name)
        replace_string_in_tex_file(f"{new_folder}/{new_article_name}.tex", article_template_string, new_article_name)
    else:
        print(f'\n You will have to manually create a new bib entry in {green}{biblatex_filepath}{reset}.\n')




###############################################################################
###############################################################################
###############################################################################

### USED FUNCTIONS ###
def initial_prompt():
        # clear terminal
    os.system('clear')
    print('\t****************************************************************************************************')
    print(f'\t {bold}You are about to initiate a new article folder and respective files based on the existing template.{reset}')
    print(f'\t Script works with shell languages: {blue+bold}zsh (MacOS){reset}, {blue+bold}Batch Scripting (windows){reset}')
    print('\t****************************************************************************************************\n')

    print((f'Type {bold+red}"q"{reset} or {bold+red}"quit"{reset} to exit program'))
    print((f'File name convention: use only {bold+green}lowercase{reset}  characters and {bold+green}underscores{reset} for spaces (script performs automatic correction).'))
    print('')


def list_existing_articles(dir_path):
    # list of article names already used
    article_names = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        # check if path is directory:
        if os.path.isdir(file_path):
            article_names.append(file_name)
    print("\nArticle names already in use:")
    for name in article_names:
        print("- " + name)
    print("")
    return article_names


def request_article_name(article_names):
    new_article_name = input("Write filename for new article: ").lower().replace(" ", "_")
    # check if article already exists and keep requesting name until original name is given or user quits:
    while new_article_name in article_names:
        if new_article_name != "q" and new_article_name != "quit":
            print("Article already exists. Please pick a new name or quit.\n")
            new_article_name =  request_article_name(article_names)
        else:
            print("\nProgram quit without creation of new file.")
            exit()
    return new_article_name

def create_new_folder_with_files(new_article_name, dir_path):
    if new_article_name != "q" and new_article_name != "quit":

        # copy all contents of article template folder into newly created folder
        if os.name == 'posix': # if Unix-like OS (e.g., Linux, MacOS)
            # create file in versions folder with chosen article name
            new_folder = dir_path + '/' + new_article_name
            os.system('mkdir ' + new_folder)
            os.system(f'cp -R  {dir_path}/{new_article_name}/. {new_folder}')
        elif os.name == 'nt': # if Windows OS
            # create file in versions folder with chosen article name
            new_folder = dir_path + '\\' + new_article_name
            os.system('mkdir ' + new_folder)
            os.system(f'xcopy  {dir_path}\\{article_template_string}\\* {new_folder} /E /I > NUL')

        print(f"\n\n 🙂🙂🙂 Article successfully created with name: {bold+green}{new_article_name}{reset} 🙂🙂🙂")
    else:
        print("\nProgram quit without creation of new file.")
        exit()
    return new_folder

# Function to replace specific string in specific tex file
def replace_string_in_tex_file(file_path, old_word, new_word):
    # Open the .tex file and read the contents
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    # Replace the specific word with the new word
    modified_content = file_content.replace(old_word, new_word)

    # Open the file again in write mode and save the modified content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)
    # print(f"'{old_word}' has been replaced with '{new_word}' in {file_path}.")


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
            val = input(f"Value for {green}{bold}{field}{reset} ? You may leave it empty: " )
            # append field line
            new_entry += f'\n\t{field}={{{val}}},'
        # close entry
        new_entry += f"\n}}"
        # write to file
        file.write(new_entry)
        print(f"\n Text has been appended to {blue}{biblatex_filepath}{reset}.")
        print(f"\n You may change file manually.")
        print(f"\n {bold}LaTeX Workshop{reset} may instantly pop up an error message.")


if __name__ == "__main__":
    main()