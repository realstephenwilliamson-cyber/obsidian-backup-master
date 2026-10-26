# Container paths (/home/claude/dz/...) are those of the 26 Oct 2026 session; adjust before reuse.
# Whole-volume comparison of the old and new text layers (whitespace ignored): what the new layer deletes and inserts.
import pymupdf, re, sys, json, difflib, collections
v = sys.argv[1]; name = f'Dyczkowski - Tantraloka, vol. {v}.pdf'
old = pymupdf.open('/home/claude/dz/pdf/' + name); new = pymupdf.open(f'/home/claude/dz/rb/v{v}.fixed.pdf')
dele = collections.Counter(); ins = collections.Counter(); pages = 0; deva_del = 0; ex = []
for i in range(len(old)):
    a = re.sub(r'\s+', '', old[i].get_text()); b = re.sub(r'\s+', '', new[i].get_text())
    if a == b: continue
    pages += 1
    for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if t == 'equal': continue
        for c in a[i1:i2]: dele[c] += 1
        for c in b[j1:j2]: ins[c] += 1
        d = a[i1:i2]
        if re.search('[क-हअ-औ]', d) or (b[j1:j2] and b[j1:j2] != '™'):
            if len(ex) < 8: ex.append((i + 1, t, d[:20], b[j1:j2][:20]))
print(json.dumps(dict(vol=v, pages_changed=pages, deleted=sum(dele.values()), inserted=sum(ins.values()),
    deleted_deva_letters=sum(n for c, n in dele.items() if 'क' <= c <= 'ह' or 'अ' <= c <= 'औ'),
    inserted_chars=dict(ins.most_common(10)), top_deleted=dict(dele.most_common(12)), examples=ex), ensure_ascii=False))
