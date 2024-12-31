import os
import re

base_dir = 'data/constellations'

# regex - usuwania tekstu w nawiasach wraz z nawiasami
pattern = re.compile(r'\([^)]*\)+')


for folder_name in os.listdir(base_dir):
  full_path = os.path.join(base_dir, folder_name)

  if os.path.isdir(full_path):
    new_name = re.sub(pattern, '', folder_name).strip()

    new_full_path = os.path.join(base_dir, new_name)

    os.rename(full_path, new_full_path)
    print(f'Renamed: {full_path} -> {new_full_path}')