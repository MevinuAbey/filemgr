from pathlib import Path
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

print(file_types_ext.keys())

folder_path = Path("c://python")

category_dirs = [folder_path / cat for cat in file_types_ext.keys()]
print(category_dirs)

category_dirs.append(folder_path / "Other")

print(category_dirs)