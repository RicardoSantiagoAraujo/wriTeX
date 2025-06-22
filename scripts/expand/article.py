import os
import subprocess
from scripts.utils.helpers import *
import scripts.utils.style_console_text as sty

articles_directory = "./../../articles/"  # relative to script location
expanded_file_name = "document_expanded.tex"
expanded_file_folder = ""  # /!\ leave empty until all the file imports are managed as I have done for appendix and body
bib_dir = "./../../articles_common_files/biblatex_files/"  # relative to script location"
temp_bib_file = "temp.bib"
language = "en"

# get the directory of the current script
base_dir = os.path.dirname(os.path.realpath(__file__))  # dir of current file


def main():
    """Script to generated an expanded version of an article, i.e. a .tex file where all input files are included directly instead of taken from dependencies so as to reduce everything to as few separate files as possible."""
    ### MAIN PROGRAM ###
    # Print initial prompt
    print(f"\n Which article would you like to expand ? (Write full name or pick by number)")
    article_names = list_existing_things(
        os.path.join(base_dir, articles_directory),
        header_message="\nArticles that can be expanded:",
    )
    article_indexes = list(range(1, len(article_names) + 1))
    choice = input(f"{sty.blue}Pick one:{sty.reset}")
    if choice in ["q", "quit"]:
        print(f"\n💀💀💀 {sty.red}Program quit without expanding an article.{sty.reset}")
        exit()
    elif (choice not in article_names) & (int(choice) not in article_indexes):
        print(f"{sty.red}INVALID CHOICE: must pick from existing list{sty.reset}")
        # Restart proccess
        main()
    else:
        # if used picked a number:
        if choice.isdigit() and int(choice) in article_indexes:
            thing_name = article_names[int(choice) - 1]
        # if used wrote the article name:
        else:
            thing_name = choice
        print(f"\n{sty.blue} Your pick: {sty.green}{thing_name}{sty.reset}\n")
        thing_dir = os.path.join(base_dir, articles_directory, thing_name)
        extended_thing_path = os.path.join(thing_dir, expanded_file_folder, expanded_file_name)

        # Create folder for expanded output
        os.makedirs(os.path.join(thing_dir, expanded_file_folder), exist_ok=True)

        # create single temporary bib file
        tmp_bib_path = fuse_files(os.path.join(base_dir, bib_dir), os.path.join(thing_dir, temp_bib_file))

        subprocess.run(
            # latexpand --verbose --output document_expanded.tex document.tex
            [
                "latexpand",
                # "--verbose",  # for details to be printed to terminal
                # "--keep-comments", # don't strip comments (lines starting with %, and anything below\end{document}
                "--empty-comments",  # keep empty comments (i.e. % at end of lines) for clarity
                ###   "--keep-includes", # don't expand \input and \include directives
                ### "--expand-usepackage", # Expand \usepackage{...} directives
                ### "--expand-bbl FILE", # Expand the bibliography by inlining FILE (should be a *.bbl file) - not what the project uses
                ### "--explain", # generate explanatory comments in output
                ### "--show-graphics", # show included graphics
                ### "--fatal", # Die in case a file can't be found.
                # "--makeatletter", # Insert a \makeatletter in the preamble. In some rare cases it may break your document, but it may help fixing bad interactions between @-commands and inclusion.
                # ==============================================================
                # +++++ OUTPUT FILE:
                "--biber",  # Include \bibliography{} with FILE's content, as needed by biblatex with the biber backend.(similar to --expand-bbl FILE, but for biber+biblatex).
                temp_bib_file,
                # +++++ OUTPUT FILE:
                "--output",
                os.path.join(expanded_file_folder, expanded_file_name),
                # +++++ INPUT FILE:
                "document.tex",
            ],
            cwd=thing_dir,  # 👈 set your desired directory here
            check=True,
        )

        os.remove(tmp_bib_path)

        add_article_body_contents(language, thing_dir, extended_thing_path)

        handle_biblatex_bug(extended_thing_path)

        add_appendix_contents(thing_dir, extended_thing_path)

        print(f"\n\n 😁😁😁 Successfully expanded article {sty.bold+sty.green}{thing_name}{sty.reset} 😁😁😁")


# =============================================================================
# =============================================================================
# =============================================================================
# ===========================HELPER FUNCTIONS=================================


def fuse_files(directory: str, output_file: str) -> str:
    """Fuse multiple files into a single one.

    Args:
        directory (str): base directory where files to be fused are located
        output_file (str): fused output file path

    Returns:
        str: _description_
    """
    with open(output_file, "w", encoding="utf-8") as outfile:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                with open(filepath, "r", encoding="utf-8", errors="ignore") as infile:
                    # outfile.write(f"\n--- Start of {filename} ---\n")
                    outfile.write(infile.read())
                    # outfile.write(f"\n--- End of {filename} ---\n\n")
    return output_file


