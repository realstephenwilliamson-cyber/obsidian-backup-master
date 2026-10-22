# Read raised note numbers from the page image: cut the marks that sit wholly above the line, and classify each
# against digit shapes learnt from calls whose digits the text layer read correctly.
import statistics as st, re
GW, GH = 10, 14

def components(img, x0, x1, ya, yb):
    """connected dark components (8-neighbour) in the pixel box; each as (minx,miny,maxx,maxy,set of (x,y))"""
    Z = 300 / 72
    X0, X1, Y0, Y1 = max(0, int(x0 * Z)), min(img.W, int(x1 * Z)), max(0, int(ya)), min(img.H, int(yb))
    dark = set()
    for y in range(Y0, Y1):
        row = y * img.W
        for x in range(X0, X1):
            if img.b[row + x] < 120: dark.add((x, y))
    comps = []; seen = set()
    for p in sorted(dark):
        if p in seen: continue
        stack = [p]; seen.add(p); pts = []
        while stack:
            x, y = stack.pop(); pts.append((x, y))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    q = (x + dx, y + dy)
                    if q in dark and q not in seen: seen.add(q); stack.append(q)
        xs = [a for a, b in pts]; ys = [b for a, b in pts]
        comps.append((min(xs), min(ys), max(xs), max(ys), pts))
    return comps, (X0, Y0, X1, Y1)

def raised_marks(img, w, nlet, ncall, ntrail, prevw=None):
    """the raised marks in a word's call part, left to right, as normalised grids; None if the geometry fails"""
    Z = 300 / 72
    n = nlet + ncall + ntrail; cw = (w['x1'] - w['x']) / max(n, 1)
    ya, yb = w['y0'] - 2, w['y1'] + 2
    if nlet:
        xs = w['x'] + cw * nlet; xe = w['x'] + cw * (nlet + ncall)
        let = img.region(max(w['x'], xs - cw * 4), xs - cw * 0.4, ya, yb)
        x0, x1 = xs - cw * 0.8, min(xe + cw * 0.6, w['x1'] + 2)
    else:
        if not prevw: return None
        pcw = (prevw['x1'] - prevw['x']) / max(len(prevw['t']), 1)
        let = img.region(prevw['x1'] - pcw * 4, prevw['x1'] - pcw * 0.5, ya, yb)
        x0, x1 = w['x'] - 1, w['x'] + cw * ncall + 1
    if len(let) < 3: return None
    base = st.median([b for t, b in let]); top = st.median([t for t, b in let]); h = max(base - top, 1)
    cut = base - 0.3 * h                     # raised marks end above this line
    comps, box = components(img, x0, x1, ya * Z, cut)
    out = []
    for (a, b, c, d, pts) in comps:
        if d >= box[3] - 1: continue         # touches the cut: part of a letter
        if len(pts) < 6: continue            # specks
        out.append((a, b, c, d, pts))
    out = [o for o in out if (o[3] - o[1]) >= 0.3 * h]     # accents (macron, acute) are flatter than digits
    out.sort()
    # merge pieces that overlap horizontally (a broken digit)
    merged = []
    for comp in out:
        if merged and comp[0] <= merged[-1][2] - 1:
            m = merged[-1]; merged[-1] = (min(m[0], comp[0]), min(m[1], comp[1]), max(m[2], comp[2]), max(m[3], comp[3]), m[4] + comp[4])
        else: merged.append(comp)
    return [grid(m) for m in merged], [(m[0], m[1], m[2], m[3]) for m in merged], h

def marks_after(img, w, nextw):
    """raised digit-sized marks just after a word's last letter (for calls neither OCR read): grids or None"""
    Z = 300 / 72
    t = w['t']; cw = (w['x1'] - w['x']) / max(len(t), 1)
    ya, yb = w['y0'] - 2, w['y1'] + 2
    m = re.search(r'[^\W\d_](?=[^\w]*$)', t)
    if not m: return None
    xl = w['x'] + cw * (m.end())                                   # after the last letter
    let = img.region(max(w['x'], xl - cw * 4), xl - cw * 0.4, ya, yb)
    if len(let) < 3: return None
    base = st.median([b for tt, b in let]); top = st.median([tt for tt, b in let]); h = max(base - top, 1)
    x1 = min(w['x1'] + cw * 2.5, nextw['x'] - 0.5) if nextw and nextw['x'] > w['x1'] else w['x1'] + cw * 2.5
    comps, box = components(img, xl - cw * 0.3, x1, ya * Z, base - 0.3 * h)
    out = [c for c in comps if c[3] < box[3] - 1 and len(c[4]) >= 6 and (c[3] - c[1]) >= 0.55 * h]
    if not out: return None
    out.sort()
    return [grid(c) for c in out], h

def grid(comp):
    a, b, c, d, pts = comp
    W, H = c - a + 1, d - b + 1
    s = set(pts); g = []
    for gy in range(GH):
        for gx in range(GW):
            x0 = a + gx * W / GW; x1 = a + (gx + 1) * W / GW; y0 = b + gy * H / GH; y1 = b + (gy + 1) * H / GH
            tot = on = 0
            for x in range(int(x0), max(int(x0) + 1, int(x1))):
                for y in range(int(y0), max(int(y0) + 1, int(y1))):
                    tot += 1; on += (x, y) in s
            g.append(on / tot if tot else 0)
    return (g, W / max(H, 1))

def dist(g1, g2):
    return sum(abs(a - b) for a, b in zip(g1[0], g2[0])) / len(g1[0]) + 0.5 * abs(g1[1] - g2[1])

class Reader:
    def __init__(s): s.T = {}             # digit -> list of grids
    def learn(s, grids, digits):
        if len(grids) != len(digits): return False
        for g, d in zip(grids, digits): s.T.setdefault(d, []).append(g)
        return True
    def verify(s, grids, nums):
        """which of the page's note numbers do these marks show? compares every run of consecutive marks of the
        number's length with that number's digits. Returns (number, distance, margin to the next number) or None."""
        if not grids or not s.T: return None
        sc = []
        for n in set(nums):
            ds = str(n)
            if len(ds) > len(grids) or any(d not in s.T for d in ds): continue
            digitlike = [min(dist(g, t) for ts in s.T.values() for t in ts) < 0.25 for g in grids]
            best = 9
            for i in range(len(grids) - len(ds) + 1):
                d_ = sum(min(dist(grids[i + k], t) for t in s.T[d]) for k, d in enumerate(ds)) / len(ds)
                # marks left over beyond the number's digits must not themselves look like digits
                d_ += 0.2 * sum(digitlike[k] for k in range(len(grids)) if not i <= k < i + len(ds))
                best = min(best, d_)
            sc.append((best, n))
        if not sc: return None
        sc.sort()
        margin = sc[1][0] - sc[0][0] if len(sc) > 1 else 9
        return sc[0][1], sc[0][0], margin
    def read(s, grids):
        """digits string and the worst margin (distance to the second-best digit minus best)"""
        out = ''; margin = 9; worst = 0
        for g in grids:
            sc = sorted((min(dist(g, t) for t in ts), d) for d, ts in s.T.items() if ts)
            if not sc: return None, 0, 9
            out += sc[0][1]; worst = max(worst, sc[0][0])
            if len(sc) > 1: margin = min(margin, sc[1][0] - sc[0][0])
        return out, margin, worst
