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
from utils import rotate_object_randomly, place_object_on_ground, rotate_object_around_scene_origin, get_2d_bounding_box, draw_bounding_box, bounding_box_to_dataset_format, move_camera_back, reset_scene, change_object_color, move_object_away_from_origin, default_lighting, soft_lighting, hard_lighting
from colors import Color

# Yolo Detection
# - write out in Yolo format with bounding boxes
# - render multiple images, multiple parts
# - transparent colors
# - ability to specify color (can use hue augmentation)
# - list of parts + color combinations

# Part to render
partnames = ["3001", "3004", "4274"]
# partnames = ["3001"]

# Set the number of images to generate
num_images_per_part = 1

# 10% of generated images will be used for validation, remaining for training
# Setting this to 0 when experimenting makes it easier to review the results
percent_val = 0.0

# True for quick draft renders (1s per image on M1 Mac), False for high quality renders (10s per image on M1 Mac)
draft = True

randomize = True

# Input output paths
ldraw_path = "./ldraw"
ldraw_parts_path = "./ldraw/parts"
renders_path = "./renders"
dataset_yaml_path = "./renders/dataset.yaml"
dataset_path = "./renders/dataset"
train_path = "./renders/dataset/train"
val_path = "./renders/dataset/val"

os.makedirs(train_path, exist_ok=True)
os.makedirs(os.path.join(train_path, "images"), exist_ok=True)
os.makedirs(os.path.join(train_path, "labels"), exist_ok=True)
os.makedirs(val_path, exist_ok=True)
os.makedirs(os.path.join(val_path, "images"), exist_ok=True)
os.makedirs(os.path.join(val_path, "labels"), exist_ok=True)

# Render at the resolution needed by YOLO (i.e. standard Imagenet size)
render_width = 224
render_height = 224


for partname in partnames:
    bpy.ops.object.select_all(action='DESELECT')

    # Select all objects in the current scene
    for obj in bpy.context.scene.objects:
        if obj.type not in {'LIGHT', 'CAMERA'}:
            obj.select_set(True)

    # Delete selected objects
    bpy.ops.object.delete()


    # Import the part into Blender
    # Options for importing the part
    # https://github.com/TobyLobster/ImportLDraw/blob/09dd286d294672c816d33e70ac10146beb69693c/importldraw.py
    part_filename = os.path.abspath(os.path.join(ldraw_parts_path, f"{partname}.dat"))
    options = {
        "ldrawPath": os.path.abspath(ldraw_path),
        "addEnvironment": True,                       # add a white ground plane
        "resPrims": "Standard" if draft else "High",  # high resolution primitives
        "useLogoStuds": False if draft else True,     # LEGO logo on studs
    }
    if not os.path.exists(part_filename):
        print(f"Part file not found: {part_filename}")
        sys.exit()
    bpy.ops.import_scene.importldraw(filepath=part_filename, **options)
    bpy.ops.object.select_all(action='DESELECT')

    part = bpy.data.objects[0]
    light = bpy.data.objects['Light']
    camera = bpy.data.objects['Camera']

    # Do this after import b/c the importer overwrites some of these settings
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 16 if draft else 256 # increase for higher quality
    bpy.context.scene.cycles.max_bounces = 2
    bpy.context.scene.render.resolution_x = render_width
    bpy.context.scene.render.resolution_y = render_height

    for i in range(num_images_per_part):
        output_path = val_path if random.random() <= percent_val else train_path
        image_filename = os.path.join(output_path, "images", partname + "_{}.png".format(i))
        label_filename = os.path.join(output_path, "labels", partname + "_{}.txt".format(i))

        # Randomly rotate the part
        if randomize:
            rotate_object_randomly(part)
            place_object_on_ground(part)
            change_object_color(part, random.choice(list(Color)).value)

        # Move the light so each image has a random shadow
        # The importer creates a light for us at roughly 45 angle above the part so
        # we rotate it around the part (at the origin)
        if randomize:
            rotate_object_around_scene_origin(light, random.uniform(0, 360))
            lighting = [default_lighting, soft_lighting, hard_lighting]
            random.choice(lighting)(light)
        else:
            rotate_object_around_scene_origin(light, 20)
            default_lighting(light)

        # Aim and position the camera so the part is centered in the frame.
        # The importer can do this for us but we rotate and move the part
        # after importing so would need to do it again anyways.
        part.select_set(True)
        bpy.ops.view3d.camera_to_view_selected()
        move_camera_back(camera, .4)

        # Render
        bpy.context.scene.render.filepath = image_filename
        bpy.ops.render.render(write_still=True)

        # Save label and bounding box
        bounding_box = get_2d_bounding_box(part, camera)
        bounding_box = bounding_box_to_dataset_format(bounding_box, render_width, render_height)
        with open(label_filename, 'w') as f:
            f.write(f"0 {bounding_box[0]:.3f} {bounding_box[1]:.3f} {bounding_box[2]:.3f} {bounding_box[3]:.3f}\n")


# Save a Blender file so we can debug this script
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(os.path.join(renders_path, "render.blend")))

# Output a dataset yaml file
with open(dataset_yaml_path, 'w') as f:
  f.write(f"# Path must be an absolute path unless it is Ultralytics standard location\n")
  f.write(f"path: {os.path.abspath(dataset_path)}\n")
  f.write(f"train: train/images\n")
  f.write(f"val: val/images\n")
  f.write(f"\n")
  f.write(f"names:\n")
  f.write(f"  0: lego\n")
