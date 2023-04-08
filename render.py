import bpy
import os
import math
import sys
import random
from math import radians
from mathutils import Vector, Matrix


# Add current directory to the path so we can import our own modules
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from utils import rotate_object_randomly, place_object_on_ground, rotate_object_around_scene_origin, get_2d_bounding_box, draw_bounding_box


# Yolo Detection
# - write out in Yolo format with bounding boxes
# - render multiple images, multiple parts
# - transparent colors
# - ability to specify color (can use hue augmentation)
# - list of parts + color combinations

# Part to render
partnames = "3001", "3004", "3022",
partname = "4274"

# Input output paths
ldraw_path = "./ldraw"
ldraw_parts_path = "./ldraw/parts"
output_path = "./renders"

# Render at the resolution needed by YOLO (i.e. standard Imagenet size)
render_width = 224
render_height = 224

# Set the number of images to generate
num_images_per_part = 3

# Loop through each LDraw file in the directory
# for filename in os.listdir(ldraw_path):
#    if filename.endswith(".ldr"):
        # Import the LDraw file

# Options for importing the part
# https://github.com/TobyLobster/ImportLDraw/blob/09dd286d294672c816d33e70ac10146beb69693c/importldraw.py
options = {
    "ldrawPath": os.path.abspath(ldraw_path),
    "addEnvironment": True,   # add a white ground plane
    "resPrims": "High",       # high resolution primitives
    "useLogoStuds": True,     # LEGO logo on studs
}

part_filename = os.path.abspath(os.path.join(ldraw_parts_path, f"{partname}.dat"))
if not os.path.exists(part_filename):
    print(f"Part file not found: {part_filename}")
    sys.exit()

bpy.ops.import_scene.importldraw(filepath=part_filename, **options)

part = bpy.data.objects[0]
light = bpy.data.objects['Light']
camera = bpy.data.objects['Camera']

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 16 # increase for higher quality
bpy.context.scene.cycles.max_bounces = 2
bpy.context.scene.render.resolution_x = render_width
bpy.context.scene.render.resolution_y = render_height

bpy.ops.object.select_all(action='DESELECT')


for i in range(num_images_per_part):
    # Randomly rotate the part
    rotate_object_randomly(part)
    place_object_on_ground(part)

    # The importer creates a light for us at roughly 45 angle above the part
    # Rotate the light in a circle around the part so renders have somewhat random shadows
    rotate_object_around_scene_origin(light, random.uniform(0, 360))

    # Aim and position the camera so the part is centered in the frame.
    # The importer can do this for us but we rotate and move the part
    # after importing so would need to do it again anyways.
    part.select_set(True)
    bpy.ops.view3d.camera_to_view_selected()

    output_filename = os.path.join(output_path, partname + "_{}.png".format(i))
    bpy.context.scene.render.filepath = output_filename
    bpy.ops.render.render(write_still=True)

    bounding_box = get_2d_bounding_box(part, camera)

# Save a Blender file so we can debug this script
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(os.path.join(output_path, "render.blend")))
