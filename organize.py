# organize module for filemgr
import datetime
import shutil


def do_organize(usr_options):
    source_path = usr_options["source_path"]
    organize_option = usr_options["organize_option"]
    is_organize_sub_folders = usr_options["is_organize_sub_folders"]
    is_copy_or_move = usr_options["is_copy_or_move"]
    is_create_new_folder = usr_options["is_create_new_folder"]

    organize_func = OPTIONS.get(organize_option)

    report, save_path = process_files(source_path,is_organize_sub_folders,is_create_new_folder,is_copy_or_move,organize_func)

    save_report(report, save_path, organize_option)

def load_list_files(source_path,is_organize_sub_folders):
    #if user organizing files in subfolders using "rglog" otherwise using "iterdir" for listing files
    files = source_path.rglob("*") if is_organize_sub_folders else source_path.iterdir()
    return files

def save_path_fuc(source_path,create_nf):     
    #if user choosed make diffrent foldr for organized files make it
    if create_nf :
        save_path = source_path / "organized"
        save_path.mkdir(exist_ok=True)
    else:
        save_path = source_path
    return save_path

def save_report(report, save_path, organize_option):
    with open(save_path / "report.txt", "w") as f:
        f.write(f"Organized by: {organize_option}\n")
        f.write(f"Total files: {len(report)}\n\n")

        for src, dest in report:
            f.write(f"{src} -> {dest}\n")

def transfer_file(src, dest, mode):
    dest.parent.mkdir(parents=True, exist_ok=True)

    if mode == "move":
        shutil.move(str(src), str(dest))
    else:
        shutil.copy2(str(src), str(dest))

def process_files(source_path,is_organize_sub_folders,is_create_new_folder,is_copy_or_move,organize_func):
    files = list(load_list_files(source_path, is_organize_sub_folders))  # safe copy
    save_path = save_path_fuc(source_path, is_create_new_folder)

    report = []

    for file in files:
        if not file.is_file():
            continue

        dest = organize_func(file, save_path)

        if not dest:
            continue

        # avoid overwrite
        if dest.exists():
            print(f"Skipping {file.name} (already exists)")
            continue

        transfer_file(file, dest, is_copy_or_move)

        report.append((file.name, str(dest)))

    return report, save_path

def by_extension(file, base_path):
    ext = file.suffix.lower()
    if not ext:
        return None
    return base_path / ext[1:] / file.name

def by_type(file, base_path):
    ext = file.suffix.lower()

    category = next(
        (cat for cat, exts in file_types_ext.items() if ext in exts),
        "Others"
    )

    return base_path / category / file.name

def by_type_and_extension(file, base_path):
    ext = file.suffix.lower()

    category = next(
        (cat for cat, exts in file_types_ext.items() if ext in exts),
        "Others"
    )

    return base_path / category / ext[1:] / file.name

def by_date(file, base_path):
    mod_time = file.stat().st_mtime
    mod_date = datetime.datetime.fromtimestamp(mod_time)

    return base_path / str(mod_date.year) / f"{mod_date.month:02d}" / f"{mod_date.day:02d}" / file.name

OPTIONS = {
    "file type": by_type,
    "file extension": by_extension,
    "file type and extension": by_type_and_extension,
    "modified date": by_date,
}

file_types_ext = {
    "Images": [".png",".jpg",".jpeg",".gif",".bmp",".webp",".ico",".svg",".tiff",".tif",],
    "Documents": [".txt",".doc",".docx",".pdf",".rtf",".odt",".xls",".xlsx",".ppt",".pptx",".csv",".md",],
    "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"],
}