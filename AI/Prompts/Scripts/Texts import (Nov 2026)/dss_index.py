"""dss_index.py (9 Nov 2026): the Study Edition's Index of Manuscripts (printed pp. 1311-1325) -> entries
[siglum, short, title, page]; and the English (odd) pages' text -> pages.json. Usage: python3 -I dss_index.py <pdf> <outdir>"""
import fitz, re, json, sys
d = fitz.open(sys.argv[1]); OUT = sys.argv[2]
OFF = 24
lines = []
for i in range(1311 + OFF, 1350 + OFF):
    t = d[i].get_text()
    if 'INDEX OF TITLES' in t: break
    lines += [l.strip() for l in t.split('\n')[1:] if l.strip() and l.strip() != 'INDEX OF MANUSCRIPTS']
ents = []; buf = ''
for l in lines:
    buf = (buf + ' ' + l).strip() if buf else l
    if buf.endswith('-') and not re.search(r'\s\d{1,4}$', buf): buf = buf[:-1]; continue
    m = re.match(r'^(.*?)\s+(\d{1,4})$', buf)
    if m: ents.append(m.group(1).strip()); ents[-1] = (m.group(1).strip(), int(m.group(2))); buf = ''
E = []
for s, p in ents:
    m = re.match(r'^(\S+(?: \+ \S+)?)(?: \(([^)]*)\))?\s+(.*)$', s)
    E.append({'siglum': m.group(1), 'short': m.group(2) or '', 'title': m.group(3).strip(), 'page': p} if m else {'raw': s, 'page': p})
json.dump(E, open(OUT + '/index.json', 'w'), ensure_ascii=False, indent=0)
pages = {}
for i in range(OFF, d.page_count):
    t = d[i].get_text(); first = t.split('\n', 1)[0].strip()
    if first.isdigit() and int(first) % 2 == 1: pages[int(first)] = t
json.dump(pages, open(OUT + '/pages.json', 'w'), ensure_ascii=False)
print(len(E), sum(1 for e in E if 'raw' in e), len(pages), E[:3], E[-3:])
