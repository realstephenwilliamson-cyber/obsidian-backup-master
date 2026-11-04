# align.py: the positions of the unfilled gap IDs in the notes as they stand after pf679 (dy-after.json). In each note the runs of
# the 3 Nov dump, minus the runs filled by pf679, line up one to one with the runs left. -> tb/pos.json {id: [path, start, end]}
import json, re
N0 = json.load(open('/mnt/user-data/uploads/Obsidian Vault/.work/xfer/dy-notes.json')); N1 = json.load(open('dy-after.json'))
PH = r'\\\[illegible\\\]'; RUN = re.compile(PH + r'(?:[ \t]*' + PH + r')*')
loc = {g: (m['path'], m['start']) for g, m in json.load(open('matched.json')).items()}
for r in json.load(open('runs2.json')): loc[r['id']] = (r['path'], r['start'])
by = {(p, s): g for g, (p, s) in loc.items()}
dec = json.load(open('gaps-decisions.json'))
pos, bad = {}, []
for p in N0:
    r0 = [m for m in RUN.finditer(N0[p])]; r1 = [m for m in RUN.finditer(N1[p])]
    keep = [m for m in r0 if by.get((p, m.start())) not in dec]
    if len(keep) != len(r1): bad.append((p, len(keep), len(r1))); continue
    for a, b in zip(keep, r1):
        g = by.get((p, a.start()))
        if g: pos[g] = [p, b.start(), b.end()]
print(len(pos), 'positions;', len(bad), 'notes misaligned', bad[:3])
json.dump(pos, open('tb/pos.json', 'w'), ensure_ascii=False)
