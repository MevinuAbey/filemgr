#Select Source Folder
#Select Destination Folder
#Timestamped Backup Folder
#Copy All Files and Subfolders (Recursive)
#Summary Report

#File Type Exclusion

#settings saved in backup_config.json
#source folder and destination folder
#file type exclusion list
#is compression mode or normal copy
#is it timestamp backup or normal backup

import json
import shutil
from pathlib import Path
import questionary # type: ignore

def main(path):
    print(f"path to folder backup {path}")
    menu()

def check_quick_backup():
#ckeck if check_backup_config is true and then run backup by its setings
    if check_backup_config():
        print("Quick Backup Available")
        quick_backup = questionary.confirm("Do you want to perform a quick backup using the last settings?").ask()
        if not quick_backup:
            menu()
        #run backup with settings from backup_config.json
    else:
        menu()

def check_backup_config():
    #check if backup_config.json exists and is valid
    #checks
        #destination must be path that exists
        #is_timaestamp and is_compress must be boolean
        #file_types_exclude and file_types_include must be list or "None"

    try:
        with open("backup_config.json", "r") as f:
            config = json.load(f)
            dest_path = Path(config["destination"])
            if not dest_path.exists():
                return False
            if not isinstance(config["is_compress"], bool) or not isinstance(config["is_timestamp"], bool):
                return False
            if not (isinstance(config["file_types_exclude"], list) or config["file_types_exclude"] == "None"):
                return False
            if not (isinstance(config["file_types_include"], list) or config["file_types_include"] == "None"):
                return False
            return True
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        print("Invalid JSON in backup_config.json.")
        return False


def menu():
    backup_dest = questionary.text("Enter backup destination folder path: (leave blank to use default)").ask()
    if not backup_dest:
        backup_dest = str(Path.cwd() / "backup")
    is_compress = questionary.confirm("Do you want to compress the backup?").ask()
    is_timestamp = questionary.confirm("Do you want to create a timestamped backup?").ask()

    exc_or_inc = questionary.select(
        "Do you want to exclude or include specific file types?", choices=["Exclude", "Include", "None"]).ask()
    if exc_or_inc == "Exclude":
        file_types_exclude = questionary.text(
            "Enter file types to exclude (comma separated, e.g., .tmp, .log):").ask()
        file_types_exclude = [ft.strip() for ft in file_types_exclude.split(",")] if file_types_exclude else []

    elif exc_or_inc == "Include":
        file_types_include = questionary.text(
            "Enter file types to include (comma separated, e.g., .txt, .doc):").ask()
        file_types_include = [ft.strip() for ft in file_types_include.split(",")] if file_types_include else []
  
    save_backup_config(source=Path.cwd(), destination=backup_dest, file_types_exclude=file_types_exclude if exc_or_inc == "Exclude" else "None", file_types_include=file_types_include if exc_or_inc == "Include" else "None", is_compress=is_compress, is_timestamp=is_timestamp)
    #do_backup(backup_dest, is_compress, is_timestamp, file_types_exclude=file_types_exclude, file_types_include=file_types_include)
    ...

def save_backup_config(source, destination, file_types_exclude, file_types_include, is_compress, is_timestamp):
    config = {
        "source": str(source),
        "destination": destination,
        "file_types_exclude": file_types_exclude,
        "file_types_include": file_types_include,
        "is_compress": is_compress,
        "is_timestamp": is_timestamp
    }
    with open("backup_config.json", "w") as f:
        json.dump(config, f, indent=4)


def Summary_report():
    #generate summary report of backup process
    #total files copied, skipped, failed
    #log file with details of backup process
    ...

def backup_files():
    #copy files from source to destination
    #handle file type exclusion
    #handle preview mode
    #handle compression mode
    ...