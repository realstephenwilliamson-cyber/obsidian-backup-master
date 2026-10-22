# Deshpande: give each endnote in the appendix note a block id ^n-<chapter>-<number>, from the PDF layer's note labels.
import sys, os, re, json, difflib, unicodedata
VAULT = r'C:\Vaults\Obsidian Vault'
ORIG = os.path.join(VAULT, r'.work\backup-footnotes-2026-10-18\Deshpande\Library\Trika\Abhinavagupta (Deshpande)')
APPX = 'Abhinavagupta 12 - Appendix - Notes and References.md'
LAY = json.load(open(os.path.expanduser(r'~\fnwork\desh\layer.json'), encoding='utf-8'))
MARK = re.compile(r'^\*\[(?:p|PDF)\.? [^\]]*\]\* \^pg(\d+)$')

def norm(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]', '', w)

def layer_notes():
    """the layer's endnotes in order: dict(ch, n, words) ; chapters counted from number resets"""
    notes = []; ch = 0; last = 99
    for K in range(165, 180):
        for l in LAY[K - 1]['lines']:
            ws = [t for w in l['w'] for t in w['t'].split()]
            if not ws: continue
            t = ' '.join(ws)
            if re.search(r'(?i)^c\s*h\s*a\s*p\s*t\s*e\s*r\b', t) and len(t) < 25: continue
            m = re.match(r'^(\d{1,2})(?:-?([A-Z]))?[.,]$', ws[0])
            if m and l['x'] < 75:
                n = int(m.group(1))
                if n <= last and not m.group(2): ch += 1
                if not (n == last and m.group(2)): last = n
                notes.append(dict(ch=ch, n=n, suf=(m.group(2) or '').lower(), K=K, words=ws[1:]))
            elif notes:
                notes[-1]['words'] += ws
    return notes

def run():
    L = open(os.path.join(ORIG, APPX), encoding='utf-8').read().split('\n')
    start = next(i for i, l in enumerate(L) if MARK.match(l))
    # md paragraphs (blocks) after the first marker, with their line ranges; markers and headings are not text
    paras = []; cur = []
    for i in range(start, len(L)):
        l = L[i]
        if not l.strip() or MARK.match(l) or l.startswith('#'):
            if cur: paras.append(cur); cur = []
            continue
        cur.append(i)
    if cur: paras.append(cur)
    mt = []      # md tokens: (para index, line index, start, end, word, norm)
    for pi, lines in enumerate(paras):
        for li in lines:
            for m in re.finditer(r'\S+', L[li]):
                n = norm(m.group(0))
                if n: mt.append((pi, li, m.start(), m.end(), m.group(0), n))
    notes = layer_notes()
    pt = []
    for k, nt in enumerate(notes):
        for w in nt['words']:
            n = norm(w)
            if n: pt.append((k, n))
    sm = difflib.SequenceMatcher(None, [x[1] for x in pt], [x[5] for x in mt], autojunk=False)
    amap = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal' or (tag == 'replace' and i2 - i1 == j2 - j1):
            for d in range(i2 - i1): amap[i1 + d] = j1 + d
    first_pt = {}
    for i, (k, n) in enumerate(pt): first_pt.setdefault(k, i)
    anchors = {}; report = []; splits = []
    for k, nt in enumerate(notes):
        bid = 'n-%d-%d%s' % (nt['ch'], nt['n'], nt['suf'])
        i0 = first_pt.get(k)
        # the first of the note's first three words that is aligned
        hit = next(((i, amap[i]) for i in range(i0, min(i0 + 3, len(pt))) if i in amap and pt[i][0] == k), None) if i0 is not None else None
        if hit is None: report.append((bid, 'first words not aligned')); continue
        # back up to the md token of the note's first word, if the alignment started on its 2nd or 3rd
        j = hit[1] - (hit[0] - i0)
        if j < 0: report.append((bid, 'no md word before')); continue
        lay3 = [norm(w) for w in nt['words'] if norm(w)][:3]
        pi, li, s, e, w, n = mt[j]
        # similarity of the md words from here with the layer's first words
        md3 = [x[5] for x in mt[j:j + 3]]
        sim = difflib.SequenceMatcher(None, ''.join(lay3), ''.join(md3)).ratio()
        if sim < 0.6: report.append((bid, 'weak match %.2f: %s / %s' % (sim, lay3, md3))); continue
        # where does the note start in the md paragraph? before a label token ('7\.', '1I.') just before the word
        line = L[li]; cut = s
        mlab = re.search(r'(?:^|\s)(\(?[\dIlS]{1,2}(?:-?[A-Za-z])?\\?[.,]\s*(?:\([a-z]\)\s*)?)$', line[:s])
        if mlab: cut = mlab.start(1)
        if not re.search(r'\w', line[:cut]): cut = 0          # only punctuation before it ('. . . Siddhā')
        first_line_of_para = paras[pi][0]
        at_start = (li == first_line_of_para and not line[:cut].strip())
        if not at_start:
            splits.append((bid, li, cut))
        anchors[bid] = dict(pi=pi, li=li, cut=cut, at_start=at_start, K=nt['K'], first=' '.join(nt['words'][:4]))
    return L, paras, notes, anchors, report, splits

if __name__ == '__main__':
    L, paras, notes, anchors, report, splits = run()
    print('layer notes', len(notes), 'anchored', len(anchors), 'paragraph splits needed', len(splits))
    for r in report: print('  NOT', r)
    for b, li, cut in splits: print('  SPLIT', b, 'line', li + 1, repr(L[li][max(0, cut - 30):cut + 30]))
