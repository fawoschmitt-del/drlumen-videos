# Episode: Why do mosquitoes bite some people more than others?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why do mosquitoes bite some people more?"
SLUG = 'mosquito'
CAPTION = ("One person in a lab was 100x tastier to mosquitoes than another 🦟 Are you a mosquito magnet? "
           "#science #didyouknow #learnontiktok #mosquito #summer #facts")
SOURCES = [
    'https://www.rockefeller.edu/news/33019-why-mosquitoes-bite-some-people-more/',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC10069481/',
    'https://lshtm.ac.uk/newsevents/news/2015/twins_mosquito_study.html',
    'https://www.cdc.gov/mosquitoes/about/what-is-a-mosquito.html',
    'https://www.brainfacts.org/in-the-lab/animals-in-research/2019/why-do-mosquitoes-bite-us-011519',
]
BEATS = [
    ('BIG:SUMMER NIGHT.|YOU: TEN BITES.|YOUR FRIEND:|ZERO.', 'point',
     "Summer night. You: ten bites. Your friend: zero. Sound familiar?"),
    ('magnet',    'shrug', "That's not bad luck. Some people really are mosquito *magnets*."),
    ('teaser',    'point', "And in one lab test, one person was a *hundred* times tastier than another. Stay till the end."),
    ('intro',     'up',    "I'm Doctor Lumen. Let's crack this."),
    ('females',   'point', "First: only female mosquitoes bite. They need your blood to make *eggs*."),
    ('males',     'shrug', "The males? They just sip flower nectar and fruit juice. Total *vegetarians*."),
    ('co2',       'point', "Now, every time you breathe out, you release a cloud of carbon *dioxide*."),
    ('radar',     'down',  "A hungry female senses it from far away and follows the trail straight to *you*."),
    ('heat',      'point', "Closer in, she smells your skin and feels your body *heat*."),
    ('smell',     'shrug', "But here's the crazy part. To her, everyone's skin smells *different*."),
    ('stockings', 'point', "Scientists in New York had people wear nylon stockings on their arms, six *hours* a day."),
    ('tournament','down',  "Then mosquitoes had to pick between two stockings. A smelly *tournament*, for three years."),
    ('acids',     'point', "The magnets had way more of certain skin chemicals called carboxylic *acids*."),
    ('years',     'shrug', "And bad news: if you were a magnet, you *stayed* a magnet. Year after year."),
    ('twins',     'point', "A study of twins in London found it runs in families, probably through your body *odor*."),
    ('myths',     'down',  "Sweet blood? Eating bananas? Scientists found little proof for those *myths*."),
    ('winner',    'up',    "Now, the champion. Subject thirty-three. Four times tastier than the *runner-up*..."),
    ('winner2',   'point', "and a *hundred* times tastier than the least attractive person in the study!"),
    ('outro',     'shrug', "So if you always get bitten, don't take it personally. You're just *delicious*."),
    ('follow',    'up',    "Follow for a new everyday mystery, every single day!"),
]

BODY = (70, 65, 90); WING = (200, 230, 255); NYLON = (230, 190, 150); BLOOD = (200, 30, 50); CO2 = (200, 210, 230)

def mosquito(d, cx, cy, s=1.0, lt=0.0, face=1):
    """cartoon mosquito facing left, wings flap with lt"""
    flap = 0.5 + 0.5 * math.sin(lt * 40)
    h = (55 + 30 * flap) * s
    d.ellipse([cx - 5 * s, cy - 12 * s - h, cx + 55 * s, cy - 12 * s], fill=WING, outline=INK, width=max(2, int(4 * s)))
    d.ellipse([cx + 25 * s, cy - 10 * s - h * 0.8, cx + 80 * s, cy - 10 * s], fill=WING, outline=INK, width=max(2, int(4 * s)))
    for i in range(3):   # legs
        x = cx + (-10 + i * 30) * s
        d.line([(x, cy + 8 * s), (x - 20 * s, cy + 55 * s), (x - 30 * s, cy + 85 * s)], fill=INK, width=max(2, int(4 * s)))
    d.ellipse([cx - 15 * s, cy - 16 * s, cx + 120 * s, cy + 16 * s], fill=BODY, outline=INK, width=max(2, int(4 * s)))
    for k in range(3):
        x = cx + (45 + k * 22) * s
        d.line([(x, cy - 14 * s), (x, cy + 14 * s)], fill=(140, 135, 160), width=max(2, int(4 * s)))
    hx = cx - 30 * s
    d.ellipse([hx - 26 * s, cy - 26 * s, hx + 26 * s, cy + 22 * s], fill=BODY, outline=INK, width=max(2, int(4 * s)))
    d.ellipse([hx - 18 * s, cy - 18 * s, hx - 2 * s, cy - 2 * s], fill=WHITE)
    d.ellipse([hx - 14 * s, cy - 14 * s, hx - 6 * s, cy - 6 * s], fill=INK)
    d.line([(hx - 22 * s, cy + 6 * s), (hx - 95 * s, cy + 32 * s)], fill=INK, width=max(2, int(5 * s)))   # proboscis

