import bpy
import sys
import os
from copy import copy

# This script runs under Blender's python environment. Add the current
# directly to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)

from lib.renderer.renderer import Renderer
from lib.renderer.render_options import RenderOptions, Quality, LightingStyle, Look, Material
from lib.colors import RebrickableColors


renderer = Renderer(ldraw_path="./ldraw")

default_options = RenderOptions(
    image_filename="renders/test.png",
    quality=Quality.HIGH,
    lighting_style=LightingStyle.DEFAULT,
    light_angle = 160,
    part_color=RebrickableColors.MediumBlue.value.best_hex,
    material = Material.PLASTIC,
    zoom=0.0000000000000000000000001,
    width=1080,
    height=1350,
)


variants = [
    ("21", RebrickableColors.TransLightBlue.value, Material.TRANSPARENT),
]

for i, variant in enumerate(variants):
    options = copy(default_options)
    options.image_filename = f"renders/docs-instagram-header.png"
    options.part_color = variant[1].best_hex
    options.material = variant[2]
    if i == 0:
        options.part_rotation = (0, 0, 270)
    renderer.render_part(variant[0], options)
