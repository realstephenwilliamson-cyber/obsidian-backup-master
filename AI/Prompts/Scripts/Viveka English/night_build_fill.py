# Night pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof5/lib-bundle.json).
# Needs pymupdf, the wamerican-large/wbritish-large word lists and tesseract-ocr-script-latn (the Latin-script model).
# Night pass, part 2: fill [illegible] placeholders where a blind page reading and the Latin-model re-OCR agree on the letters (the reading's marks win).
import json,glob,sys,unicodedata,collections,re
from slips_common import T,PFX,L
NFC=lambda s: unicodedata.normalize("NFC",s)
def strip(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch))
def lets(s): return "".join(re.findall(rf"[{L}]+",strip(NFC(s)))).lower()
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
# the text as it is now: the bundle plus the banked patch (pf35)
N2=collections.defaultdict(list)
for p,s,e,w,v,k in json.load(open("apply5-n2.json")): N2[p].append((s,e,w,v))
T2={}
for p,t in T.items():
    u=t
    for s,e,w,v in sorted(N2.get(p,[]),reverse=True): assert u[s:e]==w; u=u[:s]+v+u[e:]
    T2[p]=u
def shift(p,s): return s+sum(len(v)-len(w) for s0,e0,w,v in N2.get(p,[]) if s0<s)
reads={}
for f in sorted(glob.glob("/home/claude/pf/read2/[FGH]-*.jsonl")):
    for l in open(f,encoding="utf-8"):
        l=l.strip()
        if l:
            try: r=json.loads(l); reads[r["id"]]=r
            except Exception: pass
acc={(a["path"],a["s"]) for a in json.load(open("acc-kept.json"))}
items=[x for x in json.load(open("g-sample.json"))+json.load(open("h-sample.json"))+json.load(open("f-items.json")) if (x["path"],x["s"]) in acc]
c=collections.Counter(); edits=[]; ex=collections.defaultdict(list)
for x in items:
    r=reads.get(x["id"])
    if not r: c["unread"]+=1; continue
    p0=NFC((r.get("printed") or "").strip()); note=(r.get("note") or "").lower()
    if r.get("conf")!="high" or not p0 or any(z in note for z in ("wrong","cut","clip","incomplete","hyphen at","line end","broken")): c["unclear"]+=1; continue
    if re.search(r"[*_`|#^\\<>{}]",p0) or re.search(r"\d",p0): c["odd characters"]+=1; continue
    fill=x["prop"]
    d=lev(lets(p0),lets(fill))
    if d>1 or len(lets(p0))<3: c["reading and re-OCR differ"]+=1; ex["differ"].append((fill,p0)); continue
    p=x["path"]; s=shift(p,x["s"]); e=s+(x["e"]-x["s"]); t=T2[p]
    assert t[s:e]==x["w"],(t[s:e],x["w"])
    pre=t[s-1:s]; post=t[e:e+1]
    if pre not in ("", " ", "\n", "(", "‘", "“", "'", '"'): c["joined to the word before"]+=1; continue
    v=p0
    if pre and pre in "(‘“'\"" and v.startswith(pre): v=v[1:]
    if post and not post.isspace() and v.endswith(post): v=v[:-1]
    if post and post.isalpha(): c["joined to the word after"]+=1; continue
    v=v.replace("[","\\[").replace("]","\\]")
    edits.append((p,s,e,x["w"],v)); c["filled"]+=1
    if len(ex["filled"])<15: ex["filled"].append((x["w"][:16],fill,p0,v))
print(dict(c)); [print(k,v[:15]) for k,v in ex.items()]
if "patch" in sys.argv:
    E=collections.defaultdict(list)
    for p,s,e,w,v in edits: E[p].append((s,e,w,v))
    patch=[]; DN=re.compile("[Yy][Aa][Hh][Ww][Ee][Hh]|[Jj][Ee][Hh][Oo][Vv][Aa][Hh]|[Yy][Hh][Ww][Hh]|יהוה"); dn=[0,0]; ilb=ila=0
    for rel,es in sorted(E.items()):
        t=T2[rel]; u=t; es.sort()
        assert all(a[1]<=b[0] for a,b in zip(es,es[1:]))
        for s,e,w,v in reversed(es): u=u[:s]+v+u[e:]
        dn[0]+=len(DN.findall(t)); dn[1]+=len(DN.findall(u)); ilb+=t.count("\\[illegible\\]"); ila+=u.count("\\[illegible\\]")
        tl=t.split("\n"); ul=u.split("\n"); assert len(tl)==len(ul)
        hunks=[]; off=0
        for a,b in zip(tl,ul):
            if a!=b: hunks.append([off,u16(a),b])
            off+=u16(a)+1
        patch.append({"path":PFX+rel,"len0":u16(t),"h0":fnv(t),"len1":u16(u),"h1":fnv(u),"hunks":hunks})
    json.dump(patch,open("lib-patch6.json","w"),ensure_ascii=False); json.dump(edits,open("apply6.json","w"),ensure_ascii=False)
    print("patch notes",len(patch),"lines",sum(len(p["hunks"]) for p in patch),"placeholders in these notes before/after",ilb,ila,"divine name",dn)
