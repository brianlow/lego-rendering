import bpy
import math
from mathutils import Vector

from lib.renderer.render_options import LightingStyle
from lib.renderer.utils import rotate_around_z_origin, aim_towards_origin, set_height_by_angle


def setup_lighting(options):
    if options.lighting_style == LightingStyle.DEFAULT:
        default_lighting(options)
    if options.lighting_style == LightingStyle.BRIGHT:
        bright_lighting(options)
    elif options.lighting_style == LightingStyle.HARD:
        hard_lighting(options)

def default_lighting(options):
    light_data = bpy.data.lights.new(name="KeyLight", type='AREA')
    light_data.energy = 300
    light_data.shape = 'SQUARE'
    light_data.size = 5
    light_data.color = (1, 1, 1)
    light = bpy.data.objects.new(name="KeyLight", object_data=light_data)
    bpy.context.collection.objects.link(light)
    light.location = (0.1, 0, 0)
    move_object_away_from_origin(light, 4.5)
    rotate_around_z_origin(light, options.light_angle)
    set_height_by_angle(light, 60)
    aim_towards_origin(light)
    return light

def bright_lighting(options):
    light = default_lighting(options)
    light.data.energy = 550

def hard_lighting(options):
    light_data = bpy.data.lights.new(name="KeyLight", type='AREA')
    light_data.energy = 500
    light_data.shape = 'SQUARE'
    light_data.size = 1
    light_data.color = (1, 1, 1)
    light = bpy.data.objects.new(name="KeyLight", object_data=light_data)
    bpy.context.collection.objects.link(light)
    light.location = (0.1, 0, 0)
    move_object_away_from_origin(light, 6)
    rotate_around_z_origin(light, options.light_angle)
    set_height_by_angle(light, 75)
    aim_towards_origin(light)
    return light


def move_object_away_from_origin(obj, distance):
    location = obj.location

    # Calculate the vector from the origin to the objects's location
    origin = Vector((0, 0, 0))
    vector_to_object = location - origin

    # Normalize the vector and multiply it by the desired distance
    vector_to_object.normalize()
    vector_to_object *= distance

    # Calculate the new location for the object
    new_location = origin + vector_to_object

    # Set the objects's location to the new location
    obj.location = new_location
