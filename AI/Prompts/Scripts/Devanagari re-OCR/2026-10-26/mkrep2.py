# Container paths (/home/claude/dz/...) are those of the 26 Oct 2026 session; adjust before reuse.
# Build dzrep.json from post.json (fixed copies) for the given volume keys, e.g. v01 v02
import json, sys
post = json.load(open('/home/claude/dz/rb/post.json')); want = set(sys.argv[1:]); L = []
for name, r in sorted(post.items()):
    key = name.replace('Dyczkowski - Tantraloka, vol. ', 'v').replace('.pdf', '')
    if key not in want: continue
    b, a = r['before'], r['after']
    line = (f"**Text layer** (26 Oct 2026, decision 7): the OCR text layer of the {r['ocr_pages']} pages that had a stray glyph after the vowel sign ि was redone "
            f"(OCRmyPDF --redo-ocr, sandwich renderer, Tesseract's Latin-script and Sanskrit models), and the look-alike letters the Latin model writes (ş, ņ, ț, ı and the like) "
            f"were changed to the IAST letters (ṣ, ṇ, ṭ, i); the page images are unchanged. Stray glyphs after ि: {b['junk']:,} before, {a['junk']:,} now; "
            f"letters with IAST marks: {r['old']['iast']:,} before, {r['new']['iast']:,} now; Devanagari letters read into English lines: {b['deva_in_latin']:,} before, {a['deva_in_latin']:,} now.")
    L.append(dict(target='Library/Trika/Dyczkowski - Tantraloka translation/' + name, parts=r['parts'], size=r['size'], sha256=r['sha256'], old_size=r['old_size'], old_sha256=r['old_sha256'], line=line))
json.dump(L, open('/mnt/user-data/outputs/work/dzrep.json', 'w'), ensure_ascii=False, indent=0)
print(len(L), 'entries'); [print(' ', x['target'].split('/')[-1], x['parts'], x['size'], x['line'][-200:]) for x in L]
