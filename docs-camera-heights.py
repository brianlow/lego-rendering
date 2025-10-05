import sys
import site
from PIL import Image

# Add user site-packages to path so we can import lego_rendering
sys.path.insert(0, site.getusersitepackages())

from lego_rendering.image_utils import grid
from lego_rendering import RebrickableColors, RenderOptions, Quality, Renderer

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
