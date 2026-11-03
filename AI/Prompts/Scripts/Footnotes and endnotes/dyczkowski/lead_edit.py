# lead_edit.py ID JSON_EDITS (2 Nov 2026, night 3): the lead's change to a reader's ops.json. JSON_EDITS is a list of
# {"match": {op fields to match}, "set": {fields to set}} or {"add": {new op}}; each changed or added op gets "by": "lead",
# and the reason goes into the file's "lead" list.
import sys, json
nid, edits, why = sys.argv[1], json.loads(sys.argv[2]), sys.argv[3]
f = f'/home/claude/dyfn/rd/{nid}/ops.json'; D = json.load(open(f, encoding='utf-8'))
for e in edits:
    if 'add' in e: o = dict(e['add']); o['by'] = 'lead'; D['ops'].append(o); continue
    hits = [o for o in D['ops'] if all(o.get(k) == v for k, v in e['match'].items())]
    if len(hits) != 1: sys.exit(f'{len(hits)} ops match {e["match"]}')
    hits[0].update(e['set']); hits[0]['by'] = 'lead'
D.setdefault('lead', []).append(why)
json.dump(D, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(nid, 'ok', len(D['ops']), 'ops')
