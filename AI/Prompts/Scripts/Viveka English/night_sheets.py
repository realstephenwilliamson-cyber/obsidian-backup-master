# Night pass, 23 Oct 2026 (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof5/lib-bundle.json).
# Needs pymupdf, the wamerican-large/wbritish-large word lists and tesseract-ocr-script-latn (the Latin-script model).
# Sheets for the night pass: full-width line strips (so nothing is cut at the edges), the target boxed.
import sys,json,os,re
sys.path.insert(0,"/home/claude/pf")
from slips_common import T
import crops, pymupdf as fitz
from PIL import Image,ImageDraw
crops.T=T
def strip_box(v,i,bx):
    pg=crops.doc(v)[i]; W=pg.rect.width; ws=crops.words(v,i)
    cy=(bx[1]+bx[3])/2; line=[w for w in ws if w[1]<cy<w[3]]
    y0=min([bx[1]]+[w[1] for w in line])-5; y1=max([bx[3]]+[w[3] for w in line])+5
    Z=3; pix=pg.get_pixmap(matrix=fitz.Matrix(Z,Z),clip=fitz.Rect(20,y0,W-20,y1))
    im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples); d=ImageDraw.Draw(im)
    d.rectangle([(bx[0]-20-8)*Z,(bx[1]-y0-3)*Z,(bx[2]-20+3)*Z,(bx[3]-y0+3)*Z],outline=(220,0,0),width=2); return im
def remap(items,applied):
    # old offsets (before the evening patch) -> offsets in the current text
    by={}
    for p,s,e,w,v,k in applied: by.setdefault(p,[]).append((s,len(v)-len(w)))
    for x in items:
        d=sum(dd for s,dd in by.get(x["path"],[]) if s<x["s"]); x["s"]+=d; x["e"]+=d
        assert T[x["path"]][x["s"]:x["e"]]==x["w"],(x["w"],T[x["path"]][x["s"]-5:x["e"]+5])
    return items
def build(items,prefix,per=15,outdir="/home/claude/pf/sheets2"):
    os.makedirs(outdir,exist_ok=True); os.makedirs("/home/claude/pf/items2",exist_ok=True)
    rows=[]; miss=[]
    for c in items:
        if "box" in c: v,i,x0,y0,x1,y1=c["box"]; bx=(x0,y0,x1,y1); c["pdf"]={"vol":v,"page":i+1,"score":9}
        else:
            b=crops.locate(c)
            if not b or b[0]<3.3: miss.append(c["id"]); continue
            sc,v,i,j=b; w=crops.words(v,i)[j]; bx=(w[0]-6,w[1],w[2],w[3]); c["pdf"]={"vol":v,"page":i+1,"score":round(sc,2)}
        rows.append((c,strip_box(v,i,bx)))
    made=[]
    from PIL import ImageFont
    F=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",26)
    for n in range(0,len(rows),per):
        part=rows[n:n+per]; W=max(im.width for _,im in part)+130; H=sum(im.height+14 for _,im in part)
        S=Image.new("RGB",(W,H),"white"); d=ImageDraw.Draw(S); y=0
        for c,im in part:
            d.text((6,y+im.height//2-14),c["id"],font=F,fill=(0,0,160)); S.paste(im,(130,y)); y+=im.height+6; d.line([(0,y+3),(W,y+3)],fill=(170,170,170)); y+=8
        sh=f"{prefix}-{n//per+1:02d}"; S.save(f"{outdir}/{sh}.png"); made.append(sh)
        with open(f"/home/claude/pf/items2/{sh}.txt","w") as f:
            for c,_ in part:
                t=T[c["path"]]; b=t[max(0,c["s"]-60):c["s"]].replace("\n"," ⏎ "); a=t[c["e"]:c["e"]+60].replace("\n"," ⏎ ")
                f.write(f"{c['id']} | before: …{b} | after: {a}…\n")
    return made,miss