def arm(d, x0, y0, x1, h=110, col=SKIN, sock=False):
    d.rounded_rectangle([x0, y0, x1, y0 + h], h // 2, fill=NYLON if sock else col, outline=INK, width=7)
    if sock:
        for k in range(int((x1 - x0) / 40)):
            xx = x0 + 30 + k * 40
            d.line([(xx, y0 + 10), (xx - 15, y0 + h - 10)], fill=(200, 160, 120), width=4)

def bite(d, x, y, r=26):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 140, 150), outline=RED, width=5)
    d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=RED)

def stink(d, cx, cy, lt, n=4, col=GRN, rise=160, spread=60):
    for k in range(n):
        ph = (lt * 0.8 + k / n) % 1
        x = cx + spread * math.sin(k * 2.1 + lt * 2)
        y = cy - rise * ph
        for j in range(3):
            yy = y - j * 22
            d.arc([x - 20 + 12 * math.sin(j + lt * 3), yy - 15, x + 20 + 12 * math.sin(j + lt * 3), yy + 15], 180, 360, fill=col, width=7)

def v_magnet(lt, b):
    im, d = X.new_card()
    title(d, 'MOSQUITO MAGNET', 88)
    head(d, 300, 400, 0.95, 'sad')
    # horseshoe magnet
    d.arc([560, 230, 820, 490], 180, 360, fill=RED, width=60)
    d.rectangle([560, 360, 620, 470], fill=RED); d.rectangle([760, 360, 820, 470], fill=RED)
    d.rectangle([560, 440, 620, 480], fill=GREY); d.rectangle([760, 440, 820, 480], fill=GREY)
    for k in range(3):
        ph = (lt * 0.6 + k / 3) % 1
        mosquito(d, 860 - 120 * ph + 0 * k, 200 + k * 130, 0.55, lt + k)
    bite(d, 240, 470, 20); bite(d, 370, 330, 18)
    return im

def v_teaser(lt, b):
    im, d = X.new_card()
    title(d, '100x TASTIER?', 92)
    head(d, 250, 400, 0.8, 'o'); head(d, 690, 400, 0.8, 'smile')
    k = popk(lt)
    label(d, (250, 590), '100x', int(90 * max(0.05, k)), PINK, FA, stroke=4)
    label(d, (690, 590), '1x', 70, INK, FA)
    mosquito(d, 470, 230 + 20 * math.sin(lt * 3), 0.7, lt)
    return im

