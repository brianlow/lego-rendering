import bpy
import os
from math import radians
from lib.renderer.utils import place_object_on_ground, zoom_camera, change_object_color, set_height_by_angle, aim_towards_origin
from lib.renderer.lighting import setup_lighting

# Render Lego parts
# This class is responsible for rendering a single image
# for a single part. It abstracts Blender and LDraw models
class Renderer:
    def __init__(self, ldraw_path = "./ldraw"):
        self.ldraw_path = ldraw_path
        self.ldraw_parts_path = os.path.join(ldraw_path, "parts")
        self.ldraw_unofficial_parts_path = os.path.join(ldraw_path, "unofficial", "parts")
        self.current_ldraw_part_id = None

    def render_part(self, ldraw_part_id, options):
        if ldraw_part_id != self.current_ldraw_part_id:
            self.import_part(ldraw_part_id, options)

        part = bpy.data.objects[0]
        camera = bpy.data.objects['Camera']

        # Do this after import b/c the importer overwrites some of these settings
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.samples = options.render_samples
        bpy.context.scene.cycles.max_bounces = 2
        bpy.context.scene.render.resolution_x = options.render_width
        bpy.context.scene.render.resolution_y = options.render_height
        bpy.context.scene.render.film_transparent = options.transparent_background
        bpy.context.scene.view_settings.view_transform = 'Standard'
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0 # turn off ambient lighting

        rotation = options.part_rotation_radian
        rotation = (rotation[0], rotation[1], rotation[2] + radians(90)) # parts feel in a natural orientation with 90 degree z rotation
        part.rotation_euler = rotation
        place_object_on_ground(part)
        change_object_color(part, options.part_color, options)

        setup_lighting(options)

        # The importer does not handle instructions look properly
        # If we skip the line that errors, we still need to re-enable these:
        # https://github.com/TobyLobster/ImportLDraw/issues/76
        if options.instructions:
            for layer in bpy.context.scene.view_layers:
                for collection in layer.layer_collection.children:
                    collection.exclude = False

        # Aim and position the camera so the part is centered in the frame.
        # The importer can do this for us but we rotate and move the part
        # after importing so would need to do it again anyways.
        part.select_set(True)
        camera.data.type = 'PERSP' # I prefer perspective even for instructions
        camera.data.lens = 120 # Long focal length so perspective is minor
        set_height_by_angle(camera, options.camera_height)
        aim_towards_origin(camera)
        bpy.ops.view3d.camera_to_view_selected()
        zoom_camera(camera, options.zoom)


        # Render
        bpy.context.scene.render.filepath = options.image_filename
        bpy.ops.render.render(write_still=True)

        # Save a Blender file so we can debug this script
        if options.blender_filename:
            bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(options.blender_filename))

    def import_part(self, ldraw_part_id, options):
        self.clear_scene()

        part_filename = os.path.abspath(os.path.join(self.ldraw_parts_path, f"{ldraw_part_id}.dat"))
        if not os.path.exists(part_filename):
            part_filename = os.path.abspath(os.path.join(self.ldraw_unofficial_parts_path, f"{ldraw_part_id}.dat"))
            if not os.path.exists(part_filename):
                raise FileNotFoundError(f"Part file not found: {part_filename}")

        # Import the part into the scene
        # https://github.com/TobyLobster/ImportLDraw/blob/09dd286d294672c816d33e70ac10146beb69693c/importldraw.py
        bpy.ops.import_scene.importldraw(filepath=part_filename, **{
            "ldrawPath": os.path.abspath(self.ldraw_path),
            "addEnvironment": True,                  # add a white ground plane
            "resPrims": options.res_prisms,          # high resolution primitives
            "useLogoStuds": options.use_logo_studs,  # LEGO logo on studs
            "look": options.look.value,              # normal (realistic) or instructions (line art)
        })

        bpy.ops.object.select_all(action='DESELECT')

    def clear_scene(self):
        bpy.ops.object.select_all(action='DESELECT')

        # Select all objects in the current scene
        for obj in bpy.context.scene.objects:
            if obj.type not in {'CAMERA'}:
                obj.select_set(True)

        # Delete selected objects
        bpy.ops.object.delete()
