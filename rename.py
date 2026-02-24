# rename module for filemgr
import questionary # type: ignore
from pathlib import Path
import re
import json

def main(path):
    folder_path = Path(path)
    rename_option = menu()
    do_rename(rename_option, folder_path)

def menu():
    rename_option = questionary.select(
        "Choose a renaming option:", choices=["Prefix", "Suffix", "Replace Text", "Auto Numbering"]).ask()
    return rename_option

def load_list_files(folder_path):
    files = folder_path.iterdir()
    return files

def do_rename(rename_option, folder_path):
    if rename_option == "Prefix":
        prefix = questionary.text("Enter the prefix to add:").ask()
        preview_rename(folder_path, rename_option, prefix)
        confirm = questionary.confirm("Do you want to apply this renaming?").ask()
        if confirm:
            rename_prefix(folder_path, prefix)
        
    elif rename_option == "Suffix":
        suffix = questionary.text("Enter the suffix to add:").ask()
        preview_rename(folder_path, rename_option, suffix)
        confirm = questionary.confirm("Do you want to apply this renaming?").ask()
        if confirm:
            rename_suffix(folder_path, suffix)
        
    elif rename_option == "Replace Text":
        old_text = questionary.text("Enter the text to replace:").ask()
        new_text = questionary.text("Enter the new text:").ask()
        preview_rename(folder_path, rename_option, old_text, new_text)
        confirm = questionary.confirm("Do you want to apply this renaming?").ask()
        if confirm:
            rename_replace_text(folder_path, old_text, new_text)
        
    elif rename_option == "Auto Numbering":
        base_name = questionary.text("Enter the base name for numbering:").ask()
        start_number = questionary.text("Enter the starting number(leave blank for 1):").ask()
        rename_auto_numbering(folder_path, base_name, start_number)

def get_file_type():
    file_type = questionary.text("Enter file type filter (e.g., .txt) or leave blank for all files:").ask()
    file_type = file_type.strip() if file_type else None
    return file_type

def preview_rename(folder_path, rename_option, *args):    
    files = load_list_files(folder_path)
    print(f"Preview of renaming {rename_option}")
    if rename_option == "Prefix":
        prefix = args[0]
        for file in files:
            if file.is_file():
                new_name = prefix + file.name
                print(f"{file.name} -> {new_name}")
                break
    elif rename_option == "Suffix":
        suffix = args[0]
        for file in files:
            if file.is_file():
                new_name = file.stem + suffix + file.suffix
                print(f"{file.name} -> {new_name}")
                break
    elif rename_option == "Replace Text":
        old_text, new_text = args
        for file in files:
            if file.is_file():
                new_name = file.name.replace(old_text, new_text)
                print(f"{file.name} -> {new_name}")
                break

def rename_prefix(folder_path, prefix):
    file_type = get_file_type()
    for file in folder_path.iterdir():
        if file.is_file() and (not file_type or file.suffix == file_type):
            new_name = prefix + file.name
            file.rename(folder_path / new_name)
    print("Renaming completed.")

def rename_suffix(folder_path, suffix):
    file_type = get_file_type()
    for file in folder_path.iterdir():
        if file.is_file() and (not file_type or file.suffix == file_type):
            new_name = file.stem + suffix + file.suffix
            file.rename(folder_path / new_name)
    print("Renaming completed.")

def rename_replace_text(folder_path, old_text, new_text):
    file_type = get_file_type()
    for file in folder_path.iterdir():
        if file.is_file() and (not file_type or file.suffix == file_type):
            new_name = file.name.replace(old_text, new_text)
            file.rename(folder_path / new_name)
    print("Renaming completed.")

def rename_auto_numbering(folder_path, base_name, start_number):
    file_type = get_file_type()
    start_number = int(start_number) if start_number else 1
    for idx, file in enumerate(folder_path.iterdir(), start=start_number):
        if file.is_file() and (not file_type or file.suffix == file_type):
            new_name = f"{base_name}_{idx}{file.suffix}"
            file.rename(folder_path / new_name)