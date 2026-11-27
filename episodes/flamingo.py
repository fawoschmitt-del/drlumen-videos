# Episode: Why do flamingos stand on one leg?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why do flamingos stand on one leg?"
SLUG = 'flamingo'
CAPTION = ("Flamingos SLEEP on one leg and wobble LESS when they doze 🦩 Here's the trick. "
           "#science #didyouknow #learnontiktok #flamingo #animals #facts")
SOURCES = [
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC5454233/',
    'https://www.news.gatech.edu/2017/05/24/tech-study-stands-flamingos-unique-pose',
    'https://www.sciencenews.org/article/how-flamingo-balances-one-leg',
    'https://pubmed.ncbi.nlm.nih.gov/19637281/',
    'https://www.smithsonianmag.com/smithsonian-institution/ask-smithsonian-why-flamingos-stand-one-leg-180956323/',
    'https://www.npr.org/sections/thetwo-way/2017/05/25/530046238/scientists-pinpoint-how-a-flamingo-balances-on-one-leg',
    'https://www.livescience.com/5732-flamingos-stand-leg.html',
]
BEATS = [
    ('BIG:STAND|ON ONE LEG.|RIGHT|NOW.', 'point', "Stand on one leg. Right now. Wobbly, right?"),
    ('sleep',    'shrug', "Flamingos stand like that for hours. They even *sleep* like that."),
    ('mystery',  'point', "And scientists found one that balanced without using a single *muscle*. Stay till the end."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('ankle',    'point', "First, that leg that bends backwards? That's not a knee. It's the *ankle*."),
    ('knee',     'down',  "The real knee is hidden way up, under the *feathers*."),
    ('warm',     'shrug', "Idea number one: staying *warm*."),
    ('water',    'down',  "Flamingos spend their days standing in water, and water pulls heat out of a body super *fast*."),
    ('tuck',     'point', "Tuck one leg into your feathers, and that's one less leg losing *heat*."),
    ('philly',   'down',  "At a zoo in Philadelphia, way *more* flamingos stood on one leg in water than on land."),
    ('cold',     'point', "And in cooler weather, even *more* of them did it."),
    ('easy',     'shrug', "Idea number two: for a flamingo, one leg might just be *easier*."),
    ('plate',    'point', "In Atlanta, scientists put eight young flamingos on a plate that measures every tiny *wobble*."),
    ('doze',     'down',  "Awake, they wobbled. But dozing, they barely moved at all. About *three* millimeters!"),
    ('lifeless', 'up',    "Now the crazy part. They tested a flamingo body that was no longer *alive*."),
    ('lifeless2','point', "Placed on one leg, it stayed up on its own. No muscle power at *all*."),
    ('lifeless3','down',  "On two legs? It wasn't *stable*. The body just flopped."),
    ('doorstop', 'point', "Gravity pulls the joints into a locked-in pose, a bit like a *doorstop*."),
    ('outro',    'shrug', "So for a flamingo, one leg isn't a balancing act. It's a *nap*."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

FPINK = (255, 130, 160); FDARK = (215, 80, 120)

def flamingo(d, cx, base, s=1.0, legs=1, lt=0.0, sway=0.0, asleep=False, show_joint=None, zz=True):
    """flamingo standing; base = ground y; legs 1 or 2"""
    s *= 0.72
    bx = cx + sway
    by = base - 330 * s
    knee_y = base - 160 * s
    # legs
    d.line([(bx, by + 50 * s), (bx + 12 * s, knee_y), (cx, base)], fill=FDARK, width=int(12 * s), joint='curve')
    if legs == 2:
        d.line([(bx + 40 * s, by + 50 * s), (bx + 52 * s, knee_y), (cx + 40 * s, base)], fill=FDARK, width=int(12 * s), joint='curve')
        d.ellipse([cx + 20 * s, base - 8 * s, cx + 80 * s, base + 10 * s], fill=FDARK)
    else:   # tucked leg: folded under body
        d.line([(bx + 30 * s, by + 50 * s), (bx + 80 * s, by + 120 * s), (bx + 20 * s, by + 70 * s)], fill=FDARK, width=int(12 * s), joint='curve')
    d.ellipse([cx - 30 * s, base - 8 * s, cx + 30 * s, base + 10 * s], fill=FDARK)
    # body
    d.ellipse([bx - 120 * s, by - 60 * s, bx + 110 * s, by + 70 * s], fill=FPINK, outline=INK, width=int(7 * s))
    d.pieslice([bx - 40 * s, by - 50 * s, bx + 140 * s, by + 60 * s], 300, 60, fill=FDARK)
    if asleep:
        d.ellipse([bx - 70 * s, by - 110 * s, bx + 10 * s, by - 40 * s], fill=FPINK, outline=INK, width=int(6 * s))
        d.arc([bx - 50 * s, by - 90 * s, bx - 20 * s, by - 70 * s], 20, 160, fill=INK, width=int(4 * s))
        for k in range(3 if zz else 0):
            ph = (lt * 0.8 + k / 3) % 1
            label(d, (bx + 60 * s + 60 * ph * s, by - 140 * s - 90 * ph * s), 'z', int((30 + 30 * ph) * s), INK, FA)
    else:
        neck = [(bx - 90 * s, by - 20 * s), (bx - 150 * s, by - 120 * s), (bx - 90 * s, by - 200 * s), (bx - 110 * s, by - 270 * s)]
        d.line(neck, fill=INK, width=int(26 * s), joint='curve')
        d.line(neck, fill=FPINK, width=int(16 * s), joint='curve')
        hx, hy = bx - 110 * s, by - 280 * s
        d.ellipse([hx - 30 * s, hy - 26 * s, hx + 30 * s, hy + 26 * s], fill=FPINK, outline=INK, width=int(6 * s))
        d.polygon([(hx - 20 * s, hy), (hx - 75 * s, hy + 10 * s), (hx - 55 * s, hy + 40 * s)], fill=INK)
        d.ellipse([hx - 6 * s, hy - 12 * s, hx + 6 * s, hy], fill=INK)
    if show_joint == 'ankle':
        d.ellipse([bx + 12 * s - 26, knee_y - 26, bx + 12 * s + 26, knee_y + 26], outline=PINK, width=8)
    if show_joint == 'knee':
        d.ellipse([bx + 30 * s - 30, by + 10 * s - 30, bx + 30 * s + 30, by + 10 * s + 30], outline=CYAN, width=9)

def water(d, lt, y=520):
    pts = [(10 + i * 920 / 30, y + 10 * math.sin(i * 0.9 + lt * 3)) for i in range(31)]
    d.polygon(pts + [(920, 660), (10, 660)], fill=(120, 200, 255))
    d.line(pts, fill=INK, width=6)

def v_sleep(lt, b):
    im, d = X.new_card()
    title(d, 'HOURS. ASLEEP.')
    flamingo(d, 470, 600, 1.0, 1, lt, asleep=True)
    return im

def v_mystery(lt, b):
    im, d = X.new_card()
    title(d, 'ZERO MUSCLE?')
    flamingo(d, 330, 600, 0.95, 1, lt)
    d.ellipse([560, 220, 820, 480], fill=(60, 55, 80), outline=INK, width=8)
    label(d, (690, 350), '?', 200, YEL, FA, stroke=6)
    return im

def v_joint(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'ankle':
        title(d, 'THAT\'S AN ANKLE!', 86)
        flamingo(d, 470, 610, 1.0, 1, lt, show_joint='ankle')
        label(d, (720, 500), 'ankle', 60, PINK, FA)
        arrow(d, (660, 500), (500, 495), PINK, 9, 26)
    else:
        title(d, 'KNEE: HIDDEN', 92)
        flamingo(d, 470, 610, 1.0, 1, lt, show_joint='knee')
        label(d, (760, 300), 'knee', 60, CYAN, FA, stroke=2)
        arrow(d, (700, 320), (520, 400), INK, 9, 26)
    return im

def v_warm(lt, b):
    im, d = X.new_card()
    v = b['vis']
    if v == 'warm':
        title(d, 'IDEA 1: WARMTH')
        thermo(d, 250, 360, 320, 0.7)
        flamingo(d, 600, 600, 0.95, 1, lt)
    elif v == 'water':
        title(d, 'WATER STEALS HEAT')
        water(d, lt, 470)
        flamingo(d, 470, 590, 0.9, 2, lt)
        for x in (420, 520):
            for k in range(2):
                ph = (lt * 1.2 + k / 2) % 1
                d.ellipse([x - 14, 500 + 100 * ph, x + 14, 528 + 100 * ph], fill=RED)
    else:
        title(d, 'TUCK = LESS LOSS')
        water(d, lt, 470)
        flamingo(d, 470, 590, 0.9, 1, lt)
        d.ellipse([450, 350, 580, 480], outline=GRN, width=9)
    return im

def v_philly(lt, b):
    im, d = X.new_card()
    k = ease_out(min(1, lt / 1.2))
    if b['vis'] == 'philly':
        title(d, 'ONE LEG: WHERE?', 88)
        bars(d, [('in water', 0.9, CYAN, 'MORE'), ('on land', 0.55, YEL, 'LESS')], x0=360, y0=280, w=480, h=72, gap=160, k=k)
    else:
        title(d, 'COLDER = MORE', 92)
        bars(d, [('warm day', 0.5, ORANGE, 'LESS'), ('cool day', 0.85, CYAN, 'MORE')], x0=360, y0=280, w=480, h=72, gap=160, k=k)
    sub(d, 'birds resting on one leg', 610)
    return im

def v_easy(lt, b):
    im, d = X.new_card()
    title(d, 'IDEA 2: EASIER')
    flamingo(d, 330, 600, 0.95, 1, lt, asleep=True)
    badge(d, 700, 360, 'LESS WORK?', 62, YEL, lt)
    return im

def v_plate(lt, b):
    im, d = X.new_card()
    doze = b['vis'] == 'doze'
    title(d, 'WOBBLE METER' if not doze else 'DOZING: ~3 MM')
    d.rounded_rectangle([250, 560, 690, 600], 12, fill=DGREY, outline=INK, width=6)
    amp = 3 if doze else 28
    flamingo(d, 470, 560, 0.85, 1, lt, sway=amp * math.sin(lt * 4), asleep=doze)
    # trace box
    d.rounded_rectangle([700, 180, 900, 380], 20, fill=WHITE, outline=INK, width=6)
    pts = [(800 + amp * 2.2 * math.sin(i * 0.7 + lt * 3) * math.cos(i * 0.31), 280 + amp * 2.2 * math.cos(i * 0.53 + lt * 2)) for i in range(40)]
    d.line(pts, fill=PINK, width=5)
    label(d, (800, 405), 'sway', 40, INK, FB)
    return im

def v_lifeless(lt, b):
    im, d = X.new_card()
    v = b['vis']
    if v == 'lifeless':
        title(d, 'NO LONGER ALIVE')
        flamingo(d, 470, 600, 1.0, 1, lt, asleep=True, zz=False)
        label(d, (760, 300), 'no muscles', 46, INK, FB)
        label(d, (760, 360), 'working', 46, INK, FB)
    elif v == 'lifeless2':
        title(d, 'ONE LEG: STABLE')
        flamingo(d, 470, 600, 1.0, 1, lt, asleep=True, zz=False)
        check(d, 780, 330, 80)
    else:
        title(d, 'TWO LEGS: FLOP')
        tilt = 30 * math.sin(lt * 3)
        flamingo(d, 470, 600, 1.0, 2, lt, sway=tilt, asleep=True, zz=False)
        cross(d, 780, 330, 80, 18)
    return im

def v_doorstop(lt, b):
    im, d = X.new_card()
    title(d, 'LIKE A DOORSTOP')
    # door + wedge
    ang = 0.25 + 0.03 * math.sin(lt * 4)
    d.rectangle([110, 160, 140, 580], fill=DGREY)
    x2 = 140 + 300 * math.cos(ang); y2 = 160 + 60 * math.sin(ang)
    d.polygon([(140, 160), (x2, y2), (x2, 580 - 40 * math.sin(ang)), (140, 580)], fill=(200, 150, 90), outline=INK)
    d.polygon([(300, 590), (420, 590), (420, 545)], fill=YEL, outline=INK)
    flamingo(d, 690, 600, 0.85, 1, lt, asleep=True)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, 'ONE LEG = NAP TIME', 86)
    flamingo(d, 330, 600, 0.95, 1, lt, asleep=True)
    flamingo(d, 640, 600, 0.95, 1, lt + 1.1, asleep=True)
    return im

VISUALS = {'sleep': v_sleep, 'mystery': v_mystery, 'ankle': v_joint, 'knee': v_joint, 'warm': v_warm, 'water': v_warm,
           'tuck': v_warm, 'philly': v_philly, 'cold': v_philly, 'easy': v_easy, 'plate': v_plate, 'doze': v_plate,
           'lifeless': v_lifeless, 'lifeless2': v_lifeless, 'lifeless3': v_lifeless, 'doorstop': v_doorstop, 'outro': v_outro}
