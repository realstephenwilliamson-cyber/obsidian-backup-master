# shared_folio_packets.py (28 Oct 2026, item 5; was build_packets.py): reading packets for links to a Zohar folio side held by two parashah notes.
# For each block: both candidate passages once (A = the lower-numbered note, B = the higher), then each citing link with its
# context, the link itself masked as ⟦label⟧ so the reader does not see the current target.
# Input: the listing job shared-folio-list.js (pf417) writes SHARED.json (rows of links to the five blocks, the holders) and DUMP.json (the citing and holding notes).
# The readers brief is shared-folio-brief.txt; two readers decide blind, and zfolio-retarget.tpl.js moves the links both place in the other note.
# usage: python3 shared_folio_packets.py SHARED.json DUMP.json OUTDIR
import sys, json, re, os
S = json.load(open(sys.argv[1])); D = json.load(open(sys.argv[2])); out = sys.argv[3]; os.makedirs(out, exist_ok=True)
def clean(s):
    s = re.sub(r'\[\^\d+\](?!:)', '', s)
    s = re.sub(r'\[\[([^\]|]*)\|([^\]]*)\]\]', r'\2', s)
    return re.sub(r'\[\[([^\]]*)\]\]', r'\1', s)
def note_path(name): return [k for k in D if k.endswith('/' + name + '.md')][0]
def candidate(name, blk):
    L = D[note_path(name)].split('\n'); i = [j for j, x in enumerate(L) if re.search(r'\^' + blk + r'\s*$', x)][0]
    v, f = blk[1], blk.split('-')[1]; num, side = int(f[:-1]), f[-1]
    nxt = f"z{v}-{num}b" if side == 'a' else f"z{v}-{num + 1}a"
    m = re.search(r'\*\*\[[^\]]*' + f + r'\]\*\*', L[i]); st = max(0, (m.start() if m else len(L[i])) - 700)
    parts = [L[i][st:]]; ended = 'the next folio side'
    for x in L[i + 1:]:
        if re.match(r'\[\^\d+\]:', x): ended = 'the end of the parashah\'s text (its notes follow)'; break
        if re.search(r'\^z\d-\d+[ab]\s*$', x):
            mm = list(re.finditer(r'\*\*\[[^\]]*\d+[ab]\]\*\*', x)); parts.append(x[:mm[-1].end()] if mm else x); break
        if x.strip(): parts.append(x)
    t = clean('\n\n'.join(parts))
    if len(t) > 8000: t = t[:8000] + ' …[cut]'
    return t, ended
rows = [r for r in S['rows'] if not r['path'].startswith('Texts/Zohar/Sefaria/') and not r['path'].endswith('Zohar folio index.md')]
groups = {'P1': ['z3-156b'], 'P2': ['z1-165b', 'z1-193a'], 'P3': ['z1-120b', 'z2-32a']}
key = []
for P, blks in groups.items():
    o = [f'# Packet {P}\n']
    for b in blks:
        hs = sorted(S['shared'][b], key=lambda n: n[6:10]); A, B = hs
        o.append(f"\n## Folio side {b[1]}:{b.split('-')[1]} (block {b})\n\nTwo notes carry this folio side: one parashah ends on it and the next begins on it.\n")
        for lab, h in (('A', A), ('B', B)):
            t, ended = candidate(h, b)
            o.append(f"\n### Passage {lab}: {h}\n\n(from just before the folio marker to {ended})\n\n```text\n{t}\n```\n")
        rs = [r for r in rows if r['block'] == b]
        o.append(f"\n### References to decide ({len(rs)})\n")
        for k, r in enumerate(rs, 1):
            rid = f"{b}-{k:02d}"; L = D[r['path']].split('\n'); line = L[r['line'] - 1]
            pos = line.find(r['original'], max(0, r['col'] - 5)); lab = re.sub(r'.*\|', '', r['original'])[:-2]
            ctx = clean(line[max(0, pos - 900):pos]) + '⟦' + lab + '⟧' + clean(line[pos + len(r['original']):pos + len(r['original']) + 350])
            fn = re.match(r'\[\^(\d+)\]:', line); pre = ''
            if not fn and line.startswith(' '):
                j = r['line'] - 2; acc = []
                while j >= 0 and (L[j].startswith(' ') or not L[j].strip() or re.match(r'\[\^\d+\]:', L[j])):
                    if L[j].strip(): acc.insert(0, L[j].strip())
                    if re.match(r'\[\^(\d+)\]:', L[j]): fn = re.match(r'\[\^(\d+)\]:', L[j]); break
                    j -= 1
                pre = clean(' / '.join(acc)); pre = ('…' + pre[-1200:]) if len(pre) > 1200 else pre
                if pre: ctx = '[earlier in the same footnote:] ' + pre + ' / ' + ctx
            where = f"footnote {fn.group(1)} of" if fn else "a line of"
            o.append(f"\n#### {rid}\n\nIn {where} *{os.path.basename(r['path'])[:-3]}* (line {r['line']}). Reference: `{lab}`\n\n> {ctx}\n")
            key.append({'id': rid, 'path': r['path'], 'line': r['line'], 'col': r['col'], 'original': r['original'], 'block': b, 'current': r['target'], 'A': A, 'B': B, 'label': lab})
    open(f'{out}/{P}.md', 'w').write(''.join(o))
json.dump(key, open(f'{out}/key.json', 'w'), ensure_ascii=False, indent=1)
print(len(key), 'references;', {P: sum(1 for k in key if k['block'] in b) for P, b in groups.items()})
