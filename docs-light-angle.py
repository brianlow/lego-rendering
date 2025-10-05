import sys
import site
from PIL import Image

# Add user site-packages to path so we can import lego_rendering
sys.path.insert(0, site.getusersitepackages())

from lego_rendering.image_utils import grid
from lego_rendering import RebrickableColors, RenderOptions, Quality, Renderer

renderer = Renderer(ldraw_path="./ldraw")

light_angles = [0, 60, 120, 180, 240]

for i, angle in enumerate(light_angles):
    renderer.render_part("3003", RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality=Quality.HIGH,
        light_angle = angle,
        part_color=RebrickableColors.MediumAzure.value.best_hex,
        zoom=0.99,
    ))

images = [Image.open(f"renders/docs{i}.png")
          for i, _ in enumerate(light_angles)]
image = grid(images, 1, 5)
image.save("docs/light_angles.png")
