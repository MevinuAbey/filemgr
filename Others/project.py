# pakages expected to use
# pathlib
# shutil
# datetime
# argparse
# logging
# re
# hashlib (optional advanced)

# command line arguments setup
# project
#   -path ........... -(b,o,r) OR just -(b,o,r)
#

import argparse
import os
import pathlib
import sys
from pathlib import Path
import questionary
import backup
import organize
import rename

# setup command-line arguments
parser = argparse.ArgumentParser(description="FileMgr")
parser.add_argument("--path", "--p", help="folder path", default=os.getcwd())
parser.add_argument("--a", "--action", choices=["backup", "organize", "rename"], nargs="?")

args = parser.parse_args()
path = args.path
action = args.a
#


def main():
    if check_path():
        selected_action = check_action(action)
        action_select(selected_action)


def check_path():
    if Path.exists(path)or Path.is_dir(path):  # cheking if path is avalable
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
        backup.main(path)
    elif action == "organize":
        organize.main(path)
    elif action == "rename":
        rename.main(path)


if __name__ == "__main__":
    main()
