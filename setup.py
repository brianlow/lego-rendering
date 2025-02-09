import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.preferences.addon_install(filepath="/Users/brianlow/dev/lego-rendering/importldraw1.2.0.zip")
bpy.ops.preferences.addon_enable(module="io_scene_importldraw")
