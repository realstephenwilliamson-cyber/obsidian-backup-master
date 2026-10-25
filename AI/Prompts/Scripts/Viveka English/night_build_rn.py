# Night pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof5/lib-bundle.json).
# Needs pymupdf, the wamerican-large/wbritish-large word lists and tesseract-ocr-script-latn (the Latin-script model).
# Night pass (23 Oct 2026): score the sample reads (R: ṁ for word-final rn; G: placeholder fills from the re-OCR; U: retries), build the patch.
import json,glob,sys,unicodedata,collections,re
from slips_common import T,PFX,L
NFC=lambda s: unicodedata.normalize("NFC",s)
def strip(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch))
def letters(s): return " ".join(re.findall(rf"[{L}]+",NFC(s)))
def u16(s): return len(s)+sum(1 for ch in s if ord(ch)>0xFFFF)
def fnv(s):
    h=0x811c9dc5; b=s.encode("utf-16-le")
    for i in range(0,len(b),2): h^=b[i]|(b[i+1]<<8); h=(h*0x01000193)&0xFFFFFFFF
    return h
reads={}
for f in sorted(glob.glob("/home/claude/pf/read2/*.jsonl")):
    for l in open(f,encoding="utf-8"):
        l=l.strip()
        if l:
            try: r=json.loads(l); reads[r["id"]]=r
            except Exception: pass
Q=json.load(open("q-items.json")); G=json.load(open("g-sample.json")); H=json.load(open("h-sample.json"))
acc=json.load(open("acc-kept.json")); acck={(a["path"],a["s"]) for a in acc}
score=collections.defaultdict(collections.Counter); bad=set(); wrong=[]; apply=[]
def rd(x):
    r=reads.get(x["id"]); 
    if not r: return None,None
    p=NFC(r.get("printed","").strip()); return (p if r.get("conf")=="high" else None), (r.get("note") or "")
for x in Q["R"]:
    p,n=rd(x)
    if p is None: score["R"]["unclear/unread"]+=1; bad.add((x["path"],x["s"])); continue
    ok=letters(p).endswith("ṁ") and strip(letters(p))[:-1].endswith(strip(x["prop"])[:-1][-3:])
    score["R"]["right" if ok else "wrong"]+=1
    if not ok: bad.add((x["path"],x["s"])); wrong.append(("R",x["id"],x["w"],x["prop"],p,n[:50]))
for x in G+H:
    if (x["path"],x["s"]) not in acck: continue
    k="G" if x["id"][0]=="G" else "H"
    p,n=rd(x)
    if p is None: score[k]["unclear/unread"]+=1; bad.add((x["path"],x["s"])); continue
    ok=letters(p)==letters(x["prop"])
    score[k]["right" if ok else "wrong"]+=1
    if not ok: bad.add((x["path"],x["s"])); wrong.append((k,x["id"],x["prop"],p,n[:50]))
for x in Q["U"]:
    p,n=rd(x)
    if p is None or not p: score["U"]["unclear"]+=1; continue
    p=p.strip("-–()[];:,.'’‘\"> !?|")
    if p==x["w"]: score["U"]["as printed"]+=1; continue
    if strip(p)==strip(x["w"]) or (strip(p)[:-1]==strip(x["w"])[:-1]): score["U"]["changed"]+=1; apply.append((x["path"],x["s"],x["e"],x["w"],p,"U"))
    else: score["U"]["other"]+=1
for k in score: print(k,dict(score[k]))
for w in wrong: print("WRONG",w)
if "patch" in sys.argv:
    gok = "--g" in sys.argv
    for x in json.load(open("rn2.json")):
        if x["w"]=="Sothern" or (x["path"],x["s"]) in bad: continue
        apply.append((x["path"],x["s"],x["e"],x["w"],x["prop"],"N2"))
    if gok:
        from slips_common import skipline
        for a in acc:
            if (a["path"],a["s"]) in bad or skipline(T[a["path"]],a["s"]) is None: continue
            apply.append((a["path"],a["s"],a["e"],a["w"],a["prop"],"G"))
    E=collections.defaultdict(dict)
    for p,s,e,w,v,k in apply: E[p].setdefault(s,(e,w,v,k))
    ov=sum(1 for p,d in E.items() for a,b in zip(sorted(d),sorted(d)[1:]) if d[a][0]>b); assert ov==0
    patch=[]; DN=re.compile("[Yy][Aa][Hh][Ww][Ee][Hh]|[Jj][Ee][Hh][Oo][Vv][Aa][Hh]|[Yy][Hh][Ww][Hh]|יהוה"); dn=[0,0]
    for rel,d in sorted(E.items()):
        t=T[rel]; u=t
        for s in sorted(d,reverse=True):
            e,w,v,k=d[s]; assert t[s:e]==w,(rel,s,w,t[s:e]); u=u[:s]+v+u[e:]
        dn[0]+=len(DN.findall(t)); dn[1]+=len(DN.findall(u))
        tl=t.split("\n"); ul=u.split("\n"); assert len(tl)==len(ul)
        hunks=[]; off=0
        for x,y in zip(tl,ul):
            if x!=y: hunks.append([off,u16(x),y])
            off+=u16(x)+1
        patch.append({"path":PFX+rel,"len0":u16(t),"h0":fnv(t),"len1":u16(u),"h1":fnv(u),"hunks":hunks})
    json.dump(patch,open("lib-patch5.json","w"),ensure_ascii=False)
    json.dump([[p,s,*d[s]] for p,d in E.items() for s in d],open("apply5.json","w"),ensure_ascii=False)
    print("changes",collections.Counter(d[s][3] for d in E.values() for s in d),"notes",len(patch),"lines",sum(len(p["hunks"]) for p in patch),"divine name",dn)
