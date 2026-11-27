# Episode: Why do cats always land on their feet?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why do cats always land on their feet?"
SLUG = 'cats'
CAPTION = ("In 1894 a falling cat seemed to break the laws of physics 🐈 Here's how it cheats. "
           "#science #didyouknow #learnontiktok #cats #physics #facts")
SOURCES = [
    'https://publicdomainreview.org/collection/photographs-of-a-falling-cat-1894',
    'https://www.scu.edu/illuminate/thought-leaders/phil-kesten/why-do-cats-always-land-on-their-feet.html',
    'https://en.wikipedia.org/wiki/Falling_cat_problem',
    'https://www.pbs.org/video/cats-accidentally-solved-a-physics-mystery-fdwwfm/',
    'https://www.everand.com/article/594133707/Cats-Give-The-Laws-Of-Physics-A-Biiiiig-Stretch',
    'https://openculture.com/2019/08/why-a-cat-always-lands-on-its-feet.html',
]
BEATS = [
    ('BIG:CATS|LAND ON|THEIR|FEET.', 'point', "Cats land on their feet. Even when they start upside down."),
    ('uproar',   'shrug', "In eighteen ninety-four, that little trick caused an *uproar* among top scientists in Paris."),
    ('lawq',     'point', "Because it seemed to *break* a law of physics. Stay till the end to see how the cat cheats."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('maxwell',  'shrug', "Even the famous physicist James Clerk Maxwell was puzzled by *cat* turning."),
    ('camera',   'point', "Then a French scientist, Étienne-Jules Marey, built a camera shaped like a *gun*."),
    ('frames',   'down',  "It shot *twelve* pictures every second, fast enough to catch a falling cat."),
    ('photos',   'point', "The photos showed it clearly. Paws up at the start, all four paws *down* at the end."),
    ('nopush',   'shrug', "But the cat wasn't spinning when it was let go, and the air didn't *help* it either."),
    ('law',      'down',  "And here's the law: you can't start spinning in midair with nothing to *push* against."),
    ('skate',    'point', "Think of a figure skater. Arms in, they spin *faster*. Arms out, they slow down."),
    ('tuck',     'up',    "Now the cat's trick. It bends in the *middle*, like two cats glued together."),
    ('tuck2',    'point', "It tucks its front legs in, so the *front* half spins fast."),
    ('tuck3',    'down',  "The back legs stick out, so the back half barely turns the *other* way."),
    ('swap',     'point', "Then it swaps. Back legs tuck, front legs stretch, and the *rear* catches up."),
    ('zero',     'shrug', "Add it all up, and the total spin is still *zero*. No law broken."),
    ('reflex',   'down',  "Scientists call it the righting *reflex*, and they still argue about the details today."),
    ('outro',    'point', "So cats don't break the laws of physics. They just *bend* in the middle."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

FUR = (255, 170, 80); FUR_D = (215, 120, 40)

def side_cat(d, cx, cy, s=1.0, front=0.0, back=0.0, bend=0.0, tuck_front=False, tuck_back=False):
    """cat seen from the side, falling. front/back = rotation (radians) of each half around the body axis,
    shown as how far the legs point down (0 = legs up, pi = legs down)."""
    # back half
    bx, fx = cx + 70 * s, cx - 70 * s
    by = cy + 20 * bend * s; fy = cy - 20 * bend * s
    d.ellipse([bx - 95 * s, by - 60 * s, bx + 85 * s, by + 60 * s], fill=FUR, outline=INK, width=int(7 * s))
    d.ellipse([fx - 85 * s, fy - 60 * s, fx + 95 * s, fy + 60 * s], fill=FUR, outline=INK, width=int(7 * s))
    def legs(x, y, rot, tuck, sgn):
        L = (45 if tuck else 95) * s
        dirx, diry = math.sin(rot) * 0.4, -math.cos(rot)
        for off in (-30, 25):
            x0, y0 = x + off * s, y + diry * 40 * s
            d.line([(x0, y0), (x0 + dirx * L, y0 + diry * L)], fill=INK, width=int(26 * s))
            d.line([(x0, y0), (x0 + dirx * L, y0 + diry * L)], fill=FUR_D, width=int(16 * s))
    legs(bx, by, back, tuck_back, 1)
    legs(fx, fy, front, tuck_front, -1)
    # tail
    tdir = -math.cos(back)
    d.line([(bx + 80 * s, by), (bx + 150 * s, by - 50 * s * tdir), (bx + 170 * s, by - 120 * s * tdir)], fill=FUR_D, width=int(18 * s), joint='curve')
    # head
    hx, hy = fx - 110 * s, fy - 20 * s * math.cos(front)
    d.ellipse([hx - 55 * s, hy - 50 * s, hx + 55 * s, hy + 50 * s], fill=FUR, outline=INK, width=int(7 * s))
    ey = -15 if math.cos(front) > 0 else 15
    d.ellipse([hx - 30 * s, hy + ey * s - 8 * s, hx - 14 * s, hy + ey * s + 8 * s], fill=INK)
    up = -1 if math.cos(front) > 0 else 1
    d.polygon([(hx + 10 * s, hy + up * 40 * s), (hx + 40 * s, hy + up * 80 * s), (hx + 45 * s, hy + up * 25 * s)], fill=FUR, outline=INK)

def v_uproar(lt, b):
    im, d = X.new_card()
    title(d, 'PARIS, 1894')
    for i, x in enumerate((200, 470, 740)):
        head(d, x, 390, 0.7, mouth='o' if (lt * 2 + i) % 2 < 1 else 'sad')
        label(d, (x + 60, 240), '!', 90, PINK, FA, stroke=3)
    sub(d, 'French Academy of Sciences', 610)
    return im

def v_lawq(lt, b):
    im, d = X.new_card()
    title(d, 'BREAKING PHYSICS?')
    side_cat(d, 380, 380, 0.9, front=0.6 * lt, back=0.3 * lt, bend=1)
    d.ellipse([640, 240, 860, 460], fill=(60, 55, 80), outline=INK, width=8)
    label(d, (750, 350), '?', 170, YEL, FA, stroke=6)
    return im

def v_maxwell(lt, b):
    im, d = X.new_card()
    title(d, 'J. C. MAXWELL')
    head(d, 300, 380, 0.95, mouth='flat')
    d.chord([170, 400, 430, 560], 0, 180, fill=(140, 140, 150), outline=INK, width=6)   # beard
    label(d, (650, 330), 'famous', 60, INK, FB)
    label(d, (650, 410), 'physicist', 60, INK, FB)
    label(d, (650, 500), '...puzzled', 56, PINK, FA)
    return im

def v_camera(lt, b):
    im, d = X.new_card()
    title(d, 'CAMERA GUN')
    d.rounded_rectangle([150, 330, 640, 420], 30, fill=DGREY, outline=INK, width=8)
    d.polygon([(260, 420), (330, 420), (300, 560), (230, 560)], fill=BROWN, outline=INK)
    d.ellipse([560, 300, 700, 450], fill=INK); d.ellipse([595, 335, 665, 415], fill=CYAN)
    d.rounded_rectangle([340, 250, 520, 330], 20, fill=(200, 200, 210), outline=INK, width=6)
    label(d, (470, 610), 'Étienne-Jules Marey', 48, INK, FB)
    return im

def v_frames(lt, b):
    im, d = X.new_card()
    title(d, '12 PER SECOND')
    n = min(12, int(lt * 8) + 1)
    for i in range(12):
        x = 110 + (i % 6) * 125; y = 220 + (i // 6) * 190
        d.rounded_rectangle([x, y, x + 110, y + 150], 14, fill=WHITE if i < n else (225, 220, 212), outline=INK, width=5)
        if i < n:
            r = math.pi * i / 11
            cx, cy = x + 55, y + 75
            d.ellipse([cx - 38, cy - 20, cx + 38, cy + 20], fill=FUR, outline=INK, width=3)
            for off in (-18, 18):
                d.line([(cx + off, cy), (cx + off + 10 * math.sin(r), cy - 40 * math.cos(r))], fill=FUR_D, width=7)
    return im

def v_photos(lt, b):
    im, d = X.new_card()
    title(d, 'PAWS UP -> PAWS DOWN', 80)
    side_cat(d, 260, 380, 0.75, front=0, back=0)
    arrow(d, (430, 380), (530, 380), INK, 12, 30)
    side_cat(d, 720, 380, 0.75, front=math.pi, back=math.pi)
    return im

def v_nopush(lt, b):
    im, d = X.new_card()
    title(d, 'NO SPIN, NO HELP')
    side_cat(d, 330, 360, 0.8, 0, 0)
    for k in range(3):
        y = 250 + k * 90
        ph = (lt * 1.5 + k / 3) % 1
        d.line([(620 + 200 * ph, y), (680 + 200 * ph, y)], fill=CYAN, width=8)
    label(d, (720, 560), 'air: no help', 50, INK, FB)
    return im

def v_law(lt, b):
    im, d = X.new_card()
    title(d, 'THE RULE')
    d.ellipse([170, 230, 370, 430], outline=INK, width=8)
    arrow(d, (370, 320), (360, 360), INK, 8, 26)
    cross(d, 270, 330, 110, 16)
    label(d, (640, 300), 'no push =', 58, INK, FA)
    label(d, (640, 380), 'no spin', 58, PINK, FA)
    sub(d, 'conservation of angular momentum', 590, 42)
    return im

def skater(d, cx, cy, s, arms_out, lt):
    d.ellipse([cx - 30 * s, cy - 150 * s, cx + 30 * s, cy - 90 * s], fill=SKIN, outline=INK, width=6)
    d.polygon([(cx, cy - 90 * s), (cx - 50 * s, cy + 40 * s), (cx + 50 * s, cy + 40 * s)], fill=PINK, outline=INK)
    d.line([(cx, cy + 40 * s), (cx, cy + 140 * s)], fill=INK, width=10)
    L = (140 if arms_out else 40) * s
    d.line([(cx - L, cy - 60 * s), (cx + L, cy - 60 * s)], fill=INK, width=10)
    for k in range(3 if not arms_out else 1):
        a = lt * (8 if not arms_out else 2) + k * 2.1
        d.arc([cx - 120 * s, cy + 100 * s, cx + 120 * s, cy + 170 * s], math.degrees(a) % 360, (math.degrees(a) + 40) % 360, fill=CYAN, width=8)

def v_skate(lt, b):
    im, d = X.new_card()
    title(d, 'SKATER TRICK')
    skater(d, 260, 380, 1.0, False, lt); label(d, (260, 610), 'arms in: FAST', 44, INK, FB)
    skater(d, 680, 380, 1.0, True, lt); label(d, (680, 610), 'arms out: slow', 44, INK, FB)
    return im

def v_tuck(lt, b):
    im, d = X.new_card()
    v = b['vis']
    if v == 'tuck':
        title(d, 'BEND IN THE MIDDLE', 84)
        side_cat(d, 470, 390, 1.15, 0.3 * math.sin(lt * 2), -0.3 * math.sin(lt * 2), bend=1)
    elif v == 'tuck2':
        title(d, 'FRONT: TUCK + SPIN', 84)
        k = min(1, lt / 2.0)
        side_cat(d, 470, 390, 1.15, front=k * math.pi, back=0.2 * k, bend=1, tuck_front=True)
        X.waves(d, 280, 390, lt, PINK, 3)
    elif v == 'tuck3':
        title(d, 'BACK: LEGS OUT', 88)
        side_cat(d, 470, 390, 1.15, front=math.pi, back=-0.25, bend=1, tuck_front=True)
    else:
        title(d, 'SWAP!')
        k = min(1, lt / 2.0)
        side_cat(d, 470, 390, 1.15, front=math.pi - 0.15 * k, back=-0.25 + (math.pi + 0.25) * k, bend=1 - k, tuck_back=True)
        X.waves(d, 660, 390, lt, CYAN, 3)
    return im

def v_zero(lt, b):
    im, d = X.new_card()
    title(d, 'TOTAL SPIN = 0')
    label(d, (250, 350), '+ front', 64, PINK, FA)
    label(d, (470, 350), '-', 90, INK, FA)
    label(d, (690, 350), 'back', 64, CYAN, FA)
    badge(d, 470, 520, 'NO LAW BROKEN', 64, GRN, lt)
    return im

def v_reflex(lt, b):
    im, d = X.new_card()
    title(d, 'RIGHTING REFLEX', 88)
    k = (lt * 0.5) % 1
    side_cat(d, 470, 360 + 60 * k, 1.0, front=math.pi * min(1, k * 2), back=math.pi * min(1, max(0, k * 2 - 0.4)), bend=1)
    sub(d, 'still debated today', 625)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, 'JUST BEND IT')
    cat(d, 470, 390, 1.1, FUR, lt)
    return im

VISUALS = {'uproar': v_uproar, 'lawq': v_lawq, 'maxwell': v_maxwell, 'camera': v_camera, 'frames': v_frames, 'photos': v_photos,
           'nopush': v_nopush, 'law': v_law, 'skate': v_skate, 'tuck': v_tuck, 'tuck2': v_tuck, 'tuck3': v_tuck, 'swap': v_tuck,
           'zero': v_zero, 'reflex': v_reflex, 'outro': v_outro}
