import subprocess
import os

articles_directory = "./../../articles/"  # relative to script location

build_folder = "auxiliary_files"  # relative to script location

# get the directory of the current script
base_dir = os.path.dirname(os.path.realpath(__file__))  # dir of current file
dir_path = os.path.join(base_dir, articles_directory)

def main():

    choice = input("which article? ")
    compile_with_lualatex(choice)



def compile_with_lualatex(thing_name):
    try:
        # print( os.path.join(dir_path, thing_name + ".tex"))
        # CHANGE DIRECTORY TO THING'S
        os.chdir(os.path.join(dir_path, thing_name))
        # CREATE BUILD FOLDER IF IT DOES NOT EXIST
        if not os.path.exists(build_folder):
            os.makedirs(build_folder)
        result = subprocess.run(
            ["lualatex", "-interaction=nonstopmode", f"-output-directory={build_folder}", "document.tex"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Compilation failed:")
        print(e.stdout)
        print(e.stderr)


if __name__ == "__main__":
    main()
