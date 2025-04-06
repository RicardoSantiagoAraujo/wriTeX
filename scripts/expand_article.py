import os
import subprocess
import helpers as h


articles_directory = "./../articles/"  # relative to script location
expanded_file_name = "document_expanded.tex"
expanded_file_folder = "expanded/"
bib_dir = "./../articles_common_files/biblatex_files/"  # relative to script location"
temp_bib_file = "temp.bib"

# get the directory of the current script
base_dir = os.path.dirname(os.path.realpath(__file__))  # dir of current file


def main():
    ### MAIN PROGRAM ###
    # Print initial prompt
    print(f"Which article would you like to expand ? ")
    article_names = h.list_existing_things(os.path.join(base_dir, articles_directory))
    thing_name = input(f"{h.blue}Pick one:{h.reset}")
    if thing_name in ["q", "quit"]:
        print(f"\n💀💀💀 {h.red}Program quit without expanding an article.{h.reset}")
        exit()
    elif thing_name not in article_names:
        print(f"{h.red}INVALID CHOICE: must pick from existing list{h.reset}")
        main()
    else:

        thing_dir = os.path.join(base_dir, articles_directory, thing_name)
        extended_thing_path = os.path.join(thing_dir,expanded_file_folder, expanded_file_name)

        # Create folder for expanded output
        os.makedirs(os.path.join(thing_dir, expanded_file_folder), exist_ok=True)

        # create single temporary bib file
        tmp_bib_path = fuse_files(
            os.path.join(base_dir, bib_dir),
            os.path.join(thing_dir, temp_bib_file)
            )

        subprocess.run(
            # latexpand --verbose --output document_expanded.tex document.tex
            [
                "latexpand",
                # "--verbose",  # for details to be printed to terminal
                # "--keep-comments", # don't strip comments (lines starting with %, and anything below\end{document}
                "--empty-comments", # keep empty comments (i.e. % at end of lines) for clarity
                ###   "--keep-includes", # don't expand \input and \include directives
                ### "--expand-usepackage", # Expand \usepackage{...} directives
                ### "--expand-bbl FILE", # Expand the bibliography by inlining FILE (should be a *.bbl file) - not what the project uses
                ### "--explain", # generate explanatory comments in output
                ### "--show-graphics", # show included graphics
                ### "--fatal", # Die in case a file can't be found.
                # "--makeatletter", # Insert a \makeatletter in the preamble. In some rare cases it may break your document, but it may help fixing bad interactions between @-commands and inclusion.
                #==============================================================
                # +++++ OUTPUT FILE:
                "--biber", # Include \bibliography{} with FILE's content, as needed by biblatex with the biber backend.(similar to --expand-bbl FILE, but for biber+biblatex).
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


        handle_biblatex_bug(extended_thing_path)

        add_appendix_contents(thing_dir, extended_thing_path)

        print(
            f"\n\n 😁😁😁  successfully expanded article {h.bold+h.green}{thing_name}{h.reset} 😁😁😁"
        )


# =============================================================================
# =============================================================================
# =============================================================================
# ===========================HELPER FUNCTIONS=================================


def fuse_files(directory, output_file):
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
                    # outfile.write(f"\n--- Start of {filename} ---\n")
                    outfile.write(infile.read())
                    # outfile.write(f"\n--- End of {filename} ---\n\n")
    return output_file



def replace_content_in_file(file_path, old_string, new_string):
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace the string
    content = content.replace(old_string, new_string)

    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def handle_biblatex_bug(extended_thing_path):
    print(f'\n⚠️ To get the bibliography to work, one must add a new line {h.blue}\\addbibresource{{temp_bib_file}}{h.reset} to the generated file {h.blue}{expanded_file_name}{h.reset} as well as remove the included @articles out of the surrounding macro. This can either be done manually or, as in this function, programatically but it is a finicky solution so beware. Will probably be affecte by changed to {h.blue}latexpand flags{h.reset}')

    replace_content_in_file(extended_thing_path,
                                '''\\newcommand{\loadBibIfExists}[1]%
{\IfFileExists{#1}%
    {%'''
    , "")


    replace_content_in_file(extended_thing_path,
                                f'''\\usepackage{{xpatch}}

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
}}'''
    , f'\\addbibresource{{{temp_bib_file}}}')



def add_appendix_contents(thing_dir, extended_thing_path):
    print(f'\n⚠️ To get the appendix files to work, one must add a new line, they are injected into the expanded_file above the appendix macro. Changed to macro may disturb functionality.')


    appendix_folder = os.path.join(thing_dir, "elements/appendix/")
    # List of folder names
    appendix_list = [name for name in os.listdir(appendix_folder) if os.path.isdir(os.path.join(appendix_folder, name))]

    for appendix in appendix_list:
        # Open and read the entire content of the file
        with open(os.path.join(appendix_folder, appendix, "content.tex"), "r") as file:
            contents = file.read()

        # Place the appendix items in the chosen location
        target_location = "\\NewDocumentCommand{\\myAppendix}"
        replace_content_in_file(extended_thing_path,
                target_location
                ,
                # NEW CONTENTS
                f'''\\begin{{filecontents*}}{{{appendix+".tex"}}}
                       {contents}
\\end{{filecontents*}} \n\n''' + target_location
)

    replace_content_in_file(extended_thing_path,"\\expandafter\\input\\expandafter{./elements/appendix/#1/content.tex}", "\\expandafter\\input\\expandafter{./#1.tex}")

# =============================================================================

if __name__ == "__main__":
    main()
