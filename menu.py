from pathlib import Path
import sys
import questionary # type: ignore

def organize_menu(source_path):
    organize_option = questionary.select("Organize Files in to folders according to:",
        choices=["file type","file extention","file type and file extention","modified date"]).ask()
    is_organize_sub_folders = questionary.confirm("also organize files in sub folders:").ask()
    is_copy_or_move = questionary.select("move files when organizing or copy them:",choices=["copy","move",]).ask()
    is_create_new_folder = questionary.confirm("create new folder when organizing:").ask()

    if confirm_action("organize"):
        return {"source_path": source_path,
                "organize_option": organize_option,
                "is_organize_sub_folders": is_organize_sub_folders,
                "is_copy_or_move": is_copy_or_move,
                "is_create_new_folder": is_create_new_folder
                }

def rename_menu(source_path):
    rename_option = questionary.select(
        "Choose a renaming option:", choices=["Prefix", "Suffix", "Replace Text", "Auto Numbering"]).ask()
    
    if rename_option == "Auto Numbering":
        base_name = questionary.text("Enter the base name for numbering:").ask()
        start_number = questionary.text("Enter the starting number(leave blank for 1):").ask()
        if confirm_action("rename"):
            return {"source_path": source_path,
                    "rename_option": rename_option,
                    "base_name": base_name,
                    "start_number": start_number
                    }
    
    elif rename_option in ["Prefix", "Suffix"]:
        text = questionary.text(f"Enter the text to add as {rename_option.lower()}:").ask()
        if confirm_action("rename"):
            return {"source_path": source_path,
                    "rename_option": rename_option,
                    "text": text
                    }
    
    elif rename_option == "Replace Text":
        old_text = questionary.text("Enter the text to replace:").ask()
        new_text = questionary.text("Enter the new text:").ask()
        if confirm_action("rename"):
            return {"source_path": source_path,
                    "rename_option": rename_option,
                    "old_text": old_text,
                    "new_text": new_text
                    }

def backup_menu(source_path):
    while True:
        backup_dest = questionary.text("Enter backup destination folder path: (leave blank to use default)").ask()
        if not backup_dest:
            backup_dest = (Path.home() / "backup_files_filemgr" / f"{source_path.resolve().name}_backup")
        dest_path = Path(backup_dest)

        if dest_path.exists() and dest_path.is_dir():
            break
        else:
            dest_path.mkdir(parents=True, exist_ok=True)
            break

    is_compress = questionary.confirm("Do you want to compress the backup?").ask()

    backup_mode = questionary.select("Do you want to create a timestamped backup or overwriting backup?",
                                      choices=["timestamp", "overwrite"]).ask()
    
    exc_or_inc = questionary.select("Do you want to exclude or include specific file types?",
                                     choices=["Include All", "Exclude", "Include"]).ask()
    
    file_types = []
    if exc_or_inc == "Exclude" or exc_or_inc == "Include":
        file_types = questionary.text(
            f"Enter file types to {exc_or_inc} (comma separated, e.g., .tmp, .log):").ask()
        file_types = [ft.strip() for ft in file_types.split(",")] if file_types else []

    if not file_types:
        exc_or_inc = "Include All"

    if confirm_action("backup"):
        return {"source_path": source_path, "backup_dest": backup_dest, "is_compress": is_compress,
                "backup_mode": backup_mode, "exc_or_inc": exc_or_inc, "file_types": file_types}

def confirm_action(action):
    confirm = questionary.confirm(f"Do you want to {action} with above settings?").ask()
    if not confirm:
        print(f"{action} cancelled.")
        sys.exit(0)