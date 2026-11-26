"""DR. LUMEN - the explainer host. A friendly 3D light bulb with round glasses, bow tie and white gloves.
SDF ray-marched with numpy only (same technique as the old chars3d.py). Poses are cached as PNGs in cache/.
    python lumen3d.py            -> renders every pose
"""
import numpy as np, math, os, sys
from PIL import Image

CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache')
os.makedirs(CACHE, exist_ok=True)

def v(*a): return np.array(a, dtype=np.float32)
def length(p): return np.sqrt((p * p).sum(-1))
def sph(p, c, r): return length(p - c) - r
def ell(p, c, r):
    r = np.asarray(r, np.float32); q = (p - c) / r
    k0 = length(q); k1 = length(q / r)
    return k0 * (k0 - 1) / np.maximum(k1, 1e-6)
def cap(p, a, b, r):
    a = np.asarray(a, np.float32); b = np.asarray(b, np.float32)
    pa = p - a; ba = b - a
    h = np.clip((pa * ba).sum(-1) / (ba * ba).sum(), 0, 1)[..., None]
    return length(pa - ba * h) - r
def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)
def torus_z(p, c, R, r):          # ring facing the camera
    q = p - c
    return np.sqrt((np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2) - R) ** 2 + q[..., 2] ** 2) - r
def torus_y(p, c, R, r):          # horizontal ring
    q = p - c
    return np.sqrt((np.sqrt(q[..., 0] ** 2 + q[..., 2] ** 2) - R) ** 2 + q[..., 1] ** 2) - r
def cyl_y(p, c, r, h):
    q = p - c
    return np.maximum(np.sqrt(q[..., 0] ** 2 + q[..., 2] ** 2) - r, np.abs(q[..., 1]) - h)

ARMS = {
    'down':  [((0.60, -0.05, 0.25), (0.86, -0.42, 0.30), (0.92, -0.70, 0.32)), ((-0.60, -0.05, 0.25), (-0.86, -0.42, 0.30), (-0.92, -0.70, 0.32))],
    'point': [((0.60, 0.00, 0.25), (1.02, 0.18, 0.38), (1.14, 0.62, 0.40)), ((-0.60, -0.05, 0.25), (-0.86, -0.42, 0.30), (-0.92, -0.70, 0.32))],
    'up':    [((0.60, 0.05, 0.25), (1.00, 0.40, 0.32), (1.12, 0.86, 0.34)), ((-0.60, 0.05, 0.25), (-1.00, 0.40, 0.32), (-1.12, 0.86, 0.34))],
    'shrug': [((0.60, -0.05, 0.25), (1.02, -0.22, 0.34), (1.18, 0.10, 0.40)), ((-0.60, -0.05, 0.25), (-1.02, -0.22, 0.34), (-1.18, 0.10, 0.40))],
}

