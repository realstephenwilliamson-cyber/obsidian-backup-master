# run_pinned.py — saved 28 Oct 2026 (sixth session). Usage: python3 run_pinned.py VAULT_DIR HELD_JSON OUT_JSON
# (VAULT_DIR: a folder holding the staged notes at their vault paths; HELD_JSON: .work/edits/pagelabels-2026-10-28b/held-after-A.json or a later held list in the same form).
# Its output lists each held entry with keep true/false and why; the kept fills still need the full pages read blind (page-number-fullpage-brief.txt) before a spec is made.
# run_pinned.py (28 Oct 2026, sixth session): which held page-label edits (held-after-A.json) the note's own run fixes exactly.
# Rule (Stephen, 28 Oct 2026, 15:5x): a page that prints no number takes the run's number only where printed pages on both sides
# fix it exactly: the nearest [p. X] markers before and after it in the same note, of the same kind (arabic or roman), have
# X_after - X_before == K_after - K_before, so X = X_before + (K - K_before). Anything less certain stays [PDF K].
# A fill is kept when its marker is still [PDF K] in the note, its reading was not 'diff' or 'unclear', and the run gives the held 'new'.
# A range or index label is kept when, after the kept fills, the note's first and last markers are [p. ...], give exactly the held 'new',
# and each end is fixed: its page was read 'ok' by the blind readers, or it is a fill kept by the run rule above.
import json, re, sys, os, collections
VAULT, HELD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
R = {'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000}
def rom2int(s):
    s=s.lower()
    if not s or any(ch not in R for ch in s): return None
    t=0
    for i,ch in enumerate(s):
        v=R[ch]; t += -v if i+1<len(s) and R[s[i+1]]>v else v
    return t if int2rom(t)==s else None
def int2rom(n):
    out=''
    for v,s in [(1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),(90,'xc'),(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
        while n>=v: out+=s; n-=v
    return out
def val(lab):
    if re.fullmatch(r'\d+',lab): return ('a',int(lab))
    r=rom2int(lab)
    if r: return ('r',r,lab.isupper())
    return None
MK=re.compile(r'^\*\[(p\.|PDF) ([^\]]+)\]\* \^pg(\d+)\s*$')
def markers(text):
    out=[]
    for i,l in enumerate(text.split('\n')):
        m=MK.match(l)
        if m: out.append(dict(line=i+1,kind=m.group(1),lab=m.group(2),k=int(m.group(3)),text=l))
    return out
def pinned(ms, idx):
    k=ms[idx]['k']
    b=next((m for m in reversed(ms[:idx]) if m['kind']=='p.' and val(m['lab'])),None)
    a=next((m for m in ms[idx+1:] if m['kind']=='p.' and val(m['lab'])),None)
    if not a or not b: return None,'no printed page on one side'
    vb,va=val(b['lab']),val(a['lab'])
    if vb[0]!=va[0]: return None,'arabic on one side, roman on the other'
    if va[1]-vb[1]!=a['k']-b['k']: return None,f"run broken between PDF {b['k']} ({b['lab']}) and PDF {a['k']} ({a['lab']})"
    n=vb[1]+(k-b['k'])
    if vb[0]=='a': return str(n),f"PDF {b['k']}={b['lab']}, PDF {a['k']}={a['lab']}"
    s=int2rom(n); return (s.upper() if vb[2] else s),f"PDF {b['k']}={b['lab']}, PDF {a['k']}={a['lab']}"
held=json.load(open(HELD,encoding='utf-8'))
texts={}
def T(p):
    if p not in texts:
        fp=os.path.join(VAULT,p); texts[p]=open(fp,encoding='utf-8').read() if os.path.exists(fp) else None
    return texts[p]
res=[]; fillnew={}  # (note, k) -> label kept
for i,h in enumerate(held):
    if h['kind']!='fill': continue
    t=T(h['path']); r=dict(i=i,kind='fill',path=h['path'],old=h['old'],new=h['new'])
    if t is None: r.update(keep=False,why='note not staged'); res.append(r); continue
    if t.count(h['old'])!=1: r.update(keep=False,why='old text no longer in the note (done earlier?)'); res.append(r); continue
    ms=markers(t); idx=next((j for j,m in enumerate(ms) if m['text'].strip()==h['old']),None)
    if h['status'].get('self') in ('diff','unclear'): r.update(keep=False,why='reading of the page: '+h['status']['self']); res.append(r); continue
    lab,why=pinned(ms,idx)
    want=re.match(r'\*\[p\. ([^\]]+)\]',h['new']).group(1)
    if lab is None: r.update(keep=False,why=why)
    elif lab!=want: r.update(keep=False,why=f'run gives {lab}, held edit says {want} ({why})')
    else: r.update(keep=True,why=why); fillnew[(h['path'],ms[idx]['k'])]=lab
    res.append(r)
def rng(h):
    m=re.search(r'(\d+|[ivxlcdmIVXLCDM]+)–(\d+|[ivxlcdmIVXLCDM]+)',h['new'].split('(pp. ')[-1] if h['kind']=='label' else h['new'])
    return m.group(1),m.group(2)
for i,h in enumerate(held):
    if h['kind']=='fill': continue
    r=dict(i=i,kind=h['kind'],path=h['path'],old=h['old'],new=h['new'])
    t=T(h['path'])
    if t is None: r.update(keep=False,why='note not staged'); res.append(r); continue
    if t.count(h['old'])!=1: r.update(keep=False,why='old text no longer in the note (done earlier?)'); res.append(r); continue
    note=h['deps'][0][0]; tn=T(note)
    if tn is None: r.update(keep=False,why='section note not staged'); res.append(r); continue
    ms=markers(tn)
    def lab_of(m):
        if m['kind']=='p.': return m['lab']
        return fillnew.get((note,m['k']))
    f,l=lab_of(ms[0]),lab_of(ms[-1])
    try: a,b=rng(h)
    except Exception: r.update(keep=False,why='cannot read the held range'); res.append(r); continue
    if f is None or l is None: r.update(keep=False,why=f"first or last page of the note not numbered (PDF {ms[0]['k']} {ms[0]['lab']}, PDF {ms[-1]['k']} {ms[-1]['lab']})")
    elif (f,l)!=(a,b): r.update(keep=False,why=f'note runs {f}–{l}, held edit says {a}–{b}')
    elif not ((h['status'].get('first')=='ok' or (note,ms[0]['k']) in fillnew) and (h['status'].get('last')=='ok' or (note,ms[-1]['k']) in fillnew)):
        r.update(keep=False,why=f"an end is not fixed (first {h['status'].get('first')}, last {h['status'].get('last')})")
    else: r.update(keep=True,why=f'note runs {f}–{l}')
    res.append(r)
res.sort(key=lambda r:r['i'])
json.dump(res,open(OUT,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
c=collections.Counter((r['kind'],r['keep']) for r in res); print(c)
w=collections.Counter(re.sub(r'\d+|[ivxlcdm]+\b','#',r['why'])[:70] for r in res if not r['keep']); print(w.most_common(12))
