import os
from tqdm import tqdm
import multiprocessing

# Change the target folder here
# folder_path = r"Y:\GOG Games\BG3 Mods\Export\- Patch HF3"
# folder_path = r"Y:\GOG Games\BG3 Mods\Export\- Patch HF4 redeployed"
folder_path = r"Y:\GOG Games\BG3 Mods\Export\-Base Public\Public"

# The target text is not case-sensitive
target_text = 'Infernal'

# num of parallel process
num_processes = 4

# play around this value *rec 50 - 100 (evo 970)
# depending on your disk speed it can speed up the process
batch_sizes = 50

# Exclude some extension, in this case .LSF and .LSB is encoded,
# you must decode it to .LSX first
excluded_extension = [
                        '.lsf',
                        '.lsb',
                        '.dds',
                      ]

# Exclude some file,
# ex: _merged.lsx contains copied guid from other .lsx
excluded_filenames = [
    '_merged.lsx',
    # '_merged2.lsx',
]
def gather_file(folder_path):
    all_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not any(file_path.lower().endswith(ext) for ext in excluded_extension) and \
                not any(file_name in file for file_name in excluded_filenames):
                all_files.append(file_path)
    return all_files

def process_files(file_paths_batch, target_text, result_queue):
    result_list = []

    for file_path in tqdm(file_paths_batch, desc="Progress", unit="file"):
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if target_text.lower() in content.lower():
                    result_list.append(file_path)
    result_queue.put(result_list)

def main():
    all_files = gather_file(folder_path)

    chunks = [all_files[i::num_processes] for i in range(num_processes)]

    manager = multiprocessing.Manager()
    result_queue = manager.Queue()

    processes = []
    for chunk in chunks:
        process = multiprocessing.Process(target=process_files, args=(chunk, target_text, result_queue))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    result_list = []
    while not result_queue.empty():
        result_list.extend(result_queue.get())

    if result_list:
        with open("file_list.txt", "w") as f:
            for file_path in result_list:
                f.write(file_path + "\n")
        print(f"{len(result_list)} files found, list written to file_list.txt.")
    else:
        print("No files containing the target text were found.")

if __name__ == "__main__":
    main()