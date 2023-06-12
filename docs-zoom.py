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

zooms = [0.001, 0.5, 1, 1.5, 2.0]
for i, zoom in enumerate(zooms):
    renderer.render_part("2423", RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality=Quality.NORMAL,
        part_color=RebrickableColors.DarkGreen.value.best_hex,
        zoom=zoom,
        part_rotation=(0, 0, 0),
    ))

images = [Image.open(f"renders/docs{i}.png") for i, s in enumerate(zooms)]
image = grid(images, 1, 5)
image.save("docs/zooms.png")
