import bpy
import sys
import os

# This script runs under Blender's python environment. Add the current
# directly to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)

from lib.renderer.renderer import Renderer
from lib.renderer.render_options import RenderOptions, Quality, LightingStyle, Look
from lib.colors import Color

renderer = Renderer(ldraw_path="./ldraw")

options = RenderOptions(
    image_filename = "renders/test.png",
    blender_filename = "renders/test.blend",
    quality = Quality.DRAFT,
    lighting_style = LightingStyle.DEFAULT,
    part_color = Color.WHITE.value,
    part_rotation=(0, 0, 0),
    zoom=0.8,
    look=Look.INSTRUCTIONS,
    render_width=244,
    render_height=244,
)
renderer.render_part("3001", options)
