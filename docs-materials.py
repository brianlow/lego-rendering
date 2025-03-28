import sys
import os
import random
from PIL import Image
from copy import copy

# This script runs under Blender's python environment. Add the current
# directly to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)

from lib.image_utils import grid
from lib.colors import RebrickableColors
from lib.renderer.render_options import RenderOptions, Quality, LightingStyle, Look, Material
from lib.renderer.renderer import Renderer

renderer = Renderer(ldraw_path="./ldraw")

default_options = RenderOptions(
    image_filename="renders/test.png",
    quality=Quality.HIGH,
    lighting_style=LightingStyle.DEFAULT,
    light_angle = 160,
    part_color=RebrickableColors.MediumBlue.value.best_hex,
    material = Material.PLASTIC,
    zoom=0.99,
)

variants = [
    ("6126b", RebrickableColors.TransYellow.value, Material.TRANSPARENT),
    ("6141", RebrickableColors.TransOrange.value, Material.TRANSPARENT),
    ("21", RebrickableColors.TransLightBlue.value, Material.TRANSPARENT),
    ("3004", RebrickableColors.TransClear.value, Material.TRANSPARENT),
    ("30391", RebrickableColors.Black.value, Material.RUBBER),
]

for i, variant in enumerate(variants):
    options = copy(default_options)
    options.image_filename = f"renders/docs{i}.png"
    options.part_color = variant[1].best_hex
    options.material = variant[2]
    if i == 0:
        options.part_rotation = (0, 0, 270)
    renderer.render_part(variant[0], options)

images = [Image.open(f"renders/docs{i}.png") for i, _ in enumerate(variants)]
image = grid(images, 1, 5)
image.save("docs/materials.png")
