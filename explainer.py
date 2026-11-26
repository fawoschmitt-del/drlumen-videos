"""Daily explainer video renderer – host: DR. LUMEN.
    python explainer.py <episode>            full render  -> out/<episode>/<episode>.mp4
    python explainer.py <episode> preview    contact sheet -> out/<episode>/preview.png
An episode is a file episodes/<episode>.py with TITLE, CAPTION and BEATS = [(visual, arms, text), ...].
Visuals that aren't drawn by a special function fall back to a big keyword card (see card_text)."""
import numpy as np, os, sys, math, random, subprocess, importlib, wave, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import lumen3d as L3
import voice as VO

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30

# ------------------------------------------------------------------ fonts (Linux paths or Windows fallbacks)
def _find(cands):
    for c in cands:
        hits = glob.glob(c)
        if hits: return hits[0]
    raise FileNotFoundError(cands)
FA = _find([os.path.join(HERE, 'fonts', 'Anton-Regular.ttf'), '/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf',
            os.path.expanduser('~/AppData/Local/Microsoft/Windows/Fonts/Anton*.ttf'), 'C:/Windows/Fonts/Anton*.ttf'])
FI = _find([os.path.join(HERE, 'fonts', 'Inter-Black.otf'), '/usr/share/fonts/opentype/inter/Inter-Black.otf',
            os.path.expanduser('~/AppData/Local/Microsoft/Windows/Fonts/Inter*Black*'), 'C:/Windows/Fonts/Inter*Black*', 'C:/Windows/Fonts/arialbd.ttf'])
FB = _find([os.path.join(HERE, 'fonts', 'Inter-Bold.otf'), '/usr/share/fonts/opentype/inter/Inter-Bold.otf',
            os.path.expanduser('~/AppData/Local/Microsoft/Windows/Fonts/Inter*Bold*'), 'C:/Windows/Fonts/Inter*Bold*', 'C:/Windows/Fonts/arialbd.ttf'])
_F = {}
def font(p, s):
    if (p, s) not in _F: _F[(p, s)] = ImageFont.truetype(p, s)
    return _F[(p, s)]

INK = (22, 20, 40); YEL = (255, 214, 64); PINK = (255, 92, 140); CYAN = (70, 210, 255); GRN = (90, 220, 130)
CARD = (252, 248, 240)

def ease_back(x):
    x = min(max(x, 0), 1); c = 1.7
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2
def ease_out(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3

def radial(size, color, a0=255, power=1.6):
    w, h = size
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    a = np.clip(1 - d, 0, 1) ** power * a0
    arr = np.zeros((h, w, 4), np.uint8); arr[..., :3] = color; arr[..., 3] = a.astype(np.uint8)
    return Image.fromarray(arr, 'RGBA')

def text_img(s, f, fill, stroke=10, sfill=INK):
    l, t, r, b = f.getbbox(s, stroke_width=stroke)
    im = Image.new('RGBA', (r - l + 20, b - t + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - l, 10 - t), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=sfill)
    return im

def paste_c(img, im, cx, cy, scale=1.0, angle=0, alpha=1.0):
    if scale <= 0.01 or alpha <= 0.01: return
    if scale != 1: im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BICUBIC)
    if angle: im = im.rotate(angle, Image.BICUBIC, expand=True)
    if alpha < 1:
        im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    img.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)

