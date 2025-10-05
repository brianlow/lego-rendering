import sys
import site

# Add user site-packages to path so we can import lego_rendering
# Alternatively, I think lego_rendering can be installed with sudo and --no-user to avoid this
sys.path.insert(0, site.getusersitepackages())
from lego_rendering import Renderer, RenderOptions, Quality, LightingStyle, Look, Material, RebrickableColors, BoundingBox

color = RebrickableColors.TransLightBlue.value
render_bbox = True

renderer = Renderer(ldraw_path="./ldraw")
options = RenderOptions(
    image_filename = "renders/test.png",
    bounding_box_filename = "renders/test.txt",
    blender_filename = "renders/test.blend",
    quality = Quality.NORMAL,
    lighting_style = LightingStyle.DEFAULT,
    part_color = color.best_hex,
    material = Material.TRANSPARENT if color.is_transparent else Material.PLASTIC,
    light_angle = 160,
    part_rotation=(0, 0, 0),
    camera_height=84,
    zoom=.99,
    look=Look.NORMAL,
    width=244,
    height=244,
)

renderer.render_part("3005", options)

# Draw bounding box on the rendered image
if render_bbox and options.bounding_box_filename:
    BoundingBox.annotate(options.image_filename, options.bounding_box_filename)
