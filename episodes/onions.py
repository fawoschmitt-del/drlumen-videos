# Episode: Why do onions make you cry?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why do onions make you cry?"
SLUG = 'onions'
CAPTION = ("Onions fight back with a chemical ambush 🧅😭 And scientists made one that can't. "
           "#science #didyouknow #learnontiktok #onion #cooking #facts")
SOURCES = [
    'https://www.nature.com/articles/419685a',
    'https://www.the-scientist.com/the-crying-gene-52622',
    'https://www.liverpool.ac.uk/~sd21/onion/Know_Alliums_C&I_May10.pdf',
    'https://www2.kek.jp/imss/pf/science/publ/pfhl/2019/19hl4_3.pdf',
    'https://www.scientificamerican.com/blog/scicurious-brain/ignobels-2013-the-tearless-onion/',
]
BEATS = [
    ('BIG:CUT|AN ONION.|COUNT TO|TEN.', 'point', "Cut an onion. Count to ten. Here come the tears."),
    ('fight',    'shrug', "That's not you being sad. The onion is fighting back, with *chemistry*."),
    ('tearlessq','point', "And scientists have already made an onion that *can't* do it. Stay till the end."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('cells',    'point', "An onion is packed with tiny *cells*. Inside, certain chemicals are kept apart."),
    ('chop',     'down',  "Chop it, and you burst those cells. Suddenly everything *mixes*."),
    ('enzyme1',  'point', "First, an enzyme breaks a sulfur chemical into a very *unstable* piece."),
    ('enzyme2',  'down',  "Then a second enzyme grabs that piece and turns it into a *gas*."),
    ('name',     'shrug', "Its name: syn-propanethial-S-oxide. Scientists just call it the tear *factor*."),
    ('eyes',     'point', "The gas floats up into your eyes and *irritates* them."),
    ('tears',    'down',  "So your eyes do the only thing they can: flood with *tears* to wash it out."),
    ('oneenz',   'shrug', "For a long time, scientists thought *one* enzyme did all of this."),
    ('japan',    'point', "Then in two thousand two, a team in Japan found the second, hidden *enzyme*."),
    ('ignobel',  'up',    "They published it in the journal Nature, and later won an Ig *Nobel* prize for it."),
    ('garlic',   'down',  "Fun fact: garlic doesn't have that second step. That's why it doesn't make you *cry*."),
    ('tearless', 'up',    "Now, the tearless onion. Find the gene for that enzyme, and you can switch it *off*."),
    ('tearless2','point', "Working with partners, the team grew onions that make almost *no* tear gas."),
    ('outro',    'shrug', "So next time an onion makes you cry, don't take it personally. It's a chemical *ambush*."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

ON = (235, 200, 150); ON_D = (190, 140, 90); ON_IN = (250, 240, 220); GAS = (210, 240, 160)

def onion(d, cx, cy, s=1.0, cut=False, smile=False):
    if cut:
        d.ellipse([cx - 150 * s, cy - 130 * s, cx + 150 * s, cy + 150 * s], fill=ON_IN, outline=INK, width=int(8 * s))
        for k in range(1, 5):
            r = 150 * s * (1 - k * 0.2)
            d.ellipse([cx - r, cy + 10 * s - r * 0.93, cx + r, cy + 10 * s + r * 0.93], outline=ON_D, width=int(5 * s))
        return
    d.ellipse([cx - 150 * s, cy - 130 * s, cx + 150 * s, cy + 150 * s], fill=ON, outline=INK, width=int(8 * s))
    d.polygon([(cx - 30 * s, cy - 120 * s), (cx + 30 * s, cy - 120 * s), (cx, cy - 220 * s)], fill=ON, outline=INK)
    for k in (-80, 0, 80):
        d.arc([cx + k * s - 70 * s, cy - 120 * s, cx + k * s + 70 * s, cy + 140 * s], 250 if k <= 0 else 290, 110 if k >= 0 else 70, fill=ON_D, width=int(5 * s))
    for k in range(4):
        d.line([(cx - 30 * s + k * 20 * s, cy + 148 * s), (cx - 40 * s + k * 25 * s, cy + 185 * s)], fill=ON_D, width=int(5 * s))
    if smile:
        d.ellipse([cx - 55 * s, cy - 20 * s, cx - 30 * s, cy + 5 * s], fill=INK); d.ellipse([cx + 30 * s, cy - 20 * s, cx + 55 * s, cy + 5 * s], fill=INK)
        d.arc([cx - 50 * s, cy, cx + 50 * s, cy + 70 * s], 20, 160, fill=INK, width=int(7 * s))

def knife(d, x, y, s=1.0, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    def R(px, py): return (x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s)
    d.polygon([R(0, 0), R(260, 0), R(240, 50), R(0, 50)], fill=(215, 220, 230), outline=INK)
    d.polygon([R(-130, 5), R(0, 5), R(0, 45), R(-130, 45)], fill=INK)

def gas(d, cx, cy, lt, n=5, spread=120, rise=200):
    for k in range(n):
        ph = (lt * 0.7 + k / n) % 1
        x = cx + spread * math.sin(k * 2.3 + lt) * 0.6
        y = cy - rise * ph
        r = 22 + 30 * ph
        d.ellipse([x - r, y - r, x + r, y + r], fill=GAS, outline=(120, 170, 80), width=4)

def eye(d, cx, cy, s=1.0, teary=0.0, lt=0.0):
    d.ellipse([cx - 110 * s, cy - 65 * s, cx + 110 * s, cy + 65 * s], fill=WHITE, outline=INK, width=int(7 * s))
    d.ellipse([cx - 40 * s, cy - 40 * s, cx + 40 * s, cy + 40 * s], fill=(100, 170, 90), outline=INK, width=int(5 * s))
    d.ellipse([cx - 18 * s, cy - 18 * s, cx + 18 * s, cy + 18 * s], fill=INK)
    if teary > 0:
        for k in range(2):
            ph = (lt * 1.0 + k * 0.5) % 1
            y = cy + 60 * s + 160 * s * ph
            x = cx + (60 - 120 * k) * s
            d.polygon([(x, y - 30 * s), (x - 18 * s, y + 5 * s), (x + 18 * s, y + 5 * s)], fill=CYAN)
            d.ellipse([x - 18 * s, y - 12 * s, x + 18 * s, y + 22 * s], fill=CYAN, outline=INK, width=3)

def v_fight(lt, b):
    im, d = X.new_card()
    title(d, 'IT FIGHTS BACK')
    onion(d, 300, 400, 0.95)
    d.ellipse([235, 360, 265, 390], fill=INK); d.ellipse([335, 360, 365, 390], fill=INK)
    d.line([(225, 335), (275, 355)], fill=INK, width=8); d.line([(375, 335), (325, 355)], fill=INK, width=8)
    gas(d, 650, 520, lt, 6, 160, 280)
    return im

def v_tearlessq(lt, b):
    im, d = X.new_card()
    title(d, 'NO-TEARS ONION?', 88)
    onion(d, 300, 400, 0.9, smile=True)
    d.ellipse([570, 230, 830, 490], fill=(60, 55, 80), outline=INK, width=8)
    label(d, (700, 360), '?', 180, YEL, FA, stroke=6)
    return im

def cellgrid(d, lt, burst=0.0):
    for i in range(12):
        x = 140 + (i % 4) * 190; y = 230 + (i // 4) * 130
        if burst > 0 and i % 3 != 1:
            j = burst * 18
            d.line([(x - 60 - j, y - 40), (x - 20, y - 10)], fill=INK, width=5)
            d.line([(x + 60 + j, y + 40), (x + 20, y + 10)], fill=INK, width=5)
            d.ellipse([x - 30 - j, y - 15, x - 10 - j, y + 5], fill=PINK)
            d.ellipse([x + 10 + j, y - 5, x + 30 + j, y + 15], fill=CYAN)
        else:
            d.rounded_rectangle([x - 80, y - 50, x + 80, y + 50], 20, fill=ON_IN, outline=INK, width=5)
            d.ellipse([x - 50, y - 20, x - 10, y + 20], fill=PINK); d.ellipse([x + 10, y - 20, x + 50, y + 20], fill=CYAN)
            d.line([(x, y - 45), (x, y + 45)], fill=INK, width=4)

def v_cells(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'cells':
        title(d, 'KEPT APART')
        cellgrid(d, lt)
    else:
        title(d, 'CHOP = MIX!')
        cellgrid(d, lt, burst=min(1, lt / 0.6))
        knife(d, 300, 150 + 40 * abs(math.sin(lt * 5)), 1.0)
    return im

def pac(d, cx, cy, r, col, lt):
    """an enzyme drawn as a pair of molecular scissors that snip open and shut"""
    a = 0.25 + 0.2 * abs(math.sin(lt * 6))
    for sgn in (-1, 1):
        ang = sgn * a
        tip = (cx + r * 1.1 * math.cos(ang), cy + r * 1.1 * math.sin(ang))
        back = (cx - r * 0.35 * math.cos(ang), cy - r * 0.35 * math.sin(ang))
        d.line([back, tip], fill=INK, width=int(r * 0.32)); d.line([back, tip], fill=(215, 220, 230), width=int(r * 0.2))
        hx, hy = cx - r * 0.75 * math.cos(-ang), cy - r * 0.75 * math.sin(-ang)
        d.ellipse([hx - r * 0.38, hy - r * 0.38, hx + r * 0.38, hy + r * 0.38], fill=col, outline=INK, width=6)
        d.ellipse([hx - r * 0.16, hy - r * 0.16, hx + r * 0.16, hy + r * 0.16], fill=X.CARD, outline=INK, width=4)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=INK)

def v_enzyme(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'enzyme1':
        title(d, 'ENZYME #1')
        pac(d, 250, 380, 100, YEL, lt)
        d.ellipse([400, 340, 480, 420], fill=PINK, outline=INK, width=5)
        arrow(d, (510, 380), (620, 380), INK, 10, 28)
        wob = 10 * math.sin(lt * 14)
        d.polygon([(720 + wob, 310), (790, 380 + wob), (720 - wob, 450), (650, 380 - wob)], fill=ORANGE, outline=INK)
        label(d, (720, 520), 'unstable!', 50, ORANGE, FA)
    else:
        title(d, 'ENZYME #2 = GAS')
        pac(d, 230, 380, 100, PINK, lt)
        d.polygon([(400, 340), (440, 380), (400, 420), (360, 380)], fill=ORANGE, outline=INK)
        arrow(d, (470, 380), (570, 380), INK, 10, 28)
        gas(d, 720, 470, lt, 5, 120, 240)
    return im

def v_name(lt, b):
    im, d = X.new_card()
    title(d, 'THE TEAR FACTOR', 88)
    label(d, (CW / 2 - 5, 290), 'syn-propanethial-', 72, PINK, FA, stroke=2)
    label(d, (CW / 2 - 5, 380), 'S-oxide', 72, PINK, FA, stroke=2)
    sub(d, '"lachrymatory factor" (lacrima = tear)', 540, 40)
    return im

def v_eyes(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'eyes':
        title(d, 'GAS -> EYES')
        onion(d, 220, 470, 0.7, cut=True)
        gas(d, 330, 400, lt, 6, 200, 220)
        eye(d, 690, 300, 1.0)
    else:
        title(d, 'FLUSH IT OUT!')
        eye(d, 300, 300, 0.9, 1, lt); eye(d, 640, 300, 0.9, 1, lt + 0.3)
    return im

def v_oneenz(lt, b):
    im, d = X.new_card()
    title(d, 'ONE ENZYME?')
    pac(d, 300, 380, 110, YEL, lt)
    label(d, (650, 340), 'did it', 60, INK, FA)
    label(d, (650, 420), 'ALL?', 80, PINK, FA)
    return im

def v_japan(lt, b):
    im, d = X.new_card()
    title(d, '2002: FOUND IT')
    pac(d, 280, 380, 100, YEL, lt)
    k = popk(lt)
    pac(d, 630, 380, max(1, 110 * k), PINK, lt)
    label(d, (630, 560), 'enzyme #2', 48, PINK, FA)
    return im

def v_ignobel(lt, b):
    im, d = X.new_card()
    title(d, 'PAPER + IG NOBEL', 86)
    d.rounded_rectangle([130, 190, 400, 560], 14, fill=WHITE, outline=INK, width=7)
    label(d, (265, 240), 'JOURNAL', 50, INK, FA)
    for k in range(6): d.line([(160, 300 + k * 40), (370, 300 + k * 40)], fill=(190, 190, 200), width=8)
    # trophy
    d.pieslice([540, 200, 800, 420], 0, 180, fill=YEL, outline=INK, width=7)
    d.rectangle([640, 410, 700, 490], fill=YEL, outline=INK, width=6)
    d.rounded_rectangle([580, 490, 760, 540], 12, fill=BROWN, outline=INK, width=6)
    label(d, (670, 590), '2013', 50, INK, FA)
    return im

def v_garlic(lt, b):
    im, d = X.new_card()
    title(d, 'GARLIC: NO STEP 2', 86)
    cx, cy = 300, 400
    for dx in (-60, 0, 60):
        d.ellipse([cx + dx - 70, cy - 120, cx + dx + 70, cy + 120], fill=WHITE, outline=INK, width=6)
    d.polygon([(cx - 20, cy - 110), (cx + 20, cy - 110), (cx, cy - 200)], fill=WHITE, outline=INK)
    pac(d, 650, 330, 70, YEL, lt)
    d.rounded_rectangle([580, 450, 720, 530], 20, fill=(225, 220, 212), outline=INK, width=5)
    cross(d, 650, 490, 40, 12)
    return im

def v_tearless(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'tearless':
        title(d, 'SWITCH IT OFF')
        # DNA ladder with switch
        for i in range(10):
            y = 200 + i * 38
            x1 = 200 + 50 * math.sin(i * 0.7 + lt * 2); x2 = 330 - 50 * math.sin(i * 0.7 + lt * 2)
            d.line([(x1, y), (x2, y)], fill=PINK if 4 <= i <= 5 else (190, 190, 200), width=8)
            d.ellipse([x1 - 9, y - 9, x1 + 9, y + 9], fill=CYAN); d.ellipse([x2 - 9, y - 9, x2 + 9, y + 9], fill=CYAN)
        on = lt < 1.2
        d.rounded_rectangle([520, 300, 800, 440], 70, fill=GRN if on else (200, 200, 210), outline=INK, width=8)
        kx = 730 if on else 590
        d.ellipse([kx - 55, 315, kx + 55, 425], fill=WHITE, outline=INK, width=6)
        label(d, (660, 510), 'ON' if on else 'OFF', 64, INK, FA)
    else:
        title(d, 'NO TEAR GAS')
        onion(d, 300, 410, 0.9, smile=True)
        eye(d, 690, 330, 0.9)
        check(d, 690, 520, 50, 14)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, 'CHEMICAL AMBUSH')
    onion(d, 300, 420, 0.85, cut=True)
    gas(d, 300, 380, lt, 6, 200, 220)
    eye(d, 690, 330, 0.9, 1, lt)
    return im

VISUALS = {'fight': v_fight, 'tearlessq': v_tearlessq, 'cells': v_cells, 'chop': v_cells, 'enzyme1': v_enzyme,
           'enzyme2': v_enzyme, 'name': v_name, 'eyes': v_eyes, 'tears': v_eyes, 'oneenz': v_oneenz, 'japan': v_japan,
           'ignobel': v_ignobel, 'garlic': v_garlic, 'tearless': v_tearless, 'tearless2': v_tearless, 'outro': v_outro}
