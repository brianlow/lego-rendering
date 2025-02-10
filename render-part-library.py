import bpy
import sys
import os
import csv

# This script runs under Blender's python environment. Add the current
# directly to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)

from lib.renderer.dat import ldraw_dat_exists
from lib.renderer.renderer import Renderer
from lib.renderer.render_options import RenderOptions, Quality, LightingStyle, Look, Format
from lib.colors import RebrickableColors

csv_file_path = '../lego-inventory/sorter-10000.csv'

ids = []

with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        canonical_part_num = row['canonical_part_num']
        ldraw_id = row['ldraw_id']
        ids.append((canonical_part_num, ldraw_id))


RENDER_DIR ="./renders/part-library"

os.makedirs(RENDER_DIR, exist_ok=True)

renderer = Renderer(ldraw_path="./ldraw")

for (part_num, ldraw_id) in ids:
  filename = f"{RENDER_DIR}/{part_num}.png"
  if os.path.exists(filename):
    print(f"------ Skipping {part_num}, already exists")
    continue

  if ldraw_id in ("70501a", "109481"):
    print(f"------ WARNING: Skipping {part_num}, problem with LDraw file")
    continue

  if not ldraw_dat_exists(ldraw_id):
    print(f"------ WARNING: Skipping {part_num}, LDraw file does not exist")
    continue

  print(f"------ Rendering {part_num} with LDraw {ldraw_id}...")
  try:
    options = RenderOptions(
        image_filename = filename,
        format = Format.PNG,
        blender_filename = None,
        quality = Quality.DRAFT,
        lighting_style = LightingStyle.BRIGHT,
        part_color = RebrickableColors.White.value.best_hex,
        part_rotation=(0, 0, 0),
        zoom=1,
        look=Look.INSTRUCTIONS,
        width=150,
        height=150,
    )
    renderer.render_part(ldraw_id, options)
  except Exception as e:
    print(f"------ ERROR: {part_num} failed to render: {e}")
    continue
