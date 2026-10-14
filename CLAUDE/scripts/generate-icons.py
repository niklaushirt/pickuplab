#!/usr/bin/env python3
"""Reproducibly rebuild the raster icons (favicon-32x32.png, favicon.ico, apple-touch-icon.png).

Draws the same graphical single-coil pickup artwork as favicon.svg (no text) with Pillow.
Usage:  python3 scripts/generate-icons.py      (run from anywhere; writes next to index.html)
Requires: Pillow (pip install pillow). Not needed at runtime.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
BG = (8, 12, 9, 255)
LIME = (213, 254, 66)
ACID = (183, 239, 56)
PANEL = (16, 23, 18)
INK = (237, 244, 238)
SS = 8  # supersampling factor


def pickup(size: int, opaque_square: bool = False) -> Image.Image:
    S = size * SS
    u = S / 64.0
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if opaque_square:
        d.rectangle([0, 0, S, S], fill=BG)
    else:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=14 * u, fill=BG)
    # blurred glow
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([13 * u, 6 * u, 51 * u, 58 * u], fill=LIME + (70,))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(5 * u)))
    d = ImageDraw.Draw(img)
    # mounting ears + body
    d.ellipse([26 * u, 5.5 * u, 38 * u, 14 * u], fill=ACID + (60,), outline=LIME, width=max(1, int(2 * u)))
    d.ellipse([26 * u, 50 * u, 38 * u, 58.5 * u], fill=ACID + (60,), outline=LIME, width=max(1, int(2 * u)))
    d.rounded_rectangle([15 * u, 10 * u, 49 * u, 54 * u], radius=5.5 * u, fill=(60, 80, 30, 255), outline=LIME, width=max(1, int(2 * u)))
    d.rounded_rectangle([21 * u, 16 * u, 43 * u, 48 * u], radius=5 * u, fill=PANEL + (200,), outline=ACID + (150,), width=max(1, int(1 * u)))
    for cy in (19.5, 24.5, 29.5, 34.5, 39.5, 44.5):
        d.ellipse([(32 - 2.4) * u, (cy - 2.4) * u, (32 + 2.4) * u, (cy + 2.4) * u], fill=LIME)
    for cy in (9.6, 54.4):
        d.ellipse([(32 - 1.5) * u, (cy - 1.5) * u, (32 + 1.5) * u, (cy + 1.5) * u], fill=INK + (160,))
    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    pickup(32).save(ROOT / "favicon-32x32.png")
    apple = pickup(180, opaque_square=True).convert("RGB")  # opaque for the iPhone home screen
    apple.save(ROOT / "apple-touch-icon.png")
    pickup(64).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("icons written to", ROOT)


if __name__ == "__main__":
    main()
