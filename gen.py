# gen.py — draws entry.png for news-image-20261122 ("THE WORLD TODAY",
# Sunday 22 November 2026). A one-page newspaper front page: masthead, date
# line, markets ticker, COP31 lead with a draft-at-a-glance panel, a six-story
# grid, and a "day in brief" strip. Run:  python3 gen.py  (writes entry.png
# next to this file). Pillow is only needed here, on the author's machine;
# the entry itself is the PNG plus a stdlib-only main.ts that validates it.

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (18, 18, 18)
RED = (176, 30, 30)
NAVY = (13, 38, 68)
GOLD = (212, 175, 88)
GREY = (90, 86, 76)
RULE = (40, 40, 40)
FAINT = (214, 206, 188)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FONT_DIR + "LiberationSerif-Bold.ttf"
SERIF = FONT_DIR + "LiberationSerif-Regular.ttf"
SANS_B = FONT_DIR + "LiberationSans-Bold.ttf"
SANS = FONT_DIR + "LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK, max_lines=None):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def hrule(draw, x0, x1, y, width=2, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 34  # side margin

# --- Masthead ------------------------------------------------------------
mast = font(SERIF_B, 96)
title = "THE WORLD TODAY"
tw = d.textlength(title, font=mast)
d.text(((W - tw) / 2, 6), title, font=mast, fill=INK)
hrule(d, M, W - M, 112, 3)
hrule(d, M, W - M, 116, 1)

# --- Date line -----------------------------------------------------------
small_b = font(SANS_B, 16)
small = font(SANS, 15)
d.text((M, 124), "SUNDAY, 22 NOVEMBER 2026", font=small_b, fill=INK)
mid = "ONE DAY  •  ONE PAGE  •  THE WORLD'S NEWS"
mw = d.textlength(mid, font=small_b)
d.text(((W - mw) / 2, 124), mid, font=small_b, fill=INK)
right = "No. 326  •  FREE"
rw = d.textlength(right, font=small)
d.text((W - M - rw, 124), right, font=small, fill=INK)
hrule(d, M, W - M, 146, 3)
hrule(d, M, W - M, 150, 1)

# --- Markets ticker ------------------------------------------------------
d.rectangle([M, 158, W - M, 186], fill=RED)
tick = font(SANS_B, 16)
ticker = ("TAIWAN ACTS: SHORT-SELLING BAN FROM NOV 23   •   TAIEX -17.5% IN A WEEK"
          "   •   GOLD AT 14-MONTH LOW   •   VIX 35.89")
tw = d.textlength(ticker, font=tick)
d.text(((W - tw) / 2, 164), ticker, font=tick, fill=(255, 255, 255))

# --- Lead ----------------------------------------------------------------
kick = font(SANS_B, 15)
d.text((M, 198), "ANTALYA  •  CLIMATE  •  LEAD STORY", font=kick, fill=RED)
lead_f = font(SERIF_B, 52)
y = 222
y = para(d, M, y,
         "COP31 draft drops fossil-fuel phase-out as talks run into overtime",
         lead_f, W - 2 * M, 56)
deck = font(SERIF, 20)
y = para(d, M, y + 2,
         "A new text released before dawn offers a deal nearly 200 nations could "
         "sign — but never names an end to oil, gas and coal. The plenary meets "
         "at 06:00 GMT to approve it.",
         deck, W - 2 * M, 25, color=(52, 50, 44))

def wrap_headed(draw, head, body, head_fnt, body_fnt, max_w):
    """Wrap a 'HEAD — body' item so the head + first body words share line 1.
    Returns a list of (x_offset, text, is_head) draw ops collapsed into lines:
    each line is (indent_px, text, head_part_or_None)."""
    head_txt = head + " — "
    head_w = draw.textlength(head_txt, font=head_fnt)
    words = body.split()
    lines = []
    cur = ""
    cap = max_w - head_w
    first = True
    for word in words:
        trial = word if not cur else cur + " " + word
        limit = cap if first else max_w
        if draw.textlength(trial, font=body_fnt) <= limit:
            cur = trial
        else:
            lines.append((head_w if first else 0, cur, first))
            cur = word
            first = False
    if cur or not lines:
        lines.append((head_w if first else 0, cur, first))
    return head_txt, lines


# --- Draft at a glance (schematic panel) ---------------------------------
top = y + 12
d.rectangle([M, top, W - M, top + 100], outline=RULE, width=2)
d.rectangle([M, top, W - M, top + 26], fill=NAVY)
cap = font(SANS_B, 14)
d.text((M + 12, top + 5), "THE DRAFT AT A GLANCE — RELEASED EARLY SUNDAY", font=cap, fill=(255, 255, 255))
cols = [
    ("NO FOSSIL FUELS", "The 10-page text never says fossil, oil, coal or phase out — only a nod to the 2023 Dubai deal."),
    ("35% CLEAN POWER", "Electricity's share of all energy to rise to 35% by 2035, up from about 21% today."),
    ("1BN TONNES", "A goal for carbon capture and storage — the draft's answer to cutting emissions."),
]
cw = (W - 2 * M - 24) / 3
for i, (head, body) in enumerate(cols):
    x = M + 12 + i * cw
    if i:
        d.line([(x - 8, top + 34), (x - 8, top + 100)], fill=FAINT, width=1)
    d.text((x, top + 32), head, font=font(SANS_B, 15), fill=RED)
    para(d, x, top + 52, body, font(SERIF, 15), cw - 16, 18, color=(52, 50, 44))
hrule(d, M, W - M, top + 110, 2)

# --- Story grid (2 rows x 3 columns) -------------------------------------
grid = [
    ("TAIPEI  •  MARKETS",
     "Taiwan halts the rout with a short-selling ban",
     "Short sales below the previous close are banned from Nov 23; the "
     "stabilisation fund steps in after a 17.5% weekly fall."),
    ("HONG KONG",
     "Record 45% turnout in the first hour of the Election Committee vote",
     "856 candidates contest 723 seats in the race to form the 1,500-member "
     "college."),
    ("THE GULF",
     "Iran plans rolling blackouts as Bahrain reports an attack",
     "Tehran says war damage forces nationwide cuts from Monday; Bahrain says "
     "an Iranian strike set fire to a civilian plant."),
    ("WASHINGTON",
     "Trump vows a 10% cap on credit-card rates",
     "The president says he will work with Democrats to cap rates, now about "
     "22% for a typical borrower."),
    ("MANIPUR",
     "Suspect liquor toll reaches 19 in Manipur",
     "Six arrested and a probe ordered after hundreds fall ill in Chandel "
     "district."),
    ("SCIENCE",
     "Alzheimer's study finds 48 new risk regions",
     "A gene study of 2.8 million people maps 48 regions tied to the "
     "disease."),
]

gy = top + 124
col_w = (W - 2 * M) / 3
row_h = 136
for row in range(2):
    for col in range(3):
        story = grid[row * 3 + col]
        x = M + col * col_w
        y = gy + row * row_h
        d.text((x + 2, y), story[0], font=font(SANS_B, 13), fill=RED)
        y = para(d, x + 2, y + 20, story[1], font(SERIF_B, 22),
                 col_w - 18, 25, max_lines=3)
        para(d, x + 2, y + 2, story[2], font(SERIF, 15), col_w - 18, 18,
             color=(52, 50, 44), max_lines=3)
        if col:
            d.line([(x - 8, gy + row * row_h), (x - 8, gy + (row + 1) * row_h - 10)],
                   fill=FAINT, width=1)
    if row == 0:
        hrule(d, M, W - M, gy + row_h - 4, 1, color=FAINT)

# --- The day in brief (dark strip) ---------------------------------------
brief_top = gy + 2 * row_h + 4
d.rectangle([M, brief_top, W - M, H - 26], fill=NAVY)
d.text((M + 12, brief_top + 8), "THE DAY IN BRIEF", font=font(SANS_B, 16), fill=GOLD)
note = "ALL STORIES FIRST REPORTED SUNDAY 22 NOVEMBER 2026"
nw = d.textlength(note, font=font(SANS_B, 12))
d.text((W - M - 12 - nw, brief_top + 10), note, font=font(SANS_B, 12), fill=(200, 210, 225))
hrule(d, M + 12, W - M - 12, brief_top + 32, 1, color=(70, 95, 125))

brief = [
    ("AL-SHABAAB", "Claims hundreds dead in Somalia ambush."),
    ("NORWAY", "Court voids climate-disputed oil licences."),
    ("EBOLA", "Kenya's last patient out; DRC toll over 5,300."),
    ("HORMUZ", "Iran to reopen the strait in two days."),
    ("AMAZON", "To buy AI startup Decart for $7.5bn."),
    ("NVIDIA", "Board accepted Huang exit over dishonesty."),
    ("US-CHINA", "Humans to stay in charge of AI weapons."),
    ("PENGUINS", "Emperor penguins listed as endangered."),
    ("CRICKET", "Australia in command of S. Africa decider."),
    ("GHANA", "New banknotes honour Nkrumah and Annan."),
    ("SAHEL", "States restart talks with West Africa bloc."),
    ("SÃO TOMÉ", "Ramos reappointed prime minister."),
    ("NIGERIA", "Starts building its own naval ships."),
    ("DRC", "Tshisekedi signs constitutional reform law."),
    ("S. AFRICA", "Four ANC youths killed before polls."),
    ("UGANDA", "President raises succession question."),
    ("KATE", "Princess of Wales documentary airs."),
    ("USDA", "Reports say it was hit by hackers."),
    ("TAINAN", "Six-car crash kills two on Sunday."),
]

bcol_w = (W - 2 * M - 24) / 3
by = brief_top + 42
per_col = 7
for ci in range(3):
    bx = M + 12 + ci * bcol_w
    yy = by
    for item in brief[ci * per_col:(ci + 1) * per_col]:
        head, text = item
        head_txt, lines = wrap_headed(d, head, text, font(SANS_B, 12),
                                      font(SANS, 12), bcol_w - 14)
        for indent, chunk, is_first in lines:
            if is_first:
                d.text((bx, yy), head_txt, font=font(SANS_B, 12), fill=GOLD)
            d.text((bx + indent, yy), chunk, font=font(SANS, 12),
                   fill=(235, 238, 242))
            yy += 14
        yy += 2

# --- Footer ---------------------------------------------------------------
d.text((M, H - 20),
       "Sources: Reuters, BBC, AP, SCMP, Xinhua, Japan Times  •  Drawn for make.fun's news-image-20261122 bounty",
       font=font(SANS, 11), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png")
