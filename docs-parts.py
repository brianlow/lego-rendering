import sys
import site
from PIL import Image

# Add user site-packages to path so we can import lego_rendering
sys.path.insert(0, site.getusersitepackages())

from lego_rendering.image_utils import grid
from lego_rendering import RebrickableColors, RenderOptions, Quality, Material, Renderer

renderer = Renderer(ldraw_path="./ldraw")

variants = [
    ("3002", RenderOptions(
        part_color = RebrickableColors.Red.value.best_hex,
        part_rotation = (-60, 180, 270),
    )),
    ("3626bp01", RenderOptions(
        part_color = RebrickableColors.Yellow.value.best_hex,
        part_rotation = (0, 0, -45),
        camera_height = 15,
        quality = Quality.DRAFT, # an incorrect seam is rendered at higher quality, not sure why
    )),
    ("11212", RenderOptions(
        part_color = RebrickableColors.Green.value.best_hex,
        part_rotation = (20, 0, 60),
        light_angle = 120,
    )),
    ("3062b", RenderOptions(
        part_color = RebrickableColors.TransOrange.value.best_hex,
        material = Material.TRANSPARENT,
        light_angle = 120,
        camera_height = 25,
    )),
    ("63868", RenderOptions(
        part_color = RebrickableColors.Black.value.best_hex,
        part_rotation = (20, 50, 190),
        light_angle = 220,
    )),
    ("4070", RenderOptions(
        part_color = RebrickableColors.Orange.value.best_hex,
        part_rotation = (-20, -20, -70),
    )),
    ("15068", RenderOptions(
        part_color = RebrickableColors.White.value.best_hex,
        part_rotation = (-10, 0, -90),
        light_angle=90,
    )),
    ("60484", RenderOptions(
        part_color = RebrickableColors.LightBluishGray.value.best_hex,
        part_rotation = (90, 0, -50),
        light_angle=-90,
        camera_height=25,
    )),
    ("3665", RenderOptions(
        part_color = RebrickableColors.DarkTurquoise.value.best_hex,
        part_rotation = (0, 0, -120),
        light_angle=90,
    )),
    ("3648b", RenderOptions(
        part_color = RebrickableColors.DarkBluishGray.value.best_hex,
        part_rotation = (90, 0, 0),
        light_angle=-90,
    )),
    ("73587p01", RenderOptions(
        part_color = RebrickableColors.Blue.value.best_hex,
        part_rotation = (0, 0, 0),
    )),
    ("7049b", RenderOptions(
        part_color = RebrickableColors.LightBluishGray.value.best_hex,
        part_rotation = (0, 0, 0),
    )),
    ("3040", RenderOptions(
        part_color = RebrickableColors.Red.value.best_hex,
        part_rotation = (0, 0, -90),
    )),
    ("98138p0b", RenderOptions(
        part_color = RebrickableColors.White.value.best_hex,
        part_rotation = (0, 0, 180),
    )),
    ("3039p23", RenderOptions(
        part_color = RebrickableColors.Blue.value.best_hex,
        part_rotation = (0, 0, -90),
    )),
]

for i, variant in enumerate(variants):
    options = variant[1]
    options.image_filename = f"renders/docs{i}.png"
    options.quality = options.quality or Quality.HIGH
    options.zoom = 0.99
    renderer.render_part(variant[0], options)

images = [Image.open(f"renders/docs{i}.png") for i, _ in enumerate(variants)]
image = grid(images, 3, 5)
image.save("docs/parts.png")
