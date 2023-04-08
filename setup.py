import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.preferences.addon_install(filepath="/Users/brian/Downloads/importldraw1.1.15_for_blender_281.zip")
bpy.ops.preferences.addon_enable(module="io_scene_importldraw")
