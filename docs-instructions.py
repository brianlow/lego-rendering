import sys
import site
from PIL import Image

# Add user site-packages to path so we can import lego_rendering
sys.path.insert(0, site.getusersitepackages())

from lego_rendering.image_utils import grid
from lego_rendering import RebrickableColors, RenderOptions, Quality, Look, Renderer

renderer = Renderer(ldraw_path="./ldraw")

parts = [
    "3001", "3941", "3062b", "11212", "63868",
    "4070", "15068", "3665", "60484", "3648b"
]

for i, part in enumerate(parts):
    renderer.render_part(part, RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality = Quality.NORMAL,
        look = Look.INSTRUCTIONS,
        part_color = RebrickableColors.LightGray.value.best_hex,
        zoom = 0.99,
    ))

images = [Image.open(f"renders/docs{i}.png") for i, _ in enumerate(parts)]
image = grid(images, 2, 5)
image.save("docs/instructions.png")
