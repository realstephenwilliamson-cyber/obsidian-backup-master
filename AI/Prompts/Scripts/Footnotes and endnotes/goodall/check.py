import fitz, json, re, collections, glob, sys
doc = fitz.open("/mnt/user-data/uploads/Obsidian Vault/Library/Hinduism/Saivism and the Tantric Traditions.pdf")
OUT = sys.argv[1] if len(sys.argv) > 1 else "out/Library/Hinduism/Saivism and the Tantric Traditions (Goodall)"
exp = {}
for i in range(len(doc)):
    d = doc[i].get_text('dict'); starts = []
    for b in d['blocks']:
        if b.get('type')!=0: continue
        for l in b['lines']:
            sp = [s for s in l['spans'] if s['text'].strip()]
            if not sp: continue
            t = sp[0]['text'].strip()
            if abs(sp[0]['size']-9.0)<0.3 and l['bbox'][1] > 100 and sp[0]['bbox'][0] < 62 and re.match(r'^\d{1,3}(\s|$)', t):
                starts.append(re.match(r'^\d{1,3}', t).group(0))
    exp[i] = starts
tot = sum(len(v) for v in exp.values())
print("expected note starts (margin numbers at 9pt):", tot)
found = collections.defaultdict(list); unref = collections.defaultdict(list)
for f in glob.glob(OUT + "/*.md"):
    cur = None
    for line in open(f, encoding='utf-8'):
        m = re.match(r'^\*\[(?:p\. |PDF )([^\]]+)\]\* \^pg(\d+)', line)
        if m: cur = int(m.group(2)); continue
        m = re.match(r'^\[\^([^\]]+)\]: ', line)
        if m and cur: found[cur].append(m.group(1)); continue
        m = re.match(r'^(\d{1,3})\\\. ', line)
        if m and cur: found[cur].append(m.group(1)+'?'); unref[cur].append(m.group(1))
diff = []
for i in exp:
    e = exp[i]; f = found.get(i+1, [])
    if len(e) != len(f): diff.append((i+1, e, f))
print("notes found:", sum(len(v) for v in found.values()), "pages where the count differs:", len(diff))
for d in diff: print("  ", d)
print("unreferenced:", sum(len(v) for v in unref.values()), dict(unref))
