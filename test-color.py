import bpy
import sys
import os
import glob
from PIL import Image, ImageDraw, ImageFont

# This script runs under Blender's python environment. Add the current
# directly to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"Prepending {dir_path} to Python path...")
sys.path.insert(0, dir_path)

from lib.image_utils import grid, get_default_font
from lib.renderer.renderer import Renderer
from lib.renderer.render_options import RenderOptions, Quality, LightingStyle, Look
from lib.colors import RebrickableColors, RebrickableColorsById


renderer = Renderer(ldraw_path="./ldraw")

color_ids = [
    0,
    1,
    2,
    3,
    4,
    5,
    10,
    14,
    15,
    19,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    41,
    46,
    47,
    70,
    71,
    72,
    73,
    84,
    85,
    158,
    182,
    191,
    212,
    226,
    272,
    288,
    308,
    320,
    321,
    322,
    323,
    326,
    378,
    484,
    1050,
]

for color_id in color_ids:
    color = RebrickableColorsById[color_id]

    options = RenderOptions(
        image_filename = f"renders/color-{color.id}.png",
        blender_filename = None,
        quality = Quality.DRAFT,
        lighting_style = LightingStyle.DEFAULT,
        light_angle = 0,
        # part_color = (1.000, .223, 0, 1),  # Pantone orange
        part_color = color.blender,
        part_rotation=(0, 0, 0),
        camera_height=70,
        zoom=0.99,
        look=Look.NORMAL,
        width=244,
        height=244,
    )
    renderer.render_part("3001", options)
    options.image_filename = f"renders/color-{color.id}-bartneck.png"
    if color.bartneck_blender is None:
        options.part_color = (1, 1, 1, 1)
    else:
        options.part_color = color.bartneck_blender
    renderer.render_part("3001", options)

    image = Image.new('RGBA', (244, 244), (255, 255, 255, 255))
    d = ImageDraw.Draw(image)
    font = ImageFont.truetype(get_default_font(), 16)
    text = f"{color.id} - {color.name}"
    position = (50, 50)
    d.text(position, text, fill="black", font=font)
    image.save(f'renders/color-{color.id}-legend.png')


Image.new('RGBA', (1, 1)).save("renders/blank.png")

images = []

for color_id in color_ids:
    color = RebrickableColorsById[color_id]
    print(f"Color ID: {color_id}")
    balanced = glob.glob(os.path.join(f'../lego-color/data/lego-color-common-dataset/train/{color.id}/', '*balance*'))
    shade = glob.glob(os.path.join(f'../lego-color/data/lego-color-common-dataset/train/{color.id}/', '*shade*'))
    samples = balanced[:2] + shade[:2]
    for _ in range(4 - len(samples)):
        samples.append("renders/blank.png")

    images.append(Image.open(f"renders/color-{color.id}-legend.png"))
    images.append(Image.open(f"renders/color-{color.id}.png"))
    images.append(Image.open(f"renders/color-{color.id}-bartneck.png"))
    images.append(Image.open(samples[0]))
    images.append(Image.open(samples[1]))
    images.append(Image.open(samples[2]))
    images.append(Image.open(samples[3]))

grid(images, len(color_ids), 7).save(f"renders/colors-all.png")
