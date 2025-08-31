import bpy

bpy.ops.wm.read_factory_settings(use_empty=True)

bpy.ops.preferences.addon_install(filepath="/Users/brianlow/dev/ImportLDraw/ImportLDraw-v1.2.3.zip") # fixed bevel, should see if in next release
# bpy.ops.preferences.addon_install(filepath="/Users/brianlow/Downloads/importldraw1.2.1.zip") # bad
# bpy.ops.preferences.addon_install(filepath="/Users/brianlow/Downloads/importldraw1.2.0.zip") # bad
# bpy.ops.preferences.addon_install(filepath="/Users/brianlow/Downloads/importldraw1.1.18_for_blender_281.zip") # boost - bad
# bpy.ops.preferences.addon_install(filepath="/Users/brianlow/Downloads/importldraw1.1.17_for_blender_281.zip") # art - good
# bpy.ops.preferences.addon_install(filepath="/Users/brianlow/dev/tmp/17.0.655d998.zip")
# bpy.ops.preferences.addon_install(filepath="/Users/brianlow/dev/tmp/17.1.2813383.zip")
# bpy.ops.preferences.addon_install(filepath="/Users/brianlow/dev/tmp/17.2.4bf8756.zip")
# bpy.ops.preferences.addon_install(filepath="/Users/brianlow/dev/tmp/17.2.4bf8756.zip")

bpy.ops.preferences.addon_enable(module="io_scene_importldraw")
bpy.ops.wm.save_userpref()