# ------------------------------------------------------------------ background
_BG = None
def background():
    global _BG
    if _BG is None:
        y = np.linspace(0, 1, H)[:, None, None]
        top = np.array((34, 26, 74), np.float32); bot = np.array((12, 70, 96), np.float32)
        arr = (top * (1 - y) + bot * y) * np.ones((1, W, 1), np.float32)
        img = Image.fromarray(arr.astype(np.uint8), 'RGB')
        d = ImageDraw.Draw(img, 'RGBA')
        for x in range(-H, W, 90):                      # faint diagonal pattern
            d.line([(x, 0), (x + H, H)], fill=(255, 255, 255, 9), width=24)
        g = radial((1300, 1000), (255, 200, 90), 70, 1.4); img.paste(g, (W // 2 - 650, 1330 - 500), g)
        _BG = img
    return _BG

DOTS = [(random.Random(i).uniform(0, W), random.Random(i * 7).uniform(0, H), random.Random(i * 13).uniform(6, 22),
         random.Random(i * 17).uniform(0.15, 0.5), random.Random(i * 19).choice([YEL, CYAN, PINK, (255, 255, 255)])) for i in range(26)]
def particles(img, t):
    d = ImageDraw.Draw(img, 'RGBA')
    for x, y, r, sp, c in DOTS:
        yy = (y - t * 40 * sp) % (H + 60) - 30
        xx = x + 18 * math.sin(t * sp * 2 + x)
        d.ellipse([xx - r, yy - r, xx + r, yy + r], fill=c + (40,))

# ------------------------------------------------------------------ illustration helpers (card space 940 x 680)
CW, CH = 940, 680
def new_card():
    im = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([8, 14, CW - 2, CH - 2], 46, fill=(0, 0, 0, 90))
    d.rounded_rectangle([0, 0, CW - 10, CH - 14], 46, fill=CARD, outline=INK, width=8)
    return im, d

def label(d, xy, s, size=58, fill=INK, f=None, anchor='mm', stroke=0, sfill=INK):
    d.text(xy, s, font=font(f or FI, size), fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)

def arrow(d, a, b, col=INK, w=12, head=34):
    d.line([a, b], fill=col, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    p1 = (b[0] - head * math.cos(ang - 0.45), b[1] - head * math.sin(ang - 0.45))
    p2 = (b[0] - head * math.cos(ang + 0.45), b[1] - head * math.sin(ang + 0.45))
    d.polygon([b, p1, p2], fill=col)

def brain(d, cx, cy, s=1.0, glow=None, cereb_hi=False, dim=False):
    pink = (255, 150, 175) if not dim else (205, 180, 190)
    dark = (205, 80, 120) if not dim else (150, 130, 140)
    d.ellipse([cx - 210 * s, cy - 150 * s, cx + 210 * s, cy + 130 * s], fill=pink, outline=INK, width=int(8 * s))
    # cerebellum (back-bottom)
    cc = YEL if cereb_hi else ((235, 120, 150) if not dim else (180, 150, 160))
    d.ellipse([cx + 70 * s, cy + 60 * s, cx + 230 * s, cy + 170 * s], fill=cc, outline=INK, width=int(8 * s))
    for k in range(4):
        yy = cy + 85 * s + k * 20 * s
        d.arc([cx + 95 * s, yy - 12 * s, cx + 210 * s, yy + 12 * s], 200, 340, fill=INK, width=int(5 * s))
    # brain stem
    d.rounded_rectangle([cx + 10 * s, cy + 110 * s, cx + 70 * s, cy + 220 * s], int(20 * s), fill=pink, outline=INK, width=int(8 * s))
    # folds
    rr = random.Random(5)
    for k in range(9):
        x = cx + rr.uniform(-170, 150) * s; y = cy + rr.uniform(-110, 70) * s
        d.arc([x - 60 * s, y - 35 * s, x + 60 * s, y + 35 * s], rr.uniform(180, 220), rr.uniform(320, 360), fill=dark, width=int(7 * s))
    if glow:
        for (gx, gy) in glow:
            d.ellipse([cx + gx * s - 40 * s, cy + gy * s - 40 * s, cx + gx * s + 40 * s, cy + gy * s + 40 * s], fill=(255, 230, 60), outline=INK, width=int(5 * s))

def feather(d, cx, cy, s=1.0, ang=-35):
    a = math.radians(ang)
    def R(x, y): return (cx + (x * math.cos(a) - y * math.sin(a)) * s, cy + (x * math.sin(a) + y * math.cos(a)) * s)
    pts = [R(0, -170), R(60, -100), R(70, 20), R(30, 120), R(0, 150), R(-30, 120), R(-70, 20), R(-60, -100)]
    d.polygon(pts, fill=(130, 210, 255), outline=INK)
    d.line(pts + [pts[0]], fill=INK, width=int(7 * s))
    for k in range(-5, 6):
        d.line([R(0, k * 22), R(55 if k < 4 else 35, k * 22 - 30)], fill=(60, 150, 220), width=int(5 * s))
        d.line([R(0, k * 22), R(-55 if k < 4 else -35, k * 22 - 30)], fill=(60, 150, 220), width=int(5 * s))
    d.line([R(0, -150), R(0, 230)], fill=INK, width=int(9 * s))

def meter(d, x, y, w, h, frac, col, title):
    label(d, (x + w / 2, y - 45), title, 44)
    d.rounded_rectangle([x, y, x + w, y + h], h // 2, fill=(225, 220, 212), outline=INK, width=7)
    if frac > 0.02:
        d.rounded_rectangle([x + 9, y + 9, x + 9 + (w - 18) * frac, y + h - 9], (h - 18) // 2, fill=col)
    label(d, (x + w / 2, y + h + 50), f'{int(round(frac * 100))}%', 56)

def rat(d, cx, cy, s=1.0, spots=False):
    g = (170, 170, 185); pk = (255, 170, 190)
    d.line([(cx + 150 * s, cy + 40 * s), (cx + 260 * s, cy - 10 * s), (cx + 320 * s, cy + 60 * s)], fill=pk, width=int(14 * s), joint='curve')
    d.ellipse([cx - 160 * s, cy - 90 * s, cx + 170 * s, cy + 110 * s], fill=g, outline=INK, width=int(8 * s))
    d.ellipse([cx - 270 * s, cy - 110 * s, cx - 90 * s, cy + 40 * s], fill=g, outline=INK, width=int(8 * s))
    d.ellipse([cx - 220 * s, cy - 190 * s, cx - 130 * s, cy - 90 * s], fill=pk, outline=INK, width=int(7 * s))
    d.ellipse([cx - 150 * s, cy - 170 * s, cx - 60 * s, cy - 70 * s], fill=pk, outline=INK, width=int(7 * s))
    d.ellipse([cx - 210 * s, cy - 60 * s, cx - 180 * s, cy - 28 * s], fill=INK)
    d.ellipse([cx - 290 * s, cy - 30 * s, cx - 255 * s, cy + 2 * s], fill=pk, outline=INK, width=int(5 * s))
    d.arc([cx - 250 * s, cy - 20 * s, cx - 190 * s, cy + 30 * s], 20, 160, fill=INK, width=int(6 * s))   # smile
    for fx in (-90, 70):
        d.ellipse([cx + fx * s - 40 * s, cy + 90 * s, cx + fx * s + 40 * s, cy + 130 * s], fill=pk, outline=INK, width=int(6 * s))
    if spots:
        for (x, y, r) in ((cx - 10 * s, cy + 40 * s, 70 * s), (cx - 90 * s, cy + 112 * s, 52 * s), (cx + 70 * s, cy + 112 * s, 52 * s)):
            d.ellipse([x - r, y - r, x + r, y + r], outline=(255, 70, 110), width=int(9 * s))

def waves(d, cx, cy, t, col=PINK, n=3):
    for k in range(n):
        ph = (t * 1.6 + k / n) % 1.0
        r = 40 + 170 * ph
        a = int(255 * (1 - ph))
        d.arc([cx - r, cy - r, cx + r, cy + r], 140, 220, fill=col + (a,), width=12)

def robot_arm(d, x, y, s=1.0, ang=0, col=(150, 160, 185)):
    d.rounded_rectangle([x - 80 * s, y + 120 * s, x + 80 * s, y + 160 * s], int(14 * s), fill=(90, 95, 120), outline=INK, width=6)
    a = math.radians(ang)
    ex, ey = x + 110 * math.sin(a) * s, y - 110 * math.cos(a) * s + 120 * s - 120 * s
    d.line([(x, y + 130 * s), (x, y)], fill=INK, width=int(40 * s)); d.line([(x, y + 130 * s), (x, y)], fill=col, width=int(28 * s))
    d.line([(x, y), (ex + 90 * s, ey - 40 * s)], fill=INK, width=int(36 * s)); d.line([(x, y), (ex + 90 * s, ey - 40 * s)], fill=col, width=int(24 * s))
    for (px, py) in ((x, y), (x, y + 130 * s)):
        d.ellipse([px - 26 * s, py - 26 * s, px + 26 * s, py + 26 * s], fill=YEL, outline=INK, width=6)
    return ex + 90 * s, ey - 40 * s

def palm(d, cx, cy, s=1.0):
    sk = (255, 205, 170)
    for k, (fx, fl) in enumerate(((-75, 150), (-25, 175), (25, 170), (75, 140))):
        d.rounded_rectangle([cx + fx * s - 22 * s, cy - fl * s, cx + fx * s + 22 * s, cy - 40 * s], int(22 * s), fill=sk, outline=INK, width=6)
    d.rounded_rectangle([cx - 110 * s, cy - 70 * s, cx + 110 * s, cy + 110 * s], int(60 * s), fill=sk, outline=INK, width=7)
    d.line([(cx - 105 * s, cy + 20 * s), (cx - 175 * s, cy - 40 * s)], fill=INK, width=int(52 * s))
    d.line([(cx - 105 * s, cy + 20 * s), (cx - 175 * s, cy - 40 * s)], fill=sk, width=int(38 * s))

def stopwatch(d, cx, cy, r, frac):
    d.rectangle([cx - 22, cy - r - 46, cx + 22, cy - r + 4], fill=INK)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255), outline=INK, width=10)
    if frac > 0: d.pieslice([cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18], -90, -90 + 360 * frac, fill=(255, 200, 80))
    a = math.radians(-90 + 360 * frac)
    d.line([(cx, cy), (cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a))], fill=INK, width=10)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=INK)

# ------------------------------------------------------------------ visuals: fn(lt, beat) -> RGBA card. lt = seconds since beat start
def v_hook(lt, b):
    im, d = new_card()
    palm(d, 330, 420, 1.05)
    feather(d, 600 + 25 * math.sin(lt * 9), 330 + 15 * math.cos(lt * 9), 1.0, -40 + 12 * math.sin(lt * 9))
    label(d, (CW / 2 - 5, 95), 'TICKLE YOURSELF?', 82, INK, FA)
    return im
def v_hook2(lt, b):
    im, d = new_card()
    label(d, (CW / 2 - 5, 110), 'GIGGLE METER', 82, INK, FA)
    meter(d, 120, 300, 680, 110, 0.0, PINK, '')
    label(d, (CW / 2 - 5, 560), 'nothing. at. all.', 50, (120, 110, 130), FB)
    return im
def v_intro(lt, b):
    im, d = new_card()
    label(d, (CW / 2 - 5, 230), 'DR. LUMEN', 170, YEL, FA, stroke=10)
    label(d, (CW / 2 - 5, 400), 'everyday mysteries,', 60, INK, FI)
    label(d, (CW / 2 - 5, 480), 'explained.', 60, INK, FI)
    return im
def v_title(lt, b):
    im, d = new_card()
    for k, (s, c) in enumerate((("WHY CAN'T YOU", INK), ('TICKLE', PINK), ('YOURSELF?', INK))):
        label(d, (CW / 2 - 5, 150 + k * 175), s, 150 if k else 110, c, FA, stroke=6 if k == 1 else 0)
    return im
def v_copy(lt, b):
    im, d = new_card()
    brain(d, 520, 330, 1.15, cereb_hi=True)
    label(d, (180, 90), 'MOVE!', 64, INK, FA)
    arrow(d, (210, 140), (330, 230), INK)
    k = ease_out(lt / 1.6)
    ex, ey = 330 + (690 - 330) * k, 230 + (470 - 230) * k
    d.rounded_rectangle([ex - 60, ey - 40, ex + 60, ey + 40], 10, fill=(255, 255, 255), outline=INK, width=6)
    d.line([(ex - 60, ey - 40), (ex, ey + 5), (ex + 60, ey - 40)], fill=INK, width=6)
    label(d, (ex, ey - 75), 'COPY', 44, INK, FA)
    label(d, (720, 625), 'CEREBELLUM', 50, INK, FA)
    return im
def v_predict(lt, b):
    im, d = new_card()
    label(d, (CW / 2 - 5, 80), 'PREDICTION', 74, INK, FA)
    xs = np.linspace(80, 860, 200)
    for k, (col, off, lab) in enumerate(((CYAN, 0, 'predicted'), (PINK, 0, 'actual'))):
        y0 = 260 + k * 220
        ys = y0 + 70 * np.sin((xs - 80) / 60) * np.exp(-((xs - 470) / 230) ** 2)
        n = int(len(xs) * min(1, lt / 1.4))
        if n > 1: d.line(list(zip(xs[:n], ys[:n])), fill=col, width=12)
        label(d, (90, y0 - 95), lab, 44, INK, FB, anchor='lm')
    label(d, (CW / 2 - 5, 625), 'MATCH  =  NO SURPRISE', 50, INK, FA)
    return im
def v_volume(lt, b):
    im, d = new_card()
    label(d, (CW / 2 - 5, 90), 'TICKLE VOLUME', 82, INK, FA)
    frac = 1 - 0.8 * ease_out((lt - 0.6) / 1.6)
    # speaker
    d.rectangle([130, 280, 200, 400], fill=INK); d.polygon([(200, 280), (290, 210), (290, 470), (200, 400)], fill=INK)
    for k in range(3):
        if frac > 0.3 * k + 0.1: d.arc([270 - 40 * k, 250 - 40 * k, 390 + 40 * k, 430 + 40 * k], -45, 45, fill=INK, width=12)
    for k in range(10):
        on = k < round(frac * 10)
        x = 450 + k * 40; hh = 40 + k * 22
        d.rounded_rectangle([x, 470 - hh, x + 28, 470], 8, fill=(GRN if k < 6 else YEL if k < 8 else PINK) if on else (215, 210, 205), outline=INK, width=4)
    label(d, (CW / 2 - 5, 590), f'{int(round(frac * 100))}%', 74, INK, FA)
    return im
def v_scan(lt, b, dim_self=None):
    im, d = new_card()
    k = 1.0 if b['vis'] == 'scan2' else min(1, lt / 1.0)
    brain(d, 240, 330, 0.72, glow=[(-60, -40), (40, 10), (-10, 60)])
    brain(d, 690, 330, 0.72, glow=[(-60, -40)] if k > 0.5 else [(-60, -40), (40, 10), (-10, 60)], dim=k > 0.5)
    label(d, (240, 95), 'TICKLED BY', 46, INK, FA); label(d, (240, 145), 'A MACHINE', 46, INK, FA)
    label(d, (690, 95), 'SELF', 46, INK, FA); label(d, (690, 145), 'TICKLE', 46, INK, FA)
    label(d, (240, 600), 'LIGHTS UP', 50, GRN, FA, stroke=3); label(d, (690, 600), 'MUCH LESS', 50, PINK, FA, stroke=3)
    return im
def v_surprise(lt, b):
    im, d = new_card()
    cx, cy = 470, 300
    pts = []
    for k in range(24):
        r = 250 if k % 2 == 0 else 160
        a = k / 24 * 2 * math.pi + lt * 0.4
        pts.append((cx + r * math.cos(a), cy + r * 0.8 * math.sin(a)))
    d.polygon(pts, fill=YEL, outline=INK); d.line(pts + [pts[0]], fill=INK, width=8)
    label(d, (cx, cy), 'SURPRISE!', 104, INK, FA)
    label(d, (CW / 2 - 5, 600), 'no surprise  =  no tickle', 54, INK, FB)
    return im
def v_robot(lt, b):
    im, d = new_card()
    label(d, (CW / 2 - 5, 80), 'THE TICKLE ROBOT', 76, INK, FA)
    sw = 18 * math.sin(lt * 6) if b['vis'] == 'robot2' else 0
    robot_arm(d, 220, 360, 1.0, sw)
    d.line([(300, 500), (470, 560), (640, 500)], fill=INK, width=8, joint='curve')
    tip = robot_arm(d, 640, 360, 1.0, -sw)
    palm(d, 790 + 0, 500, 0.62)
    feather(d, tip[0] + 10, tip[1] + 30, 0.45, -60 + sw)
    label(d, (220, 625), 'you move this', 40, INK, FB); label(d, (690, 625), 'it tickles you', 40, INK, FB)
    return im
def v_delay(lt, b):
    im, d = new_card()
    late = b['vis'] == 'delay2' or lt > 2.4
    frac = 0.0 if not late else 1.0
    label(d, (CW / 2 - 5, 80), 'DELAY', 90, INK, FA)
    stopwatch(d, 230, 360, 150, 0.2 * min(1, max(0, (lt - 2.0) / 0.6)) / 0.2 * 0.55 if b['vis'] == 'delay' else 0.55)
    label(d, (230, 590), '0.2 s' if late else '0 s', 80, INK, FA)
    meter(d, 450, 360, 420, 90, (0.12 + 0.75 * ease_out((lt - 2.4) / 0.8)) if b['vis'] == 'delay' and late else (0.12 if not late else 0.87), PINK, 'TICKLISH')
    return im
def v_rats(lt, b):
    im, d = new_card()
    r2 = b['vis'] == 'rats2'
    rs = 1.0 if r2 else 1.15; rx, ry = 560, (320 if r2 else 390)
    rat(d, rx, ry, rs, spots=b['vis'] == 'rats3')
    mx, my = rx - 300 * rs, ry - 15 * rs
    if b['vis'] == 'rats':
        label(d, (CW / 2 - 5, 90), 'RATS LAUGH!', 96, INK, FA)
        d2 = ImageDraw.Draw(im, 'RGBA'); waves(d2, mx, my, lt); label(d, (130, 210), 'hee!', 50, PINK, FA)
    elif r2:
        label(d, (CW / 2 - 5, 80), '~50 kHz', 96, INK, FA)
        d.rounded_rectangle([70, 520, 870, 570], 25, fill=(220, 215, 210), outline=INK, width=6)
        d.rounded_rectangle([79, 529, 79 + 782 * 20 / 60, 561], 18, fill=CYAN)
        x50 = 79 + 782 * 50 / 60
        d.polygon([(x50, 505), (x50 - 22, 465), (x50 + 22, 465)], fill=PINK, outline=INK)
        label(d, (79 + 782 * 10 / 60, 610), 'human hearing', 36, INK, FB); label(d, (x50, 610), 'rat laugh', 36, PINK, FB)
        d2 = ImageDraw.Draw(im, 'RGBA'); waves(d2, mx, my, lt)
    else:
        label(d, (CW / 2 - 5, 80), 'BELLY + FEET', 92, INK, FA)
    return im
def v_outro(lt, b):
    im, d = new_card()
    brain(d, 470, 330, 1.05)
    label(d, (CW / 2 - 5, 80), 'PREDICTION PRO', 84, INK, FA)
    d.rounded_rectangle([250, 560, 690, 640], 40, fill=YEL, outline=INK, width=7)
    label(d, (470, 600), 'NOT TICKLISH?', 50, INK, FA)
    return im
def v_follow(lt, b):
    im, d = new_card()
    label(d, (CW / 2 - 5, 170), 'NEW MYSTERY', 120, INK, FA)
    label(d, (CW / 2 - 5, 320), 'EVERY DAY', 120, PINK, FA, stroke=5)
    p = 1 + 0.05 * math.sin(lt * 8)
    d.rounded_rectangle([CW / 2 - 5 - 230 * p, 450, CW / 2 - 5 + 230 * p, 600], 75, fill=PINK, outline=INK, width=8)
    label(d, (CW / 2 - 5, 525), '+ FOLLOW', 76, (255, 255, 255), FA, stroke=4)
    return im

def card_text(lt, b):            # fallback: keyword card from the beat text
    im, d = new_card()
    words = [w.strip('.,!?') for w in b['text'].split() if len(w.strip('.,!?')) > 3][:3]
    for k, w in enumerate(words): label(d, (CW / 2 - 5, 170 + k * 170), w.upper(), 120, [INK, PINK, INK][k], FA)
    return im

VISUALS = {'hook': v_hook, 'hook2': v_hook2, 'intro': v_intro, 'title': v_title, 'copy': v_copy, 'predict': v_predict,
           'volume': v_volume, 'scan': v_scan, 'scan2': v_scan, 'surprise': v_surprise, 'robot': v_robot, 'robot2': v_robot,
           'delay': v_delay, 'delay2': v_delay, 'rats': v_rats, 'rats2': v_rats, 'rats3': v_rats, 'outro': v_outro, 'follow': v_follow}
STATIC = set()      # visuals that don't animate could be cached; all are cheap enough

# ------------------------------------------------------------------ captions (word by word)
def chunks(words, maxw=3):
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= maxw or w[0][-1] in '.,!?':
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out

CAP_F = None
def draw_caption(img, chunk, t, cy=930):
    f = font(FA, 112)
    toks = [(w.upper().strip(), a, e) for w, a, e in chunk]
    gap = 28
    ims = []
    cur = max([i for i, (_, a, _) in enumerate(toks) if a <= t] or [-1])
    for i, (w, a, e) in enumerate(toks):
        active = i == cur
        done = t >= a - 0.03
        col = YEL if active else (255, 255, 255)
        im = text_img(w, f, col, 11)
        sc = 1.0 + (0.12 * (1 - min(1, (t - a) / 0.12)) if active else 0)
        ims.append((im, sc, done))
    total = sum(im.width for im, _, _ in ims) + gap * (len(ims) - 1)
    scale = min(1.0, 1000 / total)
    x = W / 2 - total * scale / 2
    for im, sc, done in ims:
        wpx = im.width * scale
        paste_c(img, im, x + wpx / 2, cy, scale * sc, alpha=1.0 if done else 0.0)
        x += wpx + gap * scale

# ------------------------------------------------------------------ host
_SPR = {}
def spr(name):
    if name not in _SPR: _SPR[name] = L3.get(name)
    return _SPR[name]
GLOW = radial((820, 820), (255, 220, 110), 255, 1.5)

def host(img, t, beat, env_v, bt):
    arms = beat['pose'] if beat else 'down'
    speaking = beat is not None and beat['start'] <= t <= beat['end']
    m = 'smile'
    if speaking:
        m = 'wide' if env_v > 0.62 else ('mid' if env_v > 0.16 else 'smile')
    blink = (t % 3.3) < 0.12 and m == 'smile' and arms != 'up'
    name = f'lumen_{arms}_blink' if blink else f'lumen_{arms}_{m}'
    sp = spr(name)
    sc = 0.70
    bob = 10 * math.sin(t * 2 * math.pi * 0.9)
    pop = 1 + 0.06 * math.exp(-bt * 9) * math.cos(bt * 25) if bt < 0.6 else 1      # squash on pose change
    cx, feet = W / 2, 1700
    ga = min(1, 0.55 + 0.6 * env_v + (0.25 if arms == 'up' else 0))
    gs = 1.0 + 0.08 * env_v
    g = GLOW.resize((int(820 * gs), int(820 * gs)))
    g.putalpha(g.getchannel('A').point(lambda v: int(v * ga * 0.8)))
    img.paste(g, (int(cx - g.width / 2), int(feet - sp.height * sc * 0.72 - g.height / 2 + bob)), g)
    w, h = int(sp.width * sc * pop), int(sp.height * sc / pop)
    s2 = sp.resize((w, h), Image.BICUBIC)
    # floor shadow
    sh = radial((420, 70), (0, 0, 0), 120, 1.0)
    img.paste(sh, (int(cx - 210), int(feet - 40)), sh)
    img.paste(s2, (int(cx - w / 2), int(feet - h + bob - 30)), s2)

# ------------------------------------------------------------------ frame
def frame(T, t, env):
    img = background().copy()
    particles(img, t)
    beats = T['beats']
    bi = 0
    for i, b in enumerate(beats):
        if t >= b['start'] - 0.12: bi = i
    beat = beats[bi]
    lt = t - beat['start']
    ev = float(env[min(len(env) - 1, int(t * FPS))]) if len(env) else 0
    host(img, t, beat, ev, lt + 0.12)
    # card
    fn = VISUALS.get(beat['vis'], card_text)
    same_as_prev = bi > 0 and VISUALS.get(beats[bi - 1]['vis']) is fn and fn is not card_text and beats[bi - 1]['vis'].rstrip('23') == beat['vis'].rstrip('23')
    k = 1.0 if same_as_prev else ease_back((lt + 0.12) / 0.32)
    card = fn(max(0, lt), beat)
    paste_c(img, card, W / 2, 175 + CH / 2, 0.6 + 0.4 * k, angle=(1 - min(1, k)) * -6, alpha=min(1, (lt + 0.12) / 0.12) if not same_as_prev else 1)
    # caption
    words = beat['words']
    ch = None
    for c in chunks(words):
        if t >= c[0][1] - 0.02: ch = c
    if ch and t <= beat['end'] + 0.25:
        draw_caption(img, ch, t)
    return img

# ------------------------------------------------------------------ music + sfx
SR = 44100
def music(total, beats_t):
    n = int(SR * total); buf = np.zeros(n, np.float32)
    tt = np.arange(n) / SR
    bpm = 100; beat = 60 / bpm
    chords = [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (196.0, 246.9, 293.7), (164.8, 207.7, 246.9)]
    bar = beat * 4
    for i in range(int(total / bar) + 1):
        t0 = i * bar; c = chords[i % 4]
        s0, s1 = int(t0 * SR), min(n, int((t0 + bar) * SR))
        if s0 >= n: break
        x = tt[s0:s1] - t0
        envv = np.minimum(1, x / 0.3) * np.exp(-x * 0.4)
        for f in c:
            buf[s0:s1] += 0.05 * np.sin(2 * np.pi * f * x) * envv
            buf[s0:s1] += 0.02 * np.sin(2 * np.pi * f * 2.003 * x) * envv
        # bass
        buf[s0:s1] += 0.08 * np.sin(2 * np.pi * c[0] / 2 * x) * np.exp(-x * 1.2)
    for i in range(int(total / beat) + 1):           # soft pluck arp + kick/hat
        t0 = i * beat; s0 = int(t0 * SR); L = int(0.25 * SR)
        if s0 + L >= n: break
        x = np.arange(L) / SR
        c = chords[int(t0 / bar) % 4]
        f = c[i % 3] * 2
        buf[s0:s0 + L] += 0.035 * np.sin(2 * np.pi * f * x) * np.exp(-x * 14)
        if i % 2 == 0:
            buf[s0:s0 + L] += 0.12 * np.sin(2 * np.pi * (50 + 90 * np.exp(-x / 0.03)) * x) * np.exp(-x * 18)
        h = int(t0 * SR + beat / 2 * SR); Lh = int(0.04 * SR)
        if h + Lh < n: buf[h:h + Lh] += 0.02 * np.random.default_rng(i).uniform(-1, 1, Lh) * np.exp(-np.arange(Lh) / SR * 90)
    for t0 in beats_t:                               # soft "pop" at each new card
        s0 = int(t0 * SR); L = int(0.12 * SR)
        if s0 + L < n:
            x = np.arange(L) / SR
            buf[s0:s0 + L] += 0.18 * np.sin(2 * np.pi * (500 + 2500 * x) * x) * np.exp(-x * 35)
    return buf

def mix(outdir, total, beats_t):
    import soundfile as sf
    v, sr = sf.read(os.path.join(outdir, 'voice.wav'))
    v = np.interp(np.arange(0, len(v), sr / SR), np.arange(len(v)), v)
    m = music(total, beats_t)
    n = max(len(v), len(m)); out = np.zeros(n)
    out[:len(m)] += m * 0.55
    # duck music under the voice
    out[:len(v)] = out[:len(v)] * (1 - 0.45 * (np.convolve(np.abs(v) > 0.02, np.ones(4410) / 4410, 'same')))
    out[:len(v)] += v * 0.95
    out = np.tanh(out * 1.05); out = out / (np.abs(out).max() + 1e-9) * 0.92
    fade = int(SR * 0.8); out[-fade:] *= np.linspace(1, 0, fade)
    with wave.open(os.path.join(outdir, 'mix.wav'), 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
        wf.writeframes((out * 32767).astype(np.int16).tobytes())

# ------------------------------------------------------------------ render
def _render_range(args):
    ep, a, b, path = args
    T, env = _load(ep)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for i in range(a, b):
        p.stdin.write(frame(T, i / FPS, env).convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    return path

_CACHE = {}
def _load(ep):
    if ep not in _CACHE:
        sys.path.insert(0, os.path.join(HERE, 'episodes'))
        E = importlib.import_module(ep)
        VISUALS.update(getattr(E, 'VISUALS', {}))        # episode-specific illustrations
        outdir = os.path.join(HERE, 'out', ep); os.makedirs(outdir, exist_ok=True)
        T = VO.build(E.BEATS, outdir, os.path.join(outdir, 'timing.json'))
        env = VO.envelope(os.path.join(outdir, 'voice.wav'), FPS)
        env = np.convolve(env, np.ones(2) / 2, 'same')
        _CACHE[ep] = (T, env)
    return _CACHE[ep]

if __name__ == '__main__':
    ep = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'full'
    outdir = os.path.join(HERE, 'out', ep)
    T, env = _load(ep)
    L3.make  # poses are rendered on demand
    if mode == 'preview':
        bs = T['beats']
        times = [b['start'] + (b['end'] - b['start']) * 0.6 for b in bs][:12]
        ims = [frame(T, t, env).convert('RGB').resize((270, 480)) for t in times]
        sheet = Image.new('RGB', (270 * 6, 480 * 2))
        for k, im in enumerate(ims): sheet.paste(im, ((k % 6) * 270, (k // 6) * 480))
        sheet.save(os.path.join(outdir, 'preview.png')); print(os.path.join(outdir, 'preview.png'))
    elif mode == 'still':
        t = float(sys.argv[3]); frame(T, t, env).convert('RGB').save(os.path.join(outdir, f'still_{t:.1f}.png'))
    else:
        from multiprocessing import Pool
        total = T['total']; nf = int(total * FPS)
        nproc = int(os.environ.get('NPROC', os.cpu_count() or 2))
        step = math.ceil(nf / nproc)
        jobs = [(ep, i, min(nf, i + step), os.path.join(outdir, f'_part{k}.mp4')) for k, i in enumerate(range(0, nf, step))]
        for k in L3.POSES: L3.make(k)
        with Pool(nproc) as pool: parts = pool.map(_render_range, jobs)
        mix(outdir, total, [b['start'] for b in T['beats']])
        with open(os.path.join(outdir, 'parts.txt'), 'w') as f:
            for pth in parts: f.write(f"file '{os.path.abspath(pth)}'\n")
        final = os.path.join(outdir, f'{ep}.mp4')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(outdir, 'parts.txt'),
                        '-i', os.path.join(outdir, 'mix.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100',
                        '-shortest', '-movflags', '+faststart', final], check=True)
        for pth in parts: os.remove(pth)
        print('done', final, round(total, 1), 's')
