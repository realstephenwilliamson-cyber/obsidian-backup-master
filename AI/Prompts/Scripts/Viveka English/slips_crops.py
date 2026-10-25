# Last slips pass, 23 Oct 2026, evening (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for proof.py, crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof4/lib-bundle.json).
import sys,json,random,re
sys.path.insert(0,"/home/claude/pf")
from slips_common import T,L
import crops
crops.T=T
items=json.load(open("items.json"))
# keep the Q sample to 25
random.seed(7)
q=[x for x in items if x["kind"]=="SQ"]; keepq={x["id"] for x in random.sample(q,25)}
items=[x for x in items if x["kind"]!="SQ" or x["id"] in keepq]
made,miss=crops.sheets(items,"P",per=15,outdir="/home/claude/pf/sheets")
import os; os.makedirs("/home/claude/pf/items",exist_ok=True); os.makedirs("/home/claude/pf/read",exist_ok=True)
byid={x["id"]:x for x in items}
for fn,ids in made:
    sh=os.path.basename(fn)[:-4]
    with open(f"/home/claude/pf/items/{sh}.txt","w") as f:
        for i in ids:
            x=byid[i]; t=T[x["path"]]
            b=t[max(0,x["s"]-60):x["s"]].replace("\n"," ⏎ "); a=t[x["e"]:x["e"]+60].replace("\n"," ⏎ ")
            f.write(f"{i} | before: …{b} | after: {a}…\n")
json.dump(items,open("items-placed.json","w"),ensure_ascii=False)
print("sheets",len(made),"placed",sum(len(i) for _,i in made),"missed",len(miss))
