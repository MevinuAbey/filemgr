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
