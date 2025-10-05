"""
Smoke tests to verify package imports work correctly.
These tests mock bpy and mathutils so they can run without Blender.
"""

import pytest


def test_import_main_package():
    """Test that the main package can be imported"""
    import lego_rendering
    assert lego_rendering is not None


def test_import_all_exports():
    """Test that all exported classes can be imported from root"""
    from lego_rendering import (
        Renderer,
        RenderOptions,
        Format,
        Quality,
        LightingStyle,
        Look,
        Material,
        LdrConfig,
        RebrickableColor,
        RebrickableColors,
        RebrickableMaterial,
        RebrickableMaterials,
        BoundingBox,
    )

    # Verify they're not None
    assert Renderer is not None
    assert RenderOptions is not None
    assert Format is not None
    assert Quality is not None
    assert LightingStyle is not None
    assert Look is not None
    assert Material is not None
    assert LdrConfig is not None
    assert RebrickableColor is not None
    assert RebrickableColors is not None
    assert RebrickableMaterial is not None
    assert RebrickableMaterials is not None
    assert BoundingBox is not None


def test_import_renderer_submodule():
    """Test that renderer submodule imports work"""
    from lego_rendering.renderer import renderer, render_options, lighting, utils

    assert renderer is not None
    assert render_options is not None
    assert lighting is not None
    assert utils is not None


def test_render_options_instantiation():
    """Test that RenderOptions can be instantiated"""
    from lego_rendering import RenderOptions, Quality, Material, Look, LightingStyle, Format

    options = RenderOptions(
        image_filename="test.png",
        width=224,
        height=224,
        quality=Quality.NORMAL,
        material=Material.PLASTIC,
        look=Look.NORMAL,
        lighting_style=LightingStyle.DEFAULT,
        format=Format.PNG,
    )

    assert options.width == 224
    assert options.height == 224
    assert options.quality == Quality.NORMAL
    assert options.material == Material.PLASTIC


def test_rebrickable_colors_enum():
    """Test that RebrickableColors enum has expected values"""
    from lego_rendering import RebrickableColors

    # Check that it's an enum with some expected colors
    assert hasattr(RebrickableColors, 'TransLightBlue')
    color = RebrickableColors.TransLightBlue.value
    assert color is not None
    assert hasattr(color, 'best_hex')


def test_no_lib_imports_in_source():
    """Test that no source files still have 'from lib.' imports"""
    import os
    import glob

    source_files = glob.glob('lego_rendering/**/*.py', recursive=True)

    for file_path in source_files:
        with open(file_path, 'r') as f:
            content = f.read()
            assert 'from lib.' not in content, f"File {file_path} still has 'from lib.' import"
            assert 'import lib.' not in content, f"File {file_path} still has 'import lib.' statement"
