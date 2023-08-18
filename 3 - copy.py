import os
import shutil
from tqdm import tqdm

# Source and destination folder paths
source_folder = r"Y:\GOG Games\BG3 Mods\Export\-Base Public\Public"
destination_folder = r"Y:\GOG Games\BG3 Mods\Export\-Base Public\Search\LSB"

# File Extension
included_extensions = [
                        # '.lsx',
                        '.lsb',
                       ]

# Create destination if not exist
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

def gather_files_with_extensions(source_folder, included_extensions):
    all_files = []

    for root, _, files in os.walk(source_folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in included_extensions):
                file_path = os.path.join(root, file)
                all_files.append(file_path)

    return all_files

def copy_files_with_progress(file_paths, destination_folder):
    copied_files = []

    for file_path in tqdm(file_paths, desc="Copying", unit="file"):
        destination_path = os.path.join(destination_folder, os.path.basename(file_path))
        shutil.copy2(file_path, destination_path)
        copied_files.append(file_path)

    return copied_files

all_files = gather_files_with_extensions(source_folder, included_extensions)
copied_files = copy_files_with_progress(all_files, destination_folder)

print(f"{len(copied_files)} files copied to {destination_folder}.")
