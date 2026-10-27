# sample.py (27 Oct 2026, Dyczkowski footnotes night 1): picks the blind-check sample for a batch of converted notes and builds the
# checker's folder. Per note: 8 footnotes (every inserted call, carry-over and split first, then a seeded random choice);
# for each page that holds a sampled footnote, the checker gets the page image and the body paragraphs of that page that hold a
# sampled call, with every [^n] removed. The answers (where the calls are) stay with the lead in key.json.
# Usage: sample.py OUTDIR PDF ID:ORIG:PRE:OPS:OUT [ID:ORIG:PRE:OPS:OUT ...]   (files from prepass.py / the reader / apply_ops.py)
import sys, json, re, random, os, subprocess
from PIL import Image, ImageOps
outdir, pdf = sys.argv[1:3]; os.makedirs(outdir, exist_ok=True)
PAGE = re.compile(r'^\*\[p\. ([^\]]*)\]\* \^pg(\d+)\s*$')
key, tasks = {}, []
for spec in sys.argv[3:]:
    nid, origf, pref, opsf, outf = spec.split(':')
    T = open(outf, encoding='utf-8').read().split('\n')
    O = json.load(open(opsf, encoding='utf-8')); ops = O['ops']
    pre = json.load(open(os.path.join(os.path.dirname(pref), 'pre.json'), encoding='utf-8'))
    old_real = set(pre['real_defs_before'])
    special = set(); hi = set(); top = set()
    repf = os.path.join(os.path.dirname(outf), 'rep.json')
    rl = json.load(open(repf, encoding='utf-8')).get('relabelled', {}) if os.path.exists(repf) else {}
    num = lambda n: int(rl.get(str(n), n)) if str(rl.get(str(n), n)).isdigit() else n
    for o in ops:
        if o.get('kind') == 'call' and o.get('op') == 'replace' and re.sub(r'\[\^\d+\]', '', o['new']) == o['old']: special.add(num(o['n']))
        if o.get('kind') == 'call' and '[^' in o.get('old', '') and o.get('n'): special.add(num(o['n'])); hi.add(num(o['n'])); top.add(num(o['n']))   # an already-real call moved or renumbered
        if o.get('op') == 'move' or (o.get('kind') == 'def' and '\n\n' in o.get('new', '')): special.add(num(o.get('n'))); hi.add(num(o.get('n')))
    # page of each def and each call in the output
    page, defpage, callpos = None, {}, {}
    for i, l in enumerate(T):
        m = PAGE.match(l)
        if m: page = int(m.group(2)); continue
        d = re.match(r'^\[\^(\d+)\]:', l)
        if d: defpage[int(d.group(1))] = page
        for c in re.finditer(r'\[\^(\d+)\](?!:)', l): callpos[int(c.group(1))] = (i, page)
    # pages where a carried-over part was printed (the moved line's page in the pre-pass text)
    P = open(pref, encoding='utf-8').read().split('\n'); ppage = []; cp = None
    for l in P:
        m = PAGE.match(l)
        if m: cp = int(m.group(2))
        ppage.append(cp)
    carries = [(num(o.get('n')), ppage[o['line'] - 1], re.sub(r'^\[\^\d+\]: ', '', P[o['line'] - 1].strip())[:80]) for o in ops if o.get('op') == 'move']
    new = [n for n in sorted(defpage) if (n not in old_real or n in special) and n in callpos]
    rnd = random.Random(nid)
    pick = ([n for n in new if n in top] + [n for n in new if n in hi and n not in top] + [n for n in new if n in special and n not in hi])[:8]
    rest = [n for n in new if n not in pick]; rnd.shuffle(rest)
    pick = sorted(pick + rest[:max(0, 8 - len(pick))])
    bypage = {}
    for n in pick: bypage.setdefault(defpage[n], set()).add(n)
    for pg, ns in sorted(bypage.items()):
        lines = sorted({callpos[n][0] for n in ns})
        paras = [re.sub(r'\[\^\d+\]', '', T[i]).strip() for i in lines]
        defs_on_page = [n for n in sorted(defpage) if defpage[n] == pg]
        tid = '%s-p%d' % (nid, pg)
        tasks.append({'task': tid, 'pdf_page': pg, 'image': 'p-%03d.png' % pg, 'paragraphs': paras})
        key[tid] = {'note': nid, 'sampled': sorted(ns), 'defs_on_page': defs_on_page, 'special': sorted(ns & special),
                    'calls': {n: re.sub(r'\[\^\d+\]', '', T[callpos[n][0]][:T[callpos[n][0]].index('[^%d]' % n)])[-80:] for n in ns},
                    'def_starts': {n: next(re.sub(r'^\[\^\d+\]: ', '', l)[:80] for l in T if l.startswith('[^%d]: ' % n)) for n in defs_on_page}}
        dst = os.path.join(outdir, 'p-%03d.png' % pg)
        if not os.path.exists(dst):
            tmp = os.path.join(outdir, '_t')
            subprocess.run(['pdftoppm', '-f', str(pg), '-l', str(pg), '-r', '200', '-gray', '-png', '-singlefile', pdf, tmp], check=True)
            im = Image.open(tmp + '.png').convert('L'); bb = ImageOps.invert(im).point(lambda v: 255 if v > 60 else 0).getbbox()
            if bb: im = im.crop((max(0, bb[0] - 12), max(0, bb[1] - 12), min(im.width, bb[2] + 12), min(im.height, bb[3] + 12)))
            im.save(dst, optimize=True); os.remove(tmp + '.png')
    for n, pg, first in carries:
        tid = '%s-p%d-carry' % (nid, pg)
        tasks.append({'task': tid, 'pdf_page': pg, 'image': 'p-%03d.png' % pg, 'paragraphs': []})
        key[tid] = {'note': nid, 'sampled': [], 'defs_on_page': [], 'special': [n], 'calls': {}, 'def_starts': {}, 'carry_expected': first, 'carry_of': n}
        dst = os.path.join(outdir, 'p-%03d.png' % pg)
        if not os.path.exists(dst):
            tmp = os.path.join(outdir, '_t')
            subprocess.run(['pdftoppm', '-f', str(pg), '-l', str(pg), '-r', '200', '-gray', '-png', '-singlefile', pdf, tmp], check=True)
            im = Image.open(tmp + '.png').convert('L'); bb = ImageOps.invert(im).point(lambda v: 255 if v > 60 else 0).getbbox()
            if bb: im = im.crop((max(0, bb[0] - 12), max(0, bb[1] - 12), min(im.width, bb[2] + 12), min(im.height, bb[3] + 12)))
            im.save(dst, optimize=True); os.remove(tmp + '.png')
json.dump(tasks, open(os.path.join(outdir, 'tasks.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(key, open(os.path.join(outdir, '..', os.path.basename(outdir.rstrip('/')) + '-key.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(tasks), 'pages;', sum(len(k['sampled']) for k in key.values()), 'footnotes sampled')
