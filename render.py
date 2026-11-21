#!/usr/bin/env python3
"""Render 'THE WORLD TODAY' — one-page newspaper front page summing up
Friday 20 November 2026. All artwork drawn in code with PIL; no photos,
no external images, no downloaded assets. Output: entry.png, 1024x1024,
<= 1 MiB."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (20, 20, 20)
RED = (155, 27, 27)
GREY = (90, 86, 76)
RULE = (60, 58, 50)

FDIR = "/usr/share/fonts/truetype/dejavu/"
LIB = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


F_MAST = font("DejaVuSerif-Bold.ttf", 64)
F_DATE = font("DejaVuSans-Bold.ttf", 26)
F_KICK = font("DejaVuSans-Bold.ttf", 18)
F_LEAD = font("DejaVuSerif-Bold.ttf", 40)
F_STAND = font("DejaVuSerif.ttf", 21)
F_CAP = ImageFont.truetype(LIB + "LiberationSerif-Italic.ttf", 16)
F_TAG = font("DejaVuSans-Bold.ttf", 14)
F_HEAD = font("DejaVuSerif-Bold.ttf", 20)
F_BODY = font("DejaVuSerif.ttf", 15)
F_FOOT = font("DejaVuSans.ttf", 13)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


MX = 28  # side margin

# ---------- masthead ----------
d.text((W // 2, 24), "THE WORLD TODAY", font=F_MAST, fill=INK, anchor="ma")
d.line([(MX, 100), (W - MX, 100)], fill=RULE, width=2)
d.line([(MX, 104), (W - MX, 104)], fill=RULE, width=1)

# ---------- date band ----------
d.rectangle([MX, 112, W - MX, 146], fill=RED)
d.text((W // 2, 129), "FRIDAY  \u00b7  20 NOVEMBER 2026",
       font=F_DATE, fill=(255, 255, 255), anchor="mm")

# ---------- lead kicker + headline ----------
d.text((MX, 158), "LEAD  \u2014  UKRAINE  /  POLAND  /  NATO", font=F_KICK, fill=RED)
d.text((MX, 180), "Russian missiles land in Poland", font=F_LEAD, fill=INK)
d.text((MX, 222), "as Kyiv endures huge attack", font=F_LEAD, fill=INK)

# ---------- lead illustration: night sky, missile trails, explosions ----------
IX, IY, IW, IH = MX, 276, 620, 200
# night sky gradient
for y in range(IH):
    t = y / IH
    r = int(18 + 30 * t)
    g = int(24 + 34 * t)
    b = int(52 + 44 * t)
    d.line([(IX, IY + y), (IX + IW, IY + y)], fill=(r, g, b))
# stars
for (sx, sy, sr) in ((60, 26, 2), (150, 14, 1), (240, 30, 2), (330, 12, 1),
                     (420, 34, 2), (500, 18, 1), (570, 40, 2), (90, 52, 1),
                     (290, 52, 1), (470, 58, 1), (200, 8, 1), (380, 8, 1)):
    d.ellipse([IX + sx - sr, IY + sy - sr, IX + sx + sr, IY + sy + sr],
              fill=(235, 235, 220))
# city skyline silhouette
skyline = [(0, 200), (0, 168), (34, 168), (34, 150), (58, 150), (58, 172),
           (96, 172), (96, 140), (112, 140), (112, 158), (150, 158),
           (150, 172), (196, 172), (196, 146), (214, 146), (214, 172),
           (260, 172), (260, 156), (300, 156), (300, 172), (360, 172),
           (360, 144), (380, 144), (380, 172), (430, 172), (430, 158),
           (470, 158), (470, 172), (520, 172), (520, 148), (540, 148),
           (540, 172), (580, 172), (580, 160), (620, 160), (620, 200)]
d.polygon([(IX + x, IY + y) for x, y in skyline], fill=(12, 14, 26))
# lit windows
for (wx, wy) in ((44, 178), (104, 150), (160, 180), (204, 156), (270, 164),
                 (368, 154), (440, 166), (480, 166), (528, 158), (596, 168),
                 (120, 180), (320, 180), (420, 180)):
    d.rectangle([IX + wx, IY + wy, IX + wx + 4, IY + wy + 5], fill=(255, 200, 90))
# missile trails arcing down from upper right
d.line([(IX + 610, IY + 6), (IX + 470, IY + 96)], fill=(255, 190, 90), width=3)
d.line([(IX + 590, IY + 2), (IX + 520, IY + 70)], fill=(255, 220, 140), width=2)
d.line([(IX + 610, IY + 6), (IX + 540, IY + 40)], fill=(255, 140, 60), width=2)
# explosion glows over the skyline
d.ellipse([IX + 440, IY + 74, IX + 500, IY + 124], fill=(255, 120, 30))
d.ellipse([IX + 452, IY + 84, IX + 488, IY + 114], fill=(255, 200, 80))
d.ellipse([IX + 496, IY + 46, IX + 542, IY + 84], fill=(255, 150, 50))
d.ellipse([IX + 506, IY + 54, IX + 532, IY + 76], fill=(255, 215, 110))
# smoke puffs
for (sx, sy, sr) in ((470, 66, 16), (452, 56, 11), (492, 60, 10),
                     (520, 38, 13), (536, 30, 9)):
    d.ellipse([IX + sx - sr, IY + sy - sr, IX + sx + sr, IY + sy + sr],
              fill=(70, 70, 80))
# frame + caption
d.rectangle([IX, IY, IX + IW, IY + IH], outline=RULE, width=2)
d.text((MX, 482), "Missiles streak over Kyiv on Friday; three Russian weapons also fell in Poland.",
       font=F_CAP, fill=GREY)

# ---------- lead standfirst ----------
SX = 668
stand = ("Two Russian missiles and a suspected drone came down in "
         "Poland during Moscow's biggest air attack on Ukraine "
         "\u2014 110 missiles, 400 drones, eight killed. Warsaw: a "
         "provocation. NATO: a grave violation.")
lines = wrap(stand, F_STAND, W - MX - SX)
y = 284
for ln in lines:
    d.text((SX, y), ln, font=F_STAND, fill=INK)
    y += 28

# ---------- divider ----------
d.line([(MX, 510), (W - MX, 510)], fill=RULE, width=2)

# ---------- small illustrations for the grid panels ----------
def ill_markets(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(238, 232, 216), outline=RULE)
    # falling red chart line over grey bars
    bars = [62, 58, 60, 52, 46, 48, 38, 30, 24]
    bw = s // 10
    for i, bh in enumerate(bars):
        d.rectangle([x + 6 + i * bw, y + s - 8 - bh, x + 6 + (i + 1) * bw - 2,
                     y + s - 8], fill=(150, 150, 145))
    pts = [(x + 8 + i * bw, y + s - 12 - bh) for i, bh in enumerate(bars)]
    d.line(pts, fill=(155, 27, 27), width=3)
    d.polygon([(x + s - 14, y + 8), (x + s - 4, y + 8), (x + s - 9, y + 20)],
              fill=(155, 27, 27))


def ill_flags_eu_uk(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(238, 232, 216), outline=RULE)
    # EU flag: blue field, circle of stars
    d.rectangle([x + 6, y + 12, x + s // 2 - 2, y + s - 12], fill=(0, 51, 153))
    import math
    cx, cy, r = x + s // 4 + 2, y + s // 2, 16
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        d.ellipse([cx + r * math.cos(a) - 2, cy + r * math.sin(a) - 2,
                   cx + r * math.cos(a) + 2, cy + r * math.sin(a) + 2],
                  fill=(255, 204, 0))
    # UK flag: simplified union jack
    ux0, uy0 = x + s // 2 + 2, y + 12
    ux1, uy1 = x + s - 6, y + s - 12
    d.rectangle([ux0, uy0, ux1, uy1], fill=(0, 36, 125))
    d.polygon([(ux0, uy0), (ux1, uy1), (ux1, uy0), (ux0, uy1)], fill=(255, 255, 255))
    d.line([(ux0, uy0), (ux1, uy1)], fill=(200, 16, 46), width=3)
    d.line([(ux1, uy0), (ux0, uy1)], fill=(200, 16, 46), width=3)
    d.line([(ux0, (uy0 + uy1) // 2), (ux1, (uy0 + uy1) // 2)], fill=(255, 255, 255), width=8)
    d.line([((ux0 + ux1) // 2, uy0), ((ux0 + ux1) // 2, uy1)], fill=(255, 255, 255), width=8)
    d.line([(ux0, (uy0 + uy1) // 2), (ux1, (uy0 + uy1) // 2)], fill=(200, 16, 46), width=4)
    d.line([((ux0 + ux1) // 2, uy0), ((ux0 + ux1) // 2, uy1)], fill=(200, 16, 46), width=4)


def ill_flags_three(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(238, 232, 216), outline=RULE)
    # three small flags: US, Russia, China
    fw, fh = 24, 16
    # US: stripes + blue canton
    fx, fy = x + 6, y + 12
    for i in range(5):
        d.rectangle([fx, fy + i * 3, fx + fw, fy + i * 3 + 3],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, fy, fx + 10, fy + 8], fill=(60, 59, 110))
    # Russia: white-blue-red tricolour
    fx = x + s // 2 - fw // 2
    for i, col in enumerate(((255, 255, 255), (0, 57, 166), (213, 0, 50))):
        d.rectangle([fx, fy + i * 6, fx + fw, fy + i * 6 + 6], fill=col)
    # China: red field, yellow stars
    fx = x + s - 6 - fw
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
    d.polygon([(fx + 5, fy + 3), (fx + 7, fy + 8), (fx + 3, fy + 5),
               (fx + 8, fy + 5), (fx + 4, fy + 8)], fill=(255, 222, 0))
    # table line + three podiums
    d.line([(x + 4, y + s - 18), (x + s - 4, y + s - 18)], fill=RULE, width=2)
    for px in (x + 10, x + s // 2 - 6, x + s - 22):
        d.rectangle([px, y + s - 30, px + 12, y + s - 18], fill=(90, 86, 76))


def ill_intercept(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(30, 38, 64), outline=RULE)
    # incoming missile streak
    d.line([(x + s - 8, y + 8), (x + s // 2, y + s // 2)], fill=(255, 190, 90), width=3)
    # intercept burst
    cx, cy = x + s // 2, y + s // 2
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 150, 40))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 220, 130))
    for (dx, dy) in ((-26, -8), (24, -16), (-20, 18), (26, 14), (0, -28), (4, 28)):
        d.line([(cx, cy), (cx + dx, cy + dy)], fill=(255, 200, 120), width=2)
    # ground line + towers
    d.line([(x, y + s - 12), (x + s, y + s - 12)], fill=(200, 200, 200), width=2)
    d.rectangle([x + 10, y + s - 34, x + 18, y + s - 12], fill=(120, 120, 130))
    d.rectangle([x + s - 20, y + s - 44, x + s - 12, y + s - 12], fill=(120, 120, 130))


def ill_cyclone(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(176, 208, 224), outline=RULE)
    # sea
    d.rectangle([x, y + s - 22, x + s, y + s], fill=(38, 90, 130))
    # spiral bands
    cx, cy = x + s // 2, y + s // 2 - 4
    for r, col in ((34, (255, 255, 255)), (26, (220, 235, 245)),
                   (18, (255, 255, 255)), (10, (150, 180, 200))):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=200 + 300,
              fill=col, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255))
    # rain streaks
    for rx in (x + 8, x + 22, x + s - 24, x + s - 10):
        d.line([(rx, y + 8), (rx - 4, y + 20)], fill=(90, 120, 150), width=2)


def ill_quake(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(226, 214, 190), outline=RULE)
    # cracked ground
    d.rectangle([x, y + s - 30, x + s, y + s], fill=(120, 92, 66))
    d.line([(x + 8, y + s - 30), (x + 26, y + s - 18), (x + 20, y + s - 6),
            (x + 44, y + s - 14), (x + 60, y + s - 2), (x + s - 8, y + s - 10)],
           fill=(60, 44, 28), width=3)
    # seismograph zigzag
    d.line([(x + 6, y + 26), (x + 16, y + 26), (x + 22, y + 14),
            (x + 28, y + 40), (x + 34, y + 20), (x + 40, y + 32),
            (x + 46, y + 10), (x + 52, y + 44), (x + 58, y + 22),
            (x + 64, y + 30), (x + 74, y + 26), (x + s - 6, y + 26)],
           fill=(155, 27, 27), width=3)
    # cracked building
    d.rectangle([x + s - 30, y + 34, x + s - 8, y + s - 30], fill=(90, 86, 76))
    d.line([(x + s - 30, y + 40), (x + s - 20, y + 50), (x + s - 24, y + 60)],
           fill=(40, 40, 40), width=2)


def ill_mercury(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(12, 12, 24), outline=RULE)
    # stars
    for (sx, sy) in ((8, 10), (20, 6), (70, 12), (76, 26), (10, 70)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(230, 230, 220))
    # cratered planet
    cx, cy, r = x + s // 2 - 4, y + s // 2 + 6, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 138, 122))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(90, 82, 70), width=2)
    for (ox, oy, orad) in ((-10, -6, 6), (8, 8, 8), (4, -12, 4), (-2, 12, 5)):
        d.ellipse([cx + ox - orad, cy + oy - orad, cx + ox + orad, cy + oy + orad],
                  fill=(120, 110, 96))
    # small spacecraft with solar panels
    sx, sy = x + s - 26, y + 14
    d.rectangle([sx - 8, sy - 3, sx - 2, sy + 3], fill=(40, 90, 160))
    d.rectangle([sx + 2, sy - 3, sx + 8, sy + 3], fill=(40, 90, 160))
    d.rectangle([sx - 2, sy - 4, sx + 2, sy + 4], fill=(220, 220, 220))
    d.line([(sx - 2, sy + 4), (sx - 8, sy + 12)], fill=(255, 200, 90), width=2)


def ill_fire(x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(40, 32, 28), outline=RULE)
    # hills + houses
    d.polygon([(x, y + s), (x, y + s - 26), (x + s // 2, y + s - 34),
               (x + s, y + s - 22), (x + s, y + s)], fill=(24, 40, 24))
    for hx in (x + 8, x + s // 2 - 6, x + s - 26):
        d.rectangle([hx, y + s - 44, hx + 18, y + s - 30], fill=(70, 60, 52))
        d.polygon([(hx - 2, y + s - 44), (hx + 9, y + s - 52), (hx + 20, y + s - 44)],
                  fill=(50, 42, 38))
    # flame
    fx, fy = x + s // 2, y + s // 2 - 8
    d.polygon([(fx - 16, fy + 22), (fx - 20, fy + 2), (fx - 8, fy - 14),
               (fx - 2, fy - 2), (fx + 6, fy - 20), (fx + 10, fy - 4),
               (fx + 18, fy + 6), (fx + 14, fy + 22)], fill=(230, 90, 20))
    d.polygon([(fx - 8, fy + 22), (fx - 10, fy + 8), (fx - 2, fy - 2),
               (fx + 4, fy + 6), (fx + 9, fy + 10), (fx + 7, fy + 22)],
              fill=(255, 200, 60))


# ---------- story grid: 2 cols x 4 rows ----------
stories = [
    ("MARKETS", (155, 27, 27), ill_markets,
     "AI rout drags S&P into correction",
     "S&P fell 3.7% on Friday; Nasdaq -5.3% and now negative for the year. Nikkei -5.1%."),
    ("EUROPE", (31, 78, 121), ill_flags_eu_uk,
     "UK and EU seal food and youth deals",
     "Burnham calls the Brussels reset a 'win-win'; 100,000 young people get three-year visas."),
    ("DIPLOMACY", (122, 74, 18), ill_flags_three,
     "Trump: 'very good talks' with Putin",
     "No security guarantees for Kyiv without a deal first, the US president says."),
    ("MIDDLE EAST", (155, 27, 27), ill_intercept,
     "Saudis shoot down Houthi missiles",
     "Five drones and a missile intercepted; Riyadh a target, a day after a tower was hit."),
    ("WEATHER", (46, 107, 52), ill_cyclone,
     "Cyclone Akvan hits India's east coast",
     "Over 300,000 moved to shelters in Odisha; heavy rain, no deaths reported at first."),
    ("DISASTER", (155, 27, 27), ill_quake,
     "Magnitude 6.7 quake shakes Peru",
     "Felt in Lima; centred near Carhuamayo, 108 km deep. No casualties reported."),
    ("SPACE", (106, 44, 112), ill_mercury,
     "BepiColombo reaches Mercury",
     "After eight years and 6bn miles, the ESA-JAXA probe enters orbit on Saturday."),
    ("JUSTICE", (90, 86, 76), ill_fire,
     "Guilty: man who started Palisades Fire",
     "Jury convicts Rinderknecht on retrial; the 2025 blaze killed 12 and destroyed 6,800 homes."),
]

GX, GY = MX, 524
CW, CH, CGAP, RGAP = 474, 112, 20, 6
ILL = 86
for i, (tag, color, draw_ill, head, body) in enumerate(stories):
    cx = GX + (i % 2) * (CW + CGAP)
    cy = GY + (i // 2) * (CH + RGAP)
    draw_ill(cx, cy + 4, ILL)
    tx = cx + ILL + 12
    tw = CW - ILL - 12
    d.text((tx, cy + 2), tag, font=F_TAG, fill=color)
    hl = wrap(head, F_HEAD, tw)
    hy = cy + 22
    for ln in hl[:2]:
        d.text((tx, hy), ln, font=F_HEAD, fill=INK)
        hy += 24
    bl = wrap(body, F_BODY, tw)
    by = hy + 2
    for ln in bl[:2]:
        d.text((tx, by), ln, font=F_BODY, fill=(40, 40, 40))
        by += 19

# ---------- footer ----------
d.text((W // 2, 1000), "THE WORLD TODAY  \u00b7  All stories reported on 20 November 2026",
       font=F_FOOT, fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
import os
print("saved entry.png:", os.path.getsize("entry.png"), "bytes")
