# survey.py (3 Nov 2026, night): Finn, every page's footnotes against the PDF text layer.
# Layer side from pdfside.page() (the 15 Oct reader of the PDF's own Courier/Courier-Oblique layer): note labels with first words,
# raised calls (small digit spans) with the word before. Note side: the page block (^pgK): [^X] calls, [^X]: definitions,
# plain 'N\.' paragraphs. Each layer note is matched to the block by its first words. Output: survey.json, pages that differ.
import json, re, glob, os, sys, unicodedata, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdfside
def norm(s):
    s = unicodedata.normalize('NFKD', s); s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]+', ' ', s).strip()
pages = {}
for f in sorted(glob.glob('md/The Kulacudamani Tantra [0-9]*.md')):
    T = open(f, encoding='utf-8').read().split('\n'); K = None
    for i, l in enumerate(T):
        m = re.match(r'^\*\[(?:p|PDF)\.? ([^\]]*)\]\* \^pg(\d+)$', l)
        if m: K = int(m.group(2)); pages[K] = dict(f=os.path.basename(f), pp=m.group(1), lines=[]); continue
        if K: pages[K]['lines'].append(l)
def labnum(s):
    if s is None: return None
    m = re.fullmatch(r'(\d{1,3})[.,*]?', s.strip()); return int(m.group(1)) if m else None
def base(x): return int(re.match(r'\d+', x).group(0)) if re.match(r'\d+', x) else None
out = {}
for K in sorted(pages):
    pg = pages[K]; i = K - 1
    p = pdfside.page(i)
    text = '\n'.join(pg['lines'])
    paras = [x for x in pg['lines'] if x.strip()]
    defs = [(m.group(1), m.group(2)) for x in paras for m in [re.match(r'^\[\^([^\]]+)\]: ?(.*)$', x)] if m]
    calls = re.findall(r'\[\^([^\]]+)\](?!:)', text)
    plain = [(int(m.group(1)), m.group(2)) for x in paras for m in [re.match(r'^(\d{1,3})\\\.\s*(.*)$', x)] if m]
    if not p: lnotes, lrefs = [], []
    else:
        lnotes = [dict(label=n['label'], num=labnum(n['label']), words=' '.join(n['words'][:8])) for n in p['notes'] if n['words']]
        lrefs = []
        for r in p['refs']:
            raw = r['raw']
            if not re.search(r'\d', raw): continue
            if re.fullmatch(r'\d{1,3}\.', raw.strip()) and r['x'] < p['left']: continue   # a small verse label in the margin
            w = p['body'][r['after']]['raw'] if r['after'] >= 0 else None
            lrefs.append(dict(after=w, raw=raw))
    # match each layer note to the block
    cands = [('def', x, norm(t)) for x, t in defs] + [('plain', str(n), norm(t)) for n, t in plain] + \
            [('para', None, norm(x)) for x in paras if not re.match(r'^(\[\^|\d{1,3}\\\.|\*\[)', x)]
    res = []
    for n in lnotes:
        w = n['words'][:45]; best = (0, None)
        for kind, lab, t in cands:
            r = difflib.SequenceMatcher(None, w, t[:len(w) + 5]).ratio()
            if r > best[0]: best = (r, (kind, lab))
        kind, lab = best[1] if best[1] else (None, None)
        st = 'missing' if best[0] < 0.6 else kind
        if st == 'def' and n['num'] is not None and base(lab) != n['num']: st = 'def-mislabel'
        if n['label'] is None and st == 'para': st = 'cont'
        res.append(dict(n, match=st, as_=lab, score=round(best[0], 2)))
    newnotes = [x for x in res if x['label'] is not None]
    flags = []
    if any(x['match'] in ('plain', 'para', 'missing', 'def-mislabel') for x in newnotes): flags.append('notes')
    if len(defs) != len(newnotes): flags.append('count %d/%d' % (len(defs), len(newnotes)))
    if len(calls) != len(lrefs): flags.append('calls %d/%d' % (len(calls), len(lrefs)))
    cs, ds = set(calls), set(x for x, _ in defs)
    if cs - ds or ds - cs: flags.append('pairing')
    if '<sup' in text: flags.append('sup')
    out[K] = dict(f=pg['f'], pp=pg['pp'], flags=flags, notes=res, refs=lrefs, defs=[x for x, _ in defs], calls=calls,
                  plain=[n for n, _ in plain])
json.dump(out, open('survey.json', 'w'), ensure_ascii=False, indent=0)
fl = {k: v for k, v in out.items() if v['flags']}
print('pages', len(out), 'flagged', len(fl))
import collections
c = collections.Counter(f.split()[0] for v in fl.values() for f in v['flags']); print(c)
print('layer notes', sum(len([x for x in v['notes'] if x['label'] is not None]) for v in out.values()), 'defs', sum(len(v['defs']) for v in out.values()))
