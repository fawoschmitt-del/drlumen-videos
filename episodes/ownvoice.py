# Episode: Why does your own voice sound weird on recordings?   (fast format, see tickle.py)
import math
import explainer as X
from shapes import *

TITLE = "Why does your voice sound weird on recordings?"
SLUG = 'ownvoice'
CAPTION = ("Hate your voice on recordings? That's how everyone hears you 😬 But there's a twist. "
           "#science #didyouknow #learnontiktok #voice #brain #facts")
SOURCES = [
    'https://www.scientificamerican.com/article/why-does-my-voice-sound-different/',
    'https://www.popsci.com/scitech/article/2009-06/why-your-voice-sounds-different-recordings/',
    'https://www.livescience.com/55527-why-people-hate-the-sound-of-their-voice.html',
    'https://en.wikipedia.org/wiki/Voice_confrontation',
    'https://sciencedaily.com/releases/2013/09/130912112733.htm',
]
BEATS = [
    ('BIG:RECORD|YOURSELF.|PLAY IT|BACK.', 'point', "Record yourself. Play it back."),
    ('cringe',   'shrug', "Cringe? Bad news: that's the voice everyone else hears, every single *day*."),
    ('likeq',    'point', "But scientists found a twist. Deep down, you might *like* that voice. Stay till the end."),
    ('intro',    'up',    "I'm Doctor Lumen. Let's crack this."),
    ('two',      'point', "When you talk, the sound reaches your inner ear *two* ways."),
    ('air',      'down',  "One: through the air and into your ears. That's how *other* people hear you."),
    ('bone',     'point', "Two: straight through the *bones* of your skull."),
    ('low',      'shrug', "Your skull is great at carrying the *low* notes. So to you, your voice sounds deeper and richer."),
    ('rec',      'down',  "A microphone only catches the *air* part. No bones, no bass."),
    ('plug',     'point', "Try it: plug your ears and talk. Your voice gets *deeper*, right?"),
    ('stranger', 'shrug', "You've heard the bassy version your whole life. So the real one sounds like a *stranger*."),
    ('nerves',   'down',  "Back in nineteen sixty-six, researchers found recordings also reveal things you don't notice, like *nerves*."),
    ('bilingual','point', "And bilingual people cringed *more* at recordings in their first language than in their second."),
    ('twist',    'up',    "Now, the twist. In twenty thirteen, eighty people rated recordings of voices counting to *ten*."),
    ('twist2',   'point', "Hidden in the mix was their own voice. Most didn't *recognize* it."),
    ('twist3',   'down',  "And they rated their own voice as more *attractive* than other people did!"),
    ('outro',    'shrug', "So the voice you hate? Your brain secretly likes it. It just doesn't *recognize* it."),
    ('follow',   'up',    "Follow for a new everyday mystery, every single day!"),
]

def phone(d, cx, cy, s=1.0, lt=0.0, rec=True):
    d.rounded_rectangle([cx - 90 * s, cy - 160 * s, cx + 90 * s, cy + 160 * s], int(30 * s), fill=INK)
    d.rounded_rectangle([cx - 78 * s, cy - 140 * s, cx + 78 * s, cy + 140 * s], int(20 * s), fill=(40, 45, 70))
    for i in range(9):
        h = (20 + 50 * abs(math.sin(lt * 6 + i * 0.9))) * s
        x = cx - 60 * s + i * 15 * s
        d.line([(x, cy - h / 2), (x, cy + h / 2)], fill=CYAN, width=int(8 * s))
    if rec and (lt * 2) % 1 < 0.6:
        d.ellipse([cx - 22 * s, cy + 80 * s, cx + 22 * s, cy + 124 * s], fill=RED)

def skull_head(d, cx, cy, s=1.0, lt=0.0, air=False, bone=False):
    head(d, cx, cy, s, mouth='o', lt=lt)
    # ear
    d.ellipse([cx + 135 * s, cy - 35 * s, cx + 185 * s, cy + 35 * s], fill=SKIN, outline=INK, width=int(6 * s))
    inner = (cx + 95 * s, cy)
    if bone:
        for k in range(3):
            ph = (lt * 1.2 + k / 3) % 1
            x = cx - 10 * s + (inner[0] - cx + 10 * s) * ph
            y = cy + 55 * s + (inner[1] - cy - 55 * s) * ph
            d.ellipse([x - 12 * s, y - 12 * s, x + 12 * s, y + 12 * s], fill=YEL, outline=INK, width=4)
        d.ellipse([inner[0] - 18 * s, inner[1] - 18 * s, inner[0] + 18 * s, inner[1] + 18 * s], fill=PINK, outline=INK, width=5)
    if air:
        for k in range(3):
            ph = (lt * 1.0 + k / 3) % 1
            a0 = math.pi * 0.25 + math.pi * 1.2 * ph
            x = cx + 30 * s + 230 * s * math.cos(-a0 + math.pi * 0.7)
            y = cy + 60 * s + 140 * s * math.sin(-a0 + math.pi * 0.7)
            d.ellipse([x - 12 * s, y - 12 * s, x + 12 * s, y + 12 * s], fill=CYAN, outline=INK, width=4)

def wave(d, x0, y, w, amp, freq, lt, col, width=8):
    pts = [(x0 + i * w / 60, y + amp * math.sin(i / 60 * freq * 2 * math.pi + lt * 6)) for i in range(61)]
    d.line(pts, fill=col, width=width, joint='curve')

def v_cringe(lt, b):
    im, d = X.new_card()
    title(d, 'THAT\'S YOU!')
    phone(d, 280, 380, 1.0, lt)
    head(d, 650, 380, 0.9, mouth='sad', eyes='closed')
    return im

def v_likeq(lt, b):
    im, d = X.new_card()
    title(d, 'SECRET FAN?')
    phone(d, 300, 380, 1.0, lt, rec=False)
    s = 1 + 0.1 * math.sin(lt * 6); hx, hy = 680, 360
    d.polygon([(hx, hy + 110 * s), (hx - 110 * s, hy), (hx - 65 * s, hy - 70 * s), (hx, hy - 25 * s), (hx + 65 * s, hy - 70 * s), (hx + 110 * s, hy)], fill=PINK, outline=INK)
    label(d, (680, 360), '?', 110, WHITE, FA, stroke=4)
    return im

def v_path(lt, b):
    im, d = X.new_card()
    v = b['vis']
    title(d, {'two': 'TWO ROADS', 'air': '1: THROUGH AIR', 'bone': '2: THROUGH BONE'}[v])
    skull_head(d, 420, 380, 1.05, lt, air=v in ('two', 'air'), bone=v in ('two', 'bone'))
    if v == 'two':
        label(d, (790, 260), 'air', 56, CYAN, FA, stroke=2)
        label(d, (790, 500), 'bone', 56, YEL, FA, stroke=2)
    return im

def v_low(lt, b):
    im, d = X.new_card()
    title(d, 'BONES LOVE BASS')
    label(d, (190, 280), 'low', 56, INK, FA)
    wave(d, 280, 280, 560, 70, 2.5, lt, PINK, 12)
    label(d, (190, 480), 'high', 56, INK, FA)
    wave(d, 280, 480, 560, 25, 9, lt, (200, 200, 210), 6)
    return im

def v_rec(lt, b):
    im, d = X.new_card()
    title(d, 'MIC: AIR ONLY')
    # microphone
    d.rounded_rectangle([170, 200, 310, 400], 70, fill=DGREY, outline=INK, width=8)
    for k in range(4): d.line([(185, 240 + k * 40), (295, 240 + k * 40)], fill=INK, width=4)
    d.arc([140, 300, 340, 480], 0, 180, fill=INK, width=10)
    d.line([(240, 480), (240, 560)], fill=INK, width=10); d.line([(180, 560), (300, 560)], fill=INK, width=10)
    label(d, (640, 300), 'air: yes', 60, GRN, FA)
    label(d, (640, 420), 'bone: no', 60, RED, FA)
    return im

