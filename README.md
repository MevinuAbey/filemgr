# 📁 FileMgr — Command-Line File Management Utility

Harvard CS50 Python Final Project By Mevinu Thewjaya Abeysinghe.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python">
  <img src="https://img.shields.io/badge/CLI-Tool-green">
</p>

#### 🎥 Video Demo  
<URL HERE>

---

## Description

**FileMgr** is a Python-based command-line file management utility designed to simplify everyday file operations. It helps reduce repetitive manual work by providing tools to:

- 📂 Organize files  
- 🏷️ Rename files in bulk  
- 💾 Create backups  

The goal of this project is to offer a fast, flexible, and user-friendly CLI tool for efficient file management.

---

## Core Features

### 💾 Backup

- *Create standard folder backups or compressed ZIP backups*  
- *Choose between timestamped backups or overwrite mode*  
- *Include or exclude files based on extensions*  
- *Perform quick backups using saved configurations*


### 📂 Organize

- *Organize files by:*
  - *File type*  
  - *File extension*  
  - *File type + extension*  
  - *Last modified date*  
- *Optional inclusion of subfolders*  
- *Move or copy files*  
- *Option to create a separate organized output folder*  


### 🏷️ Rename

- *Add prefixes or suffixes*  
- *Replace text within filenames*  
- *Auto-number files*  
- *Optional filtering by file type*  

---

## 🚀 Usage

### 🔹 Flags

- **`-p`, `--path`** → Target directory path  
  > Wrap paths with spaces in quotes to avoid problems when folder name have spaces like 'folder name'
  > Example: `"C:/path/to/folder 1"`

- **`-a`, `--action`** → Action to perform  
  (`backup`, `organize`, `rename`)

> If arguments are not provided, the program will prompt you interactively.



### 🔹 Run the Program

```bash
# Run with arguments
python project.py -p <path> -a <action>

# Run interactively
python project.py
```

---

## Project Structure

 - **project.py** — Main Controller  
*Handles CLI argument parsing (`-p` for path, `-a` for action), validates user input, and routes to the appropriate module that user selected. Also manages user prompts when arguments are incomplete.*

   - **menu.py** — User Interface  
*Provides interactive prompts using the `questionary` library. Collects and validates user choices for backup settings, organization options, and rename options before execute them. Separated from core logic to make the code clear and easy to read and modify.*

   - **backup.py** — Backup Logic  
*Creates both standard folder backups and compressed ZIP archives. Supports timestamped backups (for multiple versions) and overwrite mode (single backup). Includes file-type filtering (include/exclude by extension), quick-backup detection, and saves configuration in `backup_config.json`.*

   - **organize.py** — File Organization Logic  
*Implements four organization options: by file type, by extension, by type+extension, and by modified date. Handles file transfer (move or copy), creates output folder if needed, and generates a report.*

   - **rename.py** — Batch Renaming Logic  
*Performs bulk file renaming with four operations: prefix, suffix, text replacement, and auto-numbering. Includes optional file-type filtering and collision detection.*

---

### Testing & Configuration

- **test_project.py** — Unit Tests  
  Pytest tests for `project.py` functions: `check_path()`, `check_action()`, and `parse_arguments()`. Validates core behavior with mock paths and argument combinations.
  ```bash
  #to test -> run command below in terminal inside project folder whre 'project.py' is in
  pytest project.py
  ```

- **requirements.txt** — Dependencies  
  Lists required packages (`questionary` for prompts, `pytest` for testing).
  ```bash
  #to install required packages -> run command below in terminal inside project folder whre 'requirements.txt' is in
  pip install -r requirements.txt
  ```

---

## Why This Design?

**Modular Design** — Each feature (backup, organize, rename) is separated into its own module, making the code easier to read and test.

**Separation of UI and Logic** — User interaction (menu.py) is isolated from logic, makeing code clean and easy to read.

**Clear Main File** — `project.py` cordinates everything, making it easy to understand program flow.