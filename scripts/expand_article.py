import os
import subprocess
import helpers as h


articles_directory = "./../articles/"  # relative to script location
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
        # Get list of existing articles
        thing_path = os.path.join(base_dir, articles_directory, thing_name)

        subprocess.run(
            # latexpand --verbose --output document_expanded.tex document.tex
            [
                "latexpand",
                # "--verbose",  # for details to be printed to terminal
                # "--keep-comments", # don't strip comments (lines starting with %, and anything below\end{document}
                # "--empty-comments", # keep empty comments (i.e. % at end of lines) for clarity
                ###   "--keep-includes", # don't expand \input and \include directives
                ### "--expand-usepackage", # Expand \usepackage{...} directives
                ### "--expand-bbl FILE", # Expand the bibliography by inlining FILE (should be a *.bbl file) - not what the project uses
                ### "--explain", # generate explanatory comments in output
                ### "--show-graphics", # show included graphics
                ### "--fatal", # Die in case a file can't be found.
                "--makeatletter", # Insert a \makeatletter in the preamble. In some rare cases it may break your document, but it may help fixing bad interactions between @-commands and inclusion.
                #==============================================================
                # +++++ OUTPUT FILE:
                "--biber", # Include \bibliography{} with FILE's content, as needed by biblatex with the biber backend.(similar to --expand-bbl FILE, but for biber+biblatex).
                "./../../articles_common_files/biblatex_files/bibliography_template.bib",
                # +++++ OUTPUT FILE:
                "--output",
                "document_expanded.tex",
                # +++++ INPUT FILE:
                "document.tex",
            ],
            cwd=thing_path,  # 👈 set your desired directory here
            check=True,
        )
        print(
            f"\n\n 😁😁😁  successfully expanded article {h.bold+h.green}{thing_name}{h.reset} 😁😁😁"
        )


if __name__ == "__main__":
    main()
