# rename module for filemgr
import questionary # type: ignore
from pathlib import Path

def do_rename(usr_config):
    source_path = usr_config["source_path"]
    rename_option = usr_config["rename_option"]
    file_type = usr_config["file_type"]

    if file_type and not file_type.startswith("."):
        file_type = f".{file_type}"

    rename_func = OPTIONS.get(rename_option)
    
    for file in source_path.iterdir():
        if file.is_file() and (not file_type or file.suffix == file_type):
               
               new_name = rename_func(usr_config, file)
               new_filepath = source_path / new_name

               if not new_filepath.exists():
                  file.rename(new_filepath)
               else:
                  print(f"Skipped {file.name}: {new_name} already exists!")

def rename_prefix(usr_config, file):
    prefix = usr_config["prefix"]
    new_name = prefix + file.name
    return new_name

def rename_suffix(usr_config, file):
    suffix = usr_config["suffix"]
    new_name = file.stem + suffix + file.suffix
    return new_name

def rename_replace_text(usr_config, file):
    old_text = usr_config["old_text"]
    new_text = usr_config["new_text"]
    new_name = file.name.replace(old_text, new_text)
    return new_name

def rename_auto_numbering(usr_config, file):
    base_name = usr_config["base_name"]
    start_number = int(usr_config["start_number"])
    
    new_name = f"{base_name}_{start_number}{file.suffix}"
    usr_config["start_number"] = start_number + 1 
    
    return new_name


OPTIONS = {
    "Prefix": rename_prefix,
    "Suffix": rename_suffix,
    "Replace Text": rename_replace_text,
    "Auto Numbering": rename_auto_numbering
}