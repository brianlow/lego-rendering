import bpy
import addon_utils

addon_name = "io_scene_importldraw"

# Disable the add-on
print(f"Attempting to disable add-on: {addon_name}")
bpy.ops.preferences.addon_disable(module=addon_name)
print(f"Successfully disabled add-on: {addon_name}")

# Uninstall the add-on
# Note: Uninstalling might require Blender restart to fully take effect,
# but this command removes it from the current session's perspective and attempts removal.
print(f"Attempting to uninstall add-on: {addon_name}")
bpy.ops.preferences.addon_remove(module=addon_name)
print(f"Successfully initiated uninstall for add-on: {addon_name}")
# Verify (optional, might not reflect immediately if restart is needed)
installed_addons = [mod.__name__ for mod in addon_utils.modules()]
if addon_name not in installed_addons:
    print(f"Add-on {addon_name} confirmed as uninstalled from current session.")
else:
    print(f"WARNING: Add-on {addon_name} still listed. A Blender restart might be required to complete uninstallation.")


# Save preferences to make the changes persistent
bpy.ops.wm.save_userpref()
print("Saved user preferences.")

print("Script finished.")
