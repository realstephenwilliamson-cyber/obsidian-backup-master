# Deshpande: find raised marks after words (candidate endnote calls) from the PDF layer's character boxes and the image.
import sys, os, re, json, statistics as st, pymupdf
sys.path.insert(0, os.path.expanduser('~/fnwork/tor'))
from raised import Img
from callocr import components
PDF = r'C:\Vaults\Obsidian Vault\Library\Trika\G. T. Deshpande - Abhinavagupta-Sahitya Akademi (1995).pdf'
Z = 300 / 72

def words(p):
    """layer words with character boxes, in reading order: list of dict(t, chars=[(c,x0,y0,x1,y1)], line)"""
    out = []
    for bi, b in enumerate(p.get_text('rawdict')['blocks']):
        for li, l in enumerate(b.get('lines', [])):
            cur = []
            for s in l['spans']:
                for c in s['chars']:
                    if c['c'].isspace():
                        if cur: out.append(cur); cur = []
                    else: cur.append((c['c'],) + tuple(c['bbox']) + (s['size'], round(l['bbox'][1], 1), c['origin'][1]))
            if cur: out.append(cur); cur = []
    res = []
    for w in out:
        res.append(dict(t=''.join(c[0] for c in w), chars=w, y=w[0][6], size=w[0][5]))
    return res

def marks_after_word(img, w, nxt):
    """raised components between the word's last letter and the next word: list of (x0,y0,x1,y1,npix) in px"""
    ch = w['chars']
    li = max((i for i, c in enumerate(ch) if c[0].isalpha()), default=None)
    if li is None: return None, None
    em = ch[li][5]; base = ch[li][7]                # font size and baseline (layer origin), in points
    xl = ch[li][3]                                 # right edge of the last letter
    xr = nxt['chars'][0][1] - 0.3 if nxt and nxt['y'] == w['y'] and nxt['chars'][0][1] > xl else xl + 0.6 * em
    xr = min(xr, xl + 0.6 * em)
    # the band where a raised number sits: from about cap height down to well above the x-height middle
    top_pt, cut_pt = base - 1.05 * em * 0.75, base - 0.30 * em * 0.75
    comps, box = components(img, xl + 0.2, xr, top_pt * Z, cut_pt * Z)
    out = [(a, b, c, d, len(pts)) for (a, b, c, d, pts) in comps if d < box[3] - 1 and b > box[1] and len(pts) >= 4]
    return out, dict(base=base, em=em)

if __name__ == '__main__':
    a, b = int(sys.argv[1]), int(sys.argv[2])
    d = pymupdf.open(PDF)
    for K in range(a, b + 1):
        p = d[K - 1]; img = Img(d, K - 1); W = words(p)
        for i, w in enumerate(W):
            if w['y'] < 40 or not re.search(r'[^\W\d_]', w['t']): continue
            m, g = marks_after_word(img, w, W[i + 1] if i + 1 < len(W) else None)
            if m:
                ctx = ' '.join(x['t'] for x in W[max(0, i - 3):i + 2])
                print(K, repr(w['t']), [(c - a_ + 1, d_ - b_ + 1, n) for a_, b_, c, d_, n in m], '|', ctx[:70])
