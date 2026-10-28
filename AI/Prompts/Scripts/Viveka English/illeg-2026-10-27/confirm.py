# Final rule (27 Oct 2026, night): a gap is filled only where the blind page reading confirms the OCR fill letter for letter
# (diacritics aside) with high confidence; the reading's own marks and punctuation are what goes in, without repeating a
# bracket or stop the note already has beside the gap, and without the raised footnote numbers (^N) the readers noted.
import json,sys,glob,re,collections
from common import *
items={i["id"]:i for i in json.load(open("items.json"))}
acc={}
for f in sys.argv[1].split(","):
    for a in json.load(open(f)): acc[a["id"]]=a
reads={}
for d in sys.argv[2].split(","):
    for f in sorted(glob.glob(d+"/*.jsonl")):
        for l in open(f,encoding="utf-8"):
            l=l.strip()
            if not l: continue
            try: r=json.loads(l); reads[int(re.sub(r"\D","",r["id"]))]=r
            except Exception: pass
def lets(s): return "".join(WRD.findall(strip(NFC(s).replace("\\","")))).lower()
BADNOTE=re.compile(r"\bwrong\b|hyphen|line end|\bpartial|incomplete|unclear|not visible|illegible|\bcannot\b",re.I)
from rapidfuzz.distance import Levenshtein as LV
out=[]; c=collections.Counter(); ex=collections.defaultdict(list)
for i,a in acc.items():
    r=reads.get(i)
    if not r: c["not read"]+=1; continue
    pr=NFC((r.get("printed") or "")).strip(); note=r.get("note") or ""
    if r.get("conf")!="high" or not pr or "?" in pr: c["reading not confident"]+=1; continue
    if BADNOTE.search(note): c["reader's note"]+=1; ex["note"].append((i,pr,note)); continue
    pr=re.sub(r"\^\d+","",pr).strip()
    near=False
    if lets(pr)!=lets(a["fill"]):
        # as on 23 Oct: the reading wins where it and the OCR are at most one letter apart (the OCR loses a final ṁ or a first ū)
        if len(lets(pr))>=3 and LV.distance(lets(pr),lets(a["fill"]))<=1: near=True
        else: c["reading differs"]+=1; ex["differs"].append((i,a["fill"],pr)); continue
    if re.search(r"[*_`|#^<>{}\d]",pr): c["odd characters"]+=1; continue
    it=items[i]; t=NOTES[it["note"]]; pre=t[it["s"]-1:it["s"]]; post=t[it["e"]:it["e"]+1]
    v=pr
    if pre and pre in "(‘“'\"" and v.startswith(pre): v=v[1:]
    if post and post in ")’”'\".,;:" and v.endswith(post): v=v[:-1]
    v=v.strip().replace("[","\\[").replace("]","\\]")
    if not v: c["empty"]+=1; continue
    same=NFC(v)==NFC(a["fill"])
    c["filled, reading one letter from the OCR" if near else ("filled, as the OCR fill" if same else "filled, reading's marks or punctuation")]+=1
    if near: ex["near"].append((i,a["fill"],v))
    if not same and len(ex["changed"])<40: ex["changed"].append((i,a["fill"],v))
    out.append({"id":i,"fill":v,"ocrfill":a["fill"],"tier":a["tier"]+(["reading one letter from the OCR"] if near else [])})
print(dict(c))
for k,v in ex.items(): print(k,len(v),v[:25])
json.dump(out,open(sys.argv[3],"w"),ensure_ascii=False)
