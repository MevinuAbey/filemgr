import sys
import json
import shutil
from pathlib import Path
import questionary # type: ignore
import datetime
import zipfile
import os

def main(path):
    source_path = path
    print(f"path to folder backup {source_path}")
    check_quick_backup(source_path)
    backup_dest, is_compress, backup_mode, exc_or_inc, file_types = menu(source_path)
    #confirmation if backup
    confirm_backup = questionary.confirm("Do you want to backup with above settings?").ask()
    if not confirm_backup:
        print("backup cancelled.")
        sys.exit(0)
    backup(source_path, backup_dest, is_compress, backup_mode, exc_or_inc, file_types) #run backup with settings from menu
    #saving confing
    save_backup_config(source=source_path, destination=backup_dest,exc_or_inc=exc_or_inc, file_types=file_types, is_compress=is_compress, backup_mode=backup_mode)
    print("Backup Settings Saved. Next time you can use quick backup to backup with these settings.")

def check_quick_backup(source_path):
#ckeck if check_backup_config is true and then run backup by its setings
    if check_backup_config(source_path):
        print("Quick Backup Available")
        quick_backup = questionary.confirm("Do you want to perform a quick backup using the last settings?").ask()
        if not quick_backup:
            return
        #run backup with settings from backup_config.json
    else:
        return

def check_backup_config(source_path):
    #check if backup_config.json exists and is valid
    #checks
        #destination must be path that exists
        #is_timaestamp and is_compress must be boolean
        #file_types_exclude and file_types_include must be list or "None"

    try:
        with open(f"{source_path}/backup_config.json", "r") as f:
            config = json.load(f)
            dest_path = Path(config["destination"])
            if not dest_path.exists():
                return False
            if not isinstance(config["is_compress"], bool):
                return False
            if not (isinstance(config["file_types"], list)):
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

def menu(source_path):
    while True:
        backup_dest = questionary.text("Enter backup destination folder path: (leave blank to use default)").ask()
        if not backup_dest:
            backup_dest = Path(f"C:/backup_files_filemgr/{source_path.name}_backup")
        dest_path = Path(backup_dest)
        if dest_path.exists() and dest_path.is_dir():
            break
        else:
            backup_dest.mkdir(parents=True, exist_ok=True)
            break

    is_compress = questionary.confirm("Do you want to compress the backup?").ask() #yes or no
    backup_mode = questionary.select(
        "Do you want to create a timestamped backup or overwriting backup?", choices=["timestamp", "overwrite"]).ask()

    exc_or_inc = questionary.select(
        "Do you want to exclude or include specific file types?", choices=["Include All", "Exclude", "Include"]).ask()
    file_types = []

    if exc_or_inc == "Exclude" or exc_or_inc == "Include":
        file_types = questionary.text(
            f"Enter file types to {exc_or_inc} (comma separated, e.g., .tmp, .log):").ask()
        file_types = [ft.strip() for ft in file_types.split(",")] if file_types else []


  
    if not file_types:
        exc_or_inc = "Include All"

    return (backup_dest, is_compress, backup_mode,
             exc_or_inc, file_types)

def save_backup_config(source, destination, exc_or_inc, file_types, is_compress, backup_mode):
    config = {
        "source": str(source),
        "destination": str(destination),
        "exc_or_inc": exc_or_inc,
        "file_types": file_types,
        "is_compress": is_compress,
        "backup_mode": backup_mode,
    }
    with open(f"{source}/backup_config.json", "w") as f:
        json.dump(config, f, indent=4)

def Load_backup_config(): #to quick backup
    ...

def backup(source_path, backup_dest, is_compress, backup_mode, exc_or_inc, file_types):
    print("Starting backup...")

    #backup mode -> filename, time or overwrite fucn 
    if backup_mode == "timestamp":
        timestamp = datetime.datetime.now().strftime("%Y%M%d_%H%M%S")
        backup_name = (f"{source_path.name}_backup_{timestamp}")
        if is_compress:
            backup_name = f"{backup_dest}/{backup_name}.zip"
            zip_backup_it(source_path,backup_name,exc_or_inc,file_types)
        else:
            backup_name = f"{backup_dest}/{backup_name}"
            normal_backup_it(source_path, backup_name, exc_or_inc, file_types)

    elif backup_mode == "overwrite":
        backup_name = (f"{source_path.name}_backup")
        if is_compress:
            backup_name = f"{backup_dest}/{backup_name}.zip"
            zip_backup_it(source_path,backup_name,exc_or_inc,file_types)
        else:
            backup_name = f"{backup_dest}/{backup_name}"
            normal_backup_it(source_path, backup_name, exc_or_inc, file_types)

def zip_backup_it(source_path, backup_name, exc_or_inc, file_types=None):

    def include(file_name):
        if exc_or_inc == "Include All":
            return True
        
        file_name = file_name.lower()

        if exc_or_inc == "Include":
            return file_name.endswith(file_types)
        
        if exc_or_inc == "Exclude":
            return not file_name.endswith(file_types)
        return True

    with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                full_path = os.path.join(root, file)
                if include(file):
                    rel_path = os.path.relpath(full_path, source_path)
                    zipf.write(full_path, rel_path)

def normal_backup_it(source_path, backup_name, exc_or_inc, file_types=None):
    def include(file_name):
        if exc_or_inc == "Include All":
            return True
        
        file_name = file_name.lower()

        if exc_or_inc == "Include":
            return file_name.endswith(file_types)
        
        if exc_or_inc == "Exclude":
            return not file_name.endswith(file_types)
        return True
    
    for root, dirs, files in os.walk(source_path):
        for file in files:
            
            full_path = os.path.join(root, file)

            if include(file):
                
                # Create relative path
                rel_path = os.path.relpath(full_path, source_path)
                
                # Destination path
                dest_path = os.path.join(backup_name, rel_path)
                
                # Ensure destination folder exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Copy file
                shutil.copy2(full_path, dest_path)