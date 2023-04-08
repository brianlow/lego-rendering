import bpy
import os
import math
import sys
import random
from math import radians
from mathutils import Vector, Matrix


# TODO
# - ability to specify color
# - transparent colors
# - list of parts + color combinations

# Input output paths
ldraw_path = "./parts"
output_path = "./renders"

# Set the resolution of the rendered images
# Higher quality by rendering larger image and downsizing
render_width = 224
render_height = 224

# Set the number of images to generate
num_images = 1

def rotate_object_randomly(obj, min_angle=-360, max_angle=360):
    random_x = radians(random.uniform(min_angle, max_angle))
    random_y = radians(random.uniform(min_angle, max_angle))
    random_z = radians(random.uniform(min_angle, max_angle))
    obj.rotation_euler = (random_x, random_y, random_z)


# Loop through each LDraw file in the directory
# for filename in os.listdir(ldraw_path):
#    if filename.endswith(".ldr"):
        # Import the LDraw file

# https://github.com/TobyLobster/ImportLDraw/blob/09dd286d294672c816d33e70ac10146beb69693c/importldraw.py
options = {
    "ldrawPath": "/Users/brian/Downloads/ldraw",
    "addEnvironment": True,
     "resPrims": "High",
    "useLogoStuds": True,
}

filename = "3001.dat"

bpy.ops.import_scene.importldraw(filepath=f"/Users/brian/Downloads/ldraw/parts/{filename}", **options)

obj = bpy.data.objects[0]
# rotate_object_randomly(obj)

def rotate_object_around_scene_origin(obj, angle_degrees):
    # Convert the angle from degrees to radians
    angle_radians = radians(angle_degrees)

    # Create the rotation matrix around the Z-axis
    rotation_matrix = Matrix.Rotation(angle_radians, 4, 'Z')

    # Apply the rotation matrix to the object's matrix_world
    obj.matrix_world = rotation_matrix @ obj.matrix_world


def place_object_on_ground(obj):
    # Update the object's bounding box data
    bpy.context.view_layer.update()

    # Find the lowest point of the object's bounding box
    world_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    lowest_z = min(corner.z for corner in world_corners)

    # Move the object up so that its lowest point is on the ground plane (Z=0)
    obj.location.z -= lowest_z

place_object_on_ground(obj)


light = bpy.data.objects['Light']
# light.data.type = 'AREA'
# light.data.size = 1100
# light.data.energy = .001
rotate_object_around_scene_origin(light, random.uniform(0, 360))

# Set the camera position and rotation
camera = bpy.data.objects['Camera']
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.ops.view3d.camera_to_view_selected()



# quick render
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 16 # increase for higher quality
bpy.context.scene.cycles.max_bounces = 2
bpy.context.scene.render.resolution_x = render_width
bpy.context.scene.render.resolution_y = render_height

i = 0
bpy.context.scene.render.filepath = os.path.join(output_path, filename[:-4] + "_{}.png".format(i))
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath("renders/render.blend"))
