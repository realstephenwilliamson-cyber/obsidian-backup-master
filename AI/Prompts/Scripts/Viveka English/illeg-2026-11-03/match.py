# match.py: ties each placed leftover gap of 27 Oct to a placeholder run in the notes as they are now (dy-notes.json),
# by the words before and after it; drops items whose placeholder is gone (e.g. stripped as a footnote's leading
# placeholder on 3 Nov). -> matched.json {G-id: {path, start, end, run}}
import json, re, difflib
N = json.load(open('/mnt/user-data/uploads/Obsidian Vault/.work/xfer/dy-notes.json'))
L = json.load(open('/mnt/user-data/uploads/Obsidian Vault/.work/edits/illeg-2026-10-27/leftovers.json'))
items = [r for r in L if 'box400' in r]
PH = r'\\\[illegible\\\]'
RUN = re.compile(PH + r'(?:[ \t]*' + PH + r')*')
norm = lambda s: re.sub(r'\s+', ' ', re.sub(r'\[\^[^\]]*\]|\\|\*|<[^>]+>|\[\?\]', '', s)).strip()
runs = {}
for p, t in N.items():
    runs[p] = [(m.start(), m.end(), m.group(0).count('[illegible')) for m in RUN.finditer(t)]
out, miss, amb = {}, [], []
used = set()
for r in items:
    p = 'Library/Trika/Tantraloka (Dyczkowski)/' + r['note']
    if p not in N: miss.append(r['id']); continue
    t = N[p]; b, _, a = r['context'].partition('[?]'); b, a = norm(b)[-30:], norm(a)[:30]
    sc = []
    if len(b) + len(a) < 12: miss.append(r['id']); continue
    for s, e, n in runs[p]:
        bb = norm(t[max(0, s - 120):s]); aa = norm(t[e:e + 120])
        rb = difflib.SequenceMatcher(None, b, bb[-len(b):]).ratio() if b else None
        ra = difflib.SequenceMatcher(None, a, aa[:len(a)]).ratio() if a else None
        parts = [x for x in (rb, ra) if x is not None]
        score = 2 * sum(parts) / len(parts) if len(parts) == 2 else (2 * parts[0] if len(b) + len(a) >= 20 else 0)
        sc.append((score, s, e, n))
    sc.sort(reverse=True)
    if not sc or sc[0][0] < 1.7: miss.append(r['id']); continue
    if len(sc) > 1 and sc[1][0] > sc[0][0] - 0.15: amb.append(r['id']); continue
    s, e, n = sc[0][1:]
    if (p, s) in used: amb.append(r['id']); continue
    used.add((p, s)); out['G%04d' % r['id']] = {'path': p, 'start': s, 'end': e, 'run': n, 'n27': r['placeholders'], 'score': round(sc[0][0], 2)}
json.dump(out, open('matched.json', 'w'), ensure_ascii=False)
import collections
print('matched', len(out), 'gone/unmatched', len(miss), 'ambiguous', len(amb))
print('run-length mismatch', sum(1 for v in out.values() if v['run'] != v['n27']))
print(collections.Counter(round(v['score'], 1) for v in out.values()).most_common(8))
