# Second proofreading pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace with the work in /home/claude/pf/:
# done-in/ and other-in/ hold the 123 chapter notes and the 43 other notes as they were; other-proof/ the 43 after clean.py and proof.py;
# the PDFs and lib-bundle.json staged from the vault. Change the paths to run it elsewhere.
"""Crop each candidate's line from its PDF page (the OCR text layer gives word boxes), box the word, and stack the strips into sheets."""
import json,re,random,difflib,unicodedata,os,sys,collections
import pymupdf as fitz
from PIL import Image,ImageDraw,ImageFont
PDF="/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. {:02d}.pdf"
T={}
import glob
for d in ("done-in","other-proof"):
    for f in glob.glob(d+"/*/*.md"): T[f.split("/",1)[1]]=open(f,encoding="utf-8").read()
docs={}
def doc(v):
    if v not in docs: docs[v]=fitz.open(PDF.format(v))
    return docs[v]
def strip(s): return ''.join(ch for ch in unicodedata.normalize('NFD',s) if not unicodedata.combining(ch))
def norm(s): return re.sub(r"[^a-z]","",strip(s).lower())
L=r"A-Za-zÀ-ɏḀ-ỿ"
MK=re.compile(r"\*\[p\. [^\]]*\]\* \^pg(\d+)")
WCACHE={}
def words(v,i):
    if (v,i) not in WCACHE: WCACHE[(v,i)]=doc(v)[i].get_text("words")
    return WCACHE[(v,i)]
def locate(c):
    t=T[c["path"]]; v=int(re.search(r"vol (\d\d)",c["path"]).group(1))
    ms=[m for m in MK.finditer(t) if m.start()<c["s"]]
    if not ms: return None
    K=int(ms[-1].group(1))
    before=[norm(x) for x in re.findall(rf"[{L}]+",t[max(0,c['s']-60):c['s']])][-3:]
    after=[norm(x) for x in re.findall(rf"[{L}]+",t[c['e']:c['e']+60])][:3]
    target=norm(c.get("raw") or c["w"]); best=None
    for i in (K-1,K,K-2):
        if i<0 or i>=doc(v).page_count: continue
        ws=words(v,i); nw=[norm(w[4]) for w in ws]
        for j,w in enumerate(ws):
            r=difflib.SequenceMatcher(None,nw[j],target).ratio()
            if r<0.7: continue
            sc=r*2+sum(1 for k,b in enumerate(reversed(before)) if j-1-k>=0 and difflib.SequenceMatcher(None,nw[j-1-k],b).ratio()>0.7)+sum(1 for k,a in enumerate(after) if j+1+k<len(nw) and difflib.SequenceMatcher(None,nw[j+1+k],a).ratio()>0.7)
            sc-= 0.3*(i!=K-1)
            if not best or sc>best[0]: best=(sc,v,i,j)
    return best
def strip_img(best):
    sc,v,i,j=best; ws=words(v,i); w=ws[j]
    line=[x for x in ws if x[5]==w[5] and x[6]==w[6]]
    x0=min(x[0] for x in line)-16; x1=max(x[2] for x in line)+6; y0=min(x[1] for x in line)-5; y1=max(x[3] for x in line)+5
    pg=doc(v)[i]; Z=3
    pix=pg.get_pixmap(matrix=fitz.Matrix(Z,Z),clip=fitz.Rect(x0,y0,x1,y1))
    im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
    d=ImageDraw.Draw(im); d.rectangle([(w[0]-x0-10)*Z,(w[1]-y0-3)*Z,(w[2]-x0+2)*Z,(w[3]-y0+3)*Z],outline=(220,0,0),width=2)
    return im
FONT=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",26)
def sheets(items,prefix,per=12,outdir="sheets"):
    os.makedirs(outdir,exist_ok=True); made=[]; miss=[]
    rows=[]
    for c in items:
        b=locate(c)
        if not b or b[0]<1.6: miss.append(c["id"]); continue
        c["pdf"]={"vol":b[1],"page":b[2]+1,"score":round(b[0],2)}
        rows.append((c["id"],strip_img(b)))
    for n in range(0,len(rows),per):
        part=rows[n:n+per]; W=max(im.width for _,im in part)+130; H=sum(im.height+14 for _,im in part)
        S=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(S); y=0
        for id_,im in part:
            d.text((6,y+im.height//2-14),id_,font=FONT,fill=(0,0,160)); S.paste(im,(130,y)); y+=im.height+6
            d.line([(0,y+3),(W,y+3)],fill=(170,170,170),width=1); y+=8
        fn=f"{outdir}/{prefix}-{n//per+1:02d}.png"; S.save(fn); made.append((fn,[i for i,_ in part]))
    return made,miss
