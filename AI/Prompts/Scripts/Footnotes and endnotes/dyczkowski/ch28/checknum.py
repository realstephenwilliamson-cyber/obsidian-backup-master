# checknum.py: the numbered notes against the originals: the same words except the `N\.` labels added and the garble
# tokens dropped (listed in ch28-map.json); frontmatter, headings, page markers unchanged.
import json, re, difflib
M = json.load(open('/home/claude/lost/ch28/num/ch28-map.json'))
for i in '02 03 04 05 06 07'.split():
    nid = 'v10-' + i
    a = open('/home/claude/dyfn/src/%s.md' % nid).read(); b = open('/home/claude/lost/ch28/num/%s.num.md' % nid).read()
    wa = a.split(); wb = [w for w in b.split() if not re.fullmatch(r'\d+\\\.', w)]
    drops = sorted(t for r in M if r.get('note') == nid and r.get('dropped') for t in r['dropped'].split())
    sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False); gone = []; added = []
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op in ('delete', 'replace'): gone += wa[a1:a2]
        if op in ('insert', 'replace'): added += wb[b1:b2]
    keep = lambda t: [l for l in t.split('\n') if l.startswith('#') or l.startswith('*[p.') or l == '---']
    print(nid, 'labels', len(re.findall(r'(?m)^\d+\\\. ', b)), 'gone==dropped', sorted(gone) == drops, 'added', added[:5],
          'struct same', keep(a) == keep(b), 'lines', a.count('\n'), b.count('\n'))
