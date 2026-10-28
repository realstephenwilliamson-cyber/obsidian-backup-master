# Builds the line patch for the accepted fills: per note the length and FNV-1a hash (UTF-16) before and after, line hunks in UTF-16 offsets.
# Usage: python3 build_patch.py accepted.json out-patch.json out-edits.json
import json,sys,collections,re
from common import *
PFX="Library/Trika/Tantraloka (Dyczkowski)/"
def u16(s): return len(s)+sum(1 for ch in s if ord(ch)>0xFFFF)
def fnv(s):
    h=0x811c9dc5; b=s.encode("utf-16-le")
    for i in range(0,len(b),2): h^=b[i]|(b[i+1]<<8); h=(h*0x01000193)&0xFFFFFFFF
    return h
items={i["id"]:i for i in json.load(open("items.json"))}
acc=json.load(open(sys.argv[1]))
E2=collections.defaultdict(list)
for a in acc:
    it=items[a["id"]]; t=NOTES[it["note"]]
    assert IL.fullmatch(t[it["s"]:it["s"]+14]) or t[it["s"]:it["e"]].startswith("\\[illegible\\]")
    E2[it["note"]].append((it["s"],it["e"],t[it["s"]:it["e"]],a["fill"]))
DN=re.compile("[Yy][Aa][Hh][Ww][Ee][Hh]|[Jj][Ee][Hh][Oo][Vv][Aa][Hh]|[Yy][Hh][Ww][Hh]|יהוה")
patch=[]; edits=[]; dn=[0,0]; ilb=ila=0
for rel,es in sorted(E2.items()):
    t=NOTES[rel]; es.sort(); assert all(a[1]<=b[0] for a,b in zip(es,es[1:]))
    u=t
    for s,e,w,v in reversed(es): u=u[:s]+v+u[e:]
    dn[0]+=len(DN.findall(t)); dn[1]+=len(DN.findall(u)); ilb+=len(IL.findall(t)); ila+=len(IL.findall(u))
    tl=t.split("\n"); ul=u.split("\n"); assert len(tl)==len(ul)
    hunks=[]; off=0
    for a,b in zip(tl,ul):
        if a!=b: hunks.append([off,u16(a),b])
        off+=u16(a)+1
    patch.append({"path":PFX+rel,"len0":u16(t),"h0":fnv(t),"len1":u16(u),"h1":fnv(u),"hunks":hunks})
    for s,e,w,v in es: edits.append({"note":rel,"s":s,"old":w,"new":v})
json.dump(patch,open(sys.argv[2],"w"),ensure_ascii=False); json.dump(edits,open(sys.argv[3],"w"),ensure_ascii=False)
print("notes",len(patch),"lines",sum(len(p["hunks"]) for p in patch),"fills",len(edits),"placeholders in these notes before/after",ilb,ila,"divine name before/after",dn)
