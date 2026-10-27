# linkitems.py (26 Oct 2026, fourth session): link chosen Zohar references (rows of noblock.json or undecided.json, with a decided
# target) and write a linepatch2 spec. Used for Stephen's decisions of 26 Oct 21:20: the 44 folios with a Sefaria folio note and the
# 104 references whose named composition's note lacks the folio.
# usage: python3 -I linkitems.py ITEMS.json NOTES.json META.json FOLIONOTES.json OUTDIR
#   ITEMS.json   [{path, line, block, label, note, block_target}]  note = target note name; block_target = block id or null (link to the note)
#   NOTES.json   {vault path: text} as the notes are now
#   META.json    {"blocks": {note path: [block ids]}} as they are now (for Pritzker targets)
#   FOLIONOTES   a list of folio note paths (Sefaria), for targets without a block
# Each item is found by parsing its line with zoharlink.parse_line (same block and label, not already inside a link; several items
# with the same block and label on one line must match as many references, all with the same target); the link form and
# the label follow link_note (the word "Zohar" joins the label where the note's links carry it; `\|` in tables). The spec is refused if a
# line differs, an item is not found, a target does not exist, or the plain text would change. Lines holding the divine name go by offset.
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zoharlink as Z
from mkpatch import fnv, u16, LINK


def main():
    items_f, notes_f, meta_f, fol_f, outdir = sys.argv[1:6]
    items = json.load(open(items_f, encoding='utf-8')); F = json.load(open(notes_f, encoding='utf-8'))
    blocks = json.load(open(meta_f, encoding='utf-8'))['blocks']
    pritzker = {p.rsplit('/', 1)[-1][:-3]: set(b) for p, b in blocks.items()}
    folio = {p.rsplit('/', 1)[-1][:-3] for p in json.load(open(fol_f, encoding='utf-8'))}
    by = {}
    for it in items: by.setdefault(it['path'], {}).setdefault(it['line'], []).append(it)
    spec, probs, n = {}, [], 0
    for path, lines in by.items():
        t = F[path]; L = t.split('\n'); L2 = list(L); style = Z.label_style(t); changes, offs = [], []
        for ln, its in lines.items():
            line = L[ln - 1]; refs = [r for run in Z.parse_line(line) for r in run]
            is_table = line.lstrip().startswith('|'); pipe = '\\|' if is_table else '|'; edits = []
            groups = {}
            for it in its: groups.setdefault((it['block'], it['label']), []).append(it)
            pairs = []
            for (bk, lab), g in groups.items():
                cand = [r for r in refs if r.block == bk and r.label == lab and not r.inlink and not r.incode]
                if len(cand) != len(g) or len({(x['note'], x.get('block_target')) for x in g}) != 1:
                    probs.append(('found %d for %d' % (len(cand), len(g)), path, ln, lab)); continue
                pairs += list(zip(g, cand))
            for it, r in pairs:
                note, blk = it['note'], it.get('block_target')
                if blk and blk not in pritzker.get(note, ()): probs.append(('no such block', note, blk)); continue
                if not blk and note not in pritzker and note not in folio: probs.append(('no such note', note)); continue
                label, rs = r.label, r.rstart
                if r.first and not r.intro_italic and style == 'intro': label, rs = line[r.intro_rstart:r.rend], r.intro_rstart
                edits.append((rs, r.rend, '[[%s%s%s%s]]' % (note, '#^' + blk if blk else '', pipe, label)))
            if not edits: continue
            edits.sort(); s2 = line
            if any(edits[i][0] < edits[i - 1][1] for i in range(1, len(edits))): probs.append(('overlap', path, ln)); continue
            for a, b, rep in reversed(edits): s2 = s2[:a] + rep + s2[b:]
            red = s2
            for m in reversed(list(LINK.finditer(s2))):
                if m.group(0) in [x[2] for x in edits]: red = red[:m.start()] + m.group(2) + red[m.end():]
            if red != line: probs.append(('plain differs', path, ln)); continue
            L2[ln - 1] = s2; n += len(edits)
            if Z.holds_divine_name(line): offs.append({'line': ln, 'len': u16(line), 'hash': fnv(line), 'edits': [[a, b, rep] for a, b, rep in edits]})
            else: changes.append([ln, line, s2])
        new = '\n'.join(L2)
        if new != t: spec[path] = {'oldLen': u16(t), 'oldHash': fnv(t), 'newLen': u16(new), 'newHash': fnv(new), 'changes': changes, 'offsets': offs}
    if probs:
        print('NOT WRITTEN:', len(probs)); [print(' ', p) for p in probs[:50]]; sys.exit(1)
    raw = json.dumps(spec, ensure_ascii=False)
    if Z.DIVINE_NAME_RE.search(raw): print('NOT WRITTEN: divine name in the spec'); sys.exit(1)
    os.makedirs(outdir, exist_ok=True)
    open(os.path.join(outdir, 'part01.json'), 'w', encoding='utf-8').write(raw)
    print('%d notes, %d lines, %d links' % (len(spec), sum(len(s['changes']) + len(s['offsets']) for s in spec.values()), n))


if __name__ == '__main__':
    main()
