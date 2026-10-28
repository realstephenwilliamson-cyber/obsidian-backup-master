# Item 4 (28 Oct 2026, after-28-Oct session): notes whose markers are not all plain numbers. Safe subset: the page range
# (and its index label) only drops a label that is not a page number (Cover, C1, FC, a, b, Présentation, Back Cover ...) at one end;
# the other end stays; the numbered markers run without descending. A range with no numbered marker becomes "" and its label "(PDF K1–K2)".
import json, re, sys
R = json.load(open(sys.argv[1]))
R2I = lambda s: (lambda v: sum(v[i] if i + 1 == len(s) or v[i] >= v[i + 1] else -v[i] for i in range(len(s))))([{'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000}[c] for c in s.lower()])
def ends(n):
    n = n.strip()
    if re.fullmatch(r'\d+|[ivxlcdm]+|[IVXLCDM]+', n): return (n, n)
    m = re.fullmatch(r'(\d+|[ivxlcdm]+|[IVXLCDM]+)\s*[-–]\s*(\d+|[ivxlcdm]+|[IVXLCDM]+)', n)
    return (m.group(1), m.group(2)) if m else None
def num(v): return ('a', int(v)) if v.isdigit() else ('r', R2I(v))
edits, safe, rest = {}, [], []
for p, r in R.items():
    pm = [(n, K) for k, n, K in r['mk'] if k == 'p.']; allK = [K for k, n, K in r['mk']]
    vals = [(ends(n), K) for n, K in pm if ends(n)]
    nonnum = [n for n, K in pm if not ends(n)]
    cur = re.sub(r'^page_range:\s*', '', r['pr']).strip().strip('"')
    rng = '' if not vals else (vals[0][0][0] if vals[0][0][0] == vals[-1][0][1] else f'{vals[0][0][0]}–{vals[-1][0][1]}')
    if cur == rng or not nonnum: rest.append((p, cur, rng, 'same' if cur == rng else 'no cover-type label')); continue
    seq = [num(x) for (a, b), K in vals for x in (a, b)]
    desc = any(seq[i][0] == seq[i + 1][0] and seq[i + 1][1] < seq[i][1] for i in range(len(seq) - 1))
    cparts = re.split(r'–', cur); nparts = rng.split('–') if rng else []
    ok = not desc and len(cparts) <= 2 and (
        (rng == '' and all(c in nonnum for c in cparts)) or
        (len(cparts) == 2 and len(nparts) == 2 and ((cparts[0] in nonnum and cparts[1] == nparts[1]) or (cparts[1] in nonnum and cparts[0] == nparts[0]))) or
        (len(cparts) == 1 and cparts[0] in nonnum and len(nparts) >= 1))
    if not ok or not r['line']: rest.append((p, cur, rng, 'descending' if desc else 'not a one-end change' if r['line'] else 'no index line')); continue
    E = edits.setdefault(p, []); E.append([r['pr'] + '\n', f'page_range: "{rng}"\n'])
    lab = f'(pp. {rng})' if rng else '(PDF ' + (str(allK[0]) if allK[0] == allK[-1] else f'{allK[0]}–{allK[-1]}') + ')'
    nl = re.sub(r'\((pp\.|PDF) [^)]*\)\s*$', lab, r['line'])
    if nl != r['line']: edits.setdefault(r['book'], []).append([r['line'], nl])
    safe.append((p, cur, rng))
json.dump({'backup': '.work/backup-pagelabels-2026-10-28b', 'edits': edits}, open(sys.argv[2], 'w'), ensure_ascii=False)
json.dump({'safe': safe, 'rest': rest}, open('odd-sorted.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print('safe', len(safe), 'edits', sum(len(v) for v in edits.values()), 'notes', len(edits)); print(Counter(x[3] for x in rest))
