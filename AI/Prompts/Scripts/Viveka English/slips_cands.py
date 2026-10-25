# Last slips pass, 23 Oct 2026, evening (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for proof.py, crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof4/lib-bundle.json).
from slips_common import *
import random
random.seed(42)
V="aāiīuūeoṛ"; CONS="bcdfghjklmnpqstvwxyzḍḥḷṁṅṇñṭṣśBCDFGHJKLMNPQSTVWXYZŚṢṬḌṆ"
M=json.load(open("measure.json"))
items=[]   # read items: id, path, s, e, w, prop, kind
rules=[]   # rule edits: path, s, e, w, prop, kind
def add(lst,kind,p,s,w,prop,eng): lst.append({"path":p,"s":s,"e":s+len(w),"w":w,"prop":prop,"kind":kind,"eng":eng})
for p,s,w,v,e in M["D"]: add(items,"D",p,s,w,v,e)
for p,s,w,v,e in M["MH"]: add(items,"M",p,s,w,v,e)
for p,s,w,v,e in M["Hshort"]:
    prop=w[:-1]+"ḥ"
    if e or w in ("kih","ih"): add(items,"H",p,s,w,prop,e)
    else: add(rules,"HS",p,s,w,prop,e)
for p,s,w,v,e in M["ABB"]:
    if w!="KuKh": add(items,"K",p,s,w,None,e)
for p,s,w,v,e in M["RN"]:
    if v: add(rules,"N",p,s,w,v,e)
# residue of earlier fixes and rh
for p,t in sorted(T.items()):
    for m in TOKRX.finditer(t):
        w=m.group(0)
        if w.lower() in ENGL: continue
        v=w
        v=re.sub("rnṇ","rṇ",v)
        v=re.sub(rf"(?<=[{V}])rnṁ(?=[{CONS}]|$)","ṁ",v)
        v2=re.sub(rf"(?<=[{V}])rh(?=v)","ṁ",v)
        if v2!=v and tok.get(v2,0)>=3: v=v2
        if v!=w:
            line=skipline(t,m.start())
            if line is None: continue
            add(rules,"Q",p,m.start(),w,v,P.english_line(line))
        elif re.search("rn[ṇṁ]|SārnKā",w):
            line=skipline(t,m.start())
            if line is None: continue
            add(items,"X",p,m.start(),w,None,P.english_line(line))
print(collections.Counter(x["kind"] for x in items), collections.Counter(x["kind"] for x in rules))
print(collections.Counter((x["w"],x["prop"]) for x in rules if x["kind"]=="Q").most_common(40))
print(collections.Counter(x["w"] for x in items if x["kind"]=="X"))
# samples of rule items to be read: N 40, HS 15, Q all (if <=40)
smp=random.sample([r for r in rules if r["kind"]=="N"],40)+random.sample([r for r in rules if r["kind"]=="HS"],15)+[r for r in rules if r["kind"]=="Q"]
for r in smp: r["sample"]=True
for r in smp: items.append(dict(r,kind="S"+r["kind"]))
for i,x in enumerate(items): x["id"]=f"{x['kind'][0] if x['kind'][0]!='S' else 'S'}{i+1:03d}"
json.dump(items,open("items.json","w"),ensure_ascii=False); json.dump(rules,open("rules.json","w"),ensure_ascii=False)
print("read items",len(items))
