"""
Guard against mangled hex values in the color table (e.g. spreadsheet
number formatting turning '845E84' into '8.45E+86').
"""

import re

import pytest

from lego_rendering.colors import RebrickableColorsById

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}")


@pytest.mark.parametrize("color", RebrickableColorsById.values(), ids=lambda c: f"{c.id}-{c.name}")
def test_color_hex_is_valid(color):
    assert color.rebrickable_hex is not None
    assert HEX_RE.fullmatch(color.rebrickable_hex), f"rebrickable_hex {color.rebrickable_hex!r}"
    if color.bartneck_hex is not None:
        assert HEX_RE.fullmatch(color.bartneck_hex), f"bartneck_hex {color.bartneck_hex!r}"
    color.blender  # must not raise
