# Item 4 (28 Oct 2026, after-28-Oct session): pages each held page-label edit depends on.
import json, re, sys
S = json.load(open('/mnt/user-data/uploads/Obsidian Vault/.work/edits/pagelabels-2026-10-28/pf418-spec.json'))
Lf = json.load(open('/mnt/user-data/uploads/Obsidian Vault/.work/edits/pagelabels-2026-10-28/left.json'))
M = json.load(open('/mnt/user-data/uploads/Obsidian Vault/.work/out/pf448-pl-markers.json'))
notes = {n['path']: n for n in S['notes']}
fills = {(f['path'], f['K']): f for f in S['fills']}
groups = Lf['left']
def chapter_of_label(line):
    m = re.match(r'- \[\[([^\]|#]+)', line); nm = m.group(1).split('/')[-1]
    return next((p for p in M['ch'] if p.endswith('/' + nm + '.md')), None)
def marks(p):  # markers with fills applied: [(N, K, kind)]
    out = []
    for kind, N, K in M['ch'][p]['mk']:
        f = fills.get((p, K))
        out.append((f['N'] if (kind == 'PDF' and f) else N, K, 'fill' if (kind == 'PDF' and f) else kind))
    return out
E = []
for g, hs in groups.items():
    for h in hs:
        p, old, new = h[0], h[1], h[2]
        e = {'group': g, 'path': p, 'old': old, 'new': new, 'deps': []}
        if old.startswith('*[PDF'):
            K = int(re.search(r'\^pg(\d+)', old).group(1)); f = fills[(p, K)]
            e['kind'] = 'fill'; e['deps'] = [(p, K, f['N'], 'self'), (p, f['prev'][0], f['prev'][1], 'nb'), (p, f['next'][0], f['next'][1], 'nb')]
        else:
            cp = p if old.startswith('page_range') else chapter_of_label(old)
            e['kind'] = 'range' if old.startswith('page_range') else 'label'; e['chapter'] = cp
            ms = [m for m in marks(cp) if m[2] != 'PDF']
            if not ms: e['deps'] = []; E.append(e); continue
            for m in ms[:2]: e['deps'].append((cp, m[1], m[0], 'first' if m is ms[0] else 'first2'))
            for m in ms[-2:]: e['deps'].append((cp, m[1], m[0], 'last' if m is ms[-1] else 'last2'))
        E.append(e)
pages = {}
for e in E:
    for p, K, N, role in e['deps']:
        pages.setdefault((p, K), N)
print('edits', len(E), 'pages', len(pages))
from collections import Counter
print(Counter(e['kind'] for e in E))
json.dump({'edits': E, 'pages': [[p, K, N] for (p, K), N in pages.items()]}, open('deps.json', 'w'), ensure_ascii=False, indent=1)
