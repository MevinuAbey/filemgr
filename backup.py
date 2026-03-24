import sys
import json
import shutil
from pathlib import Path
import questionary # type: ignore
import datetime
import zipfile
import os

def main(source_path,backup_dest, is_compress, backup_mode, exc_or_inc, file_types):
    check_quick_backup(source_path)
    #confirmation if backup
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

def quick_backup(source_path):
    with open(f"{source_path}/backup_config.json", "r") as f:
        config = json.load(f)
    backup(source_path, config["destination"], config["is_compress"], config["backup_mode"], config["exc_or_inc"], config["file_types"])



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

    def include(file_name):
        if exc_or_inc == "Include All":
            return True
        
        file_name = file_name.lower()

        if exc_or_inc == "Include":
            return file_name.endswith(file_types)
        
        if exc_or_inc == "Exclude":
            return not file_name.endswith(file_types)
        return True

    def zip_backup_it(source_path, backup_name, exc_or_inc, file_types=None):
        with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    if include(file):
                        rel_path = os.path.relpath(full_path, source_path)
                        zipf.write(full_path, rel_path)

    def normal_backup_it(source_path, backup_name, exc_or_inc, file_types=None):
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