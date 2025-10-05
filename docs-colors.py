import sys
import site
import random
from PIL import Image
from copy import copy

# Add user site-packages to path so we can import lego_rendering
sys.path.insert(0, site.getusersitepackages())

from lego_rendering.image_utils import grid
from lego_rendering import RebrickableColors, RenderOptions, Quality, LightingStyle, Look, Material, Renderer

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
