import os
import questionary
from pathlib import Path
import shutil

def main(path):
    folder_path = Path(path)
    menu()


def menu():
    selected_option = questionary.select("Organize Files in to folders according to:",
        choices=["file type",
            "file extention",
            "file type and file extention",
            "created date",
            "modified date"
        ]
    ).ask()
    folder_selction = questionary.select("also organize files in sub folders:",choices=["yes","no",]).ask()
    com_selction = questionary.select("move files when organizing or copy them:",choices=["copy","move",]).ask()


    ...

def org_file_type(path, is_com=True, is_sub=True):
    folder = Path(path)

    # Choose traversal: recursive if is_sub, else just folder.iterdir()
    files = folder.rglob("*") if is_sub else folder.iterdir()

    # Skip folders we'll create
    category_dirs = [folder / cat for cat in file_types_ext.keys()]
    category_dirs.append(folder / "Others")

    for file in files:
        if file.is_file() and all(not str(file).startswith(str(d)) for d in category_dirs):
            ext = file.suffix.lower()
            moved = False

            for category, extensions in file_types_ext.items():
                if ext in extensions:
                    dest_folder = folder / category
                    dest_folder.mkdir(exist_ok=True)
                    if is_com:
                        shutil.move(str(file), str(dest_folder / file.name))
                    else:
                        shutil.copy2(str(file), str(dest_folder / file.name))
                    moved = True
                    break

            if not moved:
                dest_folder = folder / "Others"
                dest_folder.mkdir(exist_ok=True)
                if is_com:
                    shutil.move(str(file), str(dest_folder / file.name))
                else:
                    shutil.copy2(str(file), str(dest_folder / file.name))




def org_file_ext():
    ...

def org_file_type_ext():
    ...

def org_created_date():
    ...

def org_modified_date():
    ...


# p = Path("C:\Python\ew")

# for i in p.iterdir():
#    if i.is_file():
#        print(i)

file_types_ext = {
    "Images": [
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".bmp",
        ".webp",
        ".ico",
        ".svg",
        ".tiff",
        ".tif",
    ],
    "Documents": [
        ".txt",
        ".doc",
        ".docx",
        ".pdf",
        ".rtf",
        ".odt",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".csv",
        ".md",
    ],
    "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"],
}