def lumen(p, arms='down', mouth='smile', blink=False, brows='normal'):
    P = []
    # glass bulb + neck, melted together
    body = smin(sph(p, v(0, 0.35, 0), 0.85), cap(p, (0, -0.15, 0), (0, -0.62, 0), 0.40), 0.3)
    P.append((body, 'bulb'))
    # screw base
    P.append((cyl_y(p, v(0, -0.9, 0), 0.36, 0.24), 'chrome'))
    for y in (-0.72, -0.84, -0.96, -1.08):
        P.append((torus_y(p, v(0, y, 0), 0.37, 0.055), 'chrome'))
    P.append((ell(p, v(0, -1.17, 0), (0.22, 0.1, 0.22)), 'black'))
    # bow tie on the collar
    P.append((ell(p, v(0.18, -0.6, 0.43), (0.17, 0.11, 0.07)), 'red'))
    P.append((ell(p, v(-0.18, -0.6, 0.43), (0.17, 0.11, 0.07)), 'red'))
    P.append((sph(p, v(0, -0.6, 0.47), 0.065), 'red'))
    # eyes
    for s in (1, -1):
        if blink:
            P.append((cap(p, (s * 0.38, 0.5, 0.78), (s * 0.18, 0.5, 0.8), 0.028), 'black'))
        else:
            P.append((ell(p, v(s * 0.28, 0.5, 0.74), (0.15, 0.17, 0.1)), 'white'))
            P.append((sph(p, v(s * 0.255, 0.47, 0.83), 0.075), 'black'))
            P.append((sph(p, v(s * 0.235, 0.51, 0.895), 0.022), 'white'))
        # round glasses
        P.append((torus_z(p, v(s * 0.28, 0.5, 0.86), 0.205, 0.032), 'frame'))
        # brows
        if brows == 'up':
            P.append((cap(p, (s * 0.16, 0.86, 0.8), (s * 0.38, 0.9, 0.74), 0.03), 'brow'))
        elif brows == 'think':
            yy = 0.84 if s > 0 else 0.92
            P.append((cap(p, (s * 0.16, yy, 0.8), (s * 0.38, yy + 0.02, 0.74), 0.03), 'brow'))
        else:
            P.append((cap(p, (s * 0.16, 0.8, 0.82), (s * 0.38, 0.82, 0.76), 0.03), 'brow'))
        P.append((ell(p, v(s * 0.5, 0.2, 0.6), (0.11, 0.07, 0.05)), 'blush'))
    P.append((cap(p, (-0.08, 0.53, 0.88), (0.08, 0.53, 0.88), 0.03), 'frame'))
    # mouth
    if mouth == 'smile':
        P.append((cap(p, (-0.15, 0.1, 0.78), (0, 0.04, 0.8), 0.03), 'black'))
        P.append((cap(p, (0, 0.04, 0.8), (0.15, 0.1, 0.78), 0.03), 'black'))
    elif mouth == 'mid':
        P.append((ell(p, v(0, 0.06, 0.77), (0.13, 0.075, 0.07)), 'mouth'))
    else:  # wide
        P.append((ell(p, v(0, 0.05, 0.76), (0.16, 0.135, 0.08)), 'mouth'))
        P.append((ell(p, v(0, -0.02, 0.8), (0.09, 0.05, 0.04)), 'tongue'))
    # arms + gloves
    for (a, b, c) in ARMS[arms]:
        P.append((cap(p, a, b, 0.045), 'black'))
        P.append((cap(p, b, c, 0.045), 'black'))
        P.append((sph(p, v(*c), 0.13), 'glove'))
    if arms in ('point',):
        c = ARMS[arms][0][2]
        P.append((cap(p, (c[0] - 0.02, c[1] + 0.05, c[2] + 0.04), (c[0] - 0.05, c[1] + 0.26, c[2] + 0.06), 0.045), 'glove'))
    return P
EXT = (-1.35, 1.35, -1.32, 1.3)

COL = {'bulb': (1.0, 0.84, 0.38), 'chrome': (0.78, 0.8, 0.86), 'black': (0.06, 0.06, 0.09), 'red': (0.9, 0.12, 0.22),
       'white': (0.98, 0.98, 0.98), 'frame': (0.12, 0.1, 0.12), 'brow': (0.3, 0.2, 0.12), 'blush': (1.0, 0.55, 0.45),
       'mouth': (0.38, 0.06, 0.1), 'tongue': (0.98, 0.42, 0.5), 'glove': (0.99, 0.99, 0.99)}
SPEC = {'bulb': (0.9, 70), 'chrome': (0.9, 50), 'black': (0.6, 60), 'frame': (0.7, 60), 'red': (0.5, 30), 'white': (0.4, 40),
        'glove': (0.3, 20)}

def scene(p, kw):
    P = lumen(p, **kw)
    return np.stack([d for d, _ in P], -1), [m for _, m in P]

