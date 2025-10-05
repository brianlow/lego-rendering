import sys
import site
from PIL import Image

# Add user site-packages to path so we can import lego_rendering
sys.path.insert(0, site.getusersitepackages())

from lego_rendering.image_utils import grid
from lego_rendering import RebrickableColors, RenderOptions, Quality, Renderer

renderer = Renderer(ldraw_path="./ldraw")

zooms = [0.001, 0.5, 1, 1.5, 2.0]
for i, zoom in enumerate(zooms):
    renderer.render_part("2423", RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality=Quality.NORMAL,
        part_color=RebrickableColors.DarkGreen.value.best_hex,
        zoom=zoom,
        part_rotation=(0, 0, 0),
    ))

images = [Image.open(f"renders/docs{i}.png") for i, s in enumerate(zooms)]
image = grid(images, 1, 5)
image.save("docs/zooms.png")
