# Last slips pass, 23 Oct 2026, evening (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for proof.py, crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof4/lib-bundle.json).
from slips_common import *
byk=collections.defaultdict(list)
for w,c in tok.items(): byk[und(w)].append((c,w))
def attested(w,c,letters=None,mult=3):
    best=None
    for vc,v in byk[und(w)]:
        if v==w or len(v)!=len(w): continue
        if all(a==b or (a in DOT and DOT[a]==b) for a,b in zip(v,w)) and vc>=3 and vc>=mult*c:
            add={a for a,b in zip(v,w) if a!=b}
            if letters and not add<=letters: continue
            if not best or vc>best[0]: best=(vc,v)
    return best
D={}
for w,c in tok.items():
    if len(w)<3 or w.lower() in ENGL or w.lower() in P.STOP: continue
    b=attested(w,c)
    if b: D[w]=b[1]
CONS="bcdfghjklmnpqstvwxyzḍḥḷṁṅṇñṭṣśBCDFGHJKLMNPQSTVWXYZŚṢṬḌṆ"
RYV=re.compile(rf"(?<=[{CONS}])r(?=[yv])")
occ=collections.defaultdict(list)
for p,t in sorted(T.items()):
    for m in TOKRX.finditer(t):
        w=m.group(0)
        hit=(w in D) or (RYV.search(w) and w.lower() not in ENGL) or (len(w)<=3 and re.search(r"[aāiīuūeo]h$",w) and w.lower() not in ENGL) or w.endswith("ḥ") or w.endswith("rn") or (re.search(r"[a-z][A-Z]",w) and re.search(rf"(?<=[{CONS}])r(?=[{CONS}])|h$",w))
        if not hit: continue
        line=skipline(t,m.start())
        if line is None: continue
        eng=P.english_line(line)
        if re.search(r"(?<=[aāiīuūeoṛ])rn$",w) and w.lower() not in ENGL:
            v=w[:-2]+"ṁ"; occ["RN"].append((p,m.start(),w,v if tok.get(v,0)>=3 else None,eng))
        if w in D: occ["D"].append((p,m.start(),w,D[w],eng))
        if RYV.search(w) and w.lower() not in ENGL:
            occ["RYV-all"].append((p,m.start(),w,None,eng))
        if len(w)<=3 and re.search(r"[aāiīuūeo]h$",w) and w.lower() not in ENGL: occ["Hshort"].append((p,m.start(),w,None,eng))
        if w.endswith("ḥ"):
            v=w[:-1]+"ṁ"
            if tok.get(v,0)>=3*tok[w] and tok.get(v,0)>=3: occ["MH"].append((p,m.start(),w,v,eng))
        if re.search(r"[a-z][A-Z]",w) and re.search(rf"(?<=[{CONS}])r(?=[{CONS}])|h$",w): occ["ABB"].append((p,m.start(),w,None,eng))
for k,v in occ.items():
    print(k,len(v),"forms",len({x[2] for x in v}),"eng",sum(1 for x in v if x[4]))
    print("  ",collections.Counter((x[2],x[3]) for x in v).most_common(15))
# what letters D adds
add=collections.Counter()
for p,s,w,v,e in occ["D"]:
    for a,b in zip(v,w):
        if a!=b: add[a]+=1
print(add)
json.dump({k:v for k,v in occ.items()},open("measure.json","w"),ensure_ascii=False)
