from pathlib import Path
import sys
import questionary # type: ignore
import backup
import organize
import rename

def main(action, source_path):
    if action == "backup":
        backup_dest, is_compress, backup_mode, exc_or_inc, file_types = backup_menu(source_path)
        #confirmation if backup
        confirm_backup = questionary.confirm("Do you want to backup with above settings?").ask()
        if not confirm_backup:
            print("backup cancelled.")
            sys.exit(0)
        backup.backup(source_path, backup_dest, is_compress, backup_mode, exc_or_inc, file_types) #run backup with settings from menu
        #saving confing
        backup.save_backup_config(source=source_path, destination=backup_dest,exc_or_inc=exc_or_inc, file_types=file_types, is_compress=is_compress, backup_mode=backup_mode)
        print("Backup Settings Saved. Next time you can use quick backup to backup with these settings.")

    elif action == "organize":
        org_option, is_sub, is_com, create_nf = organize_menu()
        organize.main(source_path,org_option,is_sub,is_com,create_nf)

    elif action == "rename":
        rename_option = rename_menu()
        rename.main(source_path, rename_option)


def organize_menu():
    org_option = questionary.select("Organize Files in to folders according to:",
        choices=["file type","file extention","file type and file extention","modified date"]).ask()
    is_sub = questionary.confirm("also organize files in sub folders:").ask()
    is_com = questionary.select("move files when organizing or copy them:",choices=["copy","move",]).ask()
    create_nf = questionary.confirm("create new folder when organizing:").ask()
    return org_option,is_sub,is_com,create_nf

def rename_menu():
    rename_option = questionary.select(
        "Choose a renaming option:", choices=["Prefix", "Suffix", "Replace Text", "Auto Numbering"]).ask()
    return rename_option

def backup_menu(source_path):
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