#!/usr/bin/env python3
"""news-23 b82 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories: 3 hero scenes + 10 cards + 18 ALSO. PIL only. Output: entry.png 1024x1024.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FDIR = "/usr/share/fonts/truetype/dejavu/"
def F(name, size):
    return ImageFont.truetype(FDIR + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

# palette
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
GOLD = (201, 162, 39)
GOLD_L = (212, 175, 55)
RED = (178, 24, 24)
RED_L = (200, 40, 40)
NAVY = (18, 38, 84)
TEAL = (0, 110, 105)
TEAL_D = (0, 90, 86)
CREAM = (250, 244, 224)
GREEN_L = (207, 232, 192)
BLUE = (24, 68, 160)
PURPLE = (110, 60, 160)
GREY = (90, 90, 90)
GREY_L = (230, 230, 230)
INK = (30, 30, 30)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def chip(x, y, label, bg=BLUE, fg=WHITE):
    f = SANS_B(8)
    w = int(d.textlength(label, font=f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=3, fill=bg)
    d.text((x + 5, y + 2), label, font=f, fill=fg)
    return w

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 52], fill=BLACK)
text(10, 6, "THE WORLD TODAY", SERIF_B(42), WHITE)
text(W - 10, 14, "MONDAY 23 NOVEMBER 2026", SANS_B(16), GOLD_L, anchor="ra")

# ---------------------------------------------------------------- kicker
d.rectangle([0, 52, W, 76], fill=RED)
kicker = "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B"
text(W // 2, 58, kicker, SANS_B(14), WHITE, anchor="ma")

# ---------------------------------------------------------------- number strip (2 rows x 5)
strip = [
    ("-3.3%", "KOSPI", RED_L), ("5.3", "US-CHINA POWER GAP", BLUE),
    ("11,762", "EBOLA CASES, DRC", (0, 120, 60)), ("10T won", "SEOUL STABILISATION FUND", (120, 90, 0)),
    ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE),
    ("$450M", "SKUBAL DEAL", BLUE), ("165", "RUSSIAN MISSILES/WEEK", RED_L),
    ("12,000", "CLEARED IN MANCHESTER", (0, 120, 60)), ("264 kg", "EXPLOSIVES SEIZED", (120, 90, 0)),
    ("$107.3B", "ANTHROPIC IPO", PURPLE),
]
col_w = 1024 // 5
for i, (val, lab, col) in enumerate(strip):
    row, c = divmod(i, 5)
    x = c * col_w + 10
    yv = 80 + row * 32
    text(x, yv, val, SANS_B(19), col)
    text(x, yv + 20, lab, SANS_B(8), GREY)

# ---------------------------------------------------------------- region bar
regions = [("ASIA-PACIFIC 7", BLUE), ("AMERICAS 8", RED), ("MIDDLE EAST 6", (176, 140, 20)),
           ("EUROPE 5", TEAL), ("AFRICA 3", PURPLE), ("WORLD 2", (60, 60, 60))]
seg_w = 1024 // 6
x = 0
for name, col in regions:
    d.rectangle([x, 142, x + seg_w, 162], fill=col)
    text(x + seg_w // 2, 147, name, SANS_B(11), WHITE, anchor="ma")
    x += seg_w

# ---------------------------------------------------------------- UTC strip
d.rectangle([0, 164, W, 178], fill=(245, 245, 245))
text(8, 167, "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
     SANS(9), GREY)
text(W - 8, 167, "~ APPROX", SANS_B(9), GREY, anchor="ra")

# ---------------------------------------------------------------- heroes
HX = [8, 348, 688]          # hero column x
HW = 328                    # hero column width
HY = 180                    # scene top
SCENE_H = 108
SRC_H = 14                  # black source bar height
heroes = [
    dict(scene="kospi", source="KOREA EXCHANGE",
         head="AI ROUT HITS ASIA",
         body="Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
         src="KOREA EXCHANGE"),
    dict(scene="guterres", source="UN \u00b7 BRIDGETOWN",
         head="GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
         body="UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
         src="UNITED NATIONS"),
    dict(scene="power", source="LOWY INSTITUTE",
         head="US LEAD OVER CHINA AT RECORD LOW",
         body="Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
         src="LOWY INSTITUTE"),
]

def scene_kospi(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(12, 22, 48))
    # buildings with lit windows
    import random
    rnd = random.Random(7)
    bx = x0 + 4
    while bx < x0 + w - 14:
        bw = rnd.randint(18, 34)
        bh = rnd.randint(38, h - 6)
        by = y0 + h - bh
        d.rectangle([bx, by, bx + bw, y0 + h], fill=(24, 38, 70))
        for wy in range(by + 5, y0 + h - 5, 9):
            for wx in range(bx + 4, bx + bw - 4, 8):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 205, 90))
        bx += bw + 3
    # orange chart line
    pts = [(x0 + 8, y0 + 78), (x0 + 60, y0 + 66), (x0 + 110, y0 + 74),
           (x0 + 160, y0 + 52), (x0 + 210, y0 + 60), (x0 + 260, y0 + 40),
           (x0 + 310, y0 + 48)]
    d.line(pts, fill=(255, 130, 30), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=WHITE)
    text(x0 + 8, y0 + 4, "-3.3%", SANS_B(22), (255, 70, 60))

def scene_guterres(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=TEAL_D)
    text(x0 + 10, y0 + 8, "150 DELEGATES", SANS_B(26), GOLD_L)
    text(x0 + 10, y0 + 38, "BACK A RISK", SANS_B(26), GOLD_L)
    text(x0 + 10, y0 + 68, "FRAMEWORK", SANS_B(26), GOLD_L)
    # globe
    cx, cy, r = x0 + w - 52, y0 + h // 2, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 225, 210))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 170, 150), width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(120, 170, 150))
    d.line([cx - r, cy, cx + r, cy], fill=(120, 170, 150), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=(120, 170, 150))

def scene_power(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CREAM)
    text(x0 + 8, y0 + 3, "NARROWEST SINCE 2018", SANS_B(9), INK)
    text(x0 + w - 8, y0 + 3, "GAP 5.3", SANS_B(10), RED_L, anchor="ra")
    base = y0 + h - 16
    bars = [("78.9", 78.9, NAVY, "US"), ("73.6", 73.6, RED_L, "CHINA"), ("40.5", 40.5, GOLD, "INDIA")]
    bw, gap = 62, 34
    bx = x0 + 22
    for val, v, col, lab in bars:
        bh = int(v * 0.55)  # 78.9 -> 43, 73.6 -> 40, 40.5 -> 22
        text(bx + bw // 2, base - bh - 16, val, SANS_B(15), INK, anchor="ma")
        d.rectangle([bx, base - bh, bx + bw, base], fill=col)
        text(bx + bw // 2, base - 12, lab, SANS_B(9), WHITE, anchor="ma")
        bx += bw + gap
    text(x0 + w // 2, y0 + h - 13, "", SANS(8), GREY, anchor="ma")

for i, hero in enumerate(heroes):
    x0 = HX[i]
    if hero["scene"] == "kospi":
        scene_kospi(x0, HY, HW, SCENE_H)
    elif hero["scene"] == "guterres":
        scene_guterres(x0, HY, HW, SCENE_H)
    else:
        scene_power(x0, HY, HW, SCENE_H)
    # black source bar under scene
    d.rectangle([x0, HY + SCENE_H, x0 + HW, HY + SCENE_H + SRC_H], fill=BLACK)
    text(x0 + 6, HY + SCENE_H + 2, hero["source"], SANS_B(9), WHITE)
    # headline (2 lines max)
    hy = HY + SCENE_H + SRC_H + 6
    hl = wrap(hero["head"], SERIF_B(20), HW)
    for j, ln in enumerate(hl[:2]):
        text(x0, hy + j * 20, ln, SERIF_B(20), INK)
    # body
    by = hy + 2 * 20 + 3
    bl = wrap(hero["body"], SANS(12), HW)
    for j, ln in enumerate(bl[:2]):
        text(x0, by + j * 13, ln, SANS(12), (60, 60, 60))
    # source + chip row
    cy = by + 2 * 13 + 3
    text(x0, cy + 2, hero["src"], SANS(9), GREY)
    chip(x0 + HW - 62, cy, "REPORTED", BLUE)

# ---------------------------------------------------------------- MORE strip
MY = 398
d.rectangle([0, MY, W, MY + 18], fill=BLACK)
text(8, MY + 3, "MORE OF THE DAY  \u2014  10 STORIES", SANS_B(12), WHITE)

# ---------------------------------------------------------------- cards (5 cols x 2 rows)
cards = [
    ("AMERICAS", BLUE, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", NAVY, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", (150, 110, 0), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", TEAL, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED"),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", (0, 120, 160), "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", (190, 120, 0), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", PURPLE, "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
CW, CGAP, CX0 = 196, 7, 8
CY0, CH, RGAP = 424, 74, 6
for i, (cat, col, head, body, src, tag) in enumerate(cards):
    row, c = divmod(i, 5)
    x0 = CX0 + c * (CW + CGAP)
    y0 = CY0 + row * (CH + RGAP)
    # category bar
    d.rectangle([x0, y0, x0 + CW, y0 + 13], fill=col)
    text(x0 + 4, y0 + 2, cat, SANS_B(8), WHITE)
    text(x0 + CW - 4, y0 + 2, str(i + 1), SANS_B(8), WHITE, anchor="ra")
    # headline (2 lines)
    hl = wrap(head, SANS_B(11), CW - 4)
    for j, ln in enumerate(hl[:2]):
        text(x0 + 2, y0 + 16 + j * 12, ln, SANS_B(11), INK)
    # body
    text(x0 + 2, y0 + 16 + 2 * 12 + 2, body, SANS(9), (70, 70, 70))
    # source + chip at bottom
    cy = y0 + CH - 13
    text(x0 + 2, cy + 2, src, SANS(8), GREY)
    chip(x0 + CW - 62, cy, tag, BLUE if tag == "REPORTED" else RED)

# ---------------------------------------------------------------- map + ALSO
MAPY = 584
d.rectangle([0, MAPY, W, MAPY + 18], fill=BLACK)
text(8, MAPY + 3, "WHERE IT HAPPENED", SANS_B(12), WHITE)
text(338, MAPY + 3, "ALSO ON MONDAY", SANS_B(12), WHITE)

# map box
MX0, MY0, MW, MH = 8, MAPY + 18, 322, 228
d.rectangle([MX0, MY0, MX0 + MW, MY0 + MH], outline=(150, 150, 150), width=1)
# stylised land blobs
d.polygon([(20, 640), (55, 622), (95, 625), (120, 645), (118, 690), (95, 745), (70, 775),
           (48, 760), (30, 720), (18, 680)], fill=GREEN_L)  # Americas
d.polygon([(150, 630), (185, 618), (215, 625), (225, 655), (210, 700), (185, 745),
           (165, 730), (150, 690), (145, 655)], fill=GREEN_L)  # Europe/Africa
d.polygon([(235, 625), (275, 612), (315, 620), (322, 650), (305, 690), (270, 705),
           (240, 680), (228, 650)], fill=GREEN_L)  # Asia
d.ellipse([272, 758, 312, 782], fill=GREEN_L)  # Australia
# pins (x, y, n) — spread, min ~18px apart, inside blobs, above legend
pins = [(298, 640, 1), (88, 700, 2), (288, 622, 3), (58, 645, 4), (76, 625, 5),
        (205, 640, 6), (52, 668, 7), (30, 690, 8), (48, 720, 9), (64, 748, 10),
        (196, 622, 11), (176, 636, 12), (232, 636, 13)]
for px, py, n in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    text(px, py - 5, str(n), SANS_B(8), WHITE, anchor="ma")
# legend (3 lines, inside box)
leg = ["Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing",
       "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF",
       "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow"]
for j, ln in enumerate(leg):
    text(MX0 + 6, MY0 + MH - 34 + j * 11, ln, SANS(8), INK)

# ALSO list (items 14-31)
also = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week",
    "COP31: the day after pact rejected",
    "Benghazi: UN demands port probe  [CLAIM]",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: strike hits plant, 2 hurt",
    "Sudan: defences down drones  [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits in exam row",
    "SK Telecom -7.3% as hype cools",
    "China eases margin rules",
    "Seoul readies 10T-won fund",
]
ay = MY0 + 3
for i, item in enumerate(also):
    n = 14 + i
    # split [CLAIM] red suffix
    if "[CLAIM]" in item:
        base, _ = item.split(" [CLAIM]")
        text(338, ay, f"{n}. {base}", SANS(11), INK)
        w = d.textlength(f"{n}. {base} ", font=SANS(11))
        text(338 + w, ay, "[CLAIM]", SANS_B(10), RED_L)
    else:
        text(338, ay, f"{n}. {item}", SANS(11), INK)
    ay += 12

# ---------------------------------------------------------------- DATE CHECK
DY = 830
d.rectangle([8, DY, W - 8, DY + 66], outline=RED, width=2)
text(14, DY + 5, "DATE CHECK", SANS_B(13), RED)
text(W - 14, DY + 5, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", SANS_B(9), RED, anchor="ra")
text(14, DY + 26, "LEFT OUT \u2014 NOT 23 NOV: Dems 258 seats (22 Nov) \u00b7 Sparta II fire (22 Nov) \u00b7 El Chapo (22 Nov) \u00b7 EU-Indonesia (21 Nov) \u00b7 Nigeria boat (21 Nov) \u00b7 ICJ Myanmar (19 Nov)",
     SANS(10), INK)
text(14, DY + 44, "NOT YET \u2014 Dymer search continues (14 missing) \u00b7 4 House races uncalled \u00b7 COP32 venue not set \u00b7 WHO evacuating trapped Ebola staff",
     SANS(10), INK)

# ---------------------------------------------------------------- footer
fy = 906
text(8, fy, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 NYT \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", SANS(9), GREY)
text(8, fy + 13, "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.", SANS(9), GREY)
text(8, fy + 26, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", SANS(9), GREY)
text(W // 2, 1006, "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions", SANS_B(12), GOLD, anchor="ma")

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
