import json
import shutil
from pathlib import Path
import datetime
import zipfile
import os

# quick backup

def is_quick_backup(source_path):
    try:
        with open(f"{source_path}/backup_config.json", "r") as f:
            config = json.load(f)

            source = Path(config["source_path"])
            if not source == source_path:
                return False
            dest_path = Path(config["backup_dest"])
            if not dest_path.exists():
                return False
            if not isinstance(config["is_compress"], bool):
                return False
            if not isinstance(config["file_types"], list):
                return False
            if not isinstance(config["backup_mode"], str) or config["backup_mode"] not in ["timestamp", "overwrite"]:
                return False
            if not isinstance(config["exc_or_inc"], str) or config["exc_or_inc"] not in ["Exclude", "Include", "Include All"]:
                return False
            return True
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        print("Invalid JSON in backup_config.json.")
        return False
    except KeyError as e:
        print(f"Missing key {e} in backup_config.json.")
        return False

def do_quick_backup(source_path):
    with open(f"{source_path}/backup_config.json", "r") as f:
        config = json.load(f)
    do_backup(config)

# backup

def do_backup(usr_config):
    source_path = Path(usr_config["source_path"])
    backup_dest = Path(usr_config["backup_dest"])
    is_compress = usr_config["is_compress"]
    backup_mode = usr_config["backup_mode"]
    exc_or_inc = usr_config["exc_or_inc"]
    file_types = usr_config["file_types"]

    print("Starting backup...")

    timestamp = f"_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}" if backup_mode == "timestamp" else ""
    backup_base_name = f"{source_path.resolve().name}_backup{timestamp}"
    backup_name = backup_dest / backup_base_name

    if is_compress:
        create_zip_backup(source_path, str(backup_name) + ".zip", exc_or_inc, file_types)
    else:
        create_normal_backup(source_path, str(backup_name), exc_or_inc, file_types)
        
    save_backup_config(usr_config)

def exc_or_include(file_name, exc_or_inc, file_types):
    if exc_or_inc == "Include All" or not file_types:
        return True
        
    file_name = file_name.lower()
    file_types_tuple = tuple(file_types)

    if exc_or_inc == "Include":
        return file_name.endswith(file_types_tuple)
        
    if exc_or_inc == "Exclude":
        return not file_name.endswith(file_types_tuple)
        
    return True

def create_zip_backup(source_path, backup_zip_path, exc_or_inc, file_types):
    with zipfile.ZipFile(backup_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                if file == "backup_config.json":
                    continue
                    
                if exc_or_include(file, exc_or_inc, file_types):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, source_path)
                    zipf.write(full_path, rel_path)

def create_normal_backup(source_path, backup_dir_path, exc_or_inc, file_types):
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file == "backup_config.json":
                continue
                
            if exc_or_include(file, exc_or_inc, file_types):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, source_path)
                dest_path = os.path.join(backup_dir_path, rel_path)
                
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(full_path, dest_path)

def save_backup_config(usr_config):
    source_path = usr_config["source_path"]
    config_to_save = {
        "source_path": str(usr_config["source_path"]),
        "backup_dest": str(usr_config["backup_dest"]),
        "exc_or_inc": usr_config["exc_or_inc"],
        "file_types": usr_config["file_types"],
        "is_compress": usr_config["is_compress"],
        "backup_mode": usr_config["backup_mode"]
    }
    with open(f"{source_path}/backup_config.json", "w") as f:
        json.dump(config_to_save, f, indent=4)
    print("Backup Settings Saved. Next time you can use quick backup to backup with these settings.")
