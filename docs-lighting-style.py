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

lighting_styles = [
    LightingStyle.DEFAULT, LightingStyle.BRIGHT, LightingStyle.HARD
]

for i, lighting_style in enumerate(lighting_styles):
    options = RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality=Quality.DRAFT, # an incorrect seam is rendered at higher quality, not sure why
        lighting_style = lighting_style,
        part_color=RebrickableColors.Green.value.best_hex,
        zoom=0.99,
        part_rotation=(-30, 0, 0),
    )
    renderer.render_part("30367", options)

images = [Image.open(f"renders/docs{i}.png")
          for i, _ in enumerate(lighting_styles)]
image = grid(images, 1, 5)
image.save("docs/lighting_styles.png")
