# view.py K [K...]: compact view of a page for settling its footnotes: layer notes (label, first and last words), layer calls
# (word before, raw digits), the note's page block: body snippets around the layer's call words, and the foot lines.
import json, re, glob, os, sys, unicodedata, difflib
sys.path.insert(0, '/home/claude/finn')
import pdfside
def nw(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower(); return re.sub(r'[^a-z]', '', w)
def load():
    pages = {}
    for f in sorted(glob.glob('/home/claude/finn/md/The Kulacudamani Tantra [0-9]*.md')):
        T = open(f, encoding='utf-8').read().split('\n'); K = None
        for i, l in enumerate(T):
            m = re.match(r'^\*\[(?:p|PDF)\.? ([^\]]*)\]\* \^pg(\d+)$', l)
            if m: K = int(m.group(2)); pages[K] = dict(f=os.path.basename(f), pp=m.group(1), lines=[]); continue
            if K: pages[K]['lines'].append(l)
    return pages
P = load()
def show(K):
    pg = P[K]; p = pdfside.page(K - 1)
    print(f'===== K{K} p.{pg["pp"]} ({pg["f"][24:26]})')
    if p:
        for n in p['notes']:
            ws = n['words']; print(f'  L-note {n["label"]!s:6} {" ".join(ws[:9])} ... {" ".join(ws[-5:])}')
        print('  L-calls', '; '.join(f'{(p["body"][r["after"]]["raw"] if r["after"] >= 0 else "^")}|{r["raw"]}' for r in p['refs'] if re.search(r'\d', r['raw'])))
    lines = pg['lines']; ne = [(i, l) for i, l in enumerate(lines) if l.strip()]
    # foot: from the first line that is a definition or starts with a number label followed by text (not a verse? shown anyway)
    callw = set(nw(p['body'][r['after']]['raw']) for r in p['refs'] if r['after'] >= 0 and re.search(r'\d', r['raw'])) if p else set()
    foot = len(lines)
    if p and p['notes']:
        fw = ' '.join(p['notes'][0]['words'][:6])
        for i, l in ne:
            t = ' '.join(x for x in (nw(w) for w in l.split()) if x)
            t = re.sub(r'^\S*\s?', '', t) if re.match(r'^\[\^|^\d', l) else t
            if difflib.SequenceMatcher(None, fw, t[:len(fw) + 3]).ratio() > 0.7: foot = i; break
    for i, l in ne:
        if i >= foot or re.match(r'^(\[\^|\d{1,3}\\?[.,]\s|\d{1,3}\\?\.$)', l) or len(l) < 70:
            print(f'  {i:3}| {l[:230]}')
        else:
            # snippets: around call words from the layer and around junk digits glued to words
            sn = []
            for m in re.finditer(r'\S+', l):
                w = m.group(0); hit = nw(w) and any(difflib.SequenceMatcher(None, nw(w), c).ratio() > 0.8 for c in callw if c)
                junk = re.search(r'[^\s\d\[\]^(\-:–/.,]\d{1,3}(?!\d)|\[\^|<sup', w) or (re.fullmatch(r'[\d\\*+°!#?%]{1,5}[.,;:]?', w) and not re.match(r'(pp?\.|[IVX]+:|Verses?|Chapter|footnote)', l[max(0, m.start() - 12):m.start()].split()[-1] if l[:m.start()].split() else ''))
                if hit or junk: sn.append(l[max(0, m.start() - 45):m.end() + 25].replace('\n', ' '))
            if sn: print(f'  {i:3}: ' + ' ¦ '.join(sn))
if __name__ == "__main__":
  for a in sys.argv[1:]:
      if "-" in a: lo, hi = map(int, a.split('-')); [show(k) for k in range(lo, hi + 1)]
      else: show(int(a))
