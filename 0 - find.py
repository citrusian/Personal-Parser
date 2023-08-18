import os
from tqdm import tqdm

# Change the target folder here
# folder_path = r"Y:\GOG Games\BG3 Mods\Export\-Base Public\Search\Flags LSX"
# folder_path = r"Y:\GOG Games\BG3 Mods\Export\-Base Public\Search\Misc LSX"
# folder_path = r"Y:\GOG Games\BG3 Mods\Export\- Patch HF3"
# folder_path = r"Y:\GOG Games\BG3 Mods\Export\- Patch HF4 redeployed"
folder_path = r"Y:\GOG Games\BG3 Mods\Export\-Base Public\Public"

# The target text is not case-sensitive, modify line 30-33 to use case-sensitive
target_text = 'Infernal'

# Exclude some extension, in this case .LSF and .LSB is encoded, so you must decode it to .LSX first
excluded_extension = [
                        '.lsf',
                        '.lsb',
                        '.dds',
                      ]

def gather_file(folder_path):
    all_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not any(file_path.lower().endswith(ext) for ext in excluded_extension):
                all_files.append(file_path)
    return all_files

def search_target(file_paths, target_text):
    file_list = []

    for file_path in tqdm(file_paths, desc="Progress", unit="file"):
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if target_text.lower() in content.lower():
                    file_list.append(file_path)
                # if target_text in content:
                #     file_list.append(file_path)
    return file_list

all_files = gather_file(folder_path)
file_list = search_target(all_files, target_text)

if file_list:
    with open("file_list.txt", "w") as f:
        for file_path in file_list:
            f.write(file_path + "\n")
    print(f"{len(file_list)} files found, list written to file_list.txt.")

else:
    print("No files containing the target text were found.")
