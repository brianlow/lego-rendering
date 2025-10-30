# This file is for testing the package without publishing to pypi

import sys
import os

# This script runs under Blender's python environment. Add the current
# directly to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)
from lego_rendering import Renderer, RenderOptions, Quality, LightingStyle, Look, Material, RebrickableColors, BoundingBox

color = RebrickableColors.MediumAzure.value
render_bbox = True

renderer = Renderer(ldraw_path="./ldraw")
options = RenderOptions(
    image_filename = "renders/test.png",
    bounding_box_filename = "renders/test.txt",
    blender_filename = "renders/test.blend",
    quality = Quality.DRAFT,
    lighting_style = LightingStyle.DEFAULT,
    part_color = color.best_hex,
    material = Material.TRANSPARENT if color.is_transparent else Material.PLASTIC,
    light_angle = 160,
    part_rotation=(0, 0, 0),
    camera_height=45,
    zoom=.99,
    look=Look.NORMAL,
    width=244,
    height=244,
)

print("--------- Rendering 1/3 ---------")
options.image_filename = "renders/test1.png"
renderer.render_part("3005", options)

# print("--------- Rendering 2/3 ---------")
# options.image_filename = "renders/test2.png"
# renderer.render_part("3001", options)

# print("--------- Rendering 3/3 ---------")
# options.image_filename = "renders/test3.png"
# renderer.render_part("3002", options)

Draw bounding box on the rendered image
if render_bbox and options.bounding_box_filename:
   BoundingBox.annotate(options.image_filename, options.bounding_box_filename)
