# mkpatch.py (26 Oct 2026, third session): turn the linker's proposals.json into a linepatch2 spec for the job runner.
# usage: python3 -I mkpatch.py PROPOSALS.json NOTES.json META.json OUTDIR [PER_PART]
#   PROPOSALS.json  run_cur.py's output, built on NOTES.json
#   NOTES.json      {vault path: full note text} as the notes are NOW (a fresh read-only bundle; re-run run_cur.py first if any note changed)
#   META.json       the bundle's meta.json ("blocks": {note path: [block ids]}), to check every new link resolves
#   OUTDIR          receives part01.json, part02.json, ... (default 40 notes each): {path: {oldLen, oldHash, newLen, newHash,
#                   changes: [[line, oldLine, newLine]], offsets: [{line, len, hash, edits: [[start, end, replacement]]}]}}
# Copy OUTDIR to .work/edits/<NAME>/ and make the jobs with mkjob.py from .work/edits/linepatch2.tpl.js (dry run first).
# Lengths and hashes are FNV-1a over UTF-16 code units, as the job computes them. Lines holding the divine name come as offsets only,
# so the name is never written into the spec; the script refuses to write a spec that holds it.
# Checks before writing: each oldLine equals the note's line; the result, with every new link reduced to its label, equals the old
# line; every new link's note and block exist in META.json.
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zoharlink as Z

def fnv(s):
    h = 0x811c9dc5; b = s.encode('utf-16-le')
    for i in range(0, len(b), 2):
        h ^= b[i] | (b[i + 1] << 8); h = (h * 0x01000193) & 0xffffffff
    return h

def u16(s): return len(s.encode('utf-16-le')) // 2

LINK = re.compile(r'\[\[([^\]|\\]+?)(?:\\?\|)([^\]]+?)\]\]')

def main():
    prop_f, notes_f, meta_f, outdir = sys.argv[1:5]
    per = int(sys.argv[5]) if len(sys.argv) > 5 else 40
    P = json.load(open(prop_f, encoding='utf-8')); F = json.load(open(notes_f, encoding='utf-8'))
    blocks = json.load(open(meta_f, encoding='utf-8'))['blocks']
    names = {p.rsplit('/', 1)[-1][:-3]: p for p in blocks}
    spec, probs, nlinks = {}, [], 0
    for p, v in P.items():
        t = F[p]; L = t.split('\n'); L2 = list(L)
        for ln, old, new in v.get('changes', []):
            if L[ln - 1] != old: probs.append(('old line differs', p, ln)); continue
            if Z.holds_divine_name(old) or Z.holds_divine_name(new): probs.append(('divine name in a whole line', p, ln)); continue
            L2[ln - 1] = new
        offs = []
        for o in v.get('changes_by_offset', []):
            s = L[o['line'] - 1]; s2 = s
            for a, b, r in sorted(o['edits'], key=lambda e: -e[0]):
                if Z.holds_divine_name(r): probs.append(('divine name in a replacement', p, o['line']))
                s2 = s2[:a] + r + s2[b:]
            L2[o['line'] - 1] = s2
            offs.append({'line': o['line'], 'len': u16(s), 'hash': fnv(s), 'edits': o['edits']})
        new = '\n'.join(L2)
        for i, (a, b) in enumerate(zip(L, L2)):
            if a == b: continue
            olds = [m.group(0) for m in LINK.finditer(a)]; j = 0; added = []
            for m in LINK.finditer(b):
                if j < len(olds) and m.group(0) == olds[j]: j += 1; continue
                added.append(m)
            red = b
            for m in reversed(added):
                note, _, blk = m.group(1).partition('#^')
                if note not in names or blk not in blocks[names[note]]: probs.append(('unresolved', p, i + 1, m.group(1)))
                red = red[:m.start()] + m.group(2) + red[m.end():]; nlinks += 1
            if red != a: probs.append(('plain text differs', p, i + 1))
        spec[p] = {'oldLen': u16(t), 'oldHash': fnv(t), 'newLen': u16(new), 'newHash': fnv(new),
                   'changes': v.get('changes', []), 'offsets': offs}
    if probs:
        print('NOT WRITTEN:', len(probs), 'problems'); [print(' ', x) for x in probs[:40]]; sys.exit(1)
    raw = json.dumps(spec, ensure_ascii=False)
    if Z.DIVINE_NAME_RE.search(raw): print('NOT WRITTEN: the spec would hold the divine name'); sys.exit(1)
    os.makedirs(outdir, exist_ok=True); keys = sorted(spec)
    for i in range(0, len(keys), per):
        part = {k: spec[k] for k in keys[i:i + per]}
        open(os.path.join(outdir, 'part%02d.json' % (i // per + 1)), 'w', encoding='utf-8').write(json.dumps(part, ensure_ascii=False))
    print('%d notes, %d lines, %d new links; %d parts in %s' % (len(spec), sum(len(s['changes']) + len(s['offsets']) for s in spec.values()), nlinks, (len(keys) + per - 1) // per, outdir))

if __name__ == '__main__':
    main()
