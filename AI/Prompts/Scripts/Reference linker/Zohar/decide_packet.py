# decide_packet.py (26 Oct 2026, fifth session): build a reading packet for Zohar references the linker could not decide
# (rows of undecided.json or noblock.json): for each, the start of the citing line, the text around the reference, and for each
# candidate note the paragraphs around its block, so that a reader (an agent) can decide which passage the reference means.
# usage: python3 -I decide_packet.py VAULT_ROOT ITEMS.json OUT.md
#   ITEMS.json  [{id, path, line, label, block, why, candidates?}]  candidates = note numbers ("4.06"); if absent, taken from
#               "held by 4.06, 4.07" in `why`. A candidate may carry its own block as "11.08@z1-108a".
# Used on 26 Oct 2026 for the 37 undecided references and the seven "1:108a (ST)" ones (decisions in
# .work/edits/zohar-open-2026-10-26/undecided-decisions.json, blind check undecided-check44.json); links made with linkitems.py.
# The packet quotes source texts; tell the reader not to write the divine name.
import sys, json, re, glob, os
root, items_f, out_f = sys.argv[1:4]
root = root.rstrip('/') + '/'
items = json.load(open(items_f, encoding='utf-8'))
allz = {os.path.basename(p)[:-3]: p for p in glob.glob(root + 'Texts/Zohar/*/*.md')}
def note_by_num(num):
    m = [k for k in allz if k.startswith('Zohar ' + num + ' - ')]
    return m[0] if len(m) == 1 else None
cache = {}
def lines(p):
    if p not in cache: cache[p] = open(p, encoding='utf-8').read().split('\n')
    return cache[p]
out = ['# Zohar references to decide\n']
for it in items:
    L = lines(root + it['path']); line = L[it['line'] - 1]; lab = it['label']
    pos = line.find(lab)
    out.append(f"\n## {it['id']} — {os.path.basename(it['path'])[:-3]}, line {it['line']}\n\nReference as printed: `{lab}`; block `{it['block']}`; linker: {it.get('why','')}\n\nStart of the citing line:\n\n> {line[:250]}\n\nAround the reference (marked ⟦ ⟧):\n\n> "
               + (line[max(0, pos - 700):pos] + '⟦' + lab + '⟧' + line[pos + len(lab):pos + len(lab) + 300] if pos >= 0 else '(label not found on the line)') + '\n')
    cands = it.get('candidates') or ([h.strip() for h in re.findall(r'held by ([0-9., ]+);', it.get('why', ''))[0].split(',')] if 'held by' in it.get('why', '') else [])
    for c in cands:
        num, _, blk = c.partition('@'); blk = blk or it['block']; nn = note_by_num(num)
        if not nn: out.append(f"\n### candidate {num}: note not found\n"); continue
        HL = lines(allz[nn]); bi = [i for i, x in enumerate(HL) if re.search(r'\^' + re.escape(blk) + r'\s*$', x)]
        out.append(f"\n### candidate {num}: `{nn}`, block `^{blk}` " + (f"at line {bi[0] + 1}" if bi else "NOT PRESENT") + "\n")
        if bi:
            i = bi[0]; a = i; n = 0
            while a > 0 and n < 2:
                a -= 1; n += bool(HL[a].strip())
            b = i; n = 0
            while b < len(HL) - 1 and n < 4:
                b += 1; n += bool(HL[b].strip())
            out.append("\n```text\n" + '\n'.join(x for x in HL[a:b + 1] if x.strip())[:4500] + "\n```\n")
open(out_f, 'w', encoding='utf-8').write(''.join(out))
print(len(items), 'items ->', out_f)
