import json, re, collections, os
exec(open('seg.py').read().split("# ---- find each unit")[0])
units = json.load(open('units-pos.json'))
ROMAN = {1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI',7:'VII',8:'VIII',9:'IX',10:'X',11:'XI'}
# uid -> vault verses
u2v = collections.defaultdict(list)
for vid, v in vf.items():
    for x in v['units']: u2v[str(x)].append(vid)
def vlabel(vids):
    vids = sorted(set(vids), key=lambda s: (int(s.split('.')[0]), int(s.split('.')[1])))
    a, b = vids[0], vids[-1]
    ca, va = int(a.split('.')[0]), int(a.split('.')[1]); cb, vb = int(b.split('.')[0]), int(b.split('.')[1])
    if a == b: return f'{ca}.{va}'
    if ca == cb: return f'{ca}.{va}–{vb}'
    return f'{ca}.{va}–{cb}.{vb}'
order = sorted(NOTES)
seq = []      # all units in reading order
for name in order:
    for u in sorted([u for u in units if u['note'] == name], key=lambda u: u['ps']): seq.append(u)
# labels
for u in seq:
    vids = [v for x in (u['uid'] or []) for v in u2v.get(str(x), [])]
    if vids: u['label'] = 'TĀ ' + vlabel(vids)
    else:
        mk = dz.TAIL.search(NOTES[u['note']]['paras'][u['pe']]['text'])
        m = (mk.group(2) or mk.group(1)) if mk else None
        u['label'] = f"Dyczkowski's verse {dz.fix_marker(m)}" if m else f"Unit {u['ps']}"
# headings per note, unique
inserts = collections.defaultdict(list)   # note -> [(paragraph index, heading line)]
used = collections.defaultdict(set)
def uniq(name, h):
    k, n = h, 2
    while k in used[name]: k = f'{h} ({n})'; n += 1
    used[name].add(k); return k
for i, u in enumerate(seq):
    name = u['note']; ps = NOTES[name]['paras']
    u['h_unit'] = uniq(name, u['label'])
    inserts[name].append((u['pv'], '### ' + u['h_unit']))
    if u['ce'] >= u['cs']:
        u['h_viv'] = uniq(name, 'Viveka on ' + u['label'].replace('TĀ ', ''))
        inserts[name].append((u['cs'], '#### ' + u['h_viv']))
    else: u['h_viv'] = None
    # continuation at the top of the next note, when the next note starts with commentary prose before its first unit
    nxt = seq[i + 1] if i + 1 < len(seq) else None
    if nxt and nxt['note'] != name:
        nps = NOTES[nxt['note']]['paras']
        first = next((k for k, p in enumerate(nps) if p['kind'] not in ('nav',)), None)
        if first is not None and first < nxt['pv'] and any(p['kind'] == 'prose' for p in nps[first:nxt['pv']]):
            u['h_cont'] = (nxt['note'], uniq(nxt['note'], 'Viveka on ' + u['label'].replace('TĀ ', '') + ' (continued)'))
            inserts[nxt['note']].append((first, '#### ' + u['h_cont'][1]))
def prose_chars(name, a, b):
    ps = NOTES[name]['paras']; return sum(len(ps[k]['text']) for k in range(a, b + 1) if ps[k]['kind'] == 'prose')
for u in seq:
    u['has'] = (u['ce'] >= u['cs'] and prose_chars(u['note'], u['cs'], u['ce']) > 0) or bool(u.get('h_cont'))
def page_label(name, k):
    ps = NOTES[name]['paras']
    for j in range(min(k, len(ps) - 1), -1, -1):
        if ps[j]['kind'] == 'page': return ps[j]['label']
    return None
def vol_of(name): return int(re.search(r'v(\d\d) ', name).group(1))
# 2. the verse-note callouts
pos = {id(u): i for i, u in enumerate(seq)}
byuid = {}
for u in seq:
    for x in (u['uid'] or []): byuid[str(x)] = u
callouts = {}; stats = collections.Counter()
for vid, v in vf.items():
    us = []
    for x in v['units']:
        u = byuid.get(str(x))
        if u and u not in us: us.append(u)
    if not us: stats['no unit'] += 1; continue
    secs = []   # (embed link, label of the unit whose commentary it is, pages)
    for u in us:
        w = u; hops = 0
        while not w['has'] and hops < 3 and pos[id(w)] + 1 < len(seq):
            w = seq[pos[id(w)] + 1]; hops += 1
        if not w['has']: continue
        name = w['note']
        if w['h_viv']: secs.append((f"{name}#{w['h_viv']}", w, page_label(name, w['cs']), page_label(name, w['ce']), hops))
        if w.get('h_cont'):
            n2, h2 = w['h_cont']; secs.append((f"{n2}#{h2}", w, None, None, hops))
    seen = set(); secs = [s for s in secs if not (s[0] in seen or seen.add(s[0]))]
    if not secs: stats['no commentary'] += 1; continue
    pages = [p for s in secs for p in (s[2], s[3]) if p]
    vol = ROMAN[vol_of(secs[0][1]['note'])]
    pr = (f'p. {pages[0]}' if pages[0] == pages[-1] else f'pp. {pages[0]}–{pages[-1]}') if pages else ''
    after = [s for s in secs if s[4] > 0]
    title = f"Viveka in English (Dyczkowski, vol. {vol}{', ' + pr if pr else ''})"
    lines = [f"> [!viveka]- {title}"]
    if after:
        lines.append(f"> *Dyczkowski gives the commentary on these verses together, after {after[0][1]['label']}.*")
        lines.append('>')
    for k, s in enumerate(secs):
        if k: lines.append('>')
        lines.append(f"> ![[{s[0]}]]")
    callouts[v['path']] = '\n'.join(lines)
    stats['callout'] += 1; stats['after' if after else 'own'] += 1; stats[f'{len(secs)} sections'] += 1
print(stats)
# library inserts as offsets with a check prefix
lib = []
for name, ins in inserts.items():
    n = NOTES[name]; raw = n['raw']; ps = n['paras']
    def u16(i): return len(raw[:i].encode('utf-16-le')) // 2
    items = sorted({(raw.rfind('\n', 0, ps[k]['pos']) + 1, h) for k, h in ins}, key=lambda t: t[0])
    lib.append({'path': 'Library/Trika/Tantraloka (Dyczkowski)/' + os.path.relpath(n['path'], 'lib'), 'len': u16(len(raw)),
                'ins': [[u16(o), h, raw[o:o + 24]] for o, h in items]})
json.dump(lib, open('lib-inserts.json', 'w'), ensure_ascii=False)
json.dump(callouts, open('verse-callouts.json', 'w'), ensure_ascii=False)
json.dump([{k: u.get(k) for k in ('note', 'label', 'h_unit', 'h_viv', 'pv', 'ps', 'pe', 'cs', 'ce', 'uid', 'has')} for u in seq], open('seq.json', 'w'), ensure_ascii=False)
print('notes', len(lib), 'headings', sum(len(x['ins']) for x in lib))
