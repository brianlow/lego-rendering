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

heights = [10, 30, 50, 70, 85]

for i, height in enumerate(heights):
    renderer.render_part("32184", RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality=Quality.HIGH,
        part_color=RebrickableColors.LightBluishGray.value.best_hex,
        camera_height=height,
        zoom=0.99,
        part_rotation=(0, 0, 0),
    ))

images = [Image.open(f"renders/docs{i}.png") for i, s in enumerate(heights)]
image = grid(images, 1, 5)
image.save("docs/camera-heights.png")
