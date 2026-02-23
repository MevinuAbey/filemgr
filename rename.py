#✅ Must Include:
#Bulk rename
#Prefix
#Suffix
#Replace text
#Auto numbering
#Preview mode
#⭐ Add:
#File type filter
#Conflict handling
#Undo feature


import questionary
from pathlib import Path
import re
import json


def main(path):
    folder_path = Path(path)

def menu():
    rename_option = questionary.select(
        "Choose a renaming option:",
        choices=["Prefix", "Suffix", "Replace Text", "Auto Numbering"]).ask()
    return rename_option
