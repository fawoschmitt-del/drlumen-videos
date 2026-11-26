# Episode: Why do your fingers wrinkle in water?   (fast format, see tickle.py)
import math
import explainer as X
from explainer import INK, YEL, PINK, CYAN, GRN, FA, FI, FB, CW, label, arrow, ease_out, ease_back

TITLE = "Why do your fingers wrinkle in water?"
SLUG = 'fingers'
CAPTION = ("Pruney bath fingers aren't water soaking in. Your nerves do it on purpose 🤯 "
           "#science #didyouknow #learnontiktok #body #facts #bath")
SOURCES = [
    'https://www.ncl.ac.uk/press/articles/archive/2013/01/getagrip-whywegetwrinklyfingersandtoes.html',
    'https://pubmed.ncbi.nlm.nih.gov/24416318/',
    'https://www.smithsonianmag.com/smithsonian-institution/ask-smithsonian-why-do-we-get-prune-fingers-180956024/',
    'https://www.npr.org/sections/thetwo-way/2011/06/29/137506950/why-do-fingers-wrinkle-when-they-get-wet',
    'https://pubmed.ncbi.nlm.nih.gov/12826076/',
]
BEATS = [
    ('BIG:LOOK AT|YOUR FINGERTIPS|AFTER A|LONG BATH.', 'point', "Look at your fingertips after a long bath."),
    ('raisin',   'shrug', "Wrinkly like a raisin, right? Here's the twist: it's not the water. It's your *nerves*."),
    ('macaque',  'point', "And only one other animal is known to get *pruney* fingers. Stay till the end."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('timer',    'down',  "Pruning isn't instant. It starts after about *five* minutes in the water."),
    ('vessels',  'point', "Your nerves tell tiny blood vessels in your fingertips to *squeeze* shut."),
    ('vessels2', 'down',  "The fingertip pads shrink a little, and the skin on top *buckles* into wrinkles."),
    ('nerve',    'point', "Proof? Back in the nineteen thirties, doctors noticed something *weird*."),
    ('nerve2',   'down',  "People with damaged finger nerves soaked their hands, and got *no* wrinkles at all."),
    ('test',     'point', "Doctors have even used a warm soak as a *test* for nerve damage."),
    ('tread',    'shrug', "But why would your body bother? One idea: rain *treads*, like on car tires."),
    ('tread2',   'point', "The wrinkles channel water away, so your fingers grip wet things *better*."),
    ('marbles',  'down',  "In England, people moved wet marbles with soaked hands. Wrinkly fingers were *twelve* percent faster."),
    ('dry',      'point', "And with dry marbles? The wrinkles made *zero* difference."),
    ('berlin',   'shrug', "But a team in Berlin tested forty people and found *no* difference. Scientists are still arguing!"),
    ('macaque2', 'up',    "Now, that other animal. It's the *macaque* monkey!"),
    ('macaque3', 'point', "As far as we know, humans and macaques are the *only* ones with pruney fingers."),
    ('outro',    'shrug', "So next bath, don't panic. Your fingers just put on their *rain* tires."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

SKIN = (255, 205, 170); SKIN_D = (215, 145, 115); RED = (220, 60, 80)

def finger(d, cx, cy, s=1.0, wr=0.0, cut=False):
    """a big fingertip seen from the pad side; wr = 0..1 wrinkle amount"""
    w, h = 250 * s, 440 * s
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], int(w / 2), fill=SKIN, outline=INK, width=int(8 * s))
    d.line([(cx - w / 2 + 20 * s, cy + 70 * s), (cx + w / 2 - 20 * s, cy + 70 * s)], fill=SKIN_D, width=int(6 * s))
    if wr > 0.02:
        for k in range(7):
            y = cy - h / 2 + 50 * s + k * 34 * s
            amp = 14 * s * wr
            pts = [(cx - w / 2 + 22 * s + i * (w - 44 * s) / 12, y + amp * math.sin(i * 1.6 + k)) for i in range(13)]
            d.line(pts, fill=SKIN_D, width=int(6 * s), joint='curve')
    if cut:
        d.line([(cx - w / 2 - 30 * s, cy + 150 * s), (cx + w / 2 + 30 * s, cy + 110 * s)], fill=RED, width=int(18 * s))
        label(d, (cx, cy - 40 * s), 'CUT', int(70 * s), RED, FA, stroke=3, sfill=(255, 255, 255))

def drops(d, lt, x0, x1, y0, y1, n=6):
    for k in range(n):
        x = x0 + (x1 - x0) * ((k * 0.37) % 1)
        y = y0 + ((lt * 260 + k * 97) % (y1 - y0))
        d.ellipse([x - 12, y - 18, x + 12, y + 18], fill=CYAN, outline=INK, width=4)

def monkey(d, cx, cy, s=1.0, lt=0.0):
    br = (150, 100, 70); face = (255, 170, 160)
    for ex in (-150, 150):
        d.ellipse([cx + ex * s - 55 * s, cy - 40 * s, cx + ex * s + 55 * s, cy + 60 * s], fill=face, outline=INK, width=int(7 * s))
    d.ellipse([cx - 160 * s, cy - 170 * s, cx + 160 * s, cy + 160 * s], fill=br, outline=INK, width=int(8 * s))
    d.ellipse([cx - 110 * s, cy - 90 * s, cx + 110 * s, cy + 140 * s], fill=face, outline=INK, width=int(7 * s))
    bl = 4 if (lt % 2.2) < 0.15 else 22
    for ex in (-45, 45):
        d.ellipse([cx + ex * s - 20 * s, cy - 30 * s - bl * s / 2, cx + ex * s + 20 * s, cy - 30 * s + bl * s / 2], fill=INK)
    d.ellipse([cx - 30 * s, cy + 20 * s, cx - 10 * s, cy + 40 * s], fill=INK); d.ellipse([cx + 10 * s, cy + 20 * s, cx + 30 * s, cy + 40 * s], fill=INK)
    d.arc([cx - 50 * s, cy + 50 * s, cx + 50 * s, cy + 110 * s], 20, 160, fill=INK, width=int(7 * s))

def v_raisin(lt, b):
    im, d = X.new_card()
    label(d, (CW / 2 - 5, 80), 'NOT THE WATER!', 84, INK, FA)
    finger(d, 260, 380, 0.95, wr=1.0)
    d.line([(150, 200), (370, 560)], fill=RED, width=14); d.line([(370, 200), (150, 560)], fill=RED, width=14)
    k = ease_back(min(1, lt / 0.5))
    d.rounded_rectangle([500, 300 - 70 * k, 880, 300 + 70 * k], 30, fill=YEL, outline=INK, width=7)
    if k > 0.6: label(d, (690, 300), 'NERVES', 90, INK, FA)
    label(d, (690, 470), 'doing it', 54, INK, FB); label(d, (690, 540), 'on purpose', 54, INK, FB)
    return im

def v_macaque(lt, b):
    im, d = X.new_card()
    v = b['vis']
    if v == 'macaque':
        label(d, (CW / 2 - 5, 80), 'WHO ELSE?', 96, INK, FA)
        d.ellipse([320, 180, 620, 520], fill=(60, 55, 80), outline=INK, width=8)
        label(d, (470, 350), '?', 220, YEL, FA, stroke=6)
        label(d, (CW / 2 - 5, 600), 'only ONE other animal', 50, INK, FB)
    elif v == 'macaque2':
        label(d, (CW / 2 - 5, 80), 'THE MACAQUE!', 96, PINK, FA, stroke=4)
        monkey(d, 470, 380, 1.15, lt)
    else:
        label(d, (CW / 2 - 5, 80), 'PRUNEY CLUB', 92, INK, FA)
        finger(d, 230, 360, 0.7, wr=1.0); label(d, (230, 600), 'humans', 50, INK, FB)
        monkey(d, 650, 350, 0.9, lt); label(d, (650, 600), 'macaques', 50, INK, FB)
    return im

def v_timer(lt, b):
    im, d = X.new_card()
    k = ease_out(min(1, lt / 2.0))
    label(d, (CW / 2 - 5, 80), '~5 MINUTES', 96, INK, FA)
    X.stopwatch(d, 260, 380, 160, 0.9 * k)
    finger(d, 680, 380, 0.8, wr=k)
    label(d, (680, 625), 'wrinkles appear', 44, INK, FB)
    return im

def v_vessels(lt, b):
    im, d = X.new_card()
    shrink = b['vis'] == 'vessels2'
    k = ease_out(min(1, lt / 1.2))
    label(d, (CW / 2 - 5, 80), 'SQUEEZE!' if not shrink else 'SKIN BUCKLES', 96, INK, FA)
    # cross-section: skin on top, pad, vessels
    top = 190 + (40 * k if shrink else 0)
    pts = [(70 + i * 800 / 40, top + (22 * k * math.sin(i * 1.3) if shrink else 0)) for i in range(41)]
    d.polygon(pts + [(870, 560), (70, 560)], fill=SKIN, outline=INK)
    d.line(pts, fill=INK, width=8)
    d.rectangle([70, 560, 870, 580], fill=SKIN_D)
    th = 34 * (1 - 0.7 * (k if not shrink else 1))
    for y in (330, 440):
        d.line([(110, y + 20), (830, y - 10)], fill=RED, width=max(8, int(th)))
    if not shrink:
        for x in (300, 640):
            arrow(d, (x, 250), (x, 300 + 10 * k), INK, 9, 26); arrow(d, (x, 520), (x, 470 - 10 * k), INK, 9, 26)
    label(d, (CW / 2 - 5, 625), 'blood vessels narrow' if not shrink else 'pad shrinks, skin folds', 46, INK, FB)
    return im

def v_nerve(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'nerve':
        label(d, (CW / 2 - 5, 80), '1930s', 110, INK, FA)
        d.rounded_rectangle([330, 200, 610, 560], 30, fill=(255, 255, 255), outline=INK, width=8)
        for k in range(5): d.line([(370, 260 + k * 55), (570, 260 + k * 55)], fill=(170, 170, 190), width=8)
        label(d, (470, 610), 'doctors noticed...', 48, INK, FB)
    else:
        label(d, (CW / 2 - 5, 70), 'NERVE DAMAGED?', 84, INK, FA)
        finger(d, 260, 380, 0.85, wr=1.0); label(d, (260, 625), 'healthy', 46, GRN, FA)
        finger(d, 680, 380, 0.85, wr=0.0, cut=True); label(d, (680, 625), 'NO WRINKLES', 46, PINK, FA)
    return im

def v_test(lt, b):
    im, d = X.new_card()
    label(d, (CW / 2 - 5, 80), 'THE BATH TEST', 92, INK, FA)
    d.rounded_rectangle([140, 330, 520, 560], 40, fill=CYAN, outline=INK, width=8)
    d.rectangle([148, 330, 512, 380], fill=(150, 230, 255))
    finger(d, 330, 300, 0.6, wr=min(1, lt / 1.5))
    for i, txt in enumerate(('wrinkles?', 'nerves OK')):
        label(d, (720, 380 + i * 120), txt, 72, INK if i == 0 else GRN, FA)
    return im

def equals(d, cx, cy):
    for dy in (-22, 22):
        d.rounded_rectangle([cx - 45, cy + dy - 12, cx + 45, cy + dy + 12], 10, fill=PINK, outline=INK, width=5)

def tire(d, cx, cy, r, lt):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(50, 50, 60), outline=INK, width=8)
    for k in range(16):
        a = k / 16 * 2 * math.pi + lt * 1.5
        p1 = (cx + r * 0.72 * math.cos(a), cy + r * 0.72 * math.sin(a)); p2 = (cx + r * 0.97 * math.cos(a + 0.12), cy + r * 0.97 * math.sin(a + 0.12))
        d.line([p1, p2], fill=(130, 130, 145), width=10)
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45], fill=(190, 195, 210), outline=INK, width=7)

