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

csv_file_path = '../lego-inventory/v3.csv'

rows = []

with open(csv_file_path, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        canonical_part_num = row['canonical_part_num']
        ldraw_id = row['ldraw_id']
        color_ids = [int(color_id.strip()) for color_id in row['color_ids'].split(",")]
        material_id = row['material_id']
        rows.append((canonical_part_num, ldraw_id, color_ids, material_id))

RENDER_DIR ="./renders/standard-views"
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
      format = Format.JPEG,
      lighting_style = LightingStyle.DEFAULT,
      zoom=.99,
      look=Look.NORMAL,
      width=224,
      height=224,
  )

  try:
    views = []
    views.extend([(0, 0, 45, 10), (0, 0, 45+90, 10), (0, 0, 45+180, 10), (0, 0, 45+270, 10)]) # front, left, back, right
    views.extend({(0, 0, 0, 90), (180, 0, 0, 90)}) # top, bottom
    for ((rx, ry, rz, camera_height)) in views:
      image_filename = os.path.join(RENDER_DIR, str(part_num), f"{part_num}_{rx}_{ry}_{rz}_{camera_height}.jpg")
      label_filename = os.path.join(RENDER_DIR, str(part_num), f"{part_num}_{rx}_{ry}_{rz}_{camera_height}.txt")
      if os.path.exists(image_filename) and os.path.exists(label_filename):
        print(f"------ Skipping {image_filename}, already exists")
        continue
      if os.path.exists(image_filename) and not os.path.exists(label_filename):
        print(f"------ Regenerating {image_filename} with bounding box")
        os.remove(image_filename)

      print(f"------ Rendering {image_filename}...")
      color = random_color_from_ids(color_ids)
      material = Material.TRANSPARENT if color.is_transparent else material_id

      options = copy.copy(base_options)
      options.image_filename = image_filename
      options.bounding_box_filename = label_filename
      options.quality = Quality.NORMAL
      options.part_rotation = (rx, ry, rz)
      options.camera_height = camera_height
      options.light_angle = random.uniform(0, 360)
      options.zoom = random.uniform(.99, 1.0)
      options.part_color = color.best_hex
      options.material = material
      renderer.render_part(ldraw_id, options)
  except Exception as e:
    print(f"------ ERROR: {part_num} failed to render: {e}")
    traceback.print_exc()
    continue
