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

parts = [
    "3001", "3941", "3062b", "11212", "63868",
    "4070", "15068", "3665", "60484", "3648b"
]

for i, part in enumerate(parts):
    renderer.render_part(part, RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality = Quality.DRAFT, # clearer look without studs
        look = Look.INSTRUCTIONS,
        part_color = RebrickableColors.LightBluishGray.value.best_hex,
        zoom = 0.99,
    ))

images = [Image.open(f"renders/docs{i}.png") for i, _ in enumerate(parts)]
image = grid(images, 2, 5)
image.save("docs/instructions.png")
