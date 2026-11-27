# Episode: Why does the moon look bigger near the horizon?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why does the moon look bigger near the horizon?"
SLUG = 'moon'
CAPTION = ("The giant horizon moon is the SAME size as the high moon 🌕 Even astronauts get fooled. "
           "#science #didyouknow #learnontiktok #moon #space #illusion")
SOURCES = [
    'https://science.nasa.gov/earth/moon/the-moon-illusion-why-does-the-moon-look-so-big-sometimes/',
    'https://science.nasa.gov/resource/photographing-the-moon-illusion',
    'https://www.nationalgeographic.com/science/article/moon-illusion-explained-horizon-size-supermoon-space-science',
    'https://www.scientificamerican.com/article/why-does-the-moon-look-bigger-near-the-horizon/',
    'https://www.universetoday.com/articles/explaining-the-moon-illusion',
]
BEATS = [
    ('BIG:LOOK AT|THE MOON|ON THE|HORIZON.', 'point', "Look at the moon on the horizon. Huge, right?"),
    ('same',     'shrug', "Here's the thing: it's the exact *same* size as when it's high in the sky."),
    ('astroq',   'point', "And even astronauts in *space* get fooled by it. Stay till the end."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('photo',    'point', "Proof? NASA photographed the moon low and high on the same night. Same *width*."),
    ('thumb',    'down',  "Try it yourself. Hold out your arm. The moon is about the size of your *fingertip*. Low or high."),
    ('tube',     'point', "Or look through a paper tube. The giant moon *shrinks* back to normal."),
    ('squash',   'shrug', "Near the horizon, the air actually squashes the moon a tiny bit. *Flatter*, not bigger."),
    ('ancient',  'down',  "People have puzzled over this for almost *two* thousand years. Ptolemy wrote about it."),
    ('haytham',  'point', "Around a thousand years ago, Ibn al-Haytham said it's about how your brain judges *distance*."),
    ('trees',    'shrug', "Idea one: trees and buildings next to the moon make it look *bigger*."),
    ('sea',      'down',  "But the illusion still works over an empty *ocean*. Hmm."),
    ('dome',     'point', "Idea two: your brain imagines the sky as a flattened *dome*."),
    ('dome2',    'down',  "The horizon feels farther away, so your brain *inflates* anything sitting there."),
    ('astro',    'up',    "Now, the astronauts. In orbit, there are no trees, no buildings, no *horizon* tricks."),
    ('astro2',   'point', "And they still see the moon illusion! So even NASA says it's not fully *solved*."),
    ('legs',     'shrug', "Bonus trick: bend over and look at the moon *between* your legs. It shrinks. Seriously."),
    ('outro',    'point', "So the moon doesn't grow. Your brain just hits *zoom*."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

NIGHT = (35, 40, 80); MOON = (255, 240, 190); MOON_D = (225, 205, 150)

def sky(d, top=150, bottom=560):
    d.rounded_rectangle([40, top, 890, bottom], 30, fill=NIGHT, outline=INK, width=7)
    for k in range(14):
        x = 70 + (k * 157) % 800; y = top + 20 + (k * 89) % (bottom - top - 60)
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 255, 230))

def moon(d, cx, cy, r, squash=1.0, col=MOON):
    d.ellipse([cx - r, cy - r * squash, cx + r, cy + r * squash], fill=col, outline=INK, width=6)
    for (dx, dy, rr) in ((-0.3, -0.2, 0.22), (0.25, 0.15, 0.16), (-0.05, 0.4, 0.12)):
        d.ellipse([cx + dx * r - rr * r, cy + dy * r * squash - rr * r * squash, cx + dx * r + rr * r, cy + dy * r * squash + rr * r * squash], fill=MOON_D)

def ground(d, y=500, trees=True, bottom=560):
    d.rectangle([47, y, 883, bottom - 7], fill=(40, 70, 50))
    if trees:
        for x in (120, 210, 700, 790):
            d.polygon([(x - 40, y), (x + 40, y), (x, y - 110)], fill=(30, 110, 60), outline=INK)

def v_same(lt, b):
    im, d = X.new_card()
    title(d, 'SAME SIZE!')
    sky(d)
    ground(d, 500, True)
    moon(d, 300, 440, 60)
    moon(d, 640, 240, 60)
    d.line([(240, 600), (360, 600)], fill=PINK, width=10); d.line([(580, 600), (700, 600)], fill=PINK, width=10)
    label(d, (470, 600), '=', 70, PINK, FA)
    return im

def v_astroq(lt, b):
    im, d = X.new_card()
    title(d, 'IN SPACE TOO?')
    helmet(d, 330, 380, 1.0)
    d.ellipse([570, 230, 830, 490], fill=(60, 55, 80), outline=INK, width=8)
    label(d, (700, 360), '?', 180, YEL, FA, stroke=6)
    return im

def helmet(d, cx, cy, s=1.0):
    d.ellipse([cx - 150 * s, cy - 150 * s, cx + 150 * s, cy + 150 * s], fill=WHITE, outline=INK, width=int(8 * s))
    d.ellipse([cx - 105 * s, cy - 95 * s, cx + 105 * s, cy + 85 * s], fill=NIGHT, outline=INK, width=int(6 * s))
    d.arc([cx - 80 * s, cy - 75 * s, cx + 20 * s, cy + 5 * s], 200, 260, fill=(150, 170, 230), width=int(10 * s))
    d.rounded_rectangle([cx - 160 * s, cy + 120 * s, cx + 160 * s, cy + 200 * s], int(30 * s), fill=WHITE, outline=INK, width=int(7 * s))

def v_photo(lt, b):
    im, d = X.new_card()
    title(d, 'NASA PHOTO TEST')
    for i, (x, my) in enumerate(((250, 420), (690, 260))):
        d.rounded_rectangle([x - 180, 170, x + 180, 540], 20, fill=NIGHT, outline=INK, width=7)
        moon(d, x, my, 55, 0.92 if i == 0 else 1.0)
        d.line([(x - 55, 570), (x + 55, 570)], fill=GRN, width=10)
    sub(d, 'same width', 625)
    return im

def v_thumb(lt, b):
    im, d = X.new_card()
    title(d, 'FINGERTIP TEST')
    sky(d)
    moon(d, 640, 300, 40)
    # arm + finger
    d.line([(60, 560), (560, 400)], fill=INK, width=60); d.line([(60, 560), (560, 400)], fill=SKIN, width=46)
    d.rounded_rectangle([600, 290, 680, 420], 36, fill=SKIN, outline=INK, width=6)
    d.ellipse([612, 296, 668, 336], fill=(255, 230, 220), outline=INK, width=3)
    moon(d, 640, 270, 40)
    return im

def v_tube(lt, b):
    im, d = X.new_card()
    title(d, 'PAPER TUBE TRICK')
    sky(d); ground(d, 500, True)
    r = 120 - 50 * ease_out(min(1, lt / 1.5))
    moon(d, 470, 380, r)
    d.ellipse([280, 190, 660, 570], outline=(230, 220, 200), width=40)
    return im

def v_squash(lt, b):
    im, d = X.new_card()
    title(d, 'A BIT FLATTER')
    sky(d); ground(d, 500, False)
    moon(d, 470, 400, 120, 0.88)
    d.line([(330, 400), (610, 400)], fill=PINK, width=6)
    d.line([(470, 290), (470, 510)], fill=CYAN, width=6)
    return im

def scroll(d, cx, cy, txt):
    d.rounded_rectangle([cx - 170, cy - 170, cx + 170, cy + 170], 20, fill=(245, 225, 180), outline=INK, width=7)
    for k in range(5): d.line([(cx - 120, cy - 90 + k * 50), (cx + 120, cy - 90 + k * 50)], fill=(190, 160, 110), width=8)
    label(d, (cx, cy + 210), txt, 50, INK, FA)

def v_ancient(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'ancient':
        title(d, '~2,000 YEARS')
        scroll(d, 300, 330, 'PTOLEMY')
        moon(d, 680, 360, 110)
    else:
        title(d, 'IBN AL-HAYTHAM', 88)
        scroll(d, 300, 330, '~1,000 YEARS AGO')
        X.brain(d, 690, 330, 0.55)
        arrow(d, (600, 500), (780, 500), PINK, 10, 28)
        label(d, (690, 560), 'distance', 48, INK, FB)
    return im

def v_trees(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'trees':
        title(d, 'IDEA 1: TREES')
        sky(d); ground(d, 500, True)
        moon(d, 470, 420, 85)
        for x in (330, 610):
            d.polygon([(x - 40, 500), (x + 40, 500), (x, 380)], fill=(30, 110, 60), outline=INK)
    else:
        title(d, 'BUT AT SEA?')
        sky(d)
        pts = [(47 + i * 836 / 30, 490 + 8 * math.sin(i + lt * 3)) for i in range(31)]
        d.polygon(pts + [(883, 553), (47, 553)], fill=(50, 110, 200))
        moon(d, 470, 430, 85)
        label(d, (760, 220), 'still huge', 50, YEL, FA)
    return im

def v_dome(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'dome':
        title(d, 'IDEA 2: FLAT DOME')
        d.line([(80, 540), (860, 540)], fill=INK, width=8)
        d.arc([80, 240, 860, 840], 180, 360, fill=CYAN, width=10)          # flattened dome
        head(d, 470, 500, 0.3)
        label(d, (200, 480), 'far', 50, INK, FB); label(d, (470, 220), 'near', 50, INK, FB)
    else:
        title(d, 'BRAIN INFLATES IT')
        d.line([(80, 540), (860, 540)], fill=INK, width=8)
        d.arc([80, 240, 860, 840], 180, 360, fill=CYAN, width=10)
        head(d, 470, 500, 0.3)
        k = 1 + 0.5 * ease_out(min(1, lt / 1.2))
        moon(d, 170, 470, 36 * k)
        moon(d, 470, 290, 36)
    return im

def v_astro(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'astro':
        title(d, 'IN ORBIT')
        helmet(d, 300, 380, 0.95)
        d.ellipse([560, 330, 900, 670], fill=(60, 120, 220), outline=INK, width=7)
        moon(d, 760, 220, 45)
    else:
        title(d, 'STILL UNSOLVED')
        helmet(d, 300, 380, 0.95)
        moon(d, 700, 360, 70 + 20 * ease_out(min(1, lt / 1.2)))
        label(d, (700, 560), 'illusion!', 54, PINK, FA)
    return im

def v_legs(lt, b):
    im, d = X.new_card()
    title(d, 'BEND-OVER TRICK')
    # upside down view through legs
    d.polygon([(250, 590), (330, 590), (430, 250), (370, 250)], fill=BLUE, outline=INK)
    d.polygon([(690, 590), (610, 590), (510, 250), (570, 250)], fill=BLUE, outline=INK)
    k = 1 - 0.35 * ease_out(min(1, lt / 1.5))
    moon(d, 470, 470, 70 * k)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, 'BRAIN ZOOM')
    sky(d); ground(d, 500, True)
    z = 1 + 0.25 * abs(math.sin(lt * 1.5))
    moon(d, 470, 400, 80 * z)
    for (x, y) in ((340, 260), (600, 260), (340, 520), (600, 520)):
        dx = -1 if x < 470 else 1; dy = -1 if y < 400 else 1
        d.line([(x, y), (x + 40 * dx, y)], fill=YEL, width=8); d.line([(x, y), (x, y + 40 * -dy * -1 * dy * dy)], fill=YEL, width=8)
    return im

VISUALS = {'same': v_same, 'astroq': v_astroq, 'photo': v_photo, 'thumb': v_thumb, 'tube': v_tube, 'squash': v_squash,
           'ancient': v_ancient, 'haytham': v_ancient, 'trees': v_trees, 'sea': v_trees, 'dome': v_dome, 'dome2': v_dome,
           'astro': v_astro, 'astro2': v_astro, 'legs': v_legs, 'outro': v_outro}
