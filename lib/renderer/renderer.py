import bpy
import os
import tempfile
from math import radians
from lib.renderer.utils import place_object_on_ground, zoom_camera, set_height_by_angle, aim_towards_origin, get_2d_bounding_box, select_hierarchy
from lib.renderer.lighting import setup_lighting
from lib.renderer.render_options import Material
from lib.renderer.ldr_config import LdrConfig
from io_scene_importldraw.loadldraw.loadldraw import LegoColours, BlenderMaterials, Options

# Render Lego parts
# This class is responsible for rendering a single image
# for a single part. It abstracts Blender and LDraw models
class Renderer:
    def __init__(self, ldraw_path = "./ldraw"):
        self.ldraw_path = ldraw_path
        self.ldraw_parts_path = os.path.join(ldraw_path, "parts")
        self.ldraw_unofficial_parts_path = os.path.join(ldraw_path, "unofficial", "parts")
        self.has_imported_at_least_once = False
        self.ldr_config = LdrConfig(ldraw_path="./ldraw")
        self.ldr_config.open()

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
        bpy.context.scene.render.image_settings.file_format = 'JPEG'
        bpy.context.scene.render.image_settings.quality = 90
        bpy.context.scene.render.filepath = options.image_filename
        bpy.ops.render.render(write_still=True)

        # Save a Blender file so we can debug this script
        if options.blender_filename:
            bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(options.blender_filename))

        # Save the bounding box coordinates in YOLO format
        if options.bounding_box_filename:
            bounding_box = get_2d_bounding_box(part, camera).to_yolo(options.render_width, options.render_height)
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
        # Colors are tricky because:
        #   - the importer uses the LDraw color to determine color AND material (e.g. transparent)
        #   - a part may have multiple materials (slopes 3039) and colors (hinged attenna 73587p01)
        #   - I want to use my own colors that I've found to be more accurate for rendering
        # To do this we pick a LDraw color that matches the material we want
        # and then change the color in the LDraw config
        ldraw_color = 1
        if options.material == Material.TRANSPARENT:
            ldraw_color = 36
        if options.material == Material.RUBBER:
            ldraw_color = 256

        self.ldr_config.change_color(ldraw_color, options.part_color.replace("#", ""))
        self.ldr_config.save()

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
        bpy.ops.object.select_all(action='DESELECT')

        # Select all objects in the current scene
        for obj in bpy.context.scene.objects:
            if obj.type not in {'CAMERA'}:
                obj.select_set(True)

        # Delete selected objects
        bpy.ops.object.delete()

        # Delete materials because we reuse the same LDraw color
        # for all renders but change the LDRConfig to change the
        # rendered color
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)

        # Clear caches. For the same reason above (LDRConfig changes)
        if self.has_imported_at_least_once:
            LegoColours.reload()
            BlenderMaterials.clearCache()
