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

def do_rename(rename_option, folder_path):
    if rename_option == "Prefix":
        prefix = questionary.text("Enter the prefix to add:").ask()
        
    elif rename_option == "Suffix":
        suffix = questionary.text("Enter the suffix to add:").ask()
        
    elif rename_option == "Replace Text":
        old_text = questionary.text("Enter the text to replace:").ask()
        new_text = questionary.text("Enter the new text:").ask()
        
    elif rename_option == "Auto Numbering":
        
        pass
