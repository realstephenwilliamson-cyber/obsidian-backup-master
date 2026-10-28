# apply_ops.py (27 Oct 2026, Dyczkowski footnotes night 1; adapted from ../kubjika/apply_ops.py). Applies a page reader's op list
# (see reader-brief.txt) to the pre-pass output of one note, and checks the result against the original note.
# Usage: apply_ops.py ORIG PRE OPS OUT REPORT [--renumber]
#   ORIG = the note as it is in the vault; PRE = prepass.py's pre.md (the op line numbers refer to it); OPS = the reader's ops.json.
# Ops: replace (call, def fix, split of two run-together notes: `new` may hold "\n\n[^n]: "), indent / unindent (same-page
# continuation), move (a part carried over to the next page: joined after line `after`, indented), delete (stray number lines).
# A call glued to an opening parenthesis gets a space (Obsidian reads `[^n](x)` as a link).
# Checks: every footnote number of the note once as a call and once as a definition; calls in order; page markers, headings and
# frontmatter unchanged and in order; the word-level differences against ORIG (to be read by the lead: only removed garble marks
# and moved carry-overs are expected).
import sys, json, re, difflib
from collections import Counter
origf, pref, opsf, outf, repf = sys.argv[1:6]; RENUM = '--renumber' in sys.argv
# --start=N (28 Oct 2026, night 2): with --renumber, the first label is N (the printed number of the note's first footnote) instead of the lowest label
START = next((int(a.split('=')[1]) for a in sys.argv if a.startswith('--start=')), None)
O = open(origf, encoding='utf-8').read()
L = open(pref, encoding='utf-8').read().split('\n')
D = json.load(open(opsf, encoding='utf-8')); ops = D['ops'] if isinstance(D, dict) else D
probs = []
rep = {i: [] for i in range(1, len(L) + 1)}
indent, unindent, delete, moves = set(), set(), set(), {}
for o in ops:
    ln = o.get('line')
    if not isinstance(ln, int) or ln < 1 or ln > len(L): probs.append(('bad line', o)); continue
    op = o.get('op')
    if op == 'replace':
        c = L[ln - 1].count(o['old'])
        if c != 1: probs.append(('old found %d times' % c, ln, o['old'][:60])); continue
        rep[ln].append(o)
    elif op == 'indent': indent.add(ln)
    elif op == 'unindent': unindent.add(ln)
    elif op == 'delete': delete.add(ln)
    elif op == 'move': moves[ln] = o['after']
    else: probs.append(('unknown op', o))
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
for ln in indent:
    if not new[ln - 1].startswith('    '): new[ln - 1] = '    ' + new[ln - 1]
for ln in unindent:
    if new[ln - 1].startswith('    '): new[ln - 1] = new[ln - 1][4:]
moved_after = {}
for ln, after in moves.items(): moved_after.setdefault(after, []).append(ln)
out = []; skip = set(moves) | delete
def emit_after(ln):
    for m in sorted(moved_after.get(ln, [])):
        out.append(''); out.append('    ' + new[m - 1].split('\n\n')[0].lstrip()); emit_after(m)
i = 0
while i < len(new):
    ln = i + 1
    if ln in moves and '\n\n' in new[i]:
        out.append(new[i].split('\n\n', 1)[1]); emit_after(ln); i += 1; continue
    if ln in skip:
        if i + 1 < len(new) and new[i + 1].strip() == '' and out and out[-1].strip() == '': i += 1
        i += 1; continue
    out.append(new[i]); emit_after(ln); i += 1
text = '\n'.join(out)
# a call glued to an opening parenthesis, `[^n](54-55ab)`, is read by Obsidian as a link (27 Oct 2026, batch 1): keep a space
glued = len(re.findall(r'\[\^\d+\]\(', text)); text = re.sub(r'(\[\^\d+\])\(', r'\1 (', text)
# --renumber: a reader who split run-together notes may have used letter labels (232b); relabel every footnote of the note
# by the order of its calls, from the first number on (each label must have one call and one definition)
relabel = {}
# --map=FILE (28 Oct 2026, night 2): an explicit relabel map {old label: new label} (e.g. to give the printed numbers where a
# note's labels run behind the print), applied instead of --renumber
MAPF = next((a.split('=', 1)[1] for a in sys.argv if a.startswith('--map=')), None)
if MAPF:
    relabel = {str(k): str(v) for k, v in json.load(open(MAPF, encoding='utf-8')).items()}
    text = re.sub(r'\[\^([0-9A-Za-z]+)\]', lambda m: '[^%s]' % relabel.get(m.group(1), m.group(1)), text)
