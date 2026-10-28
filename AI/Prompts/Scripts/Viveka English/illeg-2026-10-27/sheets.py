# Sheets for the blind check: one full-width printed line per item with the gap boxed in red; the item list gives the
# note's words just before and after the gap, never the proposed fill.
import json,sys,os,random,pymupdf as fitz
from PIL import Image,ImageDraw,ImageFont
from common import *
items={i["id"]:i for i in json.load(open("items.json"))}
P={x["id"]:x for x in json.load(open(sys.argv[1]))}
ids=json.load(open(sys.argv[2])); prefix=sys.argv[3]; outdir=sys.argv[4]
os.makedirs(outdir+"/sheets",exist_ok=True); os.makedirs(outdir+"/items",exist_ok=True)
docs={}
F=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",26)
def strip_img(i):
    it=items[i]; r=P[i]["r"]; v=it["v"]
    if v not in docs: docs[v]=fitz.open(f"pdfs/Dyczkowski - Tantraloka, vol. {v:02d}.pdf")
    W=tsv(v,r["K"]); ln=r["lines"][0]; line=[w for w in W if w["ln"]==ln]
    s=72/400; x0,y0,x1,y1=r["box"]
    ly0=min([y0]+[w["y"] for w in line]); ly1=max([y1]+[w["y"]+w["h"] for w in line])
    pg=docs[v][r["K"]-1]; Z=3
    clip=fitz.Rect(15,ly0*s-6,pg.rect.width-15,ly1*s+6)
    pix=pg.get_pixmap(matrix=fitz.Matrix(Z,Z),clip=clip)
    im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples); d=ImageDraw.Draw(im)
    d.rectangle([(x0*s-15-7)*Z,(y0*s-clip.y0-3)*Z,(x1*s-15+5)*Z,(y1*s-clip.y0+3)*Z],outline=(220,0,0),width=3)
    return im
per=12; made=[]
for n in range(0,len(ids),per):
    part=[(i,strip_img(i)) for i in ids[n:n+per]]
    Wd=max(im.width for _,im in part)+140; H=sum(im.height+14 for _,im in part)
    S=Image.new("RGB",(Wd,H),"white"); d=ImageDraw.Draw(S); y=0
    sh=f"{prefix}-{n//per+1:02d}"
    with open(f"{outdir}/items/{sh}.txt","w",encoding="utf-8") as f:
        for i,im in part:
            lab=f"{prefix}{i:05d}"
            d.text((6,y+im.height//2-14),lab[-6:],font=F,fill=(0,0,160)); S.paste(im,(140,y)); y+=im.height+6
            d.line([(0,y+3),(Wd,y+3)],fill=(170,170,170)); y+=8
            it=items[i]; t=NOTES[it["note"]]
            b=IL.sub("[?]",t[max(0,it["s"]-70):it["s"]]).replace("\n"," ⏎ "); a=IL.sub("[?]",t[it["e"]:it["e"]+70]).replace("\n"," ⏎ ")
            f.write(f"{lab[-6:]} | before: …{b} | after: {a}…\n")
    S.save(f"{outdir}/sheets/{sh}.png"); made.append(sh)
print(made)
