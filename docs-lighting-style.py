import sys
import site
from PIL import Image

# Add user site-packages to path so we can import lego_rendering
sys.path.insert(0, site.getusersitepackages())

from lego_rendering.image_utils import grid
from lego_rendering import RebrickableColors, RenderOptions, Quality, LightingStyle, Renderer

renderer = Renderer(ldraw_path="./ldraw")

lighting_styles = [
    LightingStyle.DEFAULT, LightingStyle.BRIGHT, LightingStyle.HARD
]

for i, lighting_style in enumerate(lighting_styles):
    options = RenderOptions(
        image_filename = f"renders/docs{i}.png",
        quality=Quality.DRAFT, # an incorrect seam is rendered at higher quality, not sure why
        lighting_style = lighting_style,
        part_color=RebrickableColors.Green.value.best_hex,
        zoom=0.99,
        part_rotation=(-30, 0, 0),
    )
    renderer.render_part("30367", options)

images = [Image.open(f"renders/docs{i}.png")
          for i, _ in enumerate(lighting_styles)]
image = grid(images, 1, 5)
image.save("docs/lighting_styles.png")
