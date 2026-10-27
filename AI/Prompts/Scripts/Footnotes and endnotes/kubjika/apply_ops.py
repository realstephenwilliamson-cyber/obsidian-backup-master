# apply_ops.py (26 Oct 2026, fifth session): applies a footnote op list written by a page reader (see reader-brief.txt) to one note:
# replace (garbled call or note number -> [^n] / [^n]: ), indent (same-page continuation), move (a note carried over to the next page,
# joined to its footnote and indented), delete (stray number lines). Checks: every n in first_n..last_n has one call and one
# definition, calls in order, and lists the word-level differences against the old text for review. Used for Kubjika, Kali, Tripura
# and Trika (162 footnotes; ops in .work/edits/kubjika-listed-2026-10-26/footnote-ops-part1.json and -part2.json).
# apply_ops.py NOTE OPS OUT REPORT: apply a Kubjika footnote op list (see brief.md) to NOTE, write OUT, and check the result.
import sys, json, re
note, opsf, outf, repf = sys.argv[1:5]
L = open(note, encoding='utf-8').read().split('\n')
D = json.load(open(opsf, encoding='utf-8')); ops = D['ops']
probs = []
rep = {i: [] for i in range(1, len(L) + 1)}          # replaces per line
indent, delete, moves = set(), set(), {}
for o in ops:
    ln = o.get('line')
    if not ln or ln < 1 or ln > len(L): probs.append(('bad line', o)); continue
    if o['op'] == 'replace':
        c = L[ln - 1].count(o['old'])
        if c != 1: probs.append(('old found %d times' % c, ln, o['old'][:60])); continue
        rep[ln].append(o)
    elif o['op'] == 'indent': indent.add(ln)
    elif o['op'] == 'delete': delete.add(ln)
    elif o['op'] == 'move': moves[ln] = o['after']
    else: probs.append(('unknown op', o))
# replaces: non-overlapping within a line
new = list(L)
for ln, lst in rep.items():
    if not lst: continue
    s = L[ln - 1]; spans = []
    for o in lst:
        a = s.index(o['old']); spans.append((a, a + len(o['old']), o['new']))
    spans.sort()
    if any(spans[i][0] < spans[i - 1][1] for i in range(1, len(spans))): probs.append(('overlap', ln)); continue
    for a, b, r in reversed(spans): s = s[:a] + r + s[b:]
    new[ln - 1] = s
for ln in indent: new[ln - 1] = '    ' + new[ln - 1]
# build output with moves and deletes
moved_after = {}
for ln, after in moves.items(): moved_after.setdefault(after, []).append(ln)
out = []; skip = set(moves) | delete
def emit_after(ln, depth=0):
    for m in sorted(moved_after.get(ln, [])):
        out.append(''); out.append('    ' + new[m - 1].split('\n\n')[0].lstrip()); emit_after(m, depth + 1)
i = 0
while i < len(new):
    ln = i + 1
    if ln in moves and '\n\n' in new[i]:
        out.append(new[i].split('\n\n', 1)[1]); emit_after(ln); i += 1; continue
    if ln in skip:
        # drop the line and one following blank line if the previous output line is blank too
        if i + 1 < len(new) and new[i + 1].strip() == '' and out and out[-1].strip() == '': i += 1
        i += 1; continue
    out.append(new[i])
    emit_after(ln)
    i += 1
emitted = sum(1 for _ in moves)
text = '\n'.join(out)
# checks
calls = [int(m.group(1)) for m in re.finditer(r'\[\^(\d+)\](?!:)', text)]
defs = [int(m.group(1)) for m in re.finditer(r'(?m)^\[\^(\d+)\]:', text)]
lo, hi = D.get('first_n'), D.get('last_n')
want = list(range(lo, hi + 1)) if lo and hi else []
from collections import Counter
cc, dc = Counter(calls), Counter(defs)
miss_c = [n for n in want if cc[n] != 1]; miss_d = [n for n in want if dc[n] != 1]
order = calls == sorted(calls)
# plain-text comparison: strip [^n], [^n]: , indentation, and compare words
def norm(t):
    t = re.sub(r'\[\^\d+\]:? ?', ' ', t); return re.findall(r'[^\W\d_]+', t)
w0, w1 = norm('\n'.join(L)), norm(text)
import difflib
sm = difflib.SequenceMatcher(None, w0, w1, autojunk=False)
diffs = [(t, ' '.join(w0[a:b]), ' '.join(w1[c:d])) for t, a, b, c, d in sm.get_opcodes() if t != 'equal']
open(outf, 'w', encoding='utf-8').write(text)
R = {'problems': probs, 'calls': len(calls), 'defs': len(defs), 'range': [lo, hi], 'calls_not_once': miss_c, 'defs_not_once': miss_d,
     'calls_in_order': order, 'extra_calls': sorted(set(calls) - set(want)), 'word_diffs': diffs, 'lines_before': len(L), 'lines_after': len(out)}
json.dump(R, open(repf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k != 'word_diffs' else len(v)) for k, v in R.items()}, ensure_ascii=False)[:1500])
