import sys
import site
from PIL import Image

# Add user site-packages to path so we can import lego_rendering
sys.path.insert(0, site.getusersitepackages())

from lego_rendering.image_utils import grid
from lego_rendering import RebrickableColors, RenderOptions, Quality, Renderer

renderer = Renderer(ldraw_path="./ldraw")

fills = [0.25, 0.5, 0.75, 1.0, 1.25]
for i, fill in enumerate(fills):
    renderer.render_part("2423", RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality=Quality.NORMAL,
        part_color=RebrickableColors.DarkGreen.value.best_hex,
        fill=fill,
        part_rotation=(0, 0, 0),
    ))

images = [Image.open(f"renders/docs{i}.png") for i, s in enumerate(fills)]
image = grid(images, 1, 5)
image.save("docs/fill.png")
