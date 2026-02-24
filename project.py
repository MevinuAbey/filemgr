# File Manager (FileMgr) By Mevinu Abeysinghe
# For CS50 Python Final Project
import argparse
import sys
import os
from pathlib import Path
import questionary # type: ignore
import backup
import organize
import rename

# setup command-line arguments
parser = argparse.ArgumentParser(description="FileMgr")
parser.add_argument("--path", "--p", help="folder path", default=os.getcwd()) #needs to input paths as "path"
parser.add_argument("--a", "--action", choices=["backup", "organize", "rename"], nargs="?")

args = parser.parse_args()
path = args.path
folder_path = Path(path)
action = args.a
#

def main():
    if check_path():
        selected_action = check_action(action)
        action_select(selected_action)

def check_path():
    if Path.exists(folder_path)or Path.is_dir(folder_path):  # cheking if path is avalable
        return True
    else:
        print("Path You Entered Is not exsisting :)")
        sys.exit(1)


def check_action(action):
    if not action:
        print("FileMgr")
        choice = questionary.select("Select Action:", choices=["backup", "rename", "organize"]).ask()
        return choice
    else:
        return action


def action_select(action):
    if action == "backup":
        backup.main(folder_path)
    elif action == "organize":
        organize.main(folder_path)
    elif action == "rename":
        rename.main(folder_path)


if __name__ == "__main__":
    main()
