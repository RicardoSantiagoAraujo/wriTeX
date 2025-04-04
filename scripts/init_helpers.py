import os
import glob
import shutil

### Pimping up the console output
bold = '\033[1m' # to make console text bold
reset = '\033[0m'  # to revert o normal
# Color codes
red = '\033[31m'
green = '\033[32m'
blue = '\033[34m'



build_folder = 'auxiliary_files' # folder name where the LaTeX build compilation outputs are placed

def initial_prompt(thing_type):
        # clear terminal
    os.system('clear')
    print('\t****************************************************************************************************')
    print(f'\t {bold}You are about to initiate a new {green}{thing_type}{reset} folder and respective files based on the existing template.{reset}')
    print(f'\t Script works with shell languages: {blue+bold}zsh (MacOS){reset}, {blue+bold}Batch Scripting (windows){reset}')
    print('\t****************************************************************************************************\n')

    print((f'Type {bold+red}"q"{reset} or {bold+red}"quit"{reset} to exit program'))
    print((f'File name convention: use only {bold+green}lowercase{reset}  characters and {bold+green}underscores{reset} for spaces (script performs automatic correction).'))
    print('')

def final_message(thing_type, new_thing_name):
    print(f"\n\n 😁😁😁 {thing_type} successfully created with name: {bold+green}{new_thing_name}{reset} 😁😁😁")
    print(f'\n You can now edit the files directly in the {bold+green}{new_thing_name}{reset} folder \n')

progress_cnt = 1
def print_progress_msg(msg_content):
    global progress_cnt
    print(f"\n✅✅✅ {bold}({progress_cnt}){reset} {msg_content}")
    progress_cnt += 1


def rename_file(folder_path, old_name, new_name):
    if os.name == 'posix': # if Unix-like OS (e.g., Linux, MacOS)
        old_path = folder_path + f"/{old_name}.tex"
        new_path = folder_path + "/" + new_name + ".tex"
        os.system("mv " + old_path + " " +  new_path)
    elif os.name == 'nt': # if Windows OS
        old_path = folder_path + f"\\{old_name}.tex"
        new_path = folder_path + "\\" + new_name + ".tex"
        os.system("move " + old_path + " " +  new_path)


def delete_build(folder_path):
    if os.name == 'posix': # if Unix-like OS (e.g., Linux, MacOS)
        shutil.rmtree(os.path.join(folder_path, build_folder))
    elif os.name == 'nt': # if Windows OS
        os.system("del /S /Q " +  folder_path + f'\\{build_folder}\\* > NUL') # delete files
        os.system("rmdir /S /Q " + folder_path + f'\\{build_folder}') # delete directories

def delete_md_aux(folder_path):
    # Create the path for the target folder using a wildcard
    pattern = os.path.join(folder_path, "_markdown*")
    # Use glob to find all directories that partially match "_markdown"
    matching_dirs = glob.glob(pattern)
    # Iterate over the matching directories and delete them
    for dir_path in matching_dirs:
        if os.name == 'posix': # if Unix-like OS (e.g., Linux, MacOS)
            shutil.rmtree(dir_path)
        elif os.name == 'nt': # if Windows OS
            os.system("del /S /Q " +  dir_path + f' > NUL') # delete files
            os.system("rmdir /S /Q " + dir_path) # delete directories




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


def list_existing_things(dir_path):
    # list of thing names already used
    names = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        # check if path is directory:
        if os.path.isdir(file_path):
            names.append(file_name)
    print("\nNames already in use:")
    for name in names:
        print("- " + name)
    print("")
    return names



def request_name(thing_type, existing_names):
    new_name = input("Write filename for new {thing_type}: ").lower().replace(" ", "_")
    # check if thing already exists and keep requesting name until original name is given or user quits:
    while new_name in existing_names:
        if new_name != "q" and new_name != "quit":
            print("{thing_type} already exists. Please pick a new name or quit.\n")
            new_name =  request_name(existing_names)
        else:
            print("\nProgram quit without creation of new {thing_type}.")
            exit()
    return new_name



def create_new_folder_with_files(new_name, template_name, dir_path):
    if new_name != "q" and new_name != "quit":

        # copy all contents of template folder into newly created folder
        if os.name == 'posix': # if Unix-like OS (e.g., Linux, MacOS)
            # create file in versions folder with chosen name
            new_folder = dir_path + '/' + new_name
            os.system('mkdir ' + new_folder)
            os.system(f'cp -R  {dir_path}/{template_name}/. {new_folder}')
        elif os.name == 'nt': # if Windows OS
            # create file in versions folder with chosen name
            new_folder = dir_path + '\\' + new_name
            os.system('mkdir ' + new_folder)
            os.system(f'xcopy  {dir_path}\\{template_name}\\* {new_folder} /E /I > NUL')

        print_progress_msg(f'Created new folder with contents from {bold+green}{template_name}{reset} ')
    else:
        print("\nProgram quit without creation of new file.")
        exit()
    return new_folder