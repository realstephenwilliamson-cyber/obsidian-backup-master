# mkspec.py (27 Oct 2026, Dyczkowski footnotes night 1): builds a whole-note spec for .work/edits/textpatch.tpl.js.
# Usage: mkspec.py OUT.json VAULTPATH ORIGFILE NEWFILE [VAULTPATH ORIGFILE NEWFILE ...]
# ORIGFILE = the note as freshly staged from the vault (the job refuses a note whose text no longer has oldLen/oldHash).
import sys, json
def u16(s): b = s.encode('utf-16-le'); return [b[i] | (b[i + 1] << 8) for i in range(0, len(b), 2)]
def fnv(s):
    h = 0x811c9dc5
    for c in u16(s): h ^= c; h = (h * 0x01000193) & 0xffffffff
    return h
out = sys.argv[1]; a = sys.argv[2:]; spec = {}
for i in range(0, len(a), 3):
    vp, of, nf = a[i:i + 3]
    o = open(of, encoding='utf-8', newline='').read(); n = open(nf, encoding='utf-8', newline='').read()
    spec[vp] = {'oldLen': len(u16(o)), 'oldHash': fnv(o), 'newLen': len(u16(n)), 'newHash': fnv(n), 'newText': n}
json.dump(spec, open(out, 'w', encoding='utf-8'), ensure_ascii=False)
print(out, len(spec), 'notes')
