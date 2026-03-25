# File Manager (FileMgr) By Mevinu Abeysinghe
# For CS50 Python Final Project
import argparse
import os
from pathlib import Path
import questionary  # type: ignore
import menu

def main():
    source_path, action = parse_arguments()
    if not check_path(source_path):
        source_path = ask_for_path()
    selected_action = check_action(action)
    do_action(selected_action,source_path)

def parse_arguments():
    # setup command-line arguments
    parser = argparse.ArgumentParser(description="FileMgr")
    parser.add_argument("-p", "--path", help="folder path",
                    default=os.getcwd())  # needs to input paths as "path"
    parser.add_argument("-a", "--action", choices=["backup", "organize", "rename"], nargs="?")

    args = parser.parse_args()
    path = args.path
    source_path = Path(path)
    action = args.action
    return source_path, action

def ask_for_path():
    while True:
        path = questionary.text("Enter the folder path:").ask()
        source_path = Path(path)
        if check_path(source_path):
            return source_path
        else:
            print("Invalid path. Please enter a valid folder path.")

def check_path(source_path):
    if source_path.exists() and source_path.is_dir():  # cheking if path is available
        return True
    else:
        return False


def check_action(action):
    if not action:
        print("FileMgr")
        choice = questionary.select("Select Action:", choices=[
                                    "backup", "rename", "organize"]).ask()
        return choice
    else:
        return action

def do_action(action,source_path):
    menu.main(action,source_path)
    return True


if __name__ == "__main__":
    main()
