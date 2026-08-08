# tests/test_core.py
from pathlib import Path

import pytest
from doku.core import blur_image, make_fuzzy
from PIL import Image, ImageChops


@pytest.fixture
def edged_image() -> Image.Image:
    """100x100 split red/blue — one hard edge for the blur to soften."""
    img = Image.new("RGB", (100, 100), "red")
    img.paste((0, 0, 255), (50, 0, 100, 100))  # blue right half
    return img


def _total_difference(a: Image.Image, b: Image.Image) -> int:
    """Sum of per-pixel differences across all channels."""
    diff = ImageChops.difference(a, b)
    return sum(diff.tobytes())


def test_blur_changes_pixels(edged_image: Image.Image) -> None:
    blurred = blur_image(edged_image, radius=2.0)
    diff = ImageChops.difference(edged_image, blurred)
    assert diff.getbbox() is not None  # None would mean nothing changed


def test_blur_preserves_size_and_mode(edged_image: Image.Image) -> None:
    blurred = blur_image(edged_image, radius=2.0)
    assert blurred.size == edged_image.size
    assert blurred.mode == edged_image.mode


def test_larger_radius_blurs_more(edged_image: Image.Image) -> None:
    light = blur_image(edged_image, radius=1.0)
    heavy = blur_image(edged_image, radius=8.0)
    assert _total_difference(edged_image, heavy) > _total_difference(edged_image, light)


def test_make_fuzzy_writes_output(tmp_path: Path, edged_image: Image.Image) -> None:
    source = tmp_path / "banana.png"
    edged_image.save(source)

    make_fuzzy(str(source))

    output = tmp_path / "fuzzy_banana.png"
    assert output.exists()
    with Image.open(output) as result:
        assert result.size == edged_image.size
