import bpy
from mathutils import Vector
from lib.renderer.render_options import LightingStyle

def apply_lighting_style(light, style):
    if style == LightingStyle.DEFAULT:
        default_lighting(light)
    elif style == LightingStyle.SOFT:
        soft_lighting(light)
    elif style == LightingStyle.HARD:
        hard_lighting(light)

def default_lighting(light):
    move_object_away_from_origin(light, 5)
    light.data.shadow_soft_size = 0.1
    light.data.energy = 1000
    bpy.data.scenes['Scene'].view_settings.exposure = 0
    bpy.data.scenes["Scene"].view_settings.look = 'None'


def soft_lighting(light):
    move_object_away_from_origin(light, 1)
    light.data.shadow_soft_size = 0.1
    light.data.energy = 1
    bpy.data.scenes['Scene'].view_settings.exposure = 0
    bpy.data.scenes["Scene"].view_settings.look = 'None'


def hard_lighting(light):
    move_object_away_from_origin(light, 1)
    light.data.shadow_soft_size = 0.001
    light.data.energy = 100
    bpy.data.scenes['Scene'].view_settings.exposure = -2
    bpy.data.scenes["Scene"].view_settings.look = 'High Contrast'

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
