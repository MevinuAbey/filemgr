#Select Source Folder
#Select Destination Folder
#Timestamped Backup Folder
#Copy All Files and Subfolders (Recursive)
#Summary Report
#Only copy: New files,Modified files
#Compare: File size, Last modified time, OR file hash (advanced)
#Skip Unchanged Files
#File Type Exclusion
#Preview Mode
#Compression Mode

def main(path):
    print(f"path to folder backup {path}")

def menu():
    #if there is backup config file show quick backup option
    #else show backup options
    ...


def Summary_report():
    #generate summary report of backup process
    #total files copied, skipped, failed
    #log file with details of backup process
    ...

def backup_files():
    #copy files from source to destination
    #handle file type exclusion
    #handle preview mode
    #handle compression mode
    ...