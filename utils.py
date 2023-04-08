import os
import bpy
import random
import bpy_extras.object_utils
from math import radians
from mathutils import Vector, Matrix

def rotate_object_randomly(obj, min_angle=-360, max_angle=360):
    random_x = radians(random.uniform(min_angle, max_angle))
    random_y = radians(random.uniform(min_angle, max_angle))
    random_z = radians(random.uniform(min_angle, max_angle))
    obj.rotation_euler = (random_x, random_y, random_z)

def place_object_on_ground(obj):
    # Update the object's bounding box data
    bpy.context.view_layer.update()

    # Find the lowest point of the object's bounding box
    world_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    lowest_z = min(corner.z for corner in world_corners)

    # Move the object up so that its lowest point is on the ground plane (Z=0)
    obj.location.z -= lowest_z

def rotate_object_around_scene_origin(obj, angle_degrees):
    # Convert the angle from degrees to radians
    angle_radians = radians(angle_degrees)

    # Create the rotation matrix around the Z-axis
    rotation_matrix = Matrix.Rotation(angle_radians, 4, 'Z')

    # Apply the rotation matrix to the object's matrix_world
    obj.matrix_world = rotation_matrix @ obj.matrix_world

def project_3d_to_2d(camera, point):
    scene = bpy.context.scene
    render = scene.render
    width, height = render.resolution_x, render.resolution_y

    co_2d = bpy_extras.object_utils.world_to_camera_view(scene, camera, point)
    return Vector((co_2d.x * width, co_2d.y * height))

def get_2d_bounding_box(obj, camera):
    bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

    # Project each corner of the bounding box to 2D screen coordinates
    screen_coords = [project_3d_to_2d(camera, corner) for corner in bbox]

    # Calculate the 2D bounding box
    min_x = min(coord.x for coord in screen_coords)
    max_x = max(coord.x for coord in screen_coords)
    min_y = min(coord.y for coord in screen_coords)
    max_y = max(coord.y for coord in screen_coords)

    return [(min_x, min_y), (max_x, max_y)]

# Converts from
#   [(min_x, min_y), (max_x, max_y)] in pixels
# to
#   [center_x, center_y, width, height] normalized to 0.0-1.0
#
def bounding_box_to_dataset_format(bounding_box, width, height):
  [(min_x, min_y), (max_x, max_y)] = bounding_box
  box_width = max_x - min_x
  box_height = max_y - min_y
  center_x = min_x + (box_width / 2)
  center_y = min_y + (box_height / 2)
  return [center_x/width, center_y/width, box_width/width, box_height/height]

def draw_bounding_box(bounding_box, input_filename):
    from PIL import Image, ImageDraw
    image = Image.open(input_filename)
    draw = ImageDraw.Draw(image)
    draw.rectangle(bounding_box, outline=(0, 255, 0), width=2)
    base, ext = os.path.splitext(input_filename)
    image.save(base + "_bounding" + ext)

def move_camera_back(camera, percentage):
    # Get the camera's forward vector (negative local Z-axis)
    forward_vector = camera.matrix_world.to_3x3() @ Vector((0, 0, 1))
    # forward_vector = -forward_vector  # Negate the vector

    # Scale the forward vector by the specified percentage
    scaled_vector = forward_vector * percentage

    # Move the camera along the scaled vector
    camera.location += scaled_vector
