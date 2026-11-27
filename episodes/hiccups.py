# Episode: Why do we get hiccups?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why do we get hiccups?"
SLUG = 'hiccups'
CAPTION = ("One man hiccupped for 68 YEARS 😳 Here's what a hiccup actually is. "
           "#science #didyouknow #learnontiktok #hiccups #body #facts")
SOURCES = [
    'https://news.uams.edu/2018/04/26/hiccups/',
    'https://www.smithsonianmag.com/history/the-curious-case-of-charles-osborne-who-hiccuped-for-68-years-straight-180980232/',
    'https://discovermagazine.com/health/what-is-the-purpose-of-hiccuping',
    'https://sites.dartmouth.edu/dujs/?p=1372',
    'https://www.sciencealert.com/the-incredible-true-story-of-the-man-who-had-hiccups-for-68-years',
    'https://en.wikipedia.org/wiki/Hiccup',
]
BEATS = [
    ('BIG:HOLD YOUR|BREATH.|DRINK|WATER.', 'point', "Hold your breath. Drink water. Get a friend to scare you."),
    ('cures',    'shrug', "Hiccup cures are mostly *guesses*. But the hiccup itself is way weirder than you think."),
    ('recordq',  'point', "One man hiccupped for sixty-eight *years*. Stay till the end."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('diaphragm','point', "Under your lungs sits a big dome of muscle: your *diaphragm*."),
    ('spasm',    'down',  "A hiccup is that muscle suddenly *jerking*, and yanking air into your lungs."),
    ('snap',     'point', "About a quarter of a second later, your vocal cords snap *shut*."),
    ('hic',      'up',    "The air slams into them. And that's the *hic*!"),
    ('stomach',  'shrug', "A common trigger? A stuffed *stomach*. It sits right under the diaphragm and pokes it."),
    ('nerves',   'down',  "It's a reflex. Your nerves fire the signal, and you can't just *decide* to stop."),
    ('womb',     'point', "Here's a weird one: babies hiccup in the womb, before they ever *breathe* air."),
    ('practice', 'down',  "One idea: hiccups are *practice* for the breathing muscles."),
    ('gills',    'shrug', "A wilder idea: it's a leftover from ancient animals with both *gills* and lungs."),
    ('gills2',   'point', "Snapping the throat shut sent water over the gills, and kept it out of the *lungs*."),
    ('scare',    'down',  "And getting scared or tickled? Probably *won't* stop them. Sorry."),
    ('osborne',  'up',    "Now, the record. In nineteen twenty-two, a young farmhand named Charles *Osborne* started hiccupping."),
    ('osborne2', 'point', "It began while he was weighing a *hog*. And it didn't stop until nineteen ninety."),
    ('count',    'down',  "That's an estimated four hundred thirty *million* hiccups!"),
    ('doctor',   'shrug', "Don't worry, most bouts end in minutes. If one lasts over two *days*, see a doctor."),
    ('outro',    'point', "So next time you hiccup, relax. It might just be your inner *fish* saying hi."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

LUNG = (255, 150, 170); DIA = (230, 90, 110)

def torso(d, cx, cy, s=1.0, jerk=0.0, glottis_shut=False, stomach_big=False, air=0.0):
    cy += 35; s *= 0.86
    # body outline
    d.rounded_rectangle([cx - 200 * s, cy - 230 * s, cx + 200 * s, cy + 230 * s], int(90 * s), fill=SKIN, outline=INK, width=int(8 * s))
    # windpipe
    d.rectangle([cx - 18 * s, cy - 290 * s, cx + 18 * s, cy - 120 * s], fill=(255, 225, 225), outline=INK, width=int(5 * s))
    gy = cy - 230 * s
    if glottis_shut:
        d.line([(cx - 30 * s, gy), (cx + 30 * s, gy)], fill=RED, width=int(12 * s))
    else:
        d.line([(cx - 30 * s, gy), (cx - 10 * s, gy)], fill=INK, width=int(8 * s)); d.line([(cx + 10 * s, gy), (cx + 30 * s, gy)], fill=INK, width=int(8 * s))
    # lungs
    for sx in (-1, 1):
        x = cx + sx * 95 * s
        d.ellipse([x - 80 * s, cy - 150 * s, x + 80 * s, cy + 60 * s + 20 * jerk * s], fill=LUNG, outline=INK, width=int(6 * s))
    # diaphragm
    dy = 40 * jerk * s
    d.arc([cx - 190 * s, cy + 40 * s + dy, cx + 190 * s, cy + 200 * s + dy], 180, 360, fill=DIA, width=int(16 * s))
    # stomach
    r = (95 if stomach_big else 60) * s
    d.ellipse([cx + 10 * s - r, cy + 150 * s - r * 0.7 + dy, cx + 10 * s + r, cy + 150 * s + r * 0.7 + dy], fill=(255, 190, 120), outline=INK, width=int(6 * s))
    if air > 0:
        for k in range(3):
            y = cy - 300 * s + (air * 3 + k * 0.33) % 1 * 160 * s
            d.ellipse([cx - 10 * s, y - 10 * s, cx + 10 * s, y + 10 * s], fill=CYAN, outline=INK, width=3)

def fish(d, cx, cy, s=1.0, lt=0.0):
    w = 6 * math.sin(lt * 6)
    d.polygon([(cx + 120 * s, cy), (cx + 200 * s, cy - 70 * s + w), (cx + 200 * s, cy + 70 * s + w)], fill=CYAN, outline=INK)
    d.ellipse([cx - 150 * s, cy - 90 * s, cx + 150 * s, cy + 90 * s], fill=CYAN, outline=INK, width=int(7 * s))
    d.ellipse([cx - 105 * s, cy - 40 * s, cx - 75 * s, cy - 10 * s], fill=INK)
    for k in range(3):
        d.arc([cx - 60 * s + k * 22 * s, cy - 50 * s, cx - 20 * s + k * 22 * s, cy + 50 * s], 300, 60, fill=PINK, width=int(6 * s))

def v_cures(lt, b):
    im, d = X.new_card()
    title(d, 'JUST GUESSES?')
    for i, (t, c) in enumerate((('hold breath', CYAN), ('drink water', GRN), ('get scared', PINK))):
        badge(d, 470, 230 + i * 130, t, 56, c, lt + i, padx=40, h=95)
    label(d, (800, 360), '?', 160, INK, FA)
    return im

def v_recordq(lt, b):
    im, d = X.new_card()
    title(d, '68 YEARS?!')
    d.rounded_rectangle([250, 190, 690, 560], 30, fill=WHITE, outline=INK, width=8)
    d.rectangle([250, 190, 690, 260], fill=RED, outline=INK, width=8)
    for k in range(20):
        x = 280 + (k % 5) * 82; y = 290 + (k // 5) * 66
        d.rounded_rectangle([x, y, x + 60, y + 48], 8, outline=INK, width=4)
        if k < int(lt * 8): label(d, (x + 30, y + 24), 'hic', 26, PINK, FA)
    return im

def v_dia(lt, b):
    im, d = X.new_card()
    v = b['vis']
    if v == 'diaphragm':
        title(d, 'THE DIAPHRAGM')
        torso(d, 470, 380, 0.95)
        label(d, (790, 470), 'diaphragm', 46, DIA, FA)
    elif v == 'spasm':
        title(d, 'SUDDEN JERK!')
        j = 1.0 if (lt * 1.5) % 1 < 0.3 else 0.0
        torso(d, 470, 390, 0.95, jerk=j, air=lt if j else 0)
    elif v == 'snap':
        title(d, 'CORDS SNAP SHUT')
        torso(d, 470, 400, 0.95, jerk=1, glottis_shut=(lt % 1.2) > 0.25)
        label(d, (760, 200), '0.25 s', 56, PINK, FA)
    else:
        title(d, 'HIC!', 110, PINK, stroke=4)
        torso(d, 470, 410, 0.9, jerk=1, glottis_shut=True)
        k = popk(lt)
        label(d, (740, 260), 'HIC!', int(110 * k) + 1, YEL, FA, stroke=5)
    return im

def v_stomach(lt, b):
    im, d = X.new_card()
    title(d, 'STUFFED STOMACH')
    torso(d, 470, 400, 0.95, stomach_big=True)
    arrow(d, (480, 470), (480, 420), RED, 10, 26)
    return im

def v_nerves(lt, b):
    im, d = X.new_card()
    title(d, 'A REFLEX')
    X.brain(d, 300, 330, 0.6)
    for k in range(4):
        ph = (lt * 1.5 + k / 4) % 1
        x = 360 + 380 * ph; y = 400 + 120 * ph
        d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=YEL, outline=INK, width=4)
    d.arc([600, 470, 860, 620], 180, 360, fill=DIA, width=16)
    label(d, (730, 640), 'no off switch', 40, INK, FB)
    return im

def v_womb(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'womb':
        title(d, 'HICCUPS IN THE WOMB', 84)
    else:
        title(d, 'BREATHING PRACTICE?', 84)
    d.ellipse([270, 170, 670, 570], fill=(255, 190, 200), outline=INK, width=8)
    j = 10 if (lt * 1.4) % 1 < 0.2 else 0
    head(d, 470, 320 - j, 0.6, mouth='o', eyes='closed')
    d.ellipse([380, 390 - j, 560, 520 - j], fill=SKIN, outline=INK, width=6)
    if j: label(d, (640, 260), 'hic', 50, PINK, FA)
    return im

def v_gills(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'gills':
        title(d, 'GILLS + LUNGS?')
        fish(d, 400, 380, 1.2, lt)
        label(d, (780, 520), 'ancient', 44, INK, FB); label(d, (780, 570), 'ancestor', 44, INK, FB)
    else:
        title(d, 'WATER TO GILLS')
        fish(d, 380, 380, 1.2, lt)
        for k in range(4):
            ph = (lt * 1.2 + k / 4) % 1
            d.ellipse([200 + 120 * ph, 360 + 10 * k - 10, 220 + 120 * ph, 380 + 10 * k], fill=(120, 200, 255), outline=INK, width=3)
        label(d, (760, 300), 'lungs:', 50, INK, FA); label(d, (760, 370), 'closed', 50, RED, FA)
    return im

def v_scare(lt, b):
    im, d = X.new_card()
    title(d, 'SCARE CURE?')
    head(d, 300, 390, 0.9, mouth='o')
    label(d, (300, 180), '!', 90, PINK, FA)
    cross(d, 690, 380, 110, 20)
    return im

def v_osborne(lt, b):
    im, d = X.new_card()
    v = b['vis']
    if v == 'osborne':
        title(d, 'CHARLES OSBORNE', 88)
        head(d, 300, 380, 0.9, mouth='o')
        d.rectangle([180, 200, 420, 240], fill=BROWN, outline=INK, width=6)     # hat brim
        d.rounded_rectangle([230, 130, 370, 215], 20, fill=BROWN, outline=INK, width=6)
        label(d, (690, 380), '1922', 110, INK, FA)
    elif v == 'osborne2':
        title(d, '1922 -> 1990')
        # hog
        d.ellipse([170, 280, 470, 500], fill=(255, 175, 190), outline=INK, width=8)
        d.ellipse([110, 330, 210, 430], fill=(255, 175, 190), outline=INK, width=7)
        d.ellipse([85, 360, 125, 400], fill=PINK, outline=INK, width=5)
        for x in (220, 300, 380, 440): d.rectangle([x - 15, 490, x + 15, 550], fill=(255, 175, 190), outline=INK, width=5)
        badge(d, 680, 380, '68 YEARS', 74, YEL, lt)
    else:
        title(d, '430 MILLION HICS', 88)
        n = int(min(1, lt / 2.0) * 430)
        label(d, (CW / 2 - 5, 360), f'{n},000,000', 110, PINK, FA, stroke=4)
        sub(d, '20 to 40 every minute', 560, 50)
    return im

def v_doctor(lt, b):
    im, d = X.new_card()
    title(d, '> 2 DAYS? DOCTOR')
    X.stopwatch(d, 280, 390, 150, min(1, lt / 2) * 0.9)
    d.rounded_rectangle([540, 250, 820, 530], 40, fill=WHITE, outline=INK, width=8)
    d.rectangle([655, 290, 705, 490], fill=RED); d.rectangle([580, 365, 780, 415], fill=RED)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, 'YOUR INNER FISH')
    torso(d, 300, 400, 0.75, jerk=1 if (lt * 1.4) % 1 < 0.2 else 0)
    fish(d, 680, 380, 0.8, lt)
    label(d, (700, 230), 'hi!', 60, PINK, FA)
    return im

VISUALS = {'cures': v_cures, 'recordq': v_recordq, 'diaphragm': v_dia, 'spasm': v_dia, 'snap': v_dia, 'hic': v_dia,
           'stomach': v_stomach, 'nerves': v_nerves, 'womb': v_womb, 'practice': v_womb, 'gills': v_gills, 'gills2': v_gills,
           'scare': v_scare, 'osborne': v_osborne, 'osborne2': v_osborne, 'count': v_osborne, 'doctor': v_doctor, 'outro': v_outro}