def v_females(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'females':
        title(d, 'ONLY FEMALES BITE', 84)
        mosquito(d, 330, 360, 1.3, lt)
        label(d, (330, 560), 'FEMALE', 64, PINK, FA)
        # eggs
        for k in range(5):
            x = 640 + (k % 3) * 70; y = 320 + (k // 3) * 80
            d.ellipse([x - 28, y - 38, x + 28, y + 38], fill=WHITE, outline=INK, width=5)
        d.polygon([(700, 470), (680, 520), (720, 520)], fill=BLOOD)
        d.ellipse([675, 500, 725, 550], fill=BLOOD)
        label(d, (700, 600), 'blood -> eggs', 44, INK, FA)
    else:
        title(d, 'MALES: NECTAR ONLY', 84)
        mosquito(d, 300, 360, 1.2, lt)
        label(d, (300, 560), 'MALE', 64, CYAN, FA)
        cx, cy = 690, 360
        for k in range(6):
            a = k * math.pi / 3 + lt * 0.5
            px, py = cx + 70 * math.cos(a), cy + 70 * math.sin(a)
            d.ellipse([px - 50, py - 50, px + 50, py + 50], fill=PINK, outline=INK, width=5)
        d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=YEL, outline=INK, width=6)
        d.line([(cx, cy + 110), (cx, cy + 260)], fill=GRN, width=14)
    return im

def v_co2(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'co2':
        title(d, 'YOU EXHALE CO2')
        head(d, 250, 400, 0.9, 'o')
        for k in range(5):
            ph = (lt * 0.6 + k / 5) % 1
            x = 400 + 450 * ph; y = 430 - 40 * math.sin(ph * 3 + k)
            r = 30 + 40 * ph
            d.ellipse([x - r, y - r, x + r, y + r], fill=CO2, outline=DGREY, width=4)
            if r > 45: label(d, (x, y), 'CO2', int(r * 0.6), DGREY, FA)
    else:
        title(d, 'FOLLOW THE TRAIL')
        head(d, 180, 400, 0.7, 'o')
        for k in range(8):
            x = 290 + k * 70; y = 420 - 20 * math.sin(k)
            d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=CO2, outline=DGREY, width=3)
        p = (lt * 0.25) % 1
        mosquito(d, 830 - 300 * p, 330 + 20 * math.sin(lt * 4), 0.8, lt)
        arrow(d, (760, 560), (380, 560), PINK, 12, 34)
    return im

def v_heat(lt, b):
    im, d = X.new_card()
    title(d, 'SMELL + HEAT')
    arm(d, 80, 400, 640)
    for k in range(4):
        x = 150 + k * 130
        pts = [(x + 14 * math.sin(j * 0.9 + lt * 6), 385 - j * 14) for j in range(12)]
        d.line(pts, fill=ORANGE, width=9, joint='curve')
    stink(d, 400, 380, lt, 3, GRN)
    mosquito(d, 780, 330 + 15 * math.sin(lt * 5), 0.9, lt)
    thermo(d, 840, 500, 140, 0.8)
    return im

def v_smell(lt, b):
    im, d = X.new_card()
    title(d, 'EVERYONE SMELLS DIFFERENT', 70)
    cols = [GRN, PINK, CYAN]
    for i, x in enumerate((180, 470, 760)):
        head(d, x, 430, 0.6, 'smile')
        stink(d, x, 300, lt + i * 0.3, 3, cols[i], 110, 40)
    return im

def v_stockings(lt, b):
    im, d = X.new_card()
    title(d, 'NYLON ON YOUR ARM', 86)
    arm(d, 80, 230, 860, 140)
    k = min(1, lt / 1.2)
    x1 = 80 + 640 * ease_out(k)
    if x1 > 140: arm(d, 80, 220, int(x1), 160, sock=True)
    X.stopwatch(d, 700, 540, 70, (lt * 0.3) % 1)
    label(d, (400, 540), '6 HOURS', 80, PINK, FA)
    return im

def v_tournament(lt, b):
    im, d = X.new_card()
    title(d, 'SMELLY TOURNAMENT', 86)
    # Y-maze: two boxes with stockings
    d.rounded_rectangle([90, 200, 330, 400], 20, fill=WHITE, outline=INK, width=6)
    d.rounded_rectangle([610, 200, 850, 400], 20, fill=WHITE, outline=INK, width=6)
    for x0 in (130, 650):
        d.rounded_rectangle([x0, 270, x0 + 160, 330], 30, fill=NYLON, outline=INK, width=5)
    label(d, (210, 240), 'A', 44, INK, FA); label(d, (730, 240), 'B', 44, INK, FA)
    d.line([(330, 300), (470, 450), (610, 300)], fill=GREY, width=30)
    d.line([(470, 450), (470, 620)], fill=GREY, width=30)
    p = (lt * 0.4) % 1
    side = -1 if int(lt * 0.4) % 2 == 0 else 1
    if p < 0.5: mx, my = 470, 600 - 300 * p
    else: mx, my = 470 + side * 260 * (p - 0.5), 450 - 260 * (p - 0.5)
    mosquito(d, mx, my, 0.55, lt)
    return im

def v_acids(lt, b):
    im, d = X.new_card()
    title(d, 'CARBOXYLIC ACIDS', 88)
    bars(d, [('magnet', 1.0, PINK, 'HIGH'), ('normal', 0.45, CYAN, ''), ('low', 0.15, GRN, '')], x0=330, y0=230,
         w=500, h=70, gap=130, k=ease_out(min(1, lt / 0.8)), lw=46)
    return im

def v_years(lt, b):
    im, d = X.new_card()
    title(d, 'STILL A MAGNET', 88)
    for i, yr in enumerate(('YEAR 1', 'YEAR 2', 'YEAR 3')):
        x = 180 + i * 290
        d.rounded_rectangle([x - 120, 200, x + 120, 520], 20, fill=WHITE, outline=INK, width=6)
        label(d, (x, 250), yr, 46, INK, FA)
        d.arc([x - 70, 300, x + 70, 440], 180, 360, fill=RED, width=34)
        d.rectangle([x - 87, 370, x - 53, 440], fill=RED); d.rectangle([x + 53, 370, x + 87, 440], fill=RED)
        if lt > 0.3 * i: check(d, x, 600, 34, 12)
    return im

def v_twins(lt, b):
    im, d = X.new_card()
    title(d, 'TWINS: IN YOUR GENES', 80)
    head(d, 230, 380, 0.7, 'smile'); head(d, 450, 380, 0.7, 'smile')
    stink(d, 340, 260, lt, 4, GRN, 100, 80)
    # DNA
    for i in range(9):
        y = 210 + i * 40
        x1 = 680 + 50 * math.sin(i * 0.7 + lt * 2); x2 = 820 - 50 * math.sin(i * 0.7 + lt * 2)
        d.line([(x1, y), (x2, y)], fill=(190, 190, 200), width=8)
        d.ellipse([x1 - 9, y - 9, x1 + 9, y + 9], fill=PINK); d.ellipse([x2 - 9, y - 9, x2 + 9, y + 9], fill=CYAN)
    sub(d, 'London, 2015 (pilot study)', 600, 40)
    return im

def v_myths(lt, b):
    im, d = X.new_card()
    title(d, 'MYTHS?', 96)
    d.rounded_rectangle([150, 210, 330, 390], 16, fill=WHITE, outline=INK, width=7)   # sugar cube
    d.line([(150, 260), (330, 260)], fill=GREY, width=4); d.line([(200, 210), (200, 390)], fill=GREY, width=4)
    label(d, (240, 470), 'SWEET BLOOD', 50, INK, FA)
    d.arc([530, 130, 830, 430], 95, 200, fill=INK, width=76)      # banana
    d.arc([530, 130, 830, 430], 97, 198, fill=YEL, width=60)
    label(d, (690, 470), 'BANANAS', 50, INK, FA)
    k = popk(lt)
    if k > 0.05:
        cross(d, 240, 300, int(90 * k), 16); cross(d, 650, 300, int(90 * k), 16)
    sub(d, 'little proof for either', 590, 46)
    return im

def v_winner(lt, b):
    im, d = X.new_card()
    if b['vis'] == 'winner':
        title(d, 'SUBJECT 33', 96)
        d.pieslice([330, 190, 610, 420], 0, 180, fill=YEL, outline=INK, width=7)
        d.rectangle([440, 410, 500, 480], fill=YEL, outline=INK, width=6)
        d.rounded_rectangle([380, 480, 560, 530], 12, fill=BROWN, outline=INK, width=6)
        label(d, (470, 330), '33', 80, INK, FA)
        label(d, (470, 600), '4x the runner-up', 50, PINK, FA)
    else:
        title(d, '100x', 110, PINK, stroke=0)
        bars(d, [('#33', 1.0, PINK, '100x'), ('#19', 0.01, CYAN, '')], x0=300, y0=280, w=540, h=80, gap=150,
             k=ease_out(min(1, lt / 0.8)), lw=50)
        for k in range(4):
            mosquito(d, 300 + 520 * ((lt * 0.3 + k / 4) % 1), 240 - 0 * k, 0.4, lt + k)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, "YOU'RE DELICIOUS", 86)
    head(d, 300, 410, 0.9, 'smile')
    bite(d, 220, 470, 18); bite(d, 380, 360, 16)
    mosquito(d, 700, 360 + 15 * math.sin(lt * 4), 1.1, lt)
    label(d, (700, 560), 'YUM!', 70, PINK, FA, stroke=3)
    return im

VISUALS = {'magnet': v_magnet, 'teaser': v_teaser, 'females': v_females, 'males': v_females, 'co2': v_co2,
           'radar': v_co2, 'heat': v_heat, 'smell': v_smell, 'stockings': v_stockings, 'tournament': v_tournament,
           'acids': v_acids, 'years': v_years, 'twins': v_twins, 'myths': v_myths, 'winner': v_winner,
           'winner2': v_winner, 'outro': v_outro}
