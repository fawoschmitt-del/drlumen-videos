# Shared flat illustration helpers for episodes (card space 940 x 680). Import: from shapes import *
import math
from explainer import INK, YEL, PINK, CYAN, GRN, FA, FI, FB, CW, CH, label, arrow, ease_out, ease_back

SKIN = (255, 205, 170); SKIN_D = (215, 145, 115); RED = (220, 60, 80); WHITE = (255, 255, 255)
GREY = (170, 170, 185); DGREY = (90, 95, 120); ORANGE = (255, 150, 60); BROWN = (150, 100, 70); BLUE = (60, 120, 230)

def head(d, cx, cy, s=1.0, mouth='smile', lt=0.0, eyes='open', col=SKIN):
    """simple round cartoon head. mouth: smile / yawn / o / flat / sad"""
    r = 150 * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=INK, width=int(8 * s))
    for ex in (-55, 55):
        if eyes == 'closed':
            d.arc([cx + ex * s - 26 * s, cy - 50 * s, cx + ex * s + 26 * s, cy - 10 * s], 200, 340, fill=INK, width=int(8 * s))
        else:
            d.ellipse([cx + ex * s - 16 * s, cy - 46 * s, cx + ex * s + 16 * s, cy - 14 * s], fill=INK)
    if mouth == 'smile':
        d.arc([cx - 60 * s, cy + 10 * s, cx + 60 * s, cy + 80 * s], 20, 160, fill=INK, width=int(8 * s))
    elif mouth == 'yawn':
        k = 0.6 + 0.4 * abs(math.sin(lt * 1.6))
        d.ellipse([cx - 48 * s, cy + 20 * s, cx + 48 * s, cy + (40 + 80 * k) * s], fill=(120, 30, 50), outline=INK, width=int(7 * s))
    elif mouth == 'o':
        d.ellipse([cx - 26 * s, cy + 30 * s, cx + 26 * s, cy + 82 * s], fill=(120, 30, 50), outline=INK, width=int(6 * s))
    elif mouth == 'sad':
        d.arc([cx - 50 * s, cy + 50 * s, cx + 50 * s, cy + 100 * s], 200, 340, fill=INK, width=int(8 * s))
    else:
        d.line([(cx - 45 * s, cy + 60 * s), (cx + 45 * s, cy + 60 * s)], fill=INK, width=int(8 * s))

def dog(d, cx, cy, s=1.0, lt=0.0, yawn=False):
    br = (200, 150, 90); dk = (130, 90, 50)
    for ex in (-1, 1):   # floppy ears
        d.ellipse([cx + ex * 150 * s - 55 * s, cy - 120 * s, cx + ex * 150 * s + 55 * s, cy + 60 * s], fill=dk, outline=INK, width=int(7 * s))
    d.ellipse([cx - 150 * s, cy - 150 * s, cx + 150 * s, cy + 130 * s], fill=br, outline=INK, width=int(8 * s))
    d.ellipse([cx - 85 * s, cy - 5 * s, cx + 85 * s, cy + 125 * s], fill=(240, 215, 180), outline=INK, width=int(7 * s))
    for ex in (-55, 55):
        d.ellipse([cx + ex * s - 16 * s, cy - 60 * s, cx + ex * s + 16 * s, cy - 28 * s], fill=INK)
    d.ellipse([cx - 28 * s, cy + 5 * s, cx + 28 * s, cy + 40 * s], fill=INK)
    if yawn:
        k = 0.6 + 0.4 * abs(math.sin(lt * 1.6))
        d.ellipse([cx - 40 * s, cy + 50 * s, cx + 40 * s, cy + (60 + 60 * k) * s], fill=(120, 30, 50), outline=INK, width=int(6 * s))
    else:
        d.arc([cx - 40 * s, cy + 35 * s, cx + 40 * s, cy + 85 * s], 20, 160, fill=INK, width=int(7 * s))