def v_tread(lt, b):
    im, d = X.new_card()
    label(d, (CW / 2 - 5, 80), 'RAIN TREADS?', 96, INK, FA)
    tire(d, 250, 370, 180, lt)
    finger(d, 680, 370, 0.8, wr=1.0)
    if b['vis'] == 'tread2':
        drops(d, lt, 600, 760, 170, 560, 5)
        label(d, (CW / 2 - 5, 625), 'water drains away', 46, INK, FB)
    else:
        equals(d, 470, 370)
    return im

def v_marbles(lt, b):
    im, d = X.new_card()
    label(d, (CW / 2 - 5, 70), 'WET MARBLES', 92, INK, FA)
    k = ease_out(min(1, lt / 2.5))
    for i, (lab, frac, col) in enumerate((('smooth', 0.75, CYAN), ('wrinkly', 0.75 * 1.12, PINK))):
        y = 230 + i * 180
        label(d, (90, y), lab, 46, INK, FB, anchor='lm')
        x = 300 + 520 * min(1, frac * k)
        d.line([(300, y), (820, y)], fill=(220, 215, 210), width=10)
        d.ellipse([x - 32, y - 32, x + 32, y + 32], fill=col, outline=INK, width=6)
    label(d, (CW / 2 - 5, 590), '12% FASTER', 92, PINK, FA, stroke=4)
    return im

