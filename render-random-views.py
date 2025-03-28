import copy
import random
import traceback
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
from lib.renderer.render_options import Material, RenderOptions, Quality, LightingStyle, Look, Format
from lib.colors import RebrickableColors, random_color_from_ids

NUM_IMAGES_PER_PART = 50
csv_file_path = '../lego-inventory/v2.csv'

rows = []

with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        canonical_part_num = row['canonical_part_num']
        ldraw_id = row['ldraw_id']
        color_ids = [int(color_id.strip()) for color_id in row['color_ids'].split(",")]
        material_id = row['material_id']
        rows.append((canonical_part_num, ldraw_id, color_ids, material_id))

RENDER_DIR ="./renders/random-views"
os.makedirs(RENDER_DIR, exist_ok=True)
renderer = Renderer(ldraw_path="./ldraw")

random.shuffle(rows)
for (part_num, ldraw_id, color_ids, material_id) in rows:
  if ldraw_id in ("70501a", "109481"):
    print(f"------ WARNING: Skipping {part_num}, problem with LDraw file")
    continue

  if not ldraw_dat_exists(ldraw_id):
    print(f"------ WARNING: Skipping {part_num}, LDraw file does not exist")
    continue

  base_options = RenderOptions(
      format = Format.PNG,
      quality = Quality.DRAFT,
      lighting_style = LightingStyle.DEFAULT,
      look=Look.NORMAL,
      width=224,
      height=224,
  )

  try:
    for i in range(NUM_IMAGES_PER_PART):
      image_filename = os.path.join(RENDER_DIR, str(part_num), f"{part_num}_random{i:02}.png")
      if os.path.exists(image_filename):
        print(f"------ Skipping {image_filename}, already exists")
        continue

      color = random_color_from_ids(color_ids)
      material = Material.TRANSPARENT if color.is_transparent else material_id

      print(f"------ Rendering {image_filename} with color {color.best_hex}...")
      options = copy.copy(base_options)
      options.image_filename = image_filename
      options.light_angle = random.uniform(0, 360)
      options.part_rotation = (random.uniform(0, 360), random.uniform(0, 360), random.uniform(0, 360))
      options.camera_height = random.uniform(15, 90)
      options.zoom=random.uniform(.97, 1.0)
      options.part_color = color.best_hex
      options.material = material
      renderer.render_part(ldraw_id, options)
  except Exception as e:
    print(f"------ ERROR: {part_num} failed to render: {e}")
    traceback.print_exc()
    continue
