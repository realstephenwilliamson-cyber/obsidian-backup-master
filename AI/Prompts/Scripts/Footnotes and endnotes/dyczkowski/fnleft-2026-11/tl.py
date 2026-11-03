# tl.py: text-layer look at where each item's first words sit on its page.
import json, re, sys, pymupdf
P = '/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. %s.pdf'
full = json.load(open('full.json')); byid = {x['id']: x for x in full}
docs = {}
sq = lambda s: re.sub(r'\s+', '', s)
def lines(doc, K):
    d = doc[K-1].get_text('dict'); L = []
    for b in d['blocks']:
        for l in b.get('lines', []):
            t = ''.join(s['text'] for s in l['spans'])
            L.append({'t': t, 'bbox': l['bbox'], 'spans': [(s['text'], round(s['size'],1)) for s in l['spans']]})
    return L
def locate(it):
    doc = docs.setdefault(it['vol'], pymupdf.open(P % it['vol']))
    fw = it['first_words'].replace('\\[illegible\\]', ' ').split()
    for K in it['pages']:
        L = lines(doc, K)
        for n in (4, 3, 2):
            key = sq(' '.join(fw[:n]))[:16]
            if len(key) < 4: continue
            for i, l in enumerate(L):
                s = sq(l['t'])
                j = s.find(key)
                if j >= 0:
                    return {'K': K, 'i': i, 'line': l, 'prev': L[i-1]['t'] if i else '', 'pre': s[:j], 'n': n}
    return None
if __name__ == '__main__':
    for i in sys.argv[1:]:
        it = byid[i]; r = locate(it)
        print(i, it['label'], repr(it['first_words'][:40]))
        if r: print('   K', r['K'], 'pre', repr(r['pre']), '| line', repr(r['line']['t'][:90]), '\n   spans', r['line']['spans'][:4], '\n   prev', repr(r['prev'][:80]))
        else: print('   not located')
