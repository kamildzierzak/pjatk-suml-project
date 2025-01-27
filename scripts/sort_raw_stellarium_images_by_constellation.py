import os
import shutil


def organize_photos(stellarium_raw_dir, constellations_dir):
    """
    Organize photos from Stellarium by constellation.
    """
    if not os.path.exists(stellarium_raw_dir):
        print(f"Directory {stellarium_raw_dir} does not exist.")
        return

    if not os.path.exists(constellations_dir):
        os.makedirs(constellations_dir)
        print(f"Directory {constellations_dir} created.")

    for filename in os.listdir(stellarium_raw_dir):
        if not filename.endswith((".jpg", ".jpeg", ".png")):
            continue

        # Extract the constellation name from the filename (before the first dash)
        constellation_name = filename.split("-")[0]

        constellation_folder = os.path.join(constellations_dir, constellation_name)
        if not os.path.exists(constellation_folder):
            os.makedirs(constellation_folder)

        source_path = os.path.join(stellarium_raw_dir, filename)
        destination_path = os.path.join(constellation_folder, filename)
        shutil.move(source_path, destination_path)

    print("Images have been moved to appropriate folders.")
