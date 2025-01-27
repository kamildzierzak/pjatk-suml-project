import os


def create_constellations_folders(constellations_dir, constellations):
    """
    Create folders for each constellation in the specified directory.
    """
    os.makedirs(constellations_dir, exist_ok=True)

    for latin_name, abbreviation, polish_name in constellations:
        folder_name = f"{latin_name}"
        folder_path = os.path.join(constellations_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

    print(f"Created folders for 88 constellations in {constellations_dir}")
