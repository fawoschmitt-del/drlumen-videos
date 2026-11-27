# Episode: Why do we get goosebumps?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why do we get goosebumps?"
SLUG = 'goosebumps'
CAPTION = ("Goosebumps have a secret second job, and Harvard scientists found it 🥶 "
           "#science #didyouknow #learnontiktok #goosebumps #body #facts")
SOURCES = [
    'https://www.nih.gov/news-events/nih-research-matters/what-goosebumps-are',
    'https://www.hsci.harvard.edu/goosebumps-hair-follicle-stem-cells',
    'https://pubmed.ncbi.nlm.nih.gov/32679029/',
    'https://www.health.harvard.edu/blog/wondering-about-goosebumps-of-course-you-are-2020080320688',
    'https://www.livescience.com/32349-what-causes-goose-bumps.html',
    'https://askdruniverse.wsu.edu/2021/03/09/why-do-we-get-goosebumps/',
    'https://acibademinternational.com/blog/goosebumps-the-evolutionary-leftover-you-still-wear/',
]
BEATS = [
    ('BIG:STEP OUT|OF A WARM|SHOWER.|BUMPS!', 'point', "Step out of a warm shower. Bumps everywhere!"),
    ('muscle',   'shrug', "Here's what happened: every hair on your skin has its own tiny *muscle*. And it just pulled."),
    ('secretq',  'point', "And scientists at Harvard found goosebumps have a secret second *job*. Stay till the end."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('pull',     'point', "When you're cold or scared, your nerves tell those muscles to *squeeze*."),
    ('stand',    'down',  "The hair stands up, and the skin around it bunches into a little *bump*."),
    ('fur',      'shrug', "In furry animals, that fluffs up the fur and traps a warm layer of *air*."),
    ('jacket',   'point', "Basically a built-in puffer *jacket*."),
    ('scared',   'down',  "Scared? Fluffy fur also makes an animal look *bigger*. Think of a cat that meets a dog."),
    ('porcupine','up',    "The champion of puffing up? The *porcupine*."),
    ('ancestors','shrug', "Our ancestors were way hairier, so it really *worked* for them."),
    ('leftover', 'down',  "For us, with thin body hair, it's mostly a *leftover*. Like your tailbone."),
    ('palms',    'point', "Fun test: your palms never get goosebumps. No hairs, no *muscles*."),
    ('harvard',  'up',    "Now, the secret job. In twenty twenty, Harvard scientists zoomed into *mouse* skin."),
    ('wrap',     'point', "The nerve that triggers goosebumps also wraps around hair *stem* cells, like a ribbon."),
    ('grow',     'down',  "When the cold lasts a long time, that nerve wakes the stem cells up, and they grow new *hair*."),
    ('bridge',   'shrug', "And the goosebump muscle holds it all together. Without it, the *connection* falls apart."),
    ('outro',    'point', "So goosebumps aren't useless. Your body is trying to knit you a *fur* coat."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

def skin_section(d, x0, x1, y, lt, k, hair_len=120, n=3, show_muscle=True, nerve=False, stem=0.0):
    """skin cross-section with n hairs; k = 0 (flat) .. 1 (goosebump)"""
    pts = []
    for i in range(81):
        x = x0 + (x1 - x0) * i / 80
        bump = sum(math.exp(-((x - (x0 + (x1 - x0) * (j + 0.5) / n)) / 45) ** 2) for j in range(n))
        pts.append((x, y - 40 * k * bump))
    d.polygon(pts + [(x1, y + 220), (x0, y + 220)], fill=SKIN)
    d.line(pts, fill=INK, width=8)
    for j in range(n):
        hx = x0 + (x1 - x0) * (j + 0.5) / n
        # follicle
        d.ellipse([hx - 22, y + 70, hx + 22, y + 150], fill=(240, 170, 140), outline=INK, width=5)
        ang = math.radians(35 - 30 * k)       # leaning hair -> upright
        top = (hx + hair_len * math.sin(ang), y - 40 * k - hair_len * math.cos(ang))
        d.line([(hx, y + 110), (hx, y - 40 * k), top], fill=INK, width=7)
        if show_muscle:
            mx, my = hx + 70 - 15 * k, y + 30
            d.line([(hx + 10, y + 120), (mx, my)], fill=RED, width=int(12 + 6 * k))
        if nerve:
            d.arc([hx - 45, y + 80, hx + 45, y + 170], 0, 360, fill=GRN, width=6)
        if stem > 0:
            r = 16 + 8 * stem
            d.ellipse([hx - r, y + 140 - r, hx + r, y + 140 + r], fill=CYAN, outline=INK, width=4)

def v_muscle(lt, b):
    im, d = X.new_card()
    title(d, 'TINY HAIR MUSCLES', 86)
    k = 0.5 + 0.5 * math.sin(lt * 3)
    skin_section(d, 60, 880, 330, lt, k)
    return im

def v_secretq(lt, b):
    im, d = X.new_card()
    title(d, 'SECRET JOB?')
    skin_section(d, 60, 520, 330, lt, 1.0, n=2)
    d.ellipse([600, 230, 860, 490], fill=(60, 55, 80), outline=INK, width=8)
    label(d, (730, 360), '?', 180, YEL, FA, stroke=6)
    return im

def v_pull(lt, b):
    im, d = X.new_card()
    v = b['vis']
    k = ease_out(min(1, lt / 1.0))
    title(d, 'SQUEEZE!' if v == 'pull' else 'HAIR UP = BUMP')
    skin_section(d, 60, 880, 330, lt, k if v == 'pull' else 1.0)
    if v == 'pull':
        for x in (200, 470, 740):
            arrow(d, (x + 90, 380), (x + 55, 350), INK, 6, 18)
    return im

def furball(d, cx, cy, r, k, col=BROWN, lt=0.0):
    pts = []
    for i in range(60):
        a = i / 60 * 2 * math.pi
        rr = r * (1 + 0.25 * k) * (1.0 if i % 2 else 0.88 + 0.05 * math.sin(lt * 3 + i))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=col, outline=INK)
    d.line(pts + [pts[0]], fill=INK, width=6)

def v_fur(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'fur':
        title(d, 'FLUFF = WARM AIR')
        k = ease_out(min(1, lt / 1.2))
        furball(d, 470, 380, 150, k, BROWN, lt)
        d.ellipse([400, 320, 540, 440], fill=SKIN, outline=INK, width=6)
        for i in range(8):
            a = i / 8 * 6.28 + lt
            x, y = 470 + 120 * k * math.cos(a), 380 + 120 * k * math.sin(a)
            d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=ORANGE)
    else:
        title(d, 'PUFFER JACKET')
        d.rounded_rectangle([300, 200, 640, 560], 60, fill=CYAN, outline=INK, width=8)
        for k in range(5): d.line([(310, 250 + k * 65), (630, 250 + k * 65)], fill=INK, width=5)
        d.rectangle([460, 200, 480, 560], fill=INK)
    return im

def v_scared(lt, b):
    im, d = X.new_card()
    title(d, 'LOOK BIGGER!')
    k = ease_out(min(1, lt / 0.8))
    cat(d, 300, 400, 0.85 + 0.15 * k, (90, 90, 100), lt, puffed=k > 0.5)
    dog(d, 700, 410, 0.7, lt)
    return im

def v_porcupine(lt, b):
    im, d = X.new_card()
    title(d, 'CHAMPION: PORCUPINE', 82)
    k = 0.6 + 0.4 * abs(math.sin(lt * 2))
    cx, cy = 450, 430
    for i in range(26):
        a = math.pi + i / 25 * math.pi
        L = (150 + 60 * k)
        d.line([(cx + 120 * math.cos(a), cy + 90 * math.sin(a)), (cx + L * 1.3 * math.cos(a), cy + L * math.sin(a))], fill=INK, width=8)
        d.line([(cx + 120 * math.cos(a), cy + 90 * math.sin(a)), (cx + (L * 1.3 - 30) * math.cos(a), cy + (L - 25) * math.sin(a))], fill=(235, 230, 215), width=5)
    d.ellipse([cx - 190, cy - 110, cx + 190, cy + 110], fill=BROWN, outline=INK, width=7)
    d.ellipse([cx - 260, cy - 30, cx - 150, cy + 70], fill=(190, 140, 100), outline=INK, width=6)
    d.ellipse([cx - 225, cy - 5, cx - 205, cy + 15], fill=INK)
    return im

def v_ancestors(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'ancestors':
        title(d, 'HAIRY ANCESTORS')
        furball(d, 300, 390, 140, 0.4, BROWN, lt)
        head(d, 300, 390, 0.55)
        check(d, 680, 380, 90)
    else:
        title(d, 'A LEFTOVER')
        head(d, 300, 390, 0.95)
        label(d, (680, 330), 'like your', 54, INK, FB)
        label(d, (680, 420), 'TAILBONE', 74, PINK, FA)
    return im

def v_palms(lt, b):
    im, d = X.new_card()
    title(d, 'NO BUMPS HERE')
    X.palm(d, 470, 420, 1.3)
    check(d, 760, 300, 60, 16, GRN)
    label(d, (760, 420), 'no hair', 48, INK, FB)
    return im

def v_harvard(lt, b):
    im, d = X.new_card()
    title(d, 'HARVARD, 2020')
    X.rat(d, 330, 400, 0.65)
    # microscope
    d.rounded_rectangle([630, 470, 830, 510], 12, fill=DGREY, outline=INK, width=6)
    d.line([(760, 490), (760, 300)], fill=INK, width=18)
    d.line([(700, 400), (780, 240)], fill=INK, width=34); d.line([(700, 400), (780, 240)], fill=(200, 205, 220), width=22)
    d.ellipse([665, 395, 735, 425], fill=CYAN, outline=INK, width=5)
    sub(d, 'mouse skin, super zoomed in', 620)
    return im

def v_wrap(lt, b):
    im, d = X.new_card()
    v = b['vis']
    if v == 'wrap':
        title(d, 'NERVE + STEM CELLS', 84)
        skin_section(d, 140, 800, 300, lt, 0.4, n=2, nerve=True, stem=0.3)
        label(d, (800, 560), 'nerve', 44, GRN, FA)
        label(d, (160, 560), 'stem cells', 44, CYAN, FA, stroke=1)
    elif v == 'grow':
        title(d, 'LONG COLD = NEW HAIR', 82)
        k = ease_out(min(1, lt / 2.0))
        skin_section(d, 140, 800, 360, lt, 0.6, hair_len=60 + 110 * k, n=2, nerve=True, stem=k)
    else:
        title(d, 'MUSCLE = THE BRIDGE', 84)
        skin_section(d, 140, 800, 300, lt, 0.8, n=2, nerve=True, stem=0.3)
        badge(d, 470, 610, 'no muscle = no link', 44, YEL, lt, padx=30, h=80)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, 'KNITTING A FUR COAT', 84)
    k = 0.5 + 0.5 * math.sin(lt * 2)
    furball(d, 470, 390, 150, k, BROWN, lt)
    head(d, 470, 390, 0.6, mouth='smile')
    return im

VISUALS = {'muscle': v_muscle, 'secretq': v_secretq, 'pull': v_pull, 'stand': v_pull, 'fur': v_fur, 'jacket': v_fur,
           'scared': v_scared, 'porcupine': v_porcupine, 'ancestors': v_ancestors, 'leftover': v_ancestors, 'palms': v_palms,
           'harvard': v_harvard, 'wrap': v_wrap, 'grow': v_wrap, 'bridge': v_wrap, 'outro': v_outro}
