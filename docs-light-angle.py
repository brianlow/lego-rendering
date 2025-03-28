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

light_angles = [0, 60, 120, 180, 240]

for i, angle in enumerate(light_angles):
    renderer.render_part("3003", RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality=Quality.HIGH,
        light_angle = angle,
        part_color=RebrickableColors.MediumAzure.value.best_hex,
        zoom=0.99,
    ))

images = [Image.open(f"renders/docs{i}.png")
          for i, _ in enumerate(light_angles)]
image = grid(images, 1, 5)
image.save("docs/light_angles.png")
