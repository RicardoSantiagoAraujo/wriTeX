import os
import glob
import shutil
import scripts.utils.style_console_text as sty
from scripts.enums.ThingType import ThingType


build_folder = "auxiliary_files"  # folder name where the LaTeX build compilation outputs are placed


def final_message(thing_type: ThingType, new_thing_name: str) -> None:
    """Print out final message to console after script has successfully ran.

    Args:
        thing_type (ThingType): type of object to generate: article or portfolio.
        new_thing_name (str): Name to use for the new object.
    """
    print(
        f"\n\n 😁😁😁 {thing_type} successfully created with name: {sty.bold+sty.green}{new_thing_name}{sty.reset} 😁😁😁"
    )
    print(f"\n You can now edit the files directly in the {sty.bold+sty.green}{new_thing_name}{sty.reset} folder \n")


progress_cnt = 1


def print_progress_msg(msg_content: str) -> None:
    """Print out progress message to console with custom content.

    Args:
        msg_content (str): Content of the progress message.
    """
    global progress_cnt
    print(f"✅✅✅ {sty.bold}({progress_cnt}){sty.reset} {msg_content}")
    progress_cnt += 1


def check_if_successful(function_name: str, exit_code: int, folder_path: str = None) -> None:
    """check if a step was successful based on its exit code.

    Args:
        function_name (str): name of the function whose result is being tested.
        exit_code (int): exit code from the function
        folder_path (str, optional): Path to folder in case it needs to be deleted after the step fails. Defaults to None.
    """
    global progress_cnt
    print(f"\nStep {progress_cnt}:{sty.blue} {function_name}{sty.reset}...")
    if exit_code == 0:
        return
    elif exit_code != 0:
        print(f"❌❌❌ ({progress_cnt}) {sty.red} STEP FAILED. CANCEL CREATION. {sty.reset}")
        if folder_path != None:
            # Delete created thing
            shutil.rmtree(folder_path)
        # exit script
        exit()


def rename_file(folder_path: str, old_name: str, new_name: str) -> None:
    """Rename a file with a new name

    Args:
        folder_path (str): path to folder where file to rename is located
        old_name (str): old file name
        new_name (str): new file name
    """
    if os.name == "posix":  # if Unix-like OS (e.g., Linux, MacOS)
        old_path = folder_path + f"/{old_name}.tex"
        new_path = folder_path + "/" + new_name + ".tex"
        exit_code = os.system("mv " + old_path + " " + new_path)
    elif os.name == "nt":  # if Windows OS
        old_path = folder_path + f"\\{old_name}.tex"
        new_path = folder_path + "\\" + new_name + ".tex"
        exit_code = os.system("move " + old_path + " " + new_path)
    check_if_successful(rename_file.__name__, exit_code, folder_path)


def delete_build(folder_path: str) -> None:
    """Delete compilation outputs from the file system

    Args:
        folder_path (str): path to build to be deleted
    """
    try:
        shutil.rmtree(os.path.join(folder_path, build_folder))
    except:
        exit_code = 1
    else:
        exit_code = 0
    check_if_successful(delete_build.__name__, exit_code, folder_path)


def delete_md_aux(folder_path: str) -> None:
    """Delete Markdown outputs from the file system

    Args:
        folder_path (str): path to markdown folder to be deleted
    """
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


def delete_expanded(thing_type: ThingType, folder_path: str) -> None:
    """Deleted expanded document from file system

    Args:
        thing_type (ThingType): type of document to be deleted
        folder_path (str): Path to expanded file to be deleted
    """
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


def replace_string_in_tex_file(new_folder: str, file_name: str, old_word: str, new_word: str) -> None:
    """Replace a given string inside a tex file

    Args:
        new_folder (str): location of tex file
        file_name (str): name of tex file
        old_word (str): string to be replaced
        new_word (str): string to replace with
    """
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


def list_existing_things(dir_path: str, print_list: bool = True, header_message: str = None, cnt_start=0) -> list[str]:
    """list all things all things in a given directory

    Args:
        dir_path (str): directory where things are located (as folders)
        print_list (bool, optional): Whether to print out the list of things in addition to returning it. Defaults to True.
        header_message (str, optional): _description_. If print_list is True, add as header to printed list. Defaults to None.
        cnt_start (int, optional): _description_. Starting point for list counter when print_list=True. Defaults to 0.

    Returns:
        list[str]: list of things (articles or portfolio versions).
    """
    # list of thing names already used
    names = []
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        # check if path is directory:
        if os.path.isdir(file_path):
            names.append(file_name)

    if print_list:
        if header_message != None:
            print(sty.bold + header_message + sty.reset)
        for i, name in enumerate(names, 1):
            print(f"{i + cnt_start} - {sty.bright_blue}{name}{sty.reset}")
        print("")
    return names


def request_name(thing_type: ThingType, existing_names: list[str]) -> str:
    """Ask user to name new document

    Args:
        thing_type (ThingType): type of document to create
        existing_names (list[str]): existing names no longer available

    Returns:
        str: name for new document chosen by user
    """
    new_name = input(f"Write filename for new {thing_type}: ").lower().replace(" ", "_")
    # check if thing already exists and keep requesting name until original name is given or user quits:
    while new_name in existing_names:
        if new_name != "q" and new_name != "quit":
            print(f"{sty.red}{thing_type} already exists.{sty.reset} Please pick a new name or quit.\n")
            new_name = request_name(thing_type, existing_names)
        else:
            print(f"\n💀💀💀 {sty.red}Program quit without creation of new {thing_type}.{sty.reset}")
            exit()
    return new_name


def create_new_folder_with_files(new_name: str, template_name: str, dir_path: str) -> str:
    """Copy a template folder structure to be used as starting point.

    Args:
        new_name (str): name to be used for new folder
        template_name (str): name of template to be copied
        dir_path (str): path to template/new folder.

    Returns:
        str: _description_
    """
    if new_name != "q" and new_name != "quit":
        new_folder = dir_path + "/" + new_name
        try:
            shutil.copytree(f"{dir_path}/{template_name}/.", new_folder)
        except:
            exit_code = 1
        else:
            exit_code = 0
        check_if_successful(create_new_folder_with_files.__name__, exit_code)
        print_progress_msg(f"Created new folder with contents from {sty.bold+sty.green}{template_name}{sty.reset} ")
    else:
        print(f"\n💀💀💀 {sty.red}Program quit without creation of new folder.{sty.reset}")
        exit()
    return new_folder
