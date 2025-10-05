#!/bin/bash

set -e

IMPORTLDRAW_ZIP="$(pwd)/importldraw1.2.3.zip"
BLENDER_DIR="/Applications/Blender.app"
BLENDER_RESOURCES_DIR="${BLENDER_DIR}/Contents/Resources"
BLENDER_EXECUTABLE="${BLENDER_DIR}/Contents/MacOS/Blender"

# Find the Blender version directory (e.g., 3.6, 4.0)
BLENDER_VERSION=$(find "$BLENDER_RESOURCES_DIR" -maxdepth 1 -type d -name '[0-9]*.[0-9]*' -print -quit | xargs basename)
if [ -z "$BLENDER_VERSION" ]; then
  echo "Error: Could not find Blender version directory in $BLENDER_RESOURCES_DIR"
  exit 1
fi
echo "Detected Blender version: $BLENDER_VERSION"

PYTHON_BIN_DIR="${BLENDER_RESOURCES_DIR}/${BLENDER_VERSION}/python/bin"

# Find the python executable (handles variations like python3.10, python3.11 etc.)
# Use -perm +111 for macOS compatibility instead of -executable
PYTHON_EXECUTABLE=$(find "$PYTHON_BIN_DIR" -maxdepth 1 -name 'python*' -type f -perm +111 | head -n 1)
if [ -z "$PYTHON_EXECUTABLE" ]; then
  echo "Error: Could not find Python executable in $PYTHON_BIN_DIR"
  exit 1
fi
echo "Detected python: $PYTHON_EXECUTABLE"


echo "Install the ImportLDraw plugin"
X="import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.preferences.addon_install(filepath='${IMPORTLDRAW_ZIP}')
bpy.ops.preferences.addon_enable(module='io_scene_importldraw')
bpy.ops.wm.save_userpref()
"
"$BLENDER_EXECUTABLE" --background --python-expr "${X}"

# Run pip install using Blender's Python environment
echo "Install lego-rendering in the Blender Python environment"
"$BLENDER_EXECUTABLE" --background --python "$(pwd)/install-package.py"
