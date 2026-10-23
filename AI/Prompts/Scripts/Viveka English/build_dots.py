# Dots-below pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/dots/ for the work,
# /home/claude/pf/ for proof.py, crops.py and the sheets; the library copy from a read-only bundle job (.work/pe-proof3/lib-bundle.json).
"""Dots-below pass (23 Oct 2026): score the page-read sample per tier, then build the patch for the tiers given on the command line.
  python3 build_dots.py                 -> scores only
  python3 build_dots.py S EM AS AEM     -> patch lib-patch.json for those tiers
A sampled item is right when the print has the added dot at every place the rule adds one; wrong when the print lacks one there."""
import json,glob,sys,unicodedata,collections,re
NFC=lambda s: unicodedata.normalize("NFC",s)
def u16(s): return len(s)+sum(1 for ch in s if ord(ch)>0xFFFF)
def fnv(s):
    h=0x811c9dc5; b=s.encode("utf-16-le")
    for i in range(0,len(b),2): h^=b[i]|(b[i+1]<<8); h=(h*0x01000193)&0xFFFFFFFF
    return h
reads={}
for f in glob.glob("/home/claude/pf/read/D-*.jsonl"):
    for l in open(f,encoding="utf-8"):
        if l.strip(): r=json.loads(l); reads[r["id"]]=r
score=collections.defaultdict(collections.Counter); wrong=[]
for c in json.load(open("batchD.json")):
    r=reads.get(c["id"])
    if not r: score[c["kind"]]["unread"]+=1; continue
    p=NFC(r["printed"].strip()); w,v=c["w"],c["prop"]
    if r["conf"]!="high" or len(p)!=len(v): score[c["kind"]]["unclear"]+=1; wrong.append((c["id"],c["kind"],w,v,p,r.get("note",""))); continue
    pos=[i for i in range(len(v)) if v[i]!=w[i]]
    if all(p[i]==v[i] for i in pos): score[c["kind"]]["right"]+=1
    else: score[c["kind"]]["wrong"]+=1; wrong.append((c["id"],c["kind"],w,v,p,r.get("note","")))
for k in sorted(score): print(k,dict(score[k]))
for x in wrong: print(x)
tiers=set(sys.argv[1:])
if tiers:
    B=json.load(open("/mnt/user-data/uploads/Obsidian Vault/.work/pe-proof3/lib-bundle.json")); PFX="Library/Trika/Tantraloka (Dyczkowski)/"
    E=collections.defaultdict(list)
    for c in json.load(open("allcands.json")):
        if c["kind"] in tiers: E[c["path"]].append((c["s"],c["e"],c["prop"]))
    patch=[]; n=0
    DN=re.compile("[Yy][Aa][Hh][Ww][Ee][Hh]|[Jj][Ee][Hh][Oo][Vv][Aa][Hh]|[Yy][Hh][Ww][Hh]|יהוה"); dn0=dn1=0
    for rel,es in sorted(E.items()):
        t=B[PFX+rel]; u=t
        for s,e,v in sorted(es,reverse=True): u=u[:s]+v+u[e:]; n+=1
        dn0+=len(DN.findall(t)); dn1+=len(DN.findall(u))
        tl=t.split("\n"); ul=u.split("\n"); assert len(tl)==len(ul)
        hunks=[]; off=0
        for x,y in zip(tl,ul):
            if x!=y: hunks.append([off,u16(x),y])
            off+=u16(x)+1
        patch.append({"path":PFX+rel,"len0":u16(t),"h0":fnv(t),"len1":u16(u),"h1":fnv(u),"hunks":hunks})
    json.dump(patch,open("lib-patch.json","w"),ensure_ascii=False)
    print("tiers",sorted(tiers),"notes",len(patch),"words",n,"lines",sum(len(p["hunks"]) for p in patch),"divine name before/after",dn0,dn1)