def cat(d, cx, cy, s=1.0, col=ORANGE, lt=0.0, puffed=False):
    """cat face"""
    for ex in (-1, 1):
        d.polygon([(cx + ex * 140 * s, cy - 40 * s), (cx + ex * 120 * s, cy - 190 * s), (cx + ex * 30 * s, cy - 110 * s)], fill=col, outline=INK)
        d.line([(cx + ex * 140 * s, cy - 40 * s), (cx + ex * 120 * s, cy - 190 * s), (cx + ex * 30 * s, cy - 110 * s)], fill=INK, width=int(7 * s))
    r = 150 * s * (1.15 if puffed else 1.0)
    if puffed:
        pts = []
        for k in range(48):
            a = k / 48 * 2 * math.pi
            rr = r * (1.0 if k % 2 else 0.9)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=col, outline=INK)
        d.line(pts + [pts[0]], fill=INK, width=int(7 * s))
    else:
        d.ellipse([cx - r, cy - r * 0.9, cx + r, cy + r * 0.9], fill=col, outline=INK, width=int(8 * s))
    for ex in (-55, 55):
        d.ellipse([cx + ex * s - 20 * s, cy - 45 * s, cx + ex * s + 20 * s, cy - 5 * s], fill=(120, 220, 120), outline=INK, width=int(5 * s))
        d.ellipse([cx + ex * s - 6 * s, cy - 40 * s, cx + ex * s + 6 * s, cy - 10 * s], fill=INK)
    d.polygon([(cx - 16 * s, cy + 20 * s), (cx + 16 * s, cy + 20 * s), (cx, cy + 38 * s)], fill=PINK)
    for ex in (-1, 1):
        for k in (-1, 0, 1):
            d.line([(cx + ex * 40 * s, cy + 40 * s + k * 10 * s), (cx + ex * 150 * s, cy + 30 * s + k * 28 * s)], fill=INK, width=int(4 * s))

def thermo(d, cx, cy, h, frac, col=RED):
    d.rounded_rectangle([cx - 26, cy - h / 2, cx + 26, cy + h / 2], 26, fill=WHITE, outline=INK, width=7)
    d.ellipse([cx - 50, cy + h / 2 - 40, cx + 50, cy + h / 2 + 60], fill=col, outline=INK, width=7)
    top = cy + h / 2 - (h - 30) * frac
    d.rectangle([cx - 13, top, cx + 13, cy + h / 2], fill=col)

def bars(d, items, x0=330, y0=200, w=480, h=60, gap=120, k=1.0, lw=46):
    """items: [(label, frac 0..1, colour, value text)]"""
    for i, (lab, frac, col, val) in enumerate(items):
        y = y0 + i * gap
        label(d, (x0 - 30, y), lab, lw, INK, FB, anchor='rm')
        d.rounded_rectangle([x0, y - h / 2, x0 + w, y + h / 2], int(h / 2), fill=(225, 220, 212), outline=INK, width=6)
        ww = max(h, w * frac * k)
        d.rounded_rectangle([x0, y - h / 2, x0 + ww, y + h / 2], int(h / 2), fill=col, outline=INK, width=6)
        if k > 0.7: label(d, (x0 + ww - 20, y), val, 40, INK, FA, anchor='rm')

def cross(d, cx, cy, r=120, w=18, col=RED):
    d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=col, width=w); d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=col, width=w)

def check(d, cx, cy, r=90, w=20, col=GRN):
    d.line([(cx - r, cy), (cx - r * 0.3, cy + r * 0.7), (cx + r, cy - r * 0.8)], fill=col, width=w, joint='curve')

def badge(d, cx, cy, text, size=70, col=YEL, lt=0.0, wob=True, padx=50, h=110):
    from explainer import font
    f = font(FA, size)
    tw = d.textlength(text, font=f)
    dy = 6 * math.sin(lt * 5) if wob else 0
    d.rounded_rectangle([cx - tw / 2 - padx, cy - h / 2 + dy, cx + tw / 2 + padx, cy + h / 2 + dy], 40, fill=col, outline=INK, width=7)
    label(d, (cx, cy + dy), text, size, INK, FA)

def title(d, text, size=92, col=INK, y=80, stroke=0):
    label(d, (CW / 2 - 5, y), text, size, col, FA, stroke=stroke, sfill=INK)

def sub(d, text, y=625, size=46, col=INK):
    label(d, (CW / 2 - 5, y), text, size, col, FB)

def popk(lt, dur=0.45):
    return ease_back(min(1.0, lt / dur))