elif RENUM:
    order = []
    for m in re.finditer(r'\[\^([0-9A-Za-z]+)\](?!:)', text):
        if m.group(1) not in order: order.append(m.group(1))
    start = START if START is not None else min(int(x) for x in order if x.isdigit())
    relabel = {lab: str(start + i) for i, lab in enumerate(order)}
    text = re.sub(r'\[\^([0-9A-Za-z]+)\]', lambda m: '[^%s]' % relabel.get(m.group(1), m.group(1)), text)
    relabel = {k: v for k, v in relabel.items() if k != v}
# a definition right after a non-blank line is not a footnote of its own for Obsidian (its cache lists neither the definition
# nor its call; 27-28 Oct 2026): keep a blank line before every definition
glue = len(re.findall(r'(?m)^(?:[^\n]*\S[^\n]*)\n(?=\[\^[0-9A-Za-z]+\]:)', text))
text = re.sub(r'(?m)^([^\n]*\S[^\n]*)\n(?=\[\^[0-9A-Za-z]+\]:)', r'\1\n\n', text)
# checks
calls = [int(m.group(1)) for m in re.finditer(r'\[\^(\d+)\](?!:)', text)]
defs = [int(m.group(1)) for m in re.finditer(r'(?m)^\[\^(\d+)\]:', text)]
cc, dc = Counter(calls), Counter(defs)
nums = sorted(set(calls) | set(defs))
not_once = [n for n in nums if cc[n] != 1 or dc[n] != 1]
order = calls == sorted(calls)
def struct(t):
    T = t.split('\n'); fm = ''
    if T and T[0] == '---':
        k = T.index('---', 1); fm = '\n'.join(T[:k + 1])
    return fm, [l for l in T if re.match(r'^\*\[p\. [^\]]*\]\* \^pg\d+\s*$', l)], [l for l in T if re.match(r'^#{1,6} ', l)], re.findall(r'\^[A-Za-z0-9-]+\s*$', t, re.M)
s0, s1 = struct(O), struct(text)
struct_ok = {'frontmatter': s0[0] == s1[0], 'page_markers': s0[1] == s1[1], 'headings': s0[2] == s1[2], 'block_ids': s0[3] == s1[3]}
# every page marker still followed by a blank line (so its ^pg id registers)
T1 = text.split('\n')
pg_blank = all(i + 1 >= len(T1) or T1[i + 1].strip() == '' for i, l in enumerate(T1) if re.match(r'^\*\[p\. [^\]]*\]\* \^pg\d+\s*$', l))
def norm(t):
    t = re.sub(r'\[\^\d+\]:? ?', ' ', t); return re.findall(r'[^\W\d_]+', t)
w0, w1 = norm(O), norm(text)
sm = difflib.SequenceMatcher(None, w0, w1, autojunk=False)
diffs = [(t, ' '.join(w0[a:b])[:200], ' '.join(w1[c:d])[:200]) for t, a, b, c, d in sm.get_opcodes() if t != 'equal']
illeg = (O.count('[illegible]') + O.count('\\[illegible\\]'), text.count('[illegible]') + text.count('\\[illegible\\]'))
C0, C1 = Counter(w0), Counter(w1); removed = dict(C0 - C1); added = dict(C1 - C0)
open(outf, 'w', encoding='utf-8').write(text)
R = {'problems': probs, 'relabelled': relabel, 'space_before_paren': glued, 'blank_before_def': glue, 'calls': len(calls), 'defs': len(defs), 'numbers': [nums[0], nums[-1]] if nums else None, 'not_once': not_once,
     'calls_in_order': order, 'struct': struct_ok, 'pg_blank_after': pg_blank, 'illegible': illeg, 'words_removed': removed, 'words_added': added, 'word_diffs': diffs,
     'ops': len(ops), 'moves': len(moves), 'deletes': len(delete), 'lines_before': len(L), 'lines_after': len(out)}
json.dump(R, open(repf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if k != 'word_diffs' else len(v)) for k, v in R.items()}, ensure_ascii=False)[:1500])
