# Second proofreading pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace with the work in /home/claude/pf/:
# done-in/ and other-in/ hold the 123 chapter notes and the 43 other notes as they were; other-proof/ the 43 after clean.py and proof.py;
# the PDFs and lib-bundle.json staged from the vault. Change the paths to run it elsewhere.
"""Second proofreading pass (23 Oct 2026): build the patch for the library copy of Dyczkowski's Tantraloka.
Work text = the 123 chapter notes as they are, the 43 other notes after clean.py + proof.py. Edits on top:
  A  lost Ś/ś restored where the page image shows it (read blind; only high-confidence readings);
  B  ṁ read as "ri"/"r" (rule: the ṁ spelling occurs at least 3 times and 3 times as often), minus word forms the sample showed wrong;
  C  a parenthesised term given the print's diacritics where the page image shows them (high confidence, same letters otherwise).
placement.json (made in the session, not saved as a script): an item counts as placed only if at least two of the three words on either side match on the page and, for a bracketed term, the
brackets are in the text layer; the IDs the readers flagged (wrong line, same word in the verse, duplicate strip) were set to not placed.
Hunks are whole lines (no edit adds or removes a line). Length and FNV-1a hash (UTF-16 code units) of each note before and after."""
import json,glob,re,unicodedata,collections,sys
NFC=lambda s: unicodedata.normalize("NFC",s)
def strip(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch))
def u16(s): return len(s)+sum(1 for ch in s if ord(ch)>0xFFFF)
def fnv(s):
    h=0x811c9dc5; b=s.encode("utf-16-le")
    for i in range(0,len(b),2): h^=b[i]|(b[i+1]<<8); h=(h*0x01000193)&0xFFFFFFFF
    return h
PFX="Library/Trika/Tantraloka (Dyczkowski)/"
VAULT=json.load(open("/mnt/user-data/uploads/Obsidian Vault/.work/pe-proof2/lib-bundle.json"))
T={}
for d in ("done-in","other-proof"):
    for f in glob.glob(d+"/*/*.md"): T[f.split("/",1)[1]]=open(f,encoding="utf-8").read()
reads={}
for f in glob.glob("read/*.jsonl"):
    for l in open(f,encoding="utf-8"):
        l=l.strip()
        if l: r=json.loads(l); reads[r["id"]]=r
PL=json.load(open("placement.json"))
badB=set(json.load(open("badB.json"))) if glob.glob("badB.json") else set()
edits=collections.defaultdict(list); log=collections.Counter(); review=[]
for c in json.load(open("batchA.json")):
    r=reads.get(c["id"]); w=c["w"]
    if not r: log["A unread"]+=1; continue
    if not PL.get(c["id"],{}).get("ok"): log["A placement unsure, left"]+=1; continue
    p=NFC(r.get("printed","").strip())
    if p==w: log["A as printed already"]+=1; continue
    if r.get("conf")!="high" or "hyphen" in r.get("note","").lower(): log["A low/hyphen, left"]+=1; review.append((c["id"],w,p,r.get("note",""))); continue
    if p[:1] in "Śś" and p[1:]==w: edits[c["path"]].append((c["s"],c["e"],p,"A")); log["A Ś restored"]+=1
    elif p[:1] in "Śś" and strip(p[1:])==strip(w): edits[c["path"]].append((c["s"],c["e"],p,"A")); log["A Ś restored, with the print's other marks"]+=1
    elif p.replace("Ṁ","M").replace("ṁ","m")==w: edits[c["path"]].append((c["s"],c["e"],p,"A")); log["A ṁ (no Ś in print)"]+=1
    else: log["A other reading, left"]+=1; review.append((c["id"],w,p,r.get("note","")))
for c in json.load(open("cands.json")):
    if c["kind"]!="B": continue
    if c["w"] in badB: log["B form excluded"]+=1; continue
    edits[c["path"]].append((c["s"],c["e"],c["prop"],"B")); log["B ṁ"]+=1
for c in json.load(open("batchC.json")):
    r=reads.get(c["id"]); w=c["w"]
    if not r: log["C unread"]+=1; continue
    if not PL.get(c["id"],{}).get("ok"): log["C placement unsure, left"]+=1; continue
    p=NFC(r.get("printed","").strip())
    if p==w: log["C as printed already"]+=1; continue
    if r.get("conf")!="high": log["C low, left"]+=1; review.append((c["id"],w,p,r.get("note",""))); continue
    if strip(p)==w and " " not in p: edits[c["path"]].append((c["s"],c["e"],p,"C")); log["C diacritics"]+=1
    else: log["C other reading, left"]+=1; review.append((c["id"],w,p,r.get("note","")))
patch=[]; final={}
for rel in sorted(T):
    v=VAULT[PFX+rel]; u=T[rel]
    es=sorted(edits.get(rel,[]))
    for a,b in zip(es,es[1:]): assert a[1]<=b[0], (rel,a,b)
    for s,e,new,k in reversed(es): u=u[:s]+new+u[e:]
    if u==v: continue
    vl=v.split("\n"); ul=u.split("\n"); assert len(vl)==len(ul), rel
    hunks=[]; off=0
    for x,y in zip(vl,ul):
        if x!=y: hunks.append([off,u16(x),y])
        off+=u16(x)+1
    patch.append({"path":PFX+rel,"len0":u16(v),"h0":fnv(v),"len1":u16(u),"h1":fnv(u),"hunks":hunks}); final[rel]=u
json.dump(patch,open("lib-patch.json","w"),ensure_ascii=False)
json.dump(review,open("review.json","w"),ensure_ascii=False,indent=0)
# divine-name scan, counts only (character classes, Latin and Hebrew)
DN=re.compile("[Yy][Aa][Hh][Ww][Ee][Hh]|[Jj][Ee][Hh][Oo][Vv][Aa][Hh]|[Yy][Hh][Ww][Hh]|יהוה")
print("notes",len(patch),"line hunks",sum(len(p["hunks"]) for p in patch)); print(dict(log)); print("review",len(review))
print("divine-name matches: before",sum(len(DN.findall(VAULT[PFX+r])) for r in T),"after",sum(len(DN.findall(u)) for u in final.values()))
