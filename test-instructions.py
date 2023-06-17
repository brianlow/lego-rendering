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
    light_angle = 210,
    part_color = (1, 1, 1, 1),
    part_rotation=(0, 0, 0),
    zoom=0.6,
    look=Look.INSTRUCTIONS,
    width=244,
    height=244,
)
renderer.render_part("3001", options)
