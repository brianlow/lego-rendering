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
    material = Material.PLASTIC,
    zoom=0.99,
    part_rotation=(0, 0, 0),
)

colors = [
    RebrickableColors.BrightLightYellow.value,
    RebrickableColors.Yellow.value,
    RebrickableColors.BrightLightOrange.value,

    RebrickableColors.BrightGreen.value,
    RebrickableColors.Green.value,
    RebrickableColors.DarkGreen.value,

    RebrickableColors.MediumAzure.value,
    RebrickableColors.DarkAzure.value,
    RebrickableColors.Blue.value,

    RebrickableColors.Lavender.value,
    RebrickableColors.MediumLavender.value,
    RebrickableColors.DarkPurple.value,

    RebrickableColors.BrightPink.value,
    RebrickableColors.DarkPink.value,
    RebrickableColors.Magenta.value,

    RebrickableColors.Coral.value,
    RebrickableColors.Red.value,
    RebrickableColors.DarkRed.value,
]

transposed_colors = [colors[(i%6)*3 + i//6] for i, color in enumerate(colors)]

for i, color in enumerate(transposed_colors):
    options = copy(default_options)
    options.image_filename = f"renders/docs{i}.png"
    options.part_color = color.best_hex
    options.material = Material.TRANSPARENT if color.is_transparent else Material.PLASTIC
    renderer.render_part("3004", options)

images = [Image.open(f"renders/docs{i}.png") for i, _ in enumerate(colors)]
image = grid(images, 3, 6)
image.save("docs/colors.png")
