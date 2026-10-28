# Compares the proposed fills with the blind reading: letters with their marks (the test), and punctuation separately.
import json,sys,glob,re,unicodedata
from common import *
acc={a["id"]:a for a in json.load(open(sys.argv[1]))}
items={i["id"]:i for i in json.load(open("items.json"))}
reads={}
for f in sorted(glob.glob(sys.argv[2]+"/*.jsonl")):
    for l in open(f,encoding="utf-8"):
        l=l.strip()
        if l:
            try: r=json.loads(l); reads[int(r["id"][1:])]=r
            except Exception as e: pass
def letters(s): return " ".join(WRD.findall(NFC(s).replace("\\","")))
res=[]
for i,a in acc.items():
    r=reads.get(i)
    if not r: continue
    pr=re.sub(r"\^\d+","",NFC(r.get("printed",""))).strip()
    it=items[i]; t=NOTES[it["note"]]; pre=t[it["s"]-1:it["s"]]; post=t[it["e"]:it["e"]+1]
    if pre and pre in "(‘“'\"" and pr.startswith(pre): pr=pr[1:]
    if post and post in ")’”'\".,;:" and pr.endswith(post): pr=pr[:-1]
    ok=letters(a["fill"])==letters(pr)
    punct=re.sub(rf"[{L}\s\\\\]","",a["fill"])==re.sub(rf"[{L}\s]","",pr)
    res.append((i,ok,punct,a["fill"],pr,r.get("conf"),r.get("note",""),a["tier"],a.get("wratio")))
n=len(res); k=sum(1 for x in res if x[1]); p=sum(1 for x in res if x[1] and x[2])
print(f"read {n}: letters right {k}, letters and punctuation right {p}")
for x in res:
    if not (x[1] and x[2]): print(("LETTERS " if not x[1] else "punct   "),x[0],"| fill:",x[3],"| print:",x[4],"|",x[5],x[6],"|",x[7],x[8])
