# Episode: Why is yawning contagious?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why is yawning contagious?"
SLUG = 'yawn'
CAPTION = ("Try watching this without yawning 🥱 Spoiler: your dog can catch your yawns too. "
           "#science #didyouknow #learnontiktok #yawn #brain #facts")
SOURCES = [
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC2610100/',
    'https://kids.frontiersin.org/article/10.3389/frym.2017.00052',
    'https://journals.sagepub.com/doi/10.1177/147470490700500109',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC3534187/',
    'https://www.sciencenews.org/?p=31686',
    'https://greatergood.berkeley.edu/article/item/empathys_dogs',
]
BEATS = [
    ('BIG:WATCH THIS|AND TRY|NOT TO|YAWN.', 'point', "Watch this, and try not to yawn."),
    ('yawnface', 'shrug', "Too late? Seeing a yawn, hearing one, even *reading* the word yawn can set you off."),
    ('dogq',     'point', "And it's not just humans. One animal catches *your* yawns. Stay till the end."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('oxygen',   'shrug', "Old idea: you yawn because you need more *oxygen*."),
    ('oxygen2',  'down',  "Scientists tested it. More oxygen or less, people yawned *the same*."),
    ('cool',     'point', "Newer idea: a yawn is a *radiator* for your brain."),
    ('cool2',    'down',  "The huge jaw stretch pumps blood, and the deep breath pulls in *cooler* air."),
    ('womb',     'up',    "Fun fact: you started yawning before you were even *born*, inside the womb."),
    ('rat',      'point', "In rats, brain temperature actually *dropped* right after a yawn."),
    ('pack',     'shrug', "And people holding a *cold* pack to their forehead caught way fewer yawns."),
    ('season',   'down',  "One study even found that how often people catch yawns changes with the *seasons*."),
    ('catch',    'point', "But why do we copy each other at all? Roughly *half* of adults catch a yawn they see."),
    ('empathy',  'down',  "People who score high on *empathy* tests tend to catch more yawns."),
    ('kids',     'shrug', "And little kids barely catch yawns at all, until around age *five*."),
    ('dog',      'up',    "Now, that animal. It's your *dog*!"),
    ('dog2',     'point', "Scientists in London yawned at twenty-nine dogs. Twenty-one yawned *back*."),
    ('dog3',     'down',  "When they just opened their mouths without yawning? *Zero* dogs yawned."),
    ('outro',    'shrug', "So if you yawned during this video, it's not *boredom*. It's empathy. Probably."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

def v_yawnface(lt, b):
    im, d = X.new_card()
    title(d, 'IT SPREADS!')
    for i, x in enumerate((180, 470, 760)):
        on = lt > i * 0.5
        head(d, x, 380, 0.75, mouth='yawn' if on else 'flat', lt=lt, eyes='closed' if on else 'open')
    sub(d, 'seeing, hearing, even reading it')
    return im

def v_dogq(lt, b):
    im, d = X.new_card()
    title(d, 'WHO ELSE?')
    d.ellipse([320, 180, 620, 520], fill=(60, 55, 80), outline=INK, width=8)
    label(d, (470, 350), '?', 220, YEL, FA, stroke=6)
    sub(d, 'catches HUMAN yawns', 600)
    return im

def v_oxygen(lt, b):
    im, d = X.new_card()
    title(d, 'NEED OXYGEN?' if b['vis'] == 'oxygen' else 'MYTH BUSTED')
    # tank
    d.rounded_rectangle([170, 200, 370, 560], 70, fill=CYAN, outline=INK, width=8)
    d.rectangle([235, 160, 305, 205], fill=DGREY, outline=INK, width=6)
    label(d, (270, 390), 'O2', 110, INK, FA)
    head(d, 650, 380, 0.85, mouth='yawn', lt=lt, eyes='closed')
    if b['vis'] == 'oxygen2':
        cross(d, 270, 380, 150, 22)
        sub(d, 'more or less O2: same yawns')
    return im

def brain_temp(d, lt, hot):
    X.brain(d, 360, 380, 0.9)
    thermo(d, 760, 360, 300, 0.85 if hot else 0.35, RED if hot else CYAN)

def v_cool(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'cool':
        title(d, 'BRAIN RADIATOR')
        k = min(1, lt / 1.5)
        brain_temp(d, lt, k < 0.5)
        for y in (250, 330, 410):
            off = (lt * 160) % 120
            arrow(d, (60 + off, y), (140 + off, y), CYAN, 10, 26)
    else:
        title(d, 'STRETCH + BREATHE')
        head(d, 300, 380, 1.0, mouth='yawn', lt=lt, eyes='closed')
        for k in range(3):
            ph = (lt * 1.2 + k / 3) % 1
            x = 860 - 330 * ph
            arrow(d, (x, 360 + (k - 1) * 70), (x - 70, 370 + (k - 1) * 50), CYAN, 10, 26)
        label(d, (740, 560), 'cool air in', 50, INK, FB)
    return im

def v_womb(lt, b):
    im, d = X.new_card()
    title(d, 'BEFORE BIRTH')
    d.ellipse([270, 170, 670, 570], fill=(255, 190, 200), outline=INK, width=8)
    bob = 8 * math.sin(lt * 2)
    head(d, 470, 330 + bob, 0.6, mouth='yawn', lt=lt, eyes='closed')
    d.ellipse([380, 400 + bob, 560, 530 + bob], fill=SKIN, outline=INK, width=6)
    sub(d, 'yawning starts in the womb', 625)
    return im

def v_season(lt, b):
    im, d = X.new_card()
    title(d, 'IT\'S SEASONAL')
    cx, cy = 280, 370
    d.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], fill=YEL, outline=INK, width=7)
    for k in range(10):
        a = k / 10 * 2 * math.pi + lt
        d.line([(cx + 105 * math.cos(a), cy + 105 * math.sin(a)), (cx + 140 * math.cos(a), cy + 140 * math.sin(a))], fill=ORANGE, width=12)
    x2 = 670
    for k in range(6):
        a = k / 6 * math.pi
        d.line([(x2 - 130 * math.cos(a), cy - 130 * math.sin(a)), (x2 + 130 * math.cos(a), cy + 130 * math.sin(a))], fill=CYAN, width=16)
    d.ellipse([x2 - 30, cy - 30, x2 + 30, cy + 30], fill=WHITE, outline=INK, width=6)
    sub(d, 'it changes with the seasons', 610)
    return im

def v_rat(lt, b):
    im, d = X.new_card()
    title(d, 'RAT BRAIN COOLS')
    X.rat(d, 360, 400, 0.85)
    k = ease_out(min(1, lt / 2.0))
    thermo(d, 780, 360, 300, 0.8 - 0.45 * k, RED if k < 0.5 else CYAN)
    sub(d, 'right after a yawn', 630)
    return im

def v_pack(lt, b):
    im, d = X.new_card()
    title(d, 'COLD PACK TEST')
    head(d, 300, 400, 0.95, mouth='flat')
    d.rounded_rectangle([190, 220, 410, 290], 25, fill=CYAN, outline=INK, width=7)
    label(d, (300, 255), 'COLD', 44, INK, FA)
    bars(d, [('warm', 0.9, PINK, 'MORE'), ('cold', 0.5, CYAN, 'LESS')], x0=600, y0=320, w=300, h=60, gap=130, k=ease_out(min(1, lt / 1.0)), lw=42)
    label(d, (740, 220), 'yawns caught', 44, INK, FB)
    return im

def v_catch(lt, b):
    im, d = X.new_card()
    title(d, 'WHO CATCHES IT?')
    k = ease_out(min(1, lt / 1.2))
    bars(d, [('humans', 0.52, PINK, '45-60%'), ('chimps', 0.33, YEL, '33%')], x0=330, y0=260, w=520, h=70, gap=150, k=k)
    sub(d, 'share who catch a seen yawn', 600)
    return im

def v_empathy(lt, b):
    im, d = X.new_card()
    title(d, 'EMPATHY LINK')
    head(d, 250, 380, 0.8, mouth='yawn', lt=lt, eyes='closed')
    head(d, 690, 380, 0.8, mouth='yawn', lt=lt + 0.6, eyes='closed')
    s = 1 + 0.12 * math.sin(lt * 6)
    hx, hy = 470, 330
    d.polygon([(hx, hy + 70 * s), (hx - 70 * s, hy), (hx - 40 * s, hy - 45 * s), (hx, hy - 15 * s), (hx + 40 * s, hy - 45 * s), (hx + 70 * s, hy)], fill=PINK, outline=INK)
    sub(d, 'more empathy = more yawns caught', 610)
    return im

def v_kids(lt, b):
    im, d = X.new_card()
    title(d, 'AGE ~5')
    # cake with 5 candles
    d.rounded_rectangle([250, 380, 690, 560], 30, fill=PINK, outline=INK, width=8)
    d.rectangle([250, 380, 690, 430], fill=(255, 240, 245), outline=INK, width=6)
    for i in range(5):
        x = 310 + i * 80
        d.rectangle([x - 12, 280, x + 12, 380], fill=CYAN, outline=INK, width=5)
        fl = 8 * math.sin(lt * 8 + i)
        d.ellipse([x - 16 + fl / 3, 230, x + 16 + fl / 3, 280], fill=YEL, outline=INK, width=4)
    sub(d, 'contagious yawning switches on', 625)
    return im

def v_dog(lt, b):
    im, d = X.new_card()
    v = b['vis']
    if v == 'dog':
        title(d, 'YOUR DOG!', 104, PINK, stroke=4)
        dog(d, 470, 380, 1.1, lt, yawn=True)
    elif v == 'dog2':
        title(d, '21 OF 29 DOGS')
        head(d, 230, 380, 0.75, mouth='yawn', lt=lt, eyes='closed')
        arrow(d, (370, 380), (500, 380), INK, 12, 34)
        dog(d, 700, 380, 0.85, lt + 0.5, yawn=True)
        badge(d, 470, 590, '72% YAWNED BACK', 56, YEL, lt)
    else:
        title(d, 'FAKE YAWN?')
        head(d, 230, 380, 0.75, mouth='o')
        arrow(d, (370, 380), (500, 380), INK, 12, 34)
        dog(d, 700, 380, 0.85, lt, yawn=False)
        badge(d, 470, 590, '0 DOGS', 64, CYAN, lt)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, 'NOT BOREDOM')
    head(d, 300, 390, 0.9, mouth='yawn', lt=lt, eyes='closed')
    dog(d, 680, 390, 0.75, lt + 0.4, yawn=True)
    sub(d, 'it\'s empathy (probably)', 630)
    return im

VISUALS = {'yawnface': v_yawnface, 'dogq': v_dogq, 'oxygen': v_oxygen, 'oxygen2': v_oxygen, 'cool': v_cool, 'cool2': v_cool,
           'rat': v_rat, 'womb': v_womb, 'season': v_season, 'pack': v_pack, 'catch': v_catch, 'empathy': v_empathy, 'kids': v_kids,
           'dog': v_dog, 'dog2': v_dog, 'dog3': v_dog, 'outro': v_outro}
