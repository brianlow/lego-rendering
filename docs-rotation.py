import sys
import site
import random
from PIL import Image
from copy import copy

# Add user site-packages to path so we can import lego_rendering
sys.path.insert(0, site.getusersitepackages())

from lego_rendering.image_utils import grid
from lego_rendering import RebrickableColors, RenderOptions, Quality, LightingStyle, Material, Renderer

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
