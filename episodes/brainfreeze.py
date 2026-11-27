# Episode: Why do we get brain freeze?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why do we get brain freeze?"
SLUG = 'brainfreeze'
CAPTION = ("Brain freeze isn't your brain freezing 🧊🧠 And your tongue can stop it in seconds. "
           "#science #didyouknow #learnontiktok #brainfreeze #icecream #facts")
SOURCES = [
    'https://www.scientificamerican.com/article/brain-freeze-explained/',
    'https://www.universityofgalway.ie/about-us/news-and-events/news-archive/2012/april2012/brain-freeze-find-might-help-solve-migraine-mysteries-1.html',
    'https://www.livescience.com/19834-brain-freeze-blood-flow-migraines.html',
    'https://www.hopkinsmedicine.org/health/expert-qa/how-to-ease-brain-freeze',
    'https://my.clevelandclinic.org/health/diseases/21478-brain-freeze',
    'https://www.inquirer.com/philly/health/the-science-behind-brain-freeze-and-what-you-can-do-about-it-20170711.html',
]
BEATS = [
    ('BIG:ICE CREAM.|TOO FAST.|OUCH!', 'point', "Ice cream. Too fast. Ouch!"),
    ('stab',     'shrug', "That stabbing pain in your forehead? Your brain isn't freezing at *all*."),
    ('tongueq',  'point', "And you can stop it in seconds, with your *tongue*. Stay till the end."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('name',     'shrug', "Doctors call it sphenopalatine *ganglioneuralgia*. Try saying that with a brain freeze."),
    ('palate',   'point', "It starts up here, on the *roof* of your mouth."),
    ('straw',    'down',  "Scientists had thirteen volunteers sip ice water through a straw, aimed right at that *spot*."),
    ('scan',     'point', "Then they watched the blood flow inside their heads, second by *second*."),
    ('artery',   'down',  "Just before the pain hit, a big artery behind the eyes suddenly *widened*."),
    ('artery2',  'point', "Blood came *rushing* in. And when the artery narrowed again, the pain faded."),
    ('warm',     'shrug', "The idea? Your brain hates getting cold, so it floods itself with *warm* blood."),
    ('pressure', 'down',  "But your skull is a closed box. More blood means more *pressure*. Ouch."),
    ('migraine', 'point', "People who get migraines are even more likely to get brain *freeze*."),
    ('short',    'shrug', "The good news: in almost everyone, it's gone in under *five* minutes."),
    ('tongue',   'up',    "Now, the trick. Press your *tongue* flat against the roof of your mouth."),
    ('tongue2',  'point', "It warms the cold spot back up. A sip of *warm* water works too."),
    ('front',    'down',  "Or just keep the cold stuff at the *front* of your mouth, and slow down."),
    ('outro',    'shrug', "So brain freeze isn't a frozen brain. It's a brain *overreacting* to stay warm."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

ICE = (180, 230, 255)

def cone(d, cx, cy, s=1.0, bites=0):
    d.polygon([(cx - 70 * s, cy), (cx + 70 * s, cy), (cx, cy + 210 * s)], fill=(230, 170, 90), outline=INK)
    d.line([(cx - 70 * s, cy), (cx, cy + 210 * s), (cx + 70 * s, cy)], fill=INK, width=int(7 * s))
    for k in range(3):
        d.line([(cx - 55 * s + k * 40 * s, cy + 10 * s), (cx + 5 * s + k * 20 * s, cy + 150 * s)], fill=(200, 130, 60), width=int(5 * s))
    d.ellipse([cx - 85 * s, cy - 120 * s, cx + 85 * s, cy + 30 * s], fill=(255, 190, 210), outline=INK, width=int(7 * s))
    if bites:
        d.ellipse([cx + 30 * s, cy - 130 * s, cx + 110 * s, cy - 60 * s], fill=X.CARD)

def side_head(d, cx, cy, s=1.0, lt=0.0, cold=False, artery=0.0, pain=False):
    """head in profile facing left, with mouth palate marked"""
    d.ellipse([cx - 190 * s, cy - 200 * s, cx + 170 * s, cy + 150 * s], fill=SKIN, outline=INK, width=int(8 * s))
    d.polygon([(cx - 185 * s, cy - 10 * s), (cx - 235 * s, cy + 40 * s), (cx - 180 * s, cy + 60 * s)], fill=SKIN, outline=INK)
    d.ellipse([cx - 120 * s, cy - 70 * s, cx - 90 * s, cy - 40 * s], fill=INK)
    # mouth + palate
    d.chord([cx - 180 * s, cy + 50 * s, cx - 20 * s, cy + 150 * s], 180, 360, fill=(160, 50, 70), outline=INK, width=int(6 * s))
    d.line([(cx - 175 * s, cy + 98 * s), (cx - 30 * s, cy + 98 * s)], fill=INK, width=int(6 * s))
    if cold:
        d.arc([cx - 175 * s, cy + 55 * s, cx - 25 * s, cy + 140 * s], 200, 340, fill=CYAN, width=int(14 * s))
    if artery > 0:
        w = int((10 + 22 * artery) * s)
        d.line([(cx - 40 * s, cy + 60 * s), (cx - 20 * s, cy - 40 * s), (cx - 80 * s, cy - 130 * s)], fill=RED, width=w, joint='curve')
    if pain:
        for k in range(5):
            a = -2.4 + k * 0.25
            r1, r2 = 200 * s, (228 + 14 * math.sin(lt * 10 + k)) * s
            d.line([(cx - 60 * s + r1 * math.cos(a), cy - 60 * s + r1 * math.sin(a)), (cx - 60 * s + r2 * math.cos(a), cy - 60 * s + r2 * math.sin(a))], fill=PINK, width=int(10 * s))

def v_stab(lt, b):
    im, d = X.new_card()
    title(d, 'NOT FROZEN')
    side_head(d, 420, 420, 0.95, lt, pain=True)
    X.brain(d, 450, 340, 0.45)
    check(d, 780, 360, 70)
    return im

def v_tongueq(lt, b):
    im, d = X.new_card()
    title(d, 'THE FIX?')
    head(d, 300, 380, 1.0, mouth='o')
    d.ellipse([270, 440, 330, 470], fill=PINK)
    d.ellipse([560, 220, 820, 480], fill=(60, 55, 80), outline=INK, width=8)
    label(d, (690, 350), '?', 200, YEL, FA, stroke=6)
    return im

def v_name(lt, b):
    im, d = X.new_card()
    title(d, 'THE REAL NAME', 88)
    label(d, (CW / 2 - 5, 300), 'SPHENOPALATINE', 92, PINK, FA, stroke=3)
    label(d, (CW / 2 - 5, 420), 'GANGLIONEURALGIA', 92, PINK, FA, stroke=3)
    sub(d, '= ice cream headache', 570, 50)
    return im

def v_palate(lt, b):
    im, d = X.new_card()
    title(d, 'ROOF OF MOUTH')
    side_head(d, 470, 390, 1.1, lt, cold=True)
    arrow(d, (760, 560), (430, 510), CYAN, 10, 30)
    return im

def v_straw(lt, b):
    im, d = X.new_card()
    title(d, '13 VOLUNTEERS')
    side_head(d, 560, 390, 1.0, lt, cold=lt > 0.8)
    d.rounded_rectangle([110, 330, 230, 560], 20, fill=ICE, outline=INK, width=7)
    for k in range(3): d.rectangle([130 + k * 32, 380 + 40 * k, 160 + k * 32, 410 + 40 * k], fill=WHITE, outline=INK, width=3)
    d.line([(190, 360), (260, 300), (420, 490)], fill=PINK, width=14, joint='curve')
    return im

def v_scan(lt, b):
    im, d = X.new_card()
    title(d, 'BLOOD FLOW SCAN')
    side_head(d, 330, 390, 0.85, lt, artery=0.3)
    d.rounded_rectangle([590, 220, 880, 520], 24, fill=INK, outline=INK, width=6)
    pts = [(610 + i * 6.5, 400 - 60 * abs(math.sin(i * 0.35 + lt * 6)) * (0.5 + 0.5 * math.sin(i * 0.05))) for i in range(40)]
    d.line(pts, fill=GRN, width=6)
    return im

def v_artery(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'artery':
        title(d, 'ARTERY WIDENS')
        k = ease_out(min(1, lt / 1.0))
        side_head(d, 470, 400, 1.1, lt, cold=True, artery=k)
    else:
        title(d, 'BLOOD RUSH')
        k = 1 - 0.7 * ease_out(max(0, min(1, (lt - 1.6) / 1.0)))
        side_head(d, 470, 400, 1.1, lt, cold=True, artery=k, pain=k > 0.6)
        for j in range(3):
            ph = (lt * 1.5 + j / 3) % 1
            d.ellipse([440 - 10 + 30 * ph, 470 - 100 * ph - 10, 440 + 10 + 30 * ph, 470 - 100 * ph + 10], fill=RED)
    return im

def v_warm(lt, b):
    im, d = X.new_card()
    title(d, 'KEEP BRAIN WARM')
    X.brain(d, 360, 380, 0.85)
    thermo(d, 760, 360, 300, 0.75)
    for k in range(4):
        ph = (lt * 1.3 + k / 4) % 1
        d.ellipse([540 - 230 * ph, 560 - 120 * ph, 570 - 230 * ph, 590 - 120 * ph], fill=RED)
    return im

def v_pressure(lt, b):
    im, d = X.new_card()
    title(d, 'CLOSED BOX')
    s = 1 + 0.05 * math.sin(lt * 8)
    d.rounded_rectangle([240 - 20 * s, 200 - 20 * s, 700 + 20 * s, 560 + 20 * s], 60, fill=(240, 235, 225), outline=INK, width=10)
    X.brain(d, 470, 370, 0.85 * s)
    for (x, y, dx, dy) in ((200, 380, -1, 0), (740, 380, 1, 0)):
        arrow(d, (x - 10 * dx, y - 10 * dy), (x + 70 * dx, y + 70 * dy), PINK, 12, 30)
    return im

def v_migraine(lt, b):
    im, d = X.new_card()
    title(d, 'MIGRAINE LINK')
    head(d, 300, 390, 0.9, mouth='sad', eyes='closed')
    for k in range(4):
        a = -2.6 + k * 0.35
        d.line([(300 + 160 * math.cos(a), 390 + 160 * math.sin(a)), (300 + 210 * math.cos(a), 390 + 210 * math.sin(a))], fill=PINK, width=10)
    bars(d, [('migraine', 0.85, PINK, 'MORE'), ('no migraine', 0.5, CYAN, 'LESS')], x0=700, y0=320, w=200, h=56, gap=120, k=1, lw=32)
    label(d, (720, 210), 'brain freezes', 40, INK, FB)
    return im

def v_short(lt, b):
    im, d = X.new_card()
    title(d, '< 5 MINUTES')
    X.stopwatch(d, 470, 390, 170, min(1, lt / 2.5) * 0.9)
    sub(d, 'in 98 out of 100 people', 625)
    return im

def v_tongue(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'tongue':
        title(d, 'TONGUE UP!')
        side_head(d, 470, 390, 1.1, lt, cold=lt < 1.2)
        up = min(1, lt / 0.8)
        y = 540 - 40 * up
        d.chord([300, y - 40, 440, y + 40], 180, 360, fill=PINK, outline=INK, width=6)
    else:
        title(d, 'WARM IT UP')
        side_head(d, 330, 390, 0.85, lt)
        d.rounded_rectangle([610, 300, 790, 560], 26, fill=ORANGE, outline=INK, width=7)
        d.arc([760, 350, 860, 470], 270, 90, fill=INK, width=12)
        for k in range(3):
            ph = (lt * 1.2 + k / 3) % 1
            x = 650 + k * 50
            d.line([(x, 280 - 80 * ph), (x + 12 * math.sin(ph * 9), 240 - 80 * ph)], fill=(200, 200, 210), width=8)
    return im

def v_front(lt, b):
    im, d = X.new_card()
    title(d, 'FRONT + SLOW')
    cone(d, 280, 320, 1.0, bites=1)
    side_head(d, 640, 390, 0.75, lt)
    d.rounded_rectangle([700, 540, 900, 600], 30, fill=GRN, outline=INK, width=6)
    label(d, (800, 570), 'SLOW', 40, INK, FA)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, 'BRAIN: OVERREACTING', 80)
    X.brain(d, 330, 390, 0.75)
    for k in range(3):
        a = lt * 4 + k * 2.1
        d.line([(330 + 170 * math.cos(a), 390 + 130 * math.sin(a)), (330 + 200 * math.cos(a), 390 + 160 * math.sin(a))], fill=PINK, width=10)
    cone(d, 690, 330, 0.9)
    return im

VISUALS = {'stab': v_stab, 'tongueq': v_tongueq, 'name': v_name, 'palate': v_palate, 'straw': v_straw, 'scan': v_scan,
           'artery': v_artery, 'artery2': v_artery, 'warm': v_warm, 'pressure': v_pressure, 'migraine': v_migraine,
           'short': v_short, 'tongue': v_tongue, 'tongue2': v_tongue, 'front': v_front, 'outro': v_outro}
