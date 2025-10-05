import sys
from unittest.mock import MagicMock

# Mock Blender modules before any imports
def mock_blender_modules():
    """Mock bpy and mathutils modules so tests can run without Blender"""

    # Mock bpy
    bpy = MagicMock()
    bpy.data = MagicMock()
    bpy.context = MagicMock()
    bpy.ops = MagicMock()
    sys.modules['bpy'] = bpy

    # Mock mathutils
    mathutils = MagicMock()
    mathutils.Vector = MagicMock
    mathutils.Matrix = MagicMock
    sys.modules['mathutils'] = mathutils

    # Mock the ImportLDraw addon module
    io_scene_importldraw = MagicMock()
    sys.modules['io_scene_importldraw'] = io_scene_importldraw
    sys.modules['io_scene_importldraw.loadldraw'] = MagicMock()
    sys.modules['io_scene_importldraw.loadldraw.loadldraw'] = MagicMock()

# Call before pytest collects tests
mock_blender_modules()
