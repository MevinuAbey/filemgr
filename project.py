# File Manager (FileMgr) By Mevinu Abeysinghe
# For CS50 Python Final Project
import argparse
import os
import sys
from pathlib import Path
import questionary  # type: ignore
import menu
import backup
import organize
import rename

def main():
    try:
        source_path, action = parse_arguments()
        if not check_path(source_path):
            source_path = ask_for_path()
        selected_action = check_action(action)
        do_action(selected_action,source_path)
    except Exception as e:
        print(f"error {e}")
        sys.exit(1)

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

        if path is None:
            print("Exiting FileMgr")
            sys.exit(0)

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

def ask_for_action():
    action = questionary.select("Select Action:", choices=[
                                "backup", "rename", "organize"]).ask()
    if action is None:
        print("Exiting FileMgr")
        sys.exit(0)
    return action

def check_action(action):
    if not action:
        print("FileMgr")
        choice = ask_for_action()
        return choice
    else:
        return action

def do_action(action, source_path):
    if action == "backup":
        usr_options = menu.backup(source_path)
        backup.main(usr_options)

    elif action == "organize":
        usr_options = menu.organize(source_path)
        organize.main(usr_options)

    elif action == "rename":
        usr_options = menu.rename()
        rename.main(usr_options)

if __name__ == "__main__":
    main()
