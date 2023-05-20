import sys
import os
import random
from PIL import Image
from copy import copy

# This script runs under Blender's python environment. Add the current
# directly to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)

from lib.image_utils import grid
from lib.colors import Color
from lib.renderer.render_options import RenderOptions, Quality, LightingStyle, Look
from lib.renderer.renderer import Renderer

renderer = Renderer(ldraw_path="./ldraw")

default_options = RenderOptions(
    image_filename="renders/test.png",
    blender_filename="renders/test.blend",
    quality=Quality.NORMAL,
    lighting_style=LightingStyle.DEFAULT,
    part_color=Color.BLUE.value,
    zoom=0.6,
    part_rotation=(0, 0, 0),
)

parts = [
    "3001", "3941", "3062b", "11212", "63868",
    "4070", "15068", "3665", "60484", "3648b"
]
for i, part in enumerate(parts):
    options = copy(default_options)
    options.image_filename = f"renders/docs{i}.png"
    renderer.render_part(part, options)

images = [Image.open(f"renders/docs{i}.png") for i, _ in enumerate(parts)]
image = grid(images, 2, 5)
image.save("docs/parts.png")

colors = [
    Color.BRIGHT_LIGHT_ORANGE, Color.YELLOW, Color.ORANGE, Color.DARK_ORANGE, Color.RED,
    Color.BRIGHT_PINK, Color.DARK_PINK, Color.MAGENTA, Color.LAVENDER, Color.MEDIUM_LAVENDER,
]
for i, color in enumerate(colors):
    options = copy(default_options)
    options.image_filename = f"renders/docs{i}.png"
    options.part_color = color.value
    renderer.render_part("3001", options)

images = [Image.open(f"renders/docs{i}.png") for i, _ in enumerate(colors)]
image = grid(images, 2, 5)
image.save("docs/colors.png")

lighting_styles = [
    LightingStyle.DEFAULT, LightingStyle.HARD
]
for i, lighting_style in enumerate(lighting_styles):
    options = copy(default_options)
    options.image_filename = f"renders/docs{i}.png"
    options.lighting_style = lighting_style
    renderer.render_part("3001", options)

images = [Image.open(f"renders/docs{i}.png")
          for i, _ in enumerate(lighting_styles)]
image = grid(images, 1, 3)
image.save("docs/lighting_styles.png")

light_angles = [0, 60, 120, 180, 240]
for i, angle in enumerate(light_angles):
    options = copy(default_options)
    options.image_filename = f"renders/docs{i}.png"
    options.light_angle = angle
    renderer.render_part("3001", options)

images = [Image.open(f"renders/docs{i}.png")
          for i, _ in enumerate(light_angles)]
image = grid(images, 1, 5)
image.save("docs/light_angles.png")

part_rotations = [(random.uniform(0, 360), random.uniform(
    0, 360), random.uniform(0, 360)) for _ in range(5)]
for i, rotation in enumerate(part_rotations):
    options = copy(default_options)
    options.image_filename = f"renders/docs{i}.png"
    options.part_rotation = rotation
    renderer.render_part("3001", options)

images = [Image.open(f"renders/docs{i}.png")
          for i, _ in enumerate(part_rotations)]
image = grid(images, 1, 5)
image.save("docs/part_rotations.png")

zooms = [0.01, 0.5, 1, 1.5, 2.0]
for i, zoom in enumerate(zooms):
    options = copy(default_options)
    options.image_filename = f"renders/docs{i}.png"
    options.zoom = zoom
    renderer.render_part("3001", options)

images = [Image.open(f"renders/docs{i}.png") for i, s in enumerate(zooms)]
image = grid(images, 1, 5)
image.save("docs/zooms.png")

for i, part in enumerate(parts):
    options = copy(default_options)
    options.image_filename = f"renders/docs{i}.png"
    options.part_color = Color.WHITE.value
    options.look = Look.INSTRUCTIONS
    options.quality = Quality.DRAFT # cleaner without LEGO on studs
    renderer.render_part(part, options)

images = [Image.open(f"renders/docs{i}.png") for i, _ in enumerate(parts)]
image = grid(images, 2, 5)
image.save("docs/instructions.png")
