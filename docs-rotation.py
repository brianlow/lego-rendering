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
    quality=Quality.NORMAL,
    lighting_style=LightingStyle.DEFAULT,
    part_color=RebrickableColors.MediumLavender.value.best_hex,
    material = Material.PLASTIC,
    zoom=0.99,
    part_rotation=(0, 0, 0),
)

part_rotations = [(random.uniform(0, 360), random.uniform(
    0, 360), random.uniform(0, 360)) for _ in range(5)]

for i, rotation in enumerate(part_rotations):
    options = copy(default_options)
    options.image_filename = f"renders/docs{i}.png"
    options.part_rotation = rotation
    renderer.render_part("4070", options)

images = [Image.open(f"renders/docs{i}.png")
          for i, _ in enumerate(part_rotations)]
image = grid(images, 1, 5)
image.save("docs/part_rotations.png")
