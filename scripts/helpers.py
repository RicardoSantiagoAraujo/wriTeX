import os
import glob
import shutil

from enum import Enum


class ThingType(Enum):
    Article = "Article"
    Portfolio = "Portfolio"


### Pimping up the console output
bold = "\033[1m"  # to make console text bold
reset = "\033[0m"  # to revert o normal
# Color codes
red = "\033[31m"
green = "\033[32m"
blue = "\033[34m"


build_folder = "auxiliary_files"  # folder name where the LaTeX build compilation outputs are placed


def initial_prompt(thing_type):
    # clear terminal
    os.system("clear")
    print(
        "\t****************************************************************************************************"
    )
    print(
        f"\t {bold}You are about to initiate a new {green}{thing_type}{reset} folder and respective files based on the existing template.{reset}"
    )
    print(
        f"\t Script works with shell languages: {blue+bold}zsh (MacOS){reset}, {blue+bold}Batch Scripting (windows){reset}"
    )
    print(
        "\t****************************************************************************************************\n"
    )

    print((f'Type {bold+red}"q"{reset} or {bold+red}"quit"{reset} to exit program'))
    print(
        (
            f"File name convention: use only {bold+green}lowercase{reset}  characters and {bold+green}underscores{reset} for spaces (script performs automatic correction)."
        )
    )
    print("")


def final_message(thing_type, new_thing_name):
    print(
        f"\n\n 😁😁😁 {thing_type} successfully created with name: {bold+green}{new_thing_name}{reset} 😁😁😁"
    )
    print(
        f"\n You can now edit the files directly in the {bold+green}{new_thing_name}{reset} folder \n"
    )


progress_cnt = 1


def print_progress_msg(msg_content):
    global progress_cnt
    print(f"✅✅✅ {bold}({progress_cnt}){reset} {msg_content}")
    progress_cnt += 1


def check_if_successful(function_name, exit_code, folder_path=None):
    global progress_cnt
    print(f"\nStep {progress_cnt}:{blue} {function_name}{reset}...")
    if exit_code == 0:
        return
    elif exit_code != 0:
        print(f"❌❌❌ ({progress_cnt}) {red} STEP FAILED. CANCEL CREATION. {reset}")
        if folder_path != None:
            # Delete created thing
            shutil.rmtree(folder_path)
        # exit script
        exit()


def rename_file(folder_path, old_name, new_name):
    if os.name == "posix":  # if Unix-like OS (e.g., Linux, MacOS)
        old_path = folder_path + f"/{old_name}.tex"
        new_path = folder_path + "/" + new_name + ".tex"
        exit_code = os.system("mv " + old_path + " " + new_path)
    elif os.name == "nt":  # if Windows OS
        old_path = folder_path + f"\\{old_name}.tex"
        new_path = folder_path + "\\" + new_name + ".tex"
        exit_code = os.system("move " + old_path + " " + new_path)
    check_if_successful(rename_file.__name__, exit_code, folder_path)


def delete_build(folder_path):
    try:
        shutil.rmtree(os.path.join(folder_path, build_folder))
    except:
        exit_code = 1
    else:
        exit_code = 0
    check_if_successful(delete_build.__name__, exit_code, folder_path)


def delete_md_aux(folder_path):
    # Create the path for the target folder using a wildcard
    pattern = os.path.join(folder_path, "_markdown*")
    # Use glob to find all directories that partially match "_markdown"
    matching_dirs = glob.glob(pattern)
    # Iterate over the matching directories and delete them
    exit_code = 0
    for dir_path in matching_dirs:
        try:
            shutil.rmtree(dir_path)
        except:
            exit_code += 1
    check_if_successful(delete_md_aux.__name__, exit_code, folder_path)


def delete_expanded(thing_type, folder_path):
    try:
        if thing_type == ThingType("Article").value:
            file_path = os.path.join(folder_path, "document_expanded.tex")
        elif thing_type == ThingType("Portfolio").value:
            file_path = os.path.join(folder_path, "portfolio_document_expanded.tex")
        # check if file exists before trying to delete to avoid error
        if os.path.exists(file_path):
            os.remove(file_path)
    except:
        exit_code = 1
    else:
        exit_code = 0
    check_if_successful(delete_expanded.__name__, exit_code, folder_path)


# Function to replace specific string in specific tex file
replace_str_cnt = 1


def replace_string_in_tex_file(new_folder, file_name, old_word, new_word):
    global replace_str_cnt
    # Open the .tex file and read the contents
    try:
        with open(os.path.join(new_folder, file_name), "r", encoding="utf-8") as file:
            file_content = file.read()

        # Replace the specific word with the new word
        modified_content = file_content.replace(old_word, new_word)

        # Open the file again in write mode and save the modified content
        with open(os.path.join(new_folder, file_name), "w", encoding="utf-8") as file:
            file.write(modified_content)
    except:
        exit_code = 1
    else:
        exit_code = 0
    check_if_successful(
        f"{replace_string_in_tex_file.__name__} ({replace_str_cnt})",
        exit_code,
        new_folder,
    )
    replace_str_cnt += 1


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
    new_name = input(f"Write filename for new {thing_type}: ").lower().replace(" ", "_")
    # check if thing already exists and keep requesting name until original name is given or user quits:
    while new_name in existing_names:
        if new_name != "q" and new_name != "quit":
            print(
                f"{red}{thing_type} already exists.{reset} Please pick a new name or quit.\n"
            )
            new_name = request_name(thing_type, existing_names)
        else:
            print(
                f"\n💀💀💀 {red}Program quit without creation of new {thing_type}.{reset}"
            )
            exit()
    return new_name


def create_new_folder_with_files(new_name, template_name, dir_path):
    if new_name != "q" and new_name != "quit":
        new_folder = dir_path + "/" + new_name
        try:
            shutil.copytree(f'{dir_path}/{template_name}/.', new_folder)
        except:
            exit_code = 1
        else:
            exit_code = 0
        check_if_successful(create_new_folder_with_files.__name__, exit_code)
        print_progress_msg(
            f"Created new folder with contents from {bold+green}{template_name}{reset} "
        )
    else:
        print(f"\n💀💀💀 {red}Program quit without creation of new folder.{reset}")
        exit()
    return new_folder
