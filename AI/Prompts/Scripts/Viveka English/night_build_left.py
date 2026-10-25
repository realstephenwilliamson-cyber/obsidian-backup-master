# The ~190 leftovers, 23 Oct 2026, late (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for crops.py, the sheets and the reads; the current text rebuilt from .work/pe-proof5/lib-bundle.json plus the night patches.
# The ~190 leftovers (23 Oct 2026, late): apply the page readings of the items placed by their neighbours.
import json,glob,sys,unicodedata,collections,re,pickle
from slips_common import PFX
NFC=lambda s: unicodedata.normalize("NFC",s)
def strip(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch))
def lev(a,b):
    d=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        p,d[0]=d[0],i
        for j,y in enumerate(b,1): p,d[j]=d[j],min(d[j]+1,d[j-1]+1,p+(x!=y))
    return d[-1]
def u16(s): return len(s)+sum(1 for ch in s if ord(ch)>0xFFFF)
def fnv(s):
    h=0x811c9dc5; b=s.encode("utf-16-le")
    for i in range(0,len(b),2): h^=b[i]|(b[i+1]<<8); h=(h*0x01000193)&0xFFFFFFFF
    return h
T3=pickle.load(open("T3.pkl","rb"))
reads={}
for f in sorted(glob.glob("/home/claude/pf/read2/L-*.jsonl")):
    for l in open(f,encoding="utf-8"):
        l=l.strip()
        if l:
            try: r=json.loads(l); reads[r["id"]]=r
            except Exception: pass
c=collections.defaultdict(collections.Counter); edits=[]; ex=collections.defaultdict(list)
for x in json.load(open("l190.json")):
    k=x["src"]; r=reads.get(x["id"]); w=x["w"]
    if not r: c[k]["unread"]+=1; continue
    p0=NFC((r.get("printed") or "").strip()); note=(r.get("note") or "").lower()
    p=p0.strip("-–()[];:,.'’‘\"> !?|“”")
    if r.get("conf")!="high" or not p or "wrong" in note or p0.endswith(("-","–")) or not re.fullmatch(r"[^\W\d_]+",p): c[k]["unclear"]+=1; ex[k+" unclear"].append((x["id"],w,p0,note[:50])); continue
    if p==w: c[k]["as printed"]+=1; continue
    sw,sp=strip(w),strip(p)
    if k=="A": ok = sp.lower()=="s"+sw.lower() and p[0] in "Śś" or sw==sp
    elif k=="C": ok = sw==sp
    else: ok = sw==sp or (sw[:-1]==sp[:-1] and sw[-1:]+sp[-1:] in ("hm","mh")) or (k in ("EM","EX","EK") and lev(sw,sp)<=2 and abs(len(sw)-len(sp))<=2) or (k in ("ED","EH") and lev(sw,sp)<=2 and abs(len(sw)-len(sp))<=1 and len(sw)>=4)
    if not ok: c[k]["other reading"]+=1; ex[k+" other"].append((x["id"],w,p0)); continue
    assert T3[x["path"]][x["s"]:x["e"]]==w
    edits.append((x["path"],x["s"],x["e"],w,p,k)); c[k]["changed"]+=1; ex[k+" changed"].append((w,p))
for k in sorted(c): print(k,dict(c[k]))
for k,v in sorted(ex.items()): print(k,v[:12])
if "patch" in sys.argv:
    E=collections.defaultdict(list); seen=set()
    for p,s,e,w,v,k in edits:
        if (p,s) in seen: continue
        seen.add((p,s)); E[p].append((s,e,w,v))
    patch=[]; DN=re.compile("[Yy][Aa][Hh][Ww][Ee][Hh]|[Jj][Ee][Hh][Oo][Vv][Aa][Hh]|[Yy][Hh][Ww][Hh]|יהוה"); dn=[0,0]
    for rel,es in sorted(E.items()):
        t=T3[rel]; u=t; es.sort(); assert all(a[1]<=b[0] for a,b in zip(es,es[1:]))
        for s,e,w,v in reversed(es): u=u[:s]+v+u[e:]
        dn[0]+=len(DN.findall(t)); dn[1]+=len(DN.findall(u))
        tl=t.split("\n"); ul=u.split("\n"); assert len(tl)==len(ul)
        hunks=[]; off=0
        for a,b in zip(tl,ul):
            if a!=b: hunks.append([off,u16(a),b])
            off+=u16(a)+1
        patch.append({"path":PFX+rel,"len0":u16(t),"h0":fnv(t),"len1":u16(u),"h1":fnv(u),"hunks":hunks})
    json.dump(patch,open("lib-patch7.json","w"),ensure_ascii=False); json.dump(edits,open("apply7.json","w"),ensure_ascii=False)
    print("patch notes",len(patch),"lines",sum(len(p["hunks"]) for p in patch),"divine name",dn)
