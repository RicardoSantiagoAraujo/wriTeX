import os
import glob
import shutil
from .style_console_text import red, green, blue, bold, reset
from ..enums.ThingType import ThingType


build_folder = "auxiliary_files"  # folder name where the LaTeX build compilation outputs are placed


def initial_prompt(thing_type: ThingType) -> None:
    # clear terminal
    os.system("clear")
    print("\t****************************************************************************************************")
    print(
        f"\t {bold}You are about to initiate a new {green}{thing_type}{reset} folder and respective files based on the existing template.{reset}"
    )
    print(
        f"\t Script works with shell languages: {blue+bold}zsh (MacOS){reset}, {blue+bold}Batch Scripting (windows){reset}"
    )
    print("\t****************************************************************************************************\n")

    print((f'Type {bold+red}"q"{reset} or {bold+red}"quit"{reset} to exit program'))
    print(
        (
            f"File name convention: use only {bold+green}lowercase{reset}  characters and {bold+green}underscores{reset} for spaces (script performs automatic correction)."
        )
    )
    print("")


def final_message(thing_type: ThingType, new_thing_name: str) -> None:
    print(f"\n\n 😁😁😁 {thing_type} successfully created with name: {bold+green}{new_thing_name}{reset} 😁😁😁")
    print(f"\n You can now edit the files directly in the {bold+green}{new_thing_name}{reset} folder \n")


progress_cnt = 1


def print_progress_msg(msg_content: str) -> None:
    global progress_cnt
    print(f"✅✅✅ {bold}({progress_cnt}){reset} {msg_content}")
    progress_cnt += 1


def check_if_successful(function_name:str, exit_code: int, folder_path: str = None) -> None:
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


def rename_file(folder_path : str, old_name : str, new_name : str) -> None:
    if os.name == "posix":  # if Unix-like OS (e.g., Linux, MacOS)
        old_path = folder_path + f"/{old_name}.tex"
        new_path = folder_path + "/" + new_name + ".tex"
        exit_code = os.system("mv " + old_path + " " + new_path)
    elif os.name == "nt":  # if Windows OS
        old_path = folder_path + f"\\{old_name}.tex"
        new_path = folder_path + "\\" + new_name + ".tex"
        exit_code = os.system("move " + old_path + " " + new_path)
    check_if_successful(rename_file.__name__, exit_code, folder_path)


def delete_build(folder_path : str) -> None:
    try:
        shutil.rmtree(os.path.join(folder_path, build_folder))
    except:
        exit_code = 1
    else:
        exit_code = 0
    check_if_successful(delete_build.__name__, exit_code, folder_path)


def delete_md_aux(folder_path :str) -> None:
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


def delete_expanded(thing_type: ThingType, folder_path : str) -> None:
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


def replace_string_in_tex_file(new_folder : str, file_name : str, old_word : str, new_word : str) -> None:
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


def list_existing_things(dir_path : str) -> None:
    # list of thing names already used
    names = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        # check if path is directory:
        if os.path.isdir(file_path):
            names.append(file_name)
    print("\nNames already in use:")
    for i, name in enumerate(names, 1):
        print(f"{i} - {name}")
    print("")
    return names


def request_name(thing_type : ThingType, existing_names : list[str]) -> str:
    new_name = input(f"Write filename for new {thing_type}: ").lower().replace(" ", "_")
    # check if thing already exists and keep requesting name until original name is given or user quits:
    while new_name in existing_names:
        if new_name != "q" and new_name != "quit":
            print(f"{red}{thing_type} already exists.{reset} Please pick a new name or quit.\n")
            new_name = request_name(thing_type, existing_names)
        else:
            print(f"\n💀💀💀 {red}Program quit without creation of new {thing_type}.{reset}")
            exit()
    return new_name


def create_new_folder_with_files(new_name: str, template_name:str, dir_path : str) -> str:
    if new_name != "q" and new_name != "quit":
        new_folder = dir_path + "/" + new_name
        try:
            shutil.copytree(f"{dir_path}/{template_name}/.", new_folder)
        except:
            exit_code = 1
        else:
            exit_code = 0
        check_if_successful(create_new_folder_with_files.__name__, exit_code)
        print_progress_msg(f"Created new folder with contents from {bold+green}{template_name}{reset} ")
    else:
        print(f"\n💀💀💀 {red}Program quit without creation of new folder.{reset}")
        exit()
    return new_folder
