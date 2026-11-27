# Episode: Why does popcorn pop?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why does popcorn pop?"
SLUG = 'popcorn'
CAPTION = ("That POP isn't the shell cracking 🍿 Scientists filmed it at 2,900 frames per second. "
           "#science #didyouknow #learnontiktok #popcorn #physics #facts")
SOURCES = [
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC4345489/',
    'https://royalsociety.org/blog/2015/02/the-science-of-popcorn',
    'https://physicstoday.aip.org/backscatter/popcorn-gymnastics',
    'https://www.scientificamerican.com/article/popcorn-physics-101-how-a-kernel-pops/',
    'https://www.cbsnews.com/news/the-secret-acrobatics-of-popcorn-revealed',
]
BEATS = [
    ('BIG:THAT POP?|IT ISN\'T|THE SHELL|CRACKING.', 'point', "That pop? It isn't the shell cracking."),
    ('camera',   'shrug', "Scientists in France filmed popcorn at two thousand nine hundred *frames* per second to find out."),
    ('legq',     'point', "And they caught popcorn jumping with a tiny *leg*. Stay till the end."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('kernel',   'point', "Every kernel hides a little *water*. About fourteen percent."),
    ('moist',    'shrug', "That's on purpose. Popcorn makers aim for *exactly* that much moisture."),
    ('steam',    'down',  "Heat it past boiling, and that water turns to *steam*."),
    ('cooker',   'point', "But the shell is so tough, it traps the steam. It's a tiny *pressure* cooker."),
    ('bar',      'down',  "Inside, the pressure climbs to about *ten* times normal air pressure."),
    ('temp',     'shrug', "Then, at around one hundred eighty degrees Celsius, the shell finally *rips*."),
    ('temp2',    'point', "Big kernel, small kernel, weird shape? They all pop at that *same* temperature."),
    ('foam',     'down',  "The starch inside explodes into white *foam* in a few hundredths of a second."),
    ('sound',    'point', "And the pop? It comes *after* the crack."),
    ('sound2',   'down',  "Steam rushes out, and the kernel *rings* like a tiny instrument."),
    ('leg',      'up',    "Now, that leg. The first bit of foam bursts out and *slams* into the pan."),
    ('leg2',     'point', "It pushes off like a gymnast, and the popcorn *flips* through the air."),
    ('between',  'shrug', "The scientists say it jumps halfway between an exploding seed pod and an *animal* with muscles."),
    ('height',   'down',  "Some jump a few millimeters. Others fly *several* centimeters high!"),
    ('effort',   'shrug', "The team filmed around *four* hundred kernels, one by one. Tough job."),
    ('billion',  'up',    "Worth it. People in the US alone eat more than *seventeen* billion quarts of popcorn a year."),
    ('outro',    'point', "So next movie night, you're snacking on tiny steam-powered *gymnasts*."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

CORN = (255, 200, 70); CORN_D = (220, 140, 40); FOAM = (255, 250, 235)

def kernel(d, cx, cy, s=1.0, ang=0.0):
    pts = []
    for k in range(24):
        a = k / 24 * 2 * math.pi
        r = (95 if math.sin(a) > 0 else 70) * s
        x, y = r * 0.8 * math.cos(a), r * math.sin(a)
        ca, sa = math.cos(ang), math.sin(ang)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    d.polygon(pts, fill=CORN, outline=INK)
    d.line(pts + [pts[0]], fill=INK, width=int(7 * s))
    d.ellipse([cx - 20 * s, cy + 40 * s, cx + 20 * s, cy + 75 * s], fill=CORN_D)

def popped(d, cx, cy, s=1.0, rot=0.0):
    rr = [(0, 0, 70), (-55, -40, 50), (55, -45, 52), (-50, 40, 48), (50, 45, 50), (0, -70, 45), (0, 70, 42)]
    for (x, y, r) in rr:
        a = rot
        X2 = x * math.cos(a) - y * math.sin(a); Y2 = x * math.sin(a) + y * math.cos(a)
        d.ellipse([cx + X2 * s - r * s, cy + Y2 * s - r * s, cx + X2 * s + r * s, cy + Y2 * s + r * s], fill=FOAM, outline=INK, width=int(6 * s))
    d.ellipse([cx - 22 * s, cy - 16 * s, cx + 22 * s, cy + 16 * s], fill=CORN)

def pan(d, y=560):
    d.rounded_rectangle([120, y, 820, y + 40], 16, fill=DGREY, outline=INK, width=6)
    d.rectangle([820, y + 10, 920, y + 28], fill=INK)

def v_camera(lt, b):
    im, d = X.new_card()
    title(d, '2,900 FPS')
    d.rounded_rectangle([140, 260, 480, 480], 30, fill=DGREY, outline=INK, width=8)
    d.ellipse([400, 300, 560, 460], fill=INK); d.ellipse([435, 335, 525, 425], fill=CYAN)
    if (lt * 2) % 1 < 0.5: d.ellipse([170, 280, 200, 310], fill=RED)
    kernel(d, 740, 380, 0.9, 0.3 * math.sin(lt * 3))
    sub(d, 'super slow motion', 610)
    return im

def v_legq(lt, b):
    im, d = X.new_card()
    title(d, 'A LEG?!')
    popped(d, 400, 330, 1.0, 0.2)
    d.rounded_rectangle([460, 380, 520, 560], 26, fill=FOAM, outline=INK, width=6)
    d.ellipse([560, 200, 820, 460], fill=(60, 55, 80), outline=INK, width=8)
    label(d, (690, 330), '?', 200, YEL, FA, stroke=6)
    return im

def v_kernel(lt, b):
    im, d = X.new_card()
    title(d, '~14% WATER')
    kernel(d, 300, 380, 2.0)
    for k in range(6):
        a = k / 6 * 2 * math.pi + lt
        x, y = 300 + 60 * math.cos(a), 360 + 80 * math.sin(a)
        d.ellipse([x - 16, y - 22, x + 16, y + 22], fill=CYAN, outline=INK, width=4)
    label(d, (690, 330), 'hidden', 60, INK, FA)
    label(d, (690, 410), 'water', 60, CYAN, FA, stroke=3)
    return im

def v_moist(lt, b):
    im, d = X.new_card()
    title(d, 'JUST RIGHT')
    k = ease_out(min(1, lt / 1.2))
    bars(d, [('too dry', 0.35, YEL, 'DUDS'), ('13-14.5%', 0.9 * k + 0.05, GRN, 'BEST'), ('too wet', 0.5, CYAN, 'MEH')], x0=360, y0=230, w=480, h=64, gap=130, k=1)
    return im

def v_between(lt, b):
    im, d = X.new_card()
    title(d, 'HALF PLANT, HALF ATHLETE', 72)
    # seed pod
    d.ellipse([110, 250, 290, 480], fill=GRN, outline=INK, width=7)
    for k in range(4):
        a = k / 4 * 6.28 + lt * 2
        d.ellipse([200 + 110 * math.cos(a) - 12, 365 + 110 * math.sin(a) - 12, 200 + 110 * math.cos(a) + 12, 365 + 110 * math.sin(a) + 12], fill=BROWN)
    popped(d, 470, 370, 0.9, lt)
    # stick-figure jumper
    jy = -40 * abs(math.sin(lt * 3))
    cx = 740
    d.ellipse([cx - 32, 250 + jy, cx + 32, 314 + jy], fill=SKIN, outline=INK, width=6)
    d.line([(cx, 314 + jy), (cx, 420 + jy)], fill=INK, width=12)
    d.line([(cx - 60, 330 + jy), (cx + 60, 330 + jy)], fill=INK, width=10)
    d.line([(cx, 420 + jy), (cx - 45, 500 + jy)], fill=INK, width=10); d.line([(cx, 420 + jy), (cx + 45, 500 + jy)], fill=INK, width=10)
    label(d, (200, 560), 'seed pod', 42, INK, FB); label(d, (740, 560), 'muscles', 42, INK, FB)
    return im

def v_billion(lt, b):
    im, d = X.new_card()
    title(d, '17 BILLION QUARTS')
    for k in range(12):
        x = 140 + (k % 6) * 132; y = 250 + (k // 6) * 190
        bob = 6 * math.sin(lt * 4 + k)
        d.polygon([(x - 45, y + bob), (x + 45, y + bob), (x + 32, y + 120 + bob), (x - 32, y + 120 + bob)], fill=WHITE, outline=INK)
        for j in range(3): d.rectangle([x - 40 + j * 28, y + bob, x - 28 + j * 28, y + 118 + bob], fill=RED)
        popped(d, x, y - 10 + bob, 0.35, k)
    sub(d, 'every year, US only', 630)
    return im

def v_steam(lt, b):
    im, d = X.new_card()
    v = b['vis']
    title(d, {'steam': 'WATER -> STEAM', 'cooker': 'PRESSURE COOKER'}[v])
    kernel(d, 330, 400, 1.8, 0.05 * math.sin(lt * 20) if v == 'cooker' else 0)
    for k in range(7):
        a = k / 7 * 2 * math.pi + lt * 2
        x, y = 330 + 55 * math.cos(a), 390 + 70 * math.sin(a)
        d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=(235, 240, 250), outline=INK, width=4)
    if v == 'steam':
        thermo(d, 720, 360, 300, min(1, lt / 1.5))
        label(d, (720, 600), '100 °C+', 50, INK, FA)
    else:
        for ang in (-0.6, 0, 0.6):
            x0, y0 = 330 + 170 * math.sin(ang), 400 - 200 * math.cos(ang)
            arrow(d, (330 + 120 * math.sin(ang), 400 - 140 * math.cos(ang)), (x0, y0), RED, 10, 26)
        label(d, (720, 380), 'trapped!', 66, RED, FA)
    return im

def v_bar(lt, b):
    im, d = X.new_card()
    title(d, '10x AIR PRESSURE')
    k = ease_out(min(1, lt / 1.5))
    cx, cy, r = 470, 390, 190
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=WHITE, outline=INK, width=8)
    for i in range(11):
        a = math.pi + i / 10 * math.pi
        d.line([(cx + (r - 30) * math.cos(a), cy + (r - 30) * math.sin(a)), (cx + (r - 8) * math.cos(a), cy + (r - 8) * math.sin(a))], fill=INK, width=6)
    a = math.pi + k * 0.92 * math.pi
    d.line([(cx, cy), (cx + (r - 40) * math.cos(a), cy + (r - 40) * math.sin(a))], fill=RED, width=12)
    d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=INK)
    label(d, (cx, cy + 90), f'{int(1 + 9 * k)} bar', 80, INK, FA)
    return im

def v_temp(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'temp':
        title(d, '180 °C: RIP!')
        thermo(d, 220, 360, 320, min(1, 0.5 + lt / 2))
        if lt < 0.8: kernel(d, 620, 380, 1.6)
        else: popped(d, 620, 380, 1.4 * min(1, (lt - 0.8) / 0.3 + 0.3), 0.2)
    else:
        title(d, 'ALL AT 180 °C')
        for i, (x, s) in enumerate(((210, 1.3), (470, 0.8), (730, 1.05))):
            kernel(d, x, 360, s, i * 0.6)
        label(d, (470, 560), 'big  •  small  •  weird', 52, INK, FB)
    return im

def v_foam(lt, b):
    im, d = X.new_card()
    title(d, 'STARCH FOAM')
    k = ease_back(min(1, lt / 0.4))
    kernel(d, 250, 390, 1.3)
    arrow(d, (360, 390), (520, 390), INK, 12, 34)
    popped(d, 700, 380, 1.6 * k, lt * 0.5)
    sub(d, 'in hundredths of a second', 620)
    return im

def v_sound(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'sound':
        title(d, 'CRACK, THEN POP')
        label(d, (260, 330), '1. crack', 64, INK, FA)
        label(d, (660, 330), '2. pop!', 64, PINK, FA)
        arrow(d, (390, 330), (540, 330), INK, 10, 30)
        kernel(d, 260, 480, 0.8); popped(d, 660, 480, 0.8)
    else:
        title(d, 'IT RINGS!')
        popped(d, 330, 390, 1.4, 0.1)
        X.waves(d, 520, 390, lt, PINK, 4)
        for k in range(4):
            ph = (lt * 1.5 + k / 4) % 1
            d.ellipse([400 + 300 * ph, 220 - 40 * ph, 440 + 300 * ph, 260 - 40 * ph], fill=(235, 240, 250), outline=INK, width=3)
    return im

def v_leg(lt, b):
    im, d = X.new_card()
    v = b['vis']
    pan(d)
    if v == 'leg':
        title(d, 'THE LEG')
        popped(d, 470, 380, 1.0, 0.2)
        ext = min(1, lt / 0.6)
        d.rounded_rectangle([445, 420, 505, 420 + 140 * ext], 28, fill=FOAM, outline=INK, width=6)
    else:
        title(d, 'GYMNAST FLIP')
        ph = (lt * 0.7) % 1
        for k in range(4):
            p = max(0, ph - k * 0.08)
            x = 250 + 450 * p; y = 520 - 270 * math.sin(math.pi * p)
            if k == 0: popped(d, x, y, 0.7, p * 6.28)
            else: d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(200, 195, 190))
    return im

def v_height(lt, b):
    im, d = X.new_card()
    title(d, 'MM TO CM')
    pan(d)
    for i, (x, hgt) in enumerate(((260, 40), (470, 160), (680, 300))):
        ph = abs(math.sin(lt * 2 + i))
        popped(d, x, 510 - hgt * ph, 0.55, lt * 3 + i)
    return im

def v_effort(lt, b):
    im, d = X.new_card()
    title(d, '~400 KERNELS')
    for i in range(40):
        x = 140 + (i % 10) * 74; y = 200 + (i // 10) * 90
        if i < min(40, int(lt * 30)): popped(d, x, y + 40, 0.32, i)
        else: kernel(d, x, y + 40, 0.32)
    sub(d, '5 min to film + 10 min to analyze, EACH', 610, 40)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, 'STEAM GYMNASTS')
    # bowl
    d.pieslice([170, 260, 770, 640], 0, 180, fill=RED, outline=INK, width=8)
    for k in range(9):
        x = 230 + k * 60; y = 430 - 30 * abs(math.sin(k * 1.3))
        popped(d, x, y, 0.45, k)
    ph = (lt * 0.8) % 1
    popped(d, 470 + 200 * ph, 300 - 160 * math.sin(math.pi * ph), 0.5, ph * 6)
    return im

VISUALS = {'camera': v_camera, 'legq': v_legq, 'kernel': v_kernel, 'steam': v_steam, 'cooker': v_steam, 'bar': v_bar,
           'temp': v_temp, 'temp2': v_temp, 'foam': v_foam, 'sound': v_sound, 'sound2': v_sound, 'leg': v_leg, 'leg2': v_leg,
           'height': v_height, 'effort': v_effort, 'outro': v_outro, 'moist': v_moist, 'between': v_between, 'billion': v_billion}
