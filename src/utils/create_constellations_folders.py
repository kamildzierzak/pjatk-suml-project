import os

from config import CONSTELLATIONS_DIR, constellations

os.makedirs(CONSTELLATIONS_DIR, exist_ok=True)

for latin_name, abbreviation, polish_name in constellations:
    folder_name = f"{latin_name}"
    folder_path = os.path.join(CONSTELLATIONS_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

print(f"Created folders for 88 constellations in {CONSTELLATIONS_DIR}")