def replace_content_in_file(file_path: str, old_string: str, new_string: str) -> None:
    """Replace every occurence of a specific string in a target file.

    Args:
        file_path (str): path to target file
        old_string (str): old string that is to be replaced
        new_string (str): new string to use for replacement
    """
    # Read the file
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Replace the string
    content = content.replace(old_string, new_string)

    # Write the modified content back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def handle_biblatex_bug(extended_thing_path: str) -> None:
    """Deal with bug caused by biblatex by removing code that causes it.

    Args:
        file_path (str): path to buggy extended document.
    """

    print(
        f"\n⚠️{sty.dim} To get the bibliography to work, one must add a new line {sty.blue}\\addbibresource{{temp_bib_file}}{sty.reset+sty.dim} to the generated file {sty.blue}{expanded_file_name}{sty.reset+sty.dim} as well as remove the included @articles out of the surrounding macro. This can either be done manually or, as in this function, programatically but it is a finicky solution so beware. Will probably be affected by changes to {sty.blue}latexpand flags{sty.reset}"
    )

    replace_content_in_file(
        extended_thing_path,
        """\\newcommand{\\loadBibIfExists}[1]%
{\\IfFileExists{#1}%
    {%""",
        "",
    )

    replace_content_in_file(
        extended_thing_path,
        f"""\\usepackage{{xpatch}}

%Patch the biblatex input command.
%replace "testinput-bbl" if you change the name above.
%disable if you want to run biblatex/biber normally
\\makeatletter
\\patchcmd\\blx@bblinput{{\\blx@blxinit}}
                      {{\\blx@blxinit
                       \\def\\jobname{{{temp_bib_file}}}%new jobname
                      }}{{}}{{\\fail}}
\\makeatother
			     %
}}%
    {{}}%
}}""",
        f"\\addbibresource{{{temp_bib_file}}}",
    )


def add_article_body_contents(lang: str, thing_dir: str, extended_thing_path: str) -> None:
    """Add contents of article body into extended file.

    Args:
        lang (str): language version of the body.
        thing_dir (str): directory of the target document.
        extended_thing_path (str): path to extended document that is missing body contents.
    """

    print(
        f"\n⚠️{sty.dim} To get the body contents into the file they are injected into the expanded_file. Otherwise latexpand only really deals with standard simple \\inputs, such as for setting files. Changed to macro may disturb functionality.{sty.reset}"
    )

    body_folder = os.path.join(thing_dir, "elements/body/")
    body_file = f"body_{lang}.tex"
    # Open and read the entire content of the file
    with open(os.path.join(body_folder, body_file), "r") as file:
        contents = file.read()

    # Place the body in the chosen location
    target_location = "\\begin{document}"
    replace_content_in_file(
        extended_thing_path,
        target_location,
        # NEW CONTENTS
        f"""\\begin{{filecontents*}}{{{body_file}}}
                    {contents}
\\end{{filecontents*}} \n\n"""
        + target_location,
    )

    replace_content_in_file(
        extended_thing_path,
        "\\def\\fileAddress{elements/#1/#1\\_#2.tex}",
        "\\def\\fileAddress{./#1\\_#2.tex}",
    )


def add_appendix_contents(thing_dir: str, extended_thing_path: str) -> None:
    """Add contents of appendix items into extended file.

    Args:
        thing_dir (str): directory of the target document.
        extended_thing_path (str): path to extended document that is missing body contents.
    """

    print(
        f"\n⚠️{sty.dim} To get the appendix files to work, one must add a new line, they are injected into the expanded_file above the appendix macro. Changed to macro may disturb functionality.{sty.reset}"
    )

    appendix_folder = os.path.join(thing_dir, "elements/appendix/")
    # List of folder names
    appendix_list = [name for name in os.listdir(appendix_folder) if os.path.isdir(os.path.join(appendix_folder, name))]

    for appendix in appendix_list:
        # Open and read the entire content of the file
        with open(os.path.join(appendix_folder, appendix, "content.tex"), "r") as file:
            contents = file.read()

        # Place the appendix items in the chosen location
        target_location = "\\NewDocumentCommand{\\wrtxAppendix}"
        replace_content_in_file(
            extended_thing_path,
            target_location,
            # NEW CONTENTS
            f"""\\begin{{filecontents*}}{{{appendix+".tex"}}}
                       {contents}
\\end{{filecontents*}} \n\n"""
            + target_location,
        )

    replace_content_in_file(
        extended_thing_path,
        "\\expandafter\\input\\expandafter{./elements/appendix/#1/content.tex}",
        "\\expandafter\\input\\expandafter{./#1.tex}",
    )


# =============================================================================

if __name__ == "__main__":
    main()
