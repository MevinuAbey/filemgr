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
    check_quick_backup()
    backup_dest, is_compress, backup_mode, exc_or_inc, file_types_exclude, file_types_include = menu(path)
    save_backup_config(source=path, destination=backup_dest,exc_or_inc=exc_or_inc, file_types_exclude=file_types_exclude, file_types_include=file_types_include, is_compress=is_compress, backup_mode=backup_mode)


def check_quick_backup():
#ckeck if check_backup_config is true and then run backup by its setings
    if check_backup_config():
        print("Quick Backup Available")
        quick_backup = questionary.confirm("Do you want to perform a quick backup using the last settings?").ask()
        if not quick_backup:
            return
        #run backup with settings from backup_config.json
    else:
        return

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
            if not isinstance(config["is_compress"], bool):
                return False
            if not (isinstance(config["file_types_exclude"], list) or config["file_types_exclude"] == "None"):
                return False
            if not (isinstance(config["file_types_include"], list) or config["file_types_include"] == "None"):
                return False
            if not isinstance(config["backup_mode"],str) or not (config["backup_mode"] == "timestamp" or config["backup_mode"] == "overwrite"):
                return False
            if not isinstance(config["exc_or_inc"],str) or not (config["exc_or_inc"]== "Exclude" or config["exc_or_inc"]== "Include" or config["exc_or_inc"] == "Include All"):
                return False
            return True
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        print("Invalid JSON in backup_config.json.")
        return False

def menu(path):
    while True:
        backup_dest = questionary.text("Enter backup destination folder path: (leave blank to use default)").ask()
        if not backup_dest:
            backup_dest = path
        dest_path = Path(backup_dest)
        if dest_path.exists() and dest_path.is_dir():
            break
        else:
            print("Invalid destination path. Please try again.")

    is_compress = questionary.confirm("Do you want to compress the backup?").ask() #yes or no
    backup_mode = questionary.select(
        "Do you want to create a timestamped backup or overwriting backup?", choices=["timestamp", "overwrite"]).ask()

    exc_or_inc = questionary.select(
        "Do you want to exclude or include specific file types?", choices=["Exclude", "Include", "Include All"]).ask()
    if exc_or_inc == "Exclude":
        file_types_exclude = questionary.text(
            "Enter file types to exclude (comma separated, e.g., .tmp, .log):").ask()
        file_types_exclude = [ft.strip() for ft in file_types_exclude.split(",")] if file_types_exclude else []
    elif exc_or_inc == "Include":
        file_types_include = questionary.text(
            "Enter file types to include (comma separated, e.g., .txt, .doc):").ask()
        file_types_include = [ft.strip() for ft in file_types_include.split(",")] if file_types_include else []
  
    return (backup_dest, is_compress, backup_mode, exc_or_inc,
             file_types_exclude if exc_or_inc == "Exclude" else "None",
               file_types_include if exc_or_inc == "Include" else "None")

def save_backup_config(source, destination, exc_or_inc, file_types_exclude, file_types_include, is_compress, backup_mode):
    config = {
        "source": str(source),
        "destination": str(destination),
        "exc_or_inc": exc_or_inc,
        "file_types_exclude": file_types_exclude,
        "file_types_include": file_types_include,
        "is_compress": is_compress,
        "backup_mode": backup_mode,
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