# File Manager (FileMgr) By Mevinu Abeysinghe
# For CS50 Python Final Project
import argparse
import sys
from pathlib import Path
import questionary
import menu
import backup
import organize
import rename

# main function to run the program
def main():
    try:
        source_path, action = parse_arguments()

        if not check_path(source_path): # if path is not provided or invalid, ask for path
            source_path = ask_for_path()

        selected_action = check_action(action)
        do_action(selected_action,source_path)

    except Exception as e:
        print(f"error {e}")
        sys.exit(1)

# function to parse command-line arguments
def parse_arguments():
    # setup command-line arguments
    parser = argparse.ArgumentParser(description="FileMgr")
    parser.add_argument("-p", "--path", help="folder path")  # needs to input paths as "path"
    parser.add_argument("-a", "--action", choices=["backup", "organize", "rename"], nargs="?")

    args = parser.parse_args()
    path = args.path
    source_path = Path(path) if path else None
    action = args.action
    return source_path, action # returns the path & action

# function to check if path is valid and exists
def check_path(source_path):
    if source_path is None:
        return False
    if source_path.exists() and source_path.is_dir():  # cheking if path is available and its directory
        return True
    else:
        return False

# function to ask user for path if not provided in arguments
def ask_for_path():
    while True:
        path = questionary.text("Enter the source folder path:").ask()
        #if path input is with quotes, remove the quotes
        path = path.strip('"').strip("'")

        if path is None: # if user cancels the input (control+c) exit from program
            print("Exiting FileMgr")
            sys.exit(0)

        source_path = Path(path)
        if check_path(source_path):
            return source_path
        else:
            print("Invalid path. Please enter a valid folder path.")

# function to check if action is provided, if not ask for action
def check_action(action):
    if not action:
        print("FileMgr")
        choice = ask_for_action()
        return choice
    else:
        return action

# function to ask user for action if not provided in arguments
def ask_for_action():
    action = questionary.select("Select Action:", choices=[
                                "backup", "rename", "organize"]).ask()
    if action is None:
        print("Exiting FileMgr")
        sys.exit(0)
    return action

# function to do the selected action
def do_action(action, source_path):
    if action == "backup":
         # checks if quick backup is avalavle and user wants to do it
        if backup.is_quick_backup(source_path) and menu.ask_quick_backup():
                backup.do_quick_backup(source_path)

        # if quick backup is not available/user do not want to do it, show backup menu
        else:
            usr_config = menu.backup_menu(source_path)
            if usr_config is None:
                return
            backup.do_backup(usr_config)

        print("\nBackup completed.")

    elif action == "organize":
        usr_config = menu.organize_menu(source_path)
        if usr_config is None:
            return
        organize.do_organize(usr_config)
        print("\nOrganizing completed.")

    elif action == "rename":
        usr_config = menu.rename_menu(source_path)
        if usr_config is None:
            return
        rename.do_rename(usr_config)
        print("\nRenaming completed.")

if __name__ == "__main__":
    main()
