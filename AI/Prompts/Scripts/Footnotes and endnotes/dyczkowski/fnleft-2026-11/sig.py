# sig.py: the text-layer signal for each item: the tokens printed before the first words on the same visual line
# (text lines whose vertical extent overlaps the matched line and which lie to its left), number included.
import json, re, sys, pymupdf
from tl import P, byid, docs, sq
import unicodedata
fold = lambda s: ''.join(c for c in unicodedata.normalize('NFKD', sq(s).lower()) if c.isascii() and c.isalnum())
def page_lines(doc, K):
    d = doc[K-1].get_text('dict'); L = []
    for b in d['blocks']:
        for l in b.get('lines', []):
            sp = [s for s in l['spans'] if s['text'].strip()]
            if not sp: continue
            L.append({'t': ''.join(s['text'] for s in l['spans']), 'bbox': l['bbox'], 'spans': sp})
    return L
def signal(it):
    doc = docs.setdefault(it['vol'], pymupdf.open(P % it['vol']))
    fw = it['first_words'].replace('\\[illegible\\]', ' ').split()
    for K in it['pages']:
        L = page_lines(doc, K)
        for n in (4, 3, 2, 6, 8, 1):
            for F in (sq, fold):
                key = F(' '.join(fw[:n]))[:24 if n > 4 else 16]
                if len(key) < 4: continue
                hits = [i for i, l in enumerate(L) if key in F(l['t'])]
                if len(hits) == 1: break
            else:
                continue
            i = hits[0]; l = L[i]; x0, y0, x1, y1 = l['bbox']
            if F is fold:
                # map the folded match start back onto spans: count folded chars per span
                full = fold(l['t']); st = full.find(key); pre = []; pos = 0
                for s in l['spans']:
                    t = fold(s['text']); e = pos + len(t)
                    if e <= st: pre.append((s['text'].strip(), round(s['size'], 1)))
                    elif pos < st: pre.append((t[:st - pos], round(s['size'], 1)))
                    pos = e
                pre = [p for p in pre if p[0]]
                mid = (y0 + y1) / 2; left = []
                for j, m in enumerate(L):
                    if j == i: continue
                    a0, b0, a1, b1 = m['bbox']
                    if b0 - 1 <= mid <= b1 + 1 and a0 < x0 - 2:
                        left += [(s['text'].strip(), round(s['size'], 1)) for s in m['spans']]
                return {'K': K, 'pre': left + pre, 'n': n, 'fold': True, 'bbox': l['bbox']}
            full = sq(l['t']); st = full.find(key); pre = []; pos = 0
            for s in l['spans']:
                t = sq(s['text']); e = pos + len(t)
                if e <= st: pre.append((s['text'].strip(), round(s['size'], 1)))
                elif pos < st: pre.append((t[:st - pos], round(s['size'], 1)))
                pos = e
            # same-band lines to the left
            mid = (y0 + y1) / 2; left = []
            for j, m in enumerate(L):
                if j == i: continue
                a0, b0, a1, b1 = m['bbox']
                if b0 - 1 <= mid <= b1 + 1 and a0 < x0 - 2:
                    left += [(s['text'].strip(), round(s['size'], 1)) for s in m['spans']]
            return {'K': K, 'pre': left + pre, 'n': n, 'bbox': l['bbox']}
    return None
if __name__ == '__main__':
    for i in sys.argv[1:]:
        r = signal(byid[i]); print(i, byid[i]['label'], r)
