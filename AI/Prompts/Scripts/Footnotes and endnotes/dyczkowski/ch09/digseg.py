# digseg.py (2 Nov 2026): helpers for reading superscript footnote numbers by template matching.
import numpy as np
from PIL import Image
THR = 200
def segments(im, box):
    """im: L image (300 dpi page); box: [L,T,W,H] of the superscript token. Returns list of binary digit arrays (20x12)."""
    L, T, W, H = box
    a = np.array(im.crop((L - 3, T - 3, L + W + 3, T + H + 3))) < THR
    # keep only rows of the superscript band (drop anything far below the top: the next line's letters)
    cols = a.any(axis=0)
    runs, cur = [], None
    for x, c in enumerate(cols):
        if c and cur is None: cur = x
        if not c and cur is not None: runs.append((cur, x)); cur = None
    if cur is not None: runs.append((cur, len(cols)))
    runs = [r for r in runs if a[:, r[0]:r[1]].sum() >= 8]
    out = []
    for x0, x1 in runs:
        w = x1 - x0
        n = 1 if w <= 17 else (2 if w <= 31 else 3)
        for j in range(n):
            s0 = x0 + w * j // n; s1 = x0 + w * (j + 1) // n
            seg = a[:, s0:s1]; ys = np.where(seg.any(axis=1))[0]
            if not len(ys): continue
            seg = seg[ys[0]:ys[-1] + 1]
            out.append((s0, seg))
    return out
def norm(seg, h=20, w=12):
    im = Image.fromarray((seg * 255).astype('uint8')).resize((w, h), Image.BILINEAR)
    v = np.array(im, dtype=float).ravel(); v -= v.mean(); n = np.linalg.norm(v)
    return v / n if n else v
