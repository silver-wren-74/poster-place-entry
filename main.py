"""Solmara — a travel poster for a place that isn't there.

Entry for make.fun competition the-poster-for-a-place-that-i-2-20261121-0539.
Draws one vintage-style travel poster with PIL only (no network, no
external assets beyond the system DejaVu serif font) and writes it to
$MAKEFUN_OUTPUT_DIR/entry.png, or ./entry.png when that is unset.

The only text in the picture is the invented place name SOLMARA: no
quotes, no star ratings, no other copy, per the judge brief.
"""

import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 800, 1024
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

# Vintage poster palette.
INK = (13, 38, 58)          # deep navy, silhouettes
DUSK_TOP = (15, 76, 92)     # teal at the top of the sky
DUSK_MID = (231, 111, 81)   # coral band of the sunset
DUSK_LOW = (244, 190, 96)   # gold just above the horizon
PAPER = (250, 238, 210)     # cream for the frame and the name
WATER = (18, 82, 96)
WATER_HI = (52, 143, 152)
LAMP_RED = (198, 74, 60)
SAIL_SHADE = (214, 196, 160)

HORIZON = 640
SUN_X, SUN_Y = 520, 560


def blend(c1, c2, frac):
    """Linear blend between two RGB colours."""
    return tuple(round(c1[i] + (c2[i] - c1[i]) * frac) for i in range(3))


def sky(draw):
    """Three-stop sunset gradient, teal through coral to gold."""
    for row in range(HORIZON):
        f = row / HORIZON
        if f < 0.55:
            colour = blend(DUSK_TOP, DUSK_MID, f / 0.55)
        else:
            colour = blend(DUSK_MID, DUSK_LOW, (f - 0.55) / 0.45)
        draw.line([(0, row), (CANVAS_W, row)], fill=colour)


def sun(draw):
    """Low sun with a soft halo, right of centre above the horizon."""
    for radius, alpha in ((200, 26), (160, 38), (125, 55)):
        draw.ellipse(
            [SUN_X - radius, SUN_Y - radius, SUN_X + radius, SUN_Y + radius],
            fill=PAPER + (alpha,),
        )
    draw.ellipse(
        [SUN_X - 86, SUN_Y - 86, SUN_X + 86, SUN_Y + 86], fill=PAPER
    )


def gulls(draw):
    """Four gulls as paired arcs, high in the sky."""
    for gx, gy, size in ((150, 210, 22), (210, 260, 16),
                         (640, 180, 18), (690, 240, 14)):
        left = [gx - size, gy - size // 2, gx, gy + size // 2]
        right = [gx, gy - size // 2, gx + size, gy + size // 2]
        draw.arc(left, 200, 340, fill=PAPER, width=3)
        draw.arc(right, 200, 340, fill=PAPER, width=3)


def sea(draw):
    """The bay below the horizon: flat water, gold sun-path, pale waves."""
    draw.rectangle([0, HORIZON, CANVAS_W, CANVAS_H], fill=WATER)
    for step in range(9):
        y = HORIZON + 26 + step * 22
        half = 150 - step * 12
        draw.line([(SUN_X - half, y), (SUN_X + half, y)],
                  fill=DUSK_LOW + (170 - step * 16,), width=5)
    for i, y in enumerate(range(HORIZON + 70, CANVAS_H - 60, 34)):
        span = 26 + (i % 3) * 10
        x0 = 60 + (i * 137) % 480
        draw.line([(x0, y), (x0 + span * 2, y)], fill=WATER_HI, width=4)
        draw.line([(x0 + 30, y + 12), (x0 + 30 + span, y + 12)],
                  fill=WATER_HI + (140,), width=3)


def headlands(draw):
    """Dark cliff on the left, headland carrying the lighthouse on the right."""
    draw.polygon([(0, HORIZON), (0, CANVAS_H), (150, CANVAS_H),
                  (120, 760), (60, 700)], fill=INK)
    draw.polygon([(CANVAS_W, HORIZON), (CANVAS_W, CANVAS_H),
                  (610, CANVAS_H), (650, 730), (700, 690)], fill=INK)

def lighthouse(draw):
    """The poster's landmark: a tapered, red-banded lighthouse."""
    cx = 660
    foot, crown = 700, 470
    # Tapered tower.
    draw.polygon([(cx - 34, foot), (cx + 34, foot),
                  (cx + 20, crown), (cx - 20, crown)], fill=PAPER)
    # Two red bands, following the taper.
    for band in (560, 620):
        draw.polygon([(cx - 30, band), (cx + 30, band),
                      (cx + 26, band + 26), (cx - 26, band + 26)],
                     fill=LAMP_RED)
    # Gallery, lamp room, roof.
    draw.rectangle([cx - 30, crown - 14, cx + 30, crown], fill=INK)
    draw.rectangle([cx - 14, crown - 44, cx + 14, crown - 14],
                   fill=DUSK_LOW)
    draw.polygon([(cx - 20, crown - 44), (cx + 20, crown - 44),
                  (cx, crown - 62)], fill=INK)
    # Beam sweeping left across the bay, plus the lamp glow.
    draw.polygon([(cx - 12, crown - 30), (260, 520), (260, 560)],
                 fill=DUSK_LOW + (70,))
    draw.ellipse([cx - 9, crown - 39, cx + 9, crown - 21], fill=PAPER)


def sailboat(draw):
    """A small two-sail boat on the water, left of centre."""
    bx, by = 250, 800
    draw.line([(bx, by - 78), (bx, by - 8)], fill=INK, width=3)
    draw.polygon([(bx, by - 70), (bx, by - 8),
                  (bx + 52, by - 8)], fill=PAPER)
    draw.polygon([(bx - 6, by - 58), (bx - 6, by - 8),
                  (bx - 44, by - 8)], fill=SAIL_SHADE)
    draw.polygon([(bx - 62, by - 6), (bx + 66, by - 6),
                  (bx + 48, by + 16), (bx - 44, by + 16)], fill=INK)


def frame_and_name(draw):
    """Cream double frame, then the place name letter-spaced at the top."""
    draw.rectangle([22, 22, CANVAS_W - 22, CANVAS_H - 22],
                   outline=PAPER, width=6)
    draw.rectangle([36, 36, CANVAS_W - 36, CANVAS_H - 36],
                   outline=PAPER + (120,), width=2)

    name = "SOLMARA"
    font = ImageFont.truetype(FONT_PATH, 96)
    gap = 26
    widths = [draw.textlength(ch, font=font) for ch in name]
    total = sum(widths) + gap * (len(name) - 1)
    x = (CANVAS_W - total) / 2
    y = 96
    for ch, wch in zip(name, widths):
        draw.text((x + 4, y + 5), ch, font=font, fill=(10, 30, 46))
        draw.text((x, y), ch, font=font, fill=PAPER)
        x += wch + gap


def build(path):
    """Compose the poster and save it as an optimised PNG."""
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), DUSK_TOP)
    draw = ImageDraw.Draw(img, "RGBA")
    sky(draw)
    sun(draw)
    gulls(draw)
    sea(draw)
    headlands(draw)
    lighthouse(draw)
    sailboat(draw)
    frame_and_name(draw)
    img.save(path, "PNG", optimize=True)
    return path


if __name__ == "__main__":
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    out_path = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    build(out_path)
    print("wrote", out_path, os.path.getsize(out_path), "bytes")
