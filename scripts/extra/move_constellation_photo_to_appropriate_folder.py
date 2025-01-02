import os
import shutil

source_dir = "data/stellarium_raw"
destination_dir = "data/constellations"

def organize_photos(source_dir, destination_dir):
  if not os.path.exists(source_dir):
    print(f"Directory {source_dir} does not exist.")
    return
  
  if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)
    print(f"Directory {destination_dir} created.")
  
  for filename in os.listdir(source_dir):
    if not filename.endswith((".jpg", ".jpeg", ".png")):
      continue

    # Extract the constellation name from the filename (before the first dash)
    constellation_name = filename.split("-")[0]

    constellation_folder = os.path.join(destination_dir, constellation_name)
    if not os.path.exists(constellation_folder):
      os.makedirs(constellation_folder)

    source_path = os.path.join(source_dir, filename)
    destination_path = os.path.join(constellation_folder, filename)
    shutil.move(source_path, destination_path)

  print("Photos have been moved to appropriate folders.")

organize_photos(source_dir, destination_dir)