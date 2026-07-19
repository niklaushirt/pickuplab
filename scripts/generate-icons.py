#!/usr/bin/env python3
"""Rebuild the ИH Custom Winds raster favicons and iPhone home-screen icon."""

from math import pi, sin
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent.parent
SCALE = 4
BG = "#080c09"
PANEL = "#151e17"
PRIMARY = "#9ecb2e"
ACCENT = "#d5fe42"
TRACE = "#b7ef38"


def scaled(value):
    return int(round(value * SCALE))


def render(size):
    image = Image.new("RGB", (size * SCALE, size * SCALE), BG)
    draw = ImageDraw.Draw(image)
    factor = size / 180

    def p(value):
        return scaled(value * factor)

    draw.rounded_rectangle(
        (p(36), p(14), p(144), p(166)),
        radius=p(40),
        fill=PANEL,
        outline=PRIMARY,
        width=max(1, p(7)),
    )
    for y in (47, 133):
        for x in (64, 90, 116):
            r = p(9)
            draw.ellipse((p(x) - r, p(y) - r, p(x) + r, p(y) + r), fill=ACCENT)
    for baseline in (72, 90, 108):
        points = []
        for step in range(97):
            x = 48 + step * 84 / 96
            y = baseline - sin(step / 96 * 2 * pi) * 10
            points.append((p(x), p(y)))
        draw.line(points, fill=TRACE, width=max(1, p(7)), joint="curve")
    return image.resize((size, size), Image.Resampling.LANCZOS)


def main():
    icon_32 = render(32)
    icon_32.save(ROOT / "favicon-32x32.png", optimize=True)
    render(180).save(ROOT / "apple-touch-icon.png", optimize=True)
    render(64).save(
        ROOT / "favicon.ico",
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
    )


if __name__ == "__main__":
    main()