def v_plug(lt, b):
    im, d = X.new_card()
    title(d, 'PLUG YOUR EARS')
    head(d, 470, 390, 1.1, mouth='o', lt=lt)
    for sx in (-1, 1):
        x = 470 + sx * 175
        d.rounded_rectangle([x - 30, 330, x + 30, 470], 28, fill=SKIN, outline=INK, width=6)
    wave(d, 330, 600, 280, 30, 2.5, lt, PINK, 10)
    return im

def v_stranger(lt, b):
    im, d = X.new_card()
    title(d, 'WHO IS THAT?')
    head(d, 270, 380, 0.85, mouth='o')
    d.ellipse([530, 230, 790, 490], fill=(60, 55, 80), outline=INK, width=8)
    label(d, (660, 360), '?', 170, YEL, FA, stroke=6)
    wave(d, 380, 560, 180, 15, 8, lt, CYAN, 6)
    return im

def v_nerves(lt, b):
    im, d = X.new_card()
    title(d, '1966 STUDY')
    phone(d, 270, 380, 0.9, lt)
    for i, (t, c) in enumerate((('nervous?', PINK), ('tense?', ORANGE), ('unsure?', CYAN))):
        if lt > i * 0.4: badge(d, 650, 240 + i * 130, t, 52, c, lt, padx=30, h=90)
    return im

def v_bilingual(lt, b):
    im, d = X.new_card()
    title(d, 'BILINGUAL CRINGE', 88)
    k = ease_out(min(1, lt / 1.2))
    bars(d, [('1st language', 0.9, PINK, 'MORE'), ('2nd language', 0.45, CYAN, 'LESS')], x0=400, y0=280, w=440, h=70, gap=150, k=k, lw=40)
    sub(d, 'discomfort hearing yourself', 600)
    return im

def v_twist(lt, b):
    im, d = X.new_card()
    v = b['vis']
    if v == 'twist':
        title(d, '80 PEOPLE, 2013')
        for i in range(8):
            x = 150 + (i % 4) * 210; y = 270 + (i // 4) * 190
            d.rounded_rectangle([x - 70, y - 60, x + 70, y + 60], 20, fill=WHITE, outline=INK, width=5)
            label(d, (x, y), str((i + int(lt * 3)) % 10 + 1), 70, INK, FA)
    elif v == 'twist2':
        title(d, 'SPOT YOURSELF?')
        for i in range(5):
            x = 140 + i * 165
            mine = i == 3
            d.rounded_rectangle([x - 65, 260, x + 65, 480], 20, fill=YEL if mine and lt > 1.5 else WHITE, outline=INK, width=6)
            wave(d, x - 45, 370, 90, 22, 2 + i, lt, PINK if mine else DGREY, 6)
        sub(d, 'most people: no idea', 600)
    else:
        title(d, 'YOU RATE YOURSELF UP', 80)
        k = ease_out(min(1, lt / 1.2))
        bars(d, [('you rate it', 0.85, PINK, 'HIGHER'), ('others rate it', 0.55, CYAN, 'LOWER')], x0=410, y0=280, w=440, h=70, gap=150, k=k, lw=40)
        sub(d, 'voice attractiveness', 600)
    return im

def v_outro(lt, b):
    im, d = X.new_card()
    title(d, 'SECRETLY A FAN')
    phone(d, 290, 380, 1.0, lt, rec=False)
    head(d, 660, 380, 0.85, mouth='smile')
    return im

VISUALS = {'cringe': v_cringe, 'likeq': v_likeq, 'two': v_path, 'air': v_path, 'bone': v_path, 'low': v_low, 'rec': v_rec,
           'plug': v_plug, 'stranger': v_stranger, 'nerves': v_nerves, 'bilingual': v_bilingual, 'twist': v_twist,
           'twist2': v_twist, 'twist3': v_twist, 'outro': v_outro}
