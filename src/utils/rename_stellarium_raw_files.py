import os

from config import STELLARIUM_RAW_DIR

def rename_files(folder_path, start_number):
    print(f"Processing files in folder: {folder_path}")

    files = sorted(os.listdir(folder_path))
    constellation_files = {}
    
    # Group files by constellation
    for file in files:
        if file.endswith(".png"):
            name_parts = file.split("-")
            if len(name_parts) == 2 and name_parts[1].endswith(".png") and name_parts[1][:-4].isdigit():
                constellation_name = name_parts[0]
                if constellation_name not in constellation_files:
                    constellation_files[constellation_name] = []
                constellation_files[constellation_name].append(file)

    # Rename files in each constellation group
    for constellation, file_list in constellation_files.items():
        current_number = start_number
        for file in file_list:
            new_name = f"{constellation}-{str(current_number).zfill(3)}.png"
            old_path = os.path.join(folder_path, file)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {file} -> {new_name}")
            current_number += 1

start_number = 100

rename_files(STELLARIUM_RAW_DIR, start_number)
