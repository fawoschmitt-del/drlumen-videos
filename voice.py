"""Voice track: Kokoro (ONNX) TTS per beat + word timings via faster-whisper alignment.
Returns beats with absolute start/end and per-word timings, and writes voice.wav."""
import numpy as np, os, re, json, difflib, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.environ.get('KOKORO_DIR', os.path.join(HERE, 'models'))
VOICE = os.environ.get('LUMEN_VOICE', 'am_michael')
SPEED = float(os.environ.get('LUMEN_SPEED', '1.17'))
SR = 24000
GAP = 0.05          # pause between beats (keep it tight!)
LEAD = 0.0          # no silence at the start: the hook starts on frame 1

def _trim(s, thr=0.01):
    a = np.abs(s); idx = np.nonzero(a > thr)[0]
    if len(idx) == 0: return s
    return s[max(0, idx[0] - 240): idx[-1] + 480]

def _norm(w): return re.sub(r"[^a-z0-9']", '', w.lower().replace('’', "'"))

def _align(words, wtimes, dur):
    """map script words onto whisper words; interpolate whatever doesn't match"""
    a = [_norm(w) for w in words]; b = [_norm(w['word']) for w in wtimes]
    st = [None] * len(words); en = [None] * len(words)
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            st[blk.a + k] = wtimes[blk.b + k]['start']; en[blk.a + k] = wtimes[blk.b + k]['end']
    # fill gaps proportional to word length
    i = 0
    while i < len(words):
        if st[i] is not None: i += 1; continue
        j = i
        while j < len(words) and st[j] is None: j += 1
        t0 = en[i - 1] if i > 0 else 0.0
        t1 = st[j] if j < len(words) else dur
        L = [max(1, len(a[k])) for k in range(i, j)]; tot = sum(L); acc = t0
        for k, l in zip(range(i, j), L):
            st[k] = acc; acc += (t1 - t0) * l / tot; en[k] = acc
        i = j
    for k in range(1, len(words)):          # monotonic
        st[k] = max(st[k], st[k - 1] + 0.02)
    return [(w, float(s), float(max(e, s + 0.08))) for w, s, e in zip(words, st, en)]

def build(beats, outdir, cache_json=None):
    key = repr((VOICE, SPEED, GAP, LEAD, [tuple(b[:3]) for b in beats]))
    if cache_json and os.path.exists(cache_json):
        old = json.load(open(cache_json))
        if old.get('key') == key: return old
    from kokoro_onnx import Kokoro
    from faster_whisper import WhisperModel
    k = Kokoro(os.path.join(MODELS, 'kokoro-v1.0.onnx'), os.path.join(MODELS, 'voices-v1.0.bin'))
    wm = WhisperModel('base.en', device='cpu', compute_type='int8')
    track = [np.zeros(int(SR * LEAD), np.float32)]; t = LEAD; out = []
    for bt in beats:
        vis, pose, text = bt[:3]
        s, sr = k.create(text.replace('*', ''), voice=VOICE, speed=SPEED, lang='en-us')
        s = _trim(s.astype(np.float32), 0.006); dur = len(s) / SR
        a16 = np.interp(np.arange(0, len(s), SR / 16000), np.arange(len(s)), s).astype(np.float32)
        segs, _ = wm.transcribe(a16, word_timestamps=True, language='en', beam_size=1)
        wt = [dict(word=w.word, start=w.start, end=w.end) for sg in segs for w in sg.words]
        words = text.split()
        al = _align(words, wt, dur)
        out.append(dict(vis=vis, pose=pose, text=text, start=t, end=t + dur,
                        words=[(w, t + a, t + b) for w, a, b in al]))
        track.append(s); track.append(np.zeros(int(SR * GAP), np.float32)); t += dur + GAP
    track.append(np.zeros(int(SR * 0.9), np.float32))
    full = np.concatenate(track)
    full = full / (np.abs(full).max() + 1e-9) * 0.95
    sf.write(os.path.join(outdir, 'voice.wav'), full, SR)
    res = dict(beats=out, total=len(full) / SR, key=key)
    if cache_json: json.dump(res, open(cache_json, 'w'), indent=1)
    return res

def envelope(path, fps):
    s, sr = sf.read(path)
    hop = sr // fps
    n = len(s) // hop
    rms = np.sqrt(np.array([np.mean(s[i * hop:(i + 1) * hop] ** 2) for i in range(n)]))
    return rms / (np.percentile(rms[rms > 0.005], 90) + 1e-9) if (rms > 0.005).any() else rms
