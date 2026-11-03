# check_edits.py (SDK 1): the lead's mechanical check of the readers' edits for a list of cases, and the whole-page-block edits.
# Per edit: "old" occurs once in the block and once in the note; <sup> calls, [[ ]] and ^pg unchanged; every inserted run
# (difflib; whitespace and backslashes ignored) is a footnote number, occurs in the PDF page text (whitespace-blind), or is text
# moved from another of the case's olds; added text of 6+ characters that already stands elsewhere in the note (outside the block) is held (a
# move across pages, as Augustine 29's note 3391). Per case (a move may come as two edits, one of them marked "drops"): no non-space
# character dropped, otherwise the whole case is held for Stephen. Then, in the edited block only, a footnote number of the page
# standing in a paragraph of its own before its text is joined to it (whitespace only). Cases listed in lead/hold.txt are held.
# Writes notes-<tag>.json (accepted cases applied) and edits-<tag>.json ({path: [[old block, new block], ...]}).
# usage: py check_edits.py TAG c000-c019 [c025 ...] [--base notes-g1.json]
import json, re, sys, difflib, collections, os
tag = sys.argv[1]; ids = []
args = [a for a in sys.argv[2:] if not a.startswith('--')]
if '--base' in sys.argv: args.remove(sys.argv[sys.argv.index('--base') + 1])
for a in args:
    if '-' in a: x, y = a.split('-'); ids += ['c%03d' % i for i in range(int(x[1:]), int(y[1:]) + 1)]
    else: ids.append(a)
idx = {c['id']: c for c in json.load(open('cases.json', encoding='utf-8'))}
base = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else 'notes.json'
hold = dict(l.split(' ', 1) for l in open('lead/hold.txt', encoding='utf-8').read().splitlines() if l.strip()) if os.path.exists('lead/hold.txt') else {}
ids = [i for i in ids if i in idx]
NOTES = json.load(open(base, encoding='utf-8')); new = dict(NOTES)
acc = collections.defaultdict(list); rows = []
sq = lambda s: re.sub(r'[\s\\]', '', s)
import unicodedata
ak = lambda s: ''.join(c for c in unicodedata.normalize('NFD', sq(s)) if not unicodedata.combining(c))
def span(t, K):
    m = re.search(r'^\*\[[^\]]+\]\* \^pg%d\s*$' % K, t, re.M); m2 = re.search(r'^\*\[[^\]]+\]\* \^pg\d+\s*$', t[m.end():], re.M)
    return m.start(), (m.end() + m2.start() if m2 else len(t))
for cid in ids:
    c = idx[cid]; p = c['path']
    lf = f'lead/{cid}.json'   # the lead's own edits replace the reader's; "Ks" may span the block before (a move across pages)
    try: R = json.load(open(lf if os.path.exists(lf) else f'read/{cid}.json', encoding='utf-8-sig'))
    except Exception as e: rows.append((cid, 'NO/BAD OUTPUT', str(e)[:80])); continue
    Ks = R.get('Ks', [c['K']]); a, b = span(new[p], min(Ks))[0], span(new[p], max(Ks))[1]; blk = new[p][a:b]
    if os.path.exists(lf): R['status'] = 'lead'
    pdf = sq(open(f'cases/{cid}.pdf.txt', encoding='utf-8').read())
    E = R.get('edits', []); probs = []
    if cid in hold: probs.append('lead: ' + hold[cid])
    for e in E:
        o, n = e['old'], e['new']; why = []
        if blk.count(o) != 1: why.append(f'old in block {blk.count(o)}x')
        for k in ('<sup>', '^pg'):
            if o.count(k) != n.count(k): why.append('changes ' + k)
        for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, o, n, autojunk=False).get_opcodes():
            s2 = sq(n[b1:b2]) if op in ('insert', 'replace') else ''
            if s2 and not R.get('guard_ok') and not s2.isdigit() and s2 not in pdf and not any(s2 in sq(x['old']) for x in E): why.append('added text not in PDF: ' + s2[:40])
            for piece in re.split(r'\d+', s2):   # accent-blind, split at numbers (Chrysostom 1331 slipped past the first form, g4)
                if not R.get('guard_ok') and len(ak(piece)) >= 5 and not any(ak(piece) in ak(x['old']) for x in E) and ak(piece) in ak(new[p][:a] + ' ' + new[p][b:]): why.append('added text already in the note elsewhere (a move?): ' + piece[:40])
        if why: probs.append('; '.join(why) + ' | ' + o[:50])
    d = collections.Counter(sq(''.join(e['old'] for e in E))) - collections.Counter(sq(''.join(e['new'] for e in E)))
    for k in ('[[', ']]'):   # per case: a link may move with its note from one edit to another (c115)
        if sum(e['old'].count(k) for e in E) != sum(e['new'].count(k) for e in E): probs.append('changes ' + k)
    if d and R.get('undo_dup'): d = None   # the lead removes a copy that an earlier group of this session duplicated (logged)
    if d: probs.append('case drops ' + ''.join(d.elements())[:40])
    joins = 0
    if not probs:
        nb = blk
        for e in E: nb = nb.replace(e['old'], e['new'], 1)
        for j in c['nums']:
            nb, k = re.subn(r'(^|\n)(%d)\n\n(?=\S)' % j, r'\1\2 ', nb); joins += k
        if nb != blk:
            assert new[p].count(blk) == 1
            acc[p].append([blk, nb]); new[p] = new[p][:a] + nb + new[p][b:]
    rows.append((cid, R.get('status'), len(E), ('OK' if not probs else 'HELD: ' + ' || '.join(probs)) + (f' (+{joins} joins)' if joins else ''), R.get('note', '')[:110]))
json.dump(new, open(f'notes-{tag}.json', 'w', encoding='utf-8'), ensure_ascii=False)
json.dump({'edits': acc}, open(f'edits-{tag}.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('notes', len(acc), 'blocks', sum(len(v) for v in acc.values()))
for r in rows: print(*r, sep=' | ')