def v_dry(lt, b):
    im, d = X.new_card()
    label(d, (CW / 2 - 5, 80), 'DRY MARBLES', 92, INK, FA)
    for i, x in enumerate((250, 690)):
        finger(d, x, 340, 0.6, wr=float(i))
        d.ellipse([x - 40, 500, x + 40, 580], fill=YEL, outline=INK, width=6)
    equals(d, 470, 340)
    label(d, (CW / 2 - 5, 630), 'no difference', 46, INK, FB)
    return im

def v_berlin(lt, b):
    im, d = X.new_card()
    label(d, (CW / 2 - 5, 80), 'BERLIN: 40 PEOPLE', 82, INK, FA)
    k = ease_out(min(1, lt / 1.2))
    for i, (lab, col) in enumerate((('smooth', CYAN), ('wrinkly', PINK))):
        y = 220 + i * 120
        label(d, (90, y), lab, 46, INK, FB, anchor='lm')
        d.rounded_rectangle([290, y - 32, 290 + 540 * k, y + 32], 30, fill=col, outline=INK, width=6)
    label(d, (CW / 2 - 5, 440), 'same grip', 50, INK, FB)
    wob = 6 * math.sin(lt * 5)
    d.rounded_rectangle([200, 500 + wob, 740, 610 + wob], 40, fill=YEL, outline=INK, width=7)
    label(d, (470, 555 + wob), 'STILL DEBATED', 70, INK, FA)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    label(d, (CW / 2 - 5, 80), 'RAIN TIRES ON', 92, INK, FA)
    finger(d, 470, 380, 0.95, wr=1.0)
    drops(d, lt, 280, 660, 170, 580, 6)
    return im

VISUALS = {'raisin': v_raisin, 'macaque': v_macaque, 'macaque2': v_macaque, 'macaque3': v_macaque,
           'timer': v_timer, 'vessels': v_vessels, 'vessels2': v_vessels, 'nerve': v_nerve, 'nerve2': v_nerve,
           'test': v_test, 'tread': v_tread, 'tread2': v_tread, 'marbles': v_marbles, 'berlin': v_berlin, 'dry': v_dry, 'outro': v_outro}
