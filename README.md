# 📁 FileMgr — Command-Line File Management Utility

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
- Create standard folder backups or compressed ZIP backups  
- Choose between timestamped backups or overwrite mode  
- Include or exclude files based on extensions  
- Perform quick backups using saved configurations  

---

### 📂 Organize
- Organize files by:
  - File type  
  - File extension  
  - File type + extension  
  - Last modified date  
- Optional inclusion of subfolders  
- Move or copy files  
- Option to create a separate organized output folder  

---

### 🏷️ Rename
- Add prefixes or suffixes  
- Replace text within filenames  
- Auto-number files  
- Optional filtering by file type  

---

## Project Structure

- **project.py** - starts the app, reads CLI arguments, asks user for missing input, and send to backup/organize/rename logic.
  
  - **menu.py** -  collects user configuration before operations run.
  - **backup.py** - creates backups based on chosen options and saves settings in backup_config.json for quick backups.
  - **rename.py** -  iterates files (with optional extension filter) and renames them while avoiding name collisions.
  - **organize.py** -  scans files, chooses destination folders based on strategy, copies/moves files, and writes a report file. 
