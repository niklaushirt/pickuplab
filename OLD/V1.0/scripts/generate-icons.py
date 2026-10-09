#!/usr/bin/env python3
"""Generate Pickup Lab favicon and Apple touch-icon raster assets."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def gradient(size: int) -> Image.Image:
    start = (242, 140, 40)
    end = (255, 122, 61)
    image = Image.new("RGB", (size, size))
    pixels = image.load()
    for y in range(size):
        for x in range(size):
            mix = (x + y) / (2 * (size - 1))
            pixels[x, y] = tuple(round(a + (b - a) * mix) for a, b in zip(start, end))
    return image


def draw_mark(image: Image.Image) -> None:
    size = image.width
    scale = size / 512
    original = image.copy()
    draw = ImageDraw.Draw(image)
    ink = (33, 17, 0, 255) if image.mode == "RGBA" else (33, 17, 0)

    def box(values: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return tuple(round(value * scale) for value in values)

    # Geometric PL monogram matching the page's tight, heavy wordmark.
    draw.rounded_rectangle(box((84, 134, 298, 326)), radius=round(50 * scale), fill=ink)
    draw.rectangle(box((84, 230, 154, 378)), fill=ink)
    counter = Image.new("L", (size, size), 0)
    ImageDraw.Draw(counter).rounded_rectangle(box((154, 194, 232, 266)), radius=round(18 * scale), fill=255)
    image.paste(original, (0, 0), counter)
    draw.rectangle(box((320, 134, 390, 378)), fill=ink)
    draw.rectangle(box((320, 312, 464, 378)), fill=ink)


def make_icon(size: int, rounded: bool) -> Image.Image:
    base = gradient(size)
    border = ImageDraw.Draw(base)
    border.rounded_rectangle(
        (round(size * 10 / 512),) * 2 + (round(size * 502 / 512),) * 2,
        radius=round(size * 102 / 512),
        outline=(255, 189, 114),
        width=max(1, round(size * 12 / 512)),
    )
    draw_mark(base)
    if not rounded:
        return base

    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=round(size * 112 / 512), fill=255)
    result.paste(base, (0, 0), mask)
    return result


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)

    favicon = make_icon(512, rounded=True)
    favicon.resize((32, 32), Image.Resampling.LANCZOS).save(ASSETS / "favicon-32x32.png", optimize=True)
    favicon.save(
        ASSETS / "favicon.ico",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )

    touch_icon = make_icon(180, rounded=False)
    touch_icon.save(ASSETS / "apple-touch-icon.png", optimize=True)


if __name__ == "__main__":
    main()
