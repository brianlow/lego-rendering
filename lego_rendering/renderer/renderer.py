import copy
import bpy
import os
import tempfile
from PIL import Image
from math import radians
from lego_rendering.renderer.utils import place_object_on_ground, zoom_camera, set_height_by_angle, aim_towards_origin, get_2d_bounding_box, select_hierarchy
from lego_rendering.renderer.lighting import setup_lighting
from lego_rendering.renderer.render_options import Material
from io_scene_importldraw.loadldraw.loadldraw import LegoColours, BlenderMaterials

# Render Lego parts
# This class is responsible for rendering a single image
# for a single part. It abstracts Blender and LDraw models
class Renderer:
    def __init__(self, ldraw_path = "./ldraw"):
        self.ldraw_path = ldraw_path
        self.ldraw_parts_path = os.path.join(ldraw_path, "parts")
        self.ldraw_unofficial_parts_path = os.path.join(ldraw_path, "unofficial", "parts")
        self.has_imported_at_least_once = False
        # self.ldr_config = LdrConfig(ldraw_path="./ldraw")
        # self.ldr_config.open()

    def render_part(self, ldraw_part_id, options):
        self.import_part(ldraw_part_id, options)

        part = bpy.data.objects[0].children[0]
        camera = bpy.data.objects['Camera']

        # Do this after import b/c the importer overwrites some of these settings
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.samples = options.render_samples
        bpy.context.scene.cycles.max_bounces = 15 if options.material == Material.TRANSPARENT else 2
        bpy.context.scene.render.resolution_x = options.render_width
        bpy.context.scene.render.resolution_y = options.render_height
        bpy.context.scene.render.film_transparent = options.transparent_background
        bpy.context.scene.view_settings.view_transform = 'Standard'
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0 # turn off ambient lighting

        rotation = options.part_rotation_radian
        rotation = (rotation[0]+ radians(270), rotation[1], rotation[2] + radians(90)) # parts feel in a natural orientation with 90 degree z rotation
        part.rotation_euler = rotation
        place_object_on_ground(part)

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
        select_hierarchy(part)
        camera.data.type = 'PERSP' # I prefer perspective even for instructions
        camera.data.lens = 120 # Long focal length so perspective is minor
        set_height_by_angle(camera, options.camera_height)
        aim_towards_origin(camera)
        bpy.ops.view3d.camera_to_view_selected()
        zoom_camera(camera, options.zoom)


        # Render
        bpy.context.scene.render.image_settings.file_format = options.format.value
        bpy.context.scene.render.image_settings.quality = 90 # for jpeg
        bpy.context.scene.render.filepath = options.image_filename
        bpy.ops.render.render(write_still=True)

        # Did we render a larger size, if so resize
        if options.width != options.render_width:
            image = Image.open(options.image_filename)
            image.thumbnail((options.width, options.height), Image.LANCZOS)
            image.save(options.image_filename)

        # Save a Blender file so we can debug this script
        if options.blender_filename:
            bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(options.blender_filename))

        # Save the bounding box coordinates in YOLO format
        if options.bounding_box_filename:
            bounding_box = get_2d_bounding_box(part, camera).to_yolo(options.width, options.height)
            with open(options.bounding_box_filename, 'w') as f:
                f.write(f"0 {bounding_box[0]:.3f} {bounding_box[1]:.3f} {bounding_box[2]:.3f} {bounding_box[3]:.3f}\n")

    def import_part(self, ldraw_part_id, options):
        self.clear_scene()

        part_filename = os.path.abspath(os.path.join(self.ldraw_parts_path, f"{ldraw_part_id}.dat"))
        if not os.path.exists(part_filename):
            part_filename = os.path.abspath(os.path.join(self.ldraw_unofficial_parts_path, f"{ldraw_part_id}.dat"))
            if not os.path.exists(part_filename):
                raise FileNotFoundError(f"Part file not found: {part_filename}")


        # Set the part color
        #
        # We want to use our own colors that seem to be more realistic. The importer plugin doesn't
        # support out of the box so we access some internals to create/modify a color reserved for us.
        #
        # Colors are tricky because:
        #   - the importer uses the LDraw color to determine color and material (e.g. transparent)
        #   - a part may have multiple materials (slopes 3039) and colors (hinged attenna 73587p01)
        #   - colors are re-read from LDConfig.ldr each time the importer is invoked
        ldraw_color = 99999
        linearRGBA = LegoColours.hexDigitsToLinearRGBA(options.part_color.replace('#', ''), 1.0)
        LegoColours.colours[99999] = {
            "name": "lego-rendering-placeholder-color",
            "colour": linearRGBA[0:3],
            "alpha": 0.5 if options.material == Material.TRANSPARENT else 1,
            "luminance": 0.0,
            "material": "RUBBER" if options.material == Material.RUBBER else "BASIC",
        }

        name = ""
        with tempfile.NamedTemporaryFile(suffix=".ldr", mode='w+', delete=False) as temp:
            temp.write("0 Untitled Model\n")
            temp.write("0 Name:  UntitledModel\n")
            temp.write("0 Author:\n")
            temp.write("0 CustomBrick\n")
            temp.write(f"1 {ldraw_color} 30.000000 -24.000000 -20.000000 1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000 {ldraw_part_id}.dat\n")

            name = temp.name

        with open(name, 'r') as file:
            data = file.read()
            print("-----")
            print(data)
            print("-----")

        # Import the part into the scene
        # https://github.com/TobyLobster/ImportLDraw/blob/09dd286d294672c816d33e70ac10146beb69693c/importldraw.py
        bpy.ops.import_scene.importldraw(filepath=name, **{
            "ldrawPath": os.path.abspath(self.ldraw_path),
            "addEnvironment": True,                  # add a white ground plane
            "resPrims": options.res_prisms,          # high resolution primitives
            "useLogoStuds": options.use_logo_studs,  # LEGO logo on studs
            "look": options.look.value,              # normal (realistic) or instructions (line art)
            "colourScheme": "ldraw",
        })

        bpy.ops.object.select_all(action='DESELECT')
        os.remove(name)
        self.has_imported_at_least_once = True

    def clear_scene(self):
        # Clear all objects except cameras, lights, and other essentials
        # Use Blender's batch removal for comprehensive clearing
        bpy.ops.object.select_all(action='DESELECT')

        # Select only objects we want to delete (not cameras, lights)
        for obj in bpy.context.scene.objects:
            if obj.type not in {'CAMERA'}:
                obj.select_set(True)

        bpy.ops.object.delete(use_global=False)

        # Clear all unused data blocks (materials, meshes, etc.)
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

        # Clear caches. For the same reason above (LDRConfig changes)
        if self.has_imported_at_least_once:
            LegoColours()
            BlenderMaterials.clearCache()
