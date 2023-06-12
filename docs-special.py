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

variants = [
    ("3040", RebrickableColors.Red, (0, 0, -90)),
    ("73587p01", RebrickableColors.Blue, (0, 0, 0)),
    ("7049b", RebrickableColors.LightBluishGray, (0, 0, 0)),
    ("98138p0b", RebrickableColors.White, (0, 0, 180)),
    ("3039p23", RebrickableColors.Blue, (0, 0, -90)),
]

for i, variant in enumerate(variants):

    renderer.render_part(variant[0], RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality = Quality.NORMAL,
        part_color=variant[1].value.best_hex,
        part_rotation=variant[2],
        zoom = 0.6,
    ))

images = [Image.open(f"renders/docs{i}.png") for i, _ in enumerate(variants)]
image = grid(images, 2, 5)
image.save("docs/special.png")
