import os
import subprocess


# Choose if you want to use default notepad++ directory
# or using environment variable
# notepad_location = os.environ.get("NPP", "notepad++.exe")
notepad_location = r"C:\Program Files\Notepad++\notepad++.exe"


def open_files(file_paths):
    
    for file_path in file_paths:
        subprocess.run([notepad_location, file_path])


# Open from file_list.txt
with open("file_list.txt", "r") as f:
    file_paths = [line.strip() for line in f]

if file_paths:
    open_files(file_paths)

else:
    print("file_list.txt not found.")
