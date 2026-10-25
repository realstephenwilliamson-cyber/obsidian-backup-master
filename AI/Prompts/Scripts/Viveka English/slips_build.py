# Last slips pass, 23 Oct 2026, evening (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for proof.py, crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof4/lib-bundle.json).
# Last slips pass (23 Oct 2026, evening): score the page reads, then build one patch from the confident reads and the rules.
#   python3 build4.py          -> scores and the change list only
#   python3 build4.py patch    -> also lib-patch.json
import json,glob,sys,unicodedata,collections,re
sys.path.insert(0,"/home/claude/pf")
from slips_common import T,B,PFX
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
BADPAIR={('ŚrDpūrvapañcikā','Śrī)pūrvapañcikā'),('KrM','KṛṀ'),('mātRrvargaih','mātṚrvargaiḥ'),('diṁñmātRh','diṅmātṚḥ'),('VīranetrT','Vīranetrī')}
reads={}
for f in glob.glob("/home/claude/pf/read/P-*.jsonl"):
    for l in open(f,encoding="utf-8"):
        l=l.strip()
        if l:
            try: r=json.loads(l); reads[r["id"]]=r
            except Exception: pass
items=json.load(open("items-placed.json"))
score=collections.defaultdict(collections.Counter); apply=[]; left=collections.defaultdict(list); bad_rule=set()
for x in items:
    k=x["kind"]; r=reads.get(x["id"])
    if "pdf" not in x: score[k]["not placed"]+=1; left[k].append((x["id"],x["w"],"not placed")); continue
    if not r: score[k]["unread"]+=1; continue
    p0=NFC(r.get("printed","").strip()); note=(r.get("note") or "").lower(); w=x["w"]
    p=p0.strip("-–()[];:,.'’‘\"> !?|")
    broken=p0.endswith(("-","–")) or any(z in note for z in ("line end","line-end","end of the line","end of line","broken","continues on","split"))
    placed_ok=x["pdf"]["score"]>=3.3
    if r.get("conf")!="high" or not p or broken or "wrong" in note or not placed_ok or not re.fullmatch(r"[^\W\d_]+",p) or (w,p) in BADPAIR:
        score[k]["unclear"]+=1; left[k].append((x["id"],w,p,r.get("conf"),note[:40],x["pdf"]["score"]))
        if k.startswith("S"): bad_rule.add((x["path"],x["s"]))
        continue
    if k.startswith("S"):
        v=x["prop"]; pos=[i for i in range(min(len(v),len(w))) if i>=len(w) or v[i]!=w[i]]
        ok = (p==v) or (k=="SN" and p.endswith("ṁ") and strip(p)[:-1]==strip(v)[:-1]) or (k=="SHS" and p.endswith("ḥ")) or (k=="SQ" and strip(p)==strip(v))
        score[k]["right" if ok else "wrong"]+=1
        if not ok: left[k].append((x["id"],w,v,p,note[:40])); bad_rule.add((x["path"],x["s"]))
        if p!=w and p!=v and strip(p)==strip(v): apply.append((x["path"],x["s"],x["e"],w,p,k+"-read"))
        continue
    if p==w: score[k]["as printed"]+=1; continue
    sw,sp=strip(w),strip(p)
    okdiff = sw==sp or (sw[:-1]==sp[:-1] and sw[-1:]+sp[-1:] in ("hm","mh")) or (k in ("M","X","K") and lev(sw,sp)<=2 and abs(len(sw)-len(sp))<=2) or (k in ("D","H") and lev(sw,sp)<=2 and abs(len(sw)-len(sp))<=1 and len(sw)>=4)
    if not okdiff: score[k]["other reading"]+=1; left[k].append((x["id"],w,p,"other reading",note[:40])); continue
    score[k]["changed"]+=1; apply.append((x["path"],x["s"],x["e"],w,p,k))
for k in sorted(score): print(k,dict(score[k]))
EXCL={"Lih","Rih","rih","vih","nuh","pūh","auh","yeh","teh","aih"}
rules=[r for r in json.load(open("rules.json")) if not (r["kind"]=="HS" and r["w"] in EXCL)]+json.load(open("danda.json"))
sampled={(x["path"],x["s"]) for x in items if x["kind"].startswith("S")}
nr=collections.Counter()
for r in rules:
    if (r["path"],r["s"]) in bad_rule: continue
    if (r["path"],r["s"]) in sampled and any(a[0]==r["path"] and a[1]==r["s"] for a in apply): continue
    apply.append((r["path"],r["s"],r["e"],r["w"],r["prop"],r["kind"])); nr[r["kind"]]+=1
print("rules applied",dict(nr))
# de-duplicate and check overlaps (a read wins over a rule on the same span)
E=collections.defaultdict(dict)
for p,s,e,w,v,k in apply:
    if s in E[p] and not k.startswith(("N","Q","HS","J")): E[p][s]=(e,w,v,k)
    elif s not in E[p]: E[p][s]=(e,w,v,k)
ov=0
for p,d in E.items():
    ss=sorted(d)
    for a,b in zip(ss,ss[1:]):
        if d[a][0]>b: ov+=1
print("overlaps",ov)
for k,v in left.items(): print("LEFT",k,len(v),v[:6])
json.dump({k:v for k,v in left.items()},open("left.json","w"),ensure_ascii=False)
json.dump([[p,s,*d[s]] for p,d in E.items() for s in d],open("apply.json","w"),ensure_ascii=False)
print("changes",sum(len(d) for d in E.values()),collections.Counter(d[s][3] for d in E.values() for s in d))
if "patch" in sys.argv:
    assert ov==0
    patch=[]; DN=re.compile("[Yy][Aa][Hh][Ww][Ee][Hh]|[Jj][Ee][Hh][Oo][Vv][Aa][Hh]|[Yy][Hh][Ww][Hh]|יהוה"); dn0=dn1=0
    for rel,d in sorted(E.items()):
        t=T[rel]; u=t
        for s in sorted(d,reverse=True):
            e,w,v,k=d[s]; assert t[s:e]==w,(rel,s,w,t[s:e]); u=u[:s]+v+u[e:]
        dn0+=len(DN.findall(t)); dn1+=len(DN.findall(u))
        tl=t.split("\n"); ul=u.split("\n"); assert len(tl)==len(ul)
        hunks=[]; off=0
        for x,y in zip(tl,ul):
            if x!=y: hunks.append([off,u16(x),y])
            off+=u16(x)+1
        patch.append({"path":PFX+rel,"len0":u16(t),"h0":fnv(t),"len1":u16(u),"h1":fnv(u),"hunks":hunks})
    json.dump(patch,open("lib-patch.json","w"),ensure_ascii=False)
    print("patch notes",len(patch),"lines",sum(len(p["hunks"]) for p in patch),"divine name before/after",dn0,dn1)
