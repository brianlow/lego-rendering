import sys
import site
from copy import copy

# Add user site-packages to path so we can import lego_rendering
sys.path.insert(0, site.getusersitepackages())

from lego_rendering import Renderer, RenderOptions, Quality, LightingStyle, Material, RebrickableColors


renderer = Renderer(ldraw_path="./ldraw")

default_options = RenderOptions(
    image_filename="renders/test.png",
    quality=Quality.HIGH,
    lighting_style=LightingStyle.DEFAULT,
    light_angle = 160,
    part_color=RebrickableColors.MediumBlue.value.best_hex,
    material = Material.PLASTIC,
    zoom=0.0000000000000000000000001,
    width=1080,
    height=1350,
)


variants = [
    ("21", RebrickableColors.TransLightBlue.value, Material.TRANSPARENT),
]

for i, variant in enumerate(variants):
    options = copy(default_options)
    options.image_filename = f"renders/docs-instagram-header.png"
    options.part_color = variant[1].best_hex
    options.material = variant[2]
    if i == 0:
        options.part_rotation = (0, 0, 270)
    renderer.render_part(variant[0], options)
