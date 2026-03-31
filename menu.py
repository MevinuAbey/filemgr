from pathlib import Path
import sys
import questionary

# organize menu to get user settings for organize function
def organize_menu(source_path):
    organize_option = ask(questionary.select("Organize Files in to folders according to:",
        choices=["file type","file extension","file type and extension","modified date"]))
    is_organize_sub_folders = ask(questionary.confirm("also organize files in sub folders:"))
    is_copy_or_move = ask(questionary.select("Do you want to move or copy files when organizing?:",choices=["copy","move"]))# can use like COPY or MOVE to avoid confusion
    is_create_new_folder = ask(questionary.confirm("create new folder when organizing:"))

    if not confirm_action("organize"):
        return None

    return {"source_path": source_path,
            "organize_option": organize_option,
            "is_organize_sub_folders": is_organize_sub_folders,
            "is_copy_or_move": is_copy_or_move,
            "is_create_new_folder": is_create_new_folder
            }

# rename menu to get user settings for rename function
def rename_menu(source_path):

    file_type = ask(questionary.text("Enter file type filter (e.g., .txt) or leave blank for all files:"))
    file_type = file_type.strip() if file_type else None

    rename_option = ask(questionary.select(
        "Choose a renaming option:", choices=["Prefix", "Suffix", "Replace Text", "Auto Numbering"]))
    
    if rename_option == "Auto Numbering":
        base_name = ask(questionary.text("Enter the base name for numbering:"))
        start_number = ask(questionary.text("Enter the starting number(leave blank for 0):", default="0"))
        if not confirm_action("rename"):
            return None
        return {"source_path": source_path,
                "rename_option": rename_option,
                "file_type": file_type,
                "base_name": base_name,
                "start_number": start_number
                }
    
    elif rename_option in ["Prefix", "Suffix"]:
        text = ask(questionary.text(f"Enter the text to add as {rename_option.lower()}:"))
        if not confirm_action("rename"):
            return None
        return {"source_path": source_path,
                "rename_option": rename_option,
                "file_type": file_type,
                f"{rename_option.lower()}": text
                }
    
    elif rename_option == "Replace Text":
        old_text = ask(questionary.text("Enter the text to replace:"))
        new_text = ask(questionary.text("Enter the new text:"))
        if not confirm_action("rename"):
            return None
        return {"source_path": source_path,
                "rename_option": rename_option,
                "file_type": file_type,
                "old_text": old_text,
                "new_text": new_text
                }

# backup menu to get user settings for backup function
def backup_menu(source_path):

    backup_dest = ask(questionary.text("Enter backup destination folder path: (leave blank to use default)"))

    if backup_dest == "":
        # default backup destination
        backup_dest = (Path.home() / "backup_files_filemgr" / f"{source_path.resolve().name}_backup")
    dest_path = Path(backup_dest)

    dest_path.mkdir(parents=True, exist_ok=True) # create backup destination folder if it doesn't exist

    is_compress = ask(questionary.confirm("Do you want to compress the backup?"))

    backup_mode = ask(questionary.select("Do you want to create a timestamped backup or overwriting backup?",
                                      choices=["timestamp", "overwrite"]))
    
    exc_or_inc = ask(questionary.select("Do you want to exclude or include specific file types?",
                                     choices=["Include All", "Exclude", "Include"]))
    
    file_types = []
    if exc_or_inc == "Exclude" or exc_or_inc == "Include":
        file_types = ask(questionary.text(
            f"Enter file types to {exc_or_inc} (comma separated, e.g., .tmp, .log):"))
        
        file_types = [
                        ft.strip() if ft.strip().startswith('.') else f".{ft.strip()}"
                        for ft in file_types.split(",")
                        ] if file_types else []

    if not file_types:
        exc_or_inc = "Include All"

    if not confirm_action("backup"):
        return None
    
    return {"source_path": source_path, "backup_dest": backup_dest, "is_compress": is_compress,
            "backup_mode": backup_mode, "exc_or_inc": exc_or_inc, "file_types": file_types}

# ask user if want to do quick backup
def ask_quick_backup():
        print("Quick Backup Available")
        is_quick_backup = ask(questionary.confirm("Do you want to perform a quick backup using the last settings?"))
        if is_quick_backup:
            return True
        else:
            return False

# ask user to confirm to do selected action with user entered settings
def confirm_action(action):
    confirm = ask(questionary.confirm(f"Do you want to {action} with above settings?"))
    if not confirm:
        print(f"{action} cancelled.")
        return None
    return True

# fuction to check if user cancelled the prompt and then exit the program 
def ask(prompt):
    usr_input = prompt.ask()

    if usr_input is None:
        print("\n Program cancelled by user.")
        sys.exit(0)
    return usr_input