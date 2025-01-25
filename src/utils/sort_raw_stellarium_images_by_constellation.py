import os
import shutil

from config import STELLARIUM_RAW_DIR, CONSTELLATIONS_DIR

def organize_photos(STELLARIUM_RAW_DIR, CONSTELLATIONS_DIR):
  if not os.path.exists(STELLARIUM_RAW_DIR):
    print(f"Directory {STELLARIUM_RAW_DIR} does not exist.")
    return
  
  if not os.path.exists(CONSTELLATIONS_DIR):
    os.makedirs(CONSTELLATIONS_DIR)
    print(f"Directory {CONSTELLATIONS_DIR} created.")
  
  for filename in os.listdir(STELLARIUM_RAW_DIR):
    if not filename.endswith((".jpg", ".jpeg", ".png")):
      continue

    # Extract the constellation name from the filename (before the first dash)
    constellation_name = filename.split("-")[0]

    constellation_folder = os.path.join(CONSTELLATIONS_DIR, constellation_name)
    if not os.path.exists(constellation_folder):
      os.makedirs(constellation_folder)

    source_path = os.path.join(STELLARIUM_RAW_DIR, filename)
    destination_path = os.path.join(constellation_folder, filename)
    shutil.move(source_path, destination_path)

  print("Images have been moved to appropriate folders.")

organize_photos(STELLARIUM_RAW_DIR, CONSTELLATIONS_DIR)