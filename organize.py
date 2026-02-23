# Expected functions from this script
# 1st option, organize files into diffrent folders acording to file type like vid,img,document.
# 2nd option, organize files into diffrent folders accoring to file extention like png,jpg,mp4,pdf.
# 3rd option, organize files into diffrent folders according to file type and in that file type organize those files in to foders
#             using file extentions.
# 4th option, organize files into diffrent folders acording to created date.(year->month->date)
# 5th option, organize files into diffrent folders acording to modified date.(year->month->date)
#
# ask if scan whole folder including sub folders or only files in that folder.
# ask if need to move files when organizing or copy them to organized folder.
# export txt report in that show file conunt accrdint to file type and file extention.
#
import datetime
import questionary
from pathlib import Path
import shutil

def main(path):
    folder_path = Path(path)
    org_option, is_sub, is_com,create_nf = menu() #is_sub-yes,no #is_com-copy,move
    do_organize(org_option,is_sub,is_com,folder_path,create_nf)

def menu():
    org_option = questionary.select("Organize Files in to folders according to:",
        choices=["file type","file extention","file type and file extention","modified date"]).ask()

    is_sub = questionary.select("also organize files in sub folders:",choices=["yes","no",]).ask()

    is_com = questionary.select("move files when organizing or copy them:",choices=["copy","move",]).ask()

    create_nf = questionary.select("create new folder when organizing:",choices=["yes","no",]).ask()

    return org_option,is_sub,is_com,create_nf

def load_list_files(folder_path,is_sub):
    #if user organizing files in subfolders using "rglog" otherwise using "iterdir" for listing files
    files = folder_path.rglob("*") if is_sub == "yes" else folder_path.iterdir()
    return files

def save_path_fuc(folder_path,create_nf):     
    #if user choosed make diffrent foldr for organized files make it
    if create_nf == "yes":
        save_path = folder_path / "organized"
        save_path.mkdir(exist_ok=True)
    elif create_nf == "no":
        save_path = folder_path
    else:
        print("plz enter valid input")
    return save_path

def do_organize(org_option,is_sub,is_com,folder_path,create_nf):
    if org_option == "file type": org_file_type(folder_path,is_com,is_sub,create_nf)
    elif org_option == "file extention": org_file_ext(folder_path,is_com,is_sub,create_nf)
    elif org_option == "file type and file extention": org_file_type_ext(folder_path,is_com,is_sub,create_nf)
    elif org_option == "modified date": org_modified_date(folder_path,is_com,is_sub,create_nf)

def org_file_type(folder_path,is_com,is_sub,create_nf):
    
    files = load_list_files(folder_path,is_sub)
    save_path = save_path_fuc(folder_path,create_nf)

    # Skiping the catagorized folders we'll create
    category_dirs = [save_path / cat for cat in file_types_ext.keys()] #getting file types from file_types_ext
    category_dirs.append(save_path / "Others") #append others folder path

    for file in files: #for each file in the folder or subforlder if user chooses
        if file.is_file(): #cheks if its a file
            ext = file.suffix.lower()
            category = next((cat for cat, exts in file_types_ext.items() if ext in exts), "Others")
            dest_folder = save_path / category #folder name with catagory like Images,Documents,Video,Music,Others
            dest_folder.mkdir(exist_ok=True)

            if is_com == "move":
                shutil.move(str(file), str(dest_folder / file.name))
            else:
                shutil.copy2(str(file), str(dest_folder / file.name))

def org_file_ext(folder_path,is_com,is_sub,create_nf):
    files = load_list_files(folder_path,is_sub)
    save_path = save_path_fuc(folder_path,create_nf)

    for file in files: #for each file in the folder or subforlder if user chooses
        if file.is_file(): #cheks if its a file
            ext = file.suffix.lower()
            if ext:
                dest_folder = save_path / ext[1:] #folder name without dot like .png -> png
                dest_folder.mkdir(exist_ok=True)

                if is_com == "move":
                    shutil.move(str(file), str(dest_folder / file.name))
                else:
                    shutil.copy2(str(file), str(dest_folder / file.name))
    print(f"Files in '{folder_path}' organized by file extension ({'moved' if is_com == "move" else 'copied'})")

def org_file_type_ext(folder_path,is_com,is_sub,create_nf):
    files = load_list_files(folder_path,is_sub)
    save_path = save_path_fuc(folder_path,create_nf)

    for file in files:
        if file.is_file():
            ext = file.suffix.lower()
            category = next((cat for cat, exts in file_types_ext.items() if ext in exts), "Others")
            dest_folder = save_path / category / ext[1:] #folder name with catagory and extention like Images/png
            dest_folder.mkdir(parents=True, exist_ok=True)

            if is_com == "move":
                shutil.move(str(file), str(dest_folder / file.name))
            else:
                shutil.copy2(str(file), str(dest_folder / file.name))

    print(f"Files in '{folder_path}' organized by file type and extension ({'moved' if is_com == "move" else 'copied'})")

def org_modified_date(folder_path,is_com,is_sub,create_nf):
    files = load_list_files(folder_path,is_sub)
    save_path = save_path_fuc(folder_path,create_nf)

    for file in files:
        if file.is_file():
            mod_time = file.stat().st_mtime
            mod_date = datetime.datetime.fromtimestamp(mod_time)
            dest_folder = save_path / f"{mod_date.year}" / f"{mod_date.month:02d}" / f"{mod_date.day:02d}"
            dest_folder.mkdir(parents=True, exist_ok=True)

            if is_com == "move":
                shutil.move(str(file), str(dest_folder / file.name))
            else:
                shutil.copy2(str(file), str(dest_folder / file.name))

    print(f"Files in '{folder_path}' organized by modified date ({'moved' if is_com == "move" else 'copied'})")

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