def render(kw, out_h=900, ss=1.5, camz=9.5):
    x0, x1, y0, y1 = EXT
    cy, cx = (y0 + y1) / 2, (x0 + x1) / 2
    fov = (y1 - y0) / 2 / camz; aspect = (x1 - x0) / (y1 - y0)
    h = int(out_h / 0.92); w = int(h * aspect)
    W_, H_ = int(w * ss), int(h * ss)
    ys, xs = np.mgrid[0:H_, 0:W_].astype(np.float32)
    u = (xs + 0.5) / W_ * 2 - 1; vv = -((ys + 0.5) / H_ * 2 - 1)
    ro = np.broadcast_to(v(cx, cy, camz), (H_, W_, 3)).reshape(-1, 3).copy()
    rd = np.stack([u * aspect * fov, vv * fov, -np.ones_like(u)], -1).reshape(-1, 3)
    rd /= length(rd)[:, None]
    n = ro.shape[0]
    t = np.full(n, camz - 3.0, np.float32); hit = np.zeros(n, bool); alive = np.ones(n, bool)
    for _ in range(110):
        idx = np.nonzero(alive)[0]
        if len(idx) == 0: break
        pp = ro[idx] + rd[idx] * t[idx, None]
        d = scene(pp, kw)[0].min(-1)
        t[idx] += d * 0.9
        h_ = d < 0.002
        hit[idx[h_]] = True
        alive[idx[h_ | (t[idx] > camz + 4)]] = False
    out = np.zeros((n, 4), np.float32)
    idx = np.nonzero(hit)[0]
    pp = ro[idx] + rd[idx] * t[idx, None]
    ds, mats = scene(pp, kw)
    mid = ds.argmin(-1)
    e = 0.003; nrm = np.zeros_like(pp)
    for k in range(3):
        dp = np.zeros(3, np.float32); dp[k] = e
        nrm[:, k] = scene(pp + dp, kw)[0].min(-1) - scene(pp - dp, kw)[0].min(-1)
    nrm /= length(nrm)[:, None] + 1e-9
    ao = np.ones(len(idx), np.float32)
    for i in range(1, 6):
        hh = 0.07 * i
        ao -= (hh - scene(pp + nrm * hh, kw)[0].min(-1)) * (0.8 / i)
    ao = np.clip(ao, 0.3, 1)
    L = v(-0.5, 0.75, 0.6); L /= np.linalg.norm(L)
    sh = np.ones(len(idx), np.float32); ts = np.full(len(idx), 0.03, np.float32)
    for _ in range(24):
        dd = scene(pp + nrm * 0.004 + L * ts[:, None], kw)[0].min(-1)
        sh = np.minimum(sh, 8 * np.maximum(dd, 0) / ts)
        ts += np.clip(dd, 0.02, 0.25)
    sh = np.clip(sh, 0.0, 1) * 0.65 + 0.35
    L2 = v(0.8, 0.1, -0.5); L2 /= np.linalg.norm(L2)
    V = -rd[idx]
    base = np.array([COL[m] for m in mats], np.float32)[mid]
    names = np.array(mats)[mid]
    sp = np.array([SPEC.get(m, (0.2, 15)) for m in mats], np.float32)[mid]
    diff = np.clip((nrm * L).sum(-1), 0, 1) * sh
    Hh = L + V; Hh /= length(Hh)[:, None]
    spec = sp[:, 0] * np.clip((nrm * Hh).sum(-1), 0, 1) ** sp[:, 1] * sh
    facing = np.clip((nrm * V).sum(-1), 0, 1)
    rim = np.clip(1 - facing, 0, 1) ** 3 * 0.4
    back = np.clip((nrm * L2).sum(-1), 0, 1) * 0.35
    sky = 0.5 + 0.5 * nrm[:, 1]
    col = base * (0.45 * sky[:, None] + 0.85 * diff[:, None] + back[:, None] * v(1.0, 0.7, 0.6)) * ao[:, None] + spec[:, None] + rim[:, None] * v(1, 0.9, 0.85)
    # the bulb glows from inside: emissive core, hotter in the middle
    gb = names == 'bulb'
    if gb.any():
        glow = (0.55 + 0.55 * facing[gb] ** 1.5)[:, None] * v(1.0, 0.9, 0.6)
        col[gb] = base[gb] * (0.35 + 0.45 * diff[gb, None]) + glow * 0.75 + spec[gb, None] + rim[gb, None] * v(1, 0.95, 0.7)
    col = col / (1 + col * 0.22)
    col = np.clip(col, 0, 1) ** (1 / 1.08)
    out[idx, :3] = col; out[idx, 3] = 1
    img = Image.fromarray((out.reshape(H_, W_, 4) * 255).astype(np.uint8), 'RGBA')
    img = img.resize((w, h), Image.LANCZOS)
    return img

POSES = {}
for arms in ('down', 'point', 'shrug'):
    for m in ('smile', 'mid', 'wide'):
        POSES[f'lumen_{arms}_{m}'] = dict(arms=arms, mouth=m, brows='up' if arms == 'point' else ('think' if arms == 'shrug' else 'normal'))
    POSES[f'lumen_{arms}_blink'] = dict(arms=arms, mouth='smile', blink=True, brows='normal')
for m in ('smile', 'mid', 'wide'):
    POSES[f'lumen_up_{m}'] = dict(arms='up', mouth=m, brows='up')

def make(name):
    path = os.path.join(CACHE, name + '.png')
    if not os.path.exists(path):
        render(POSES[name]).save(path)
    return path

def get(name):
    return Image.open(make(name)).convert('RGBA')

if __name__ == '__main__':
    import time
    from multiprocessing import Pool
    names = sys.argv[1:] or list(POSES)
    t0 = time.time()
    with Pool(2) as pool:
        for r in pool.imap_unordered(make, names): print(os.path.basename(r), round(time.time() - t0, 1), flush=True)
