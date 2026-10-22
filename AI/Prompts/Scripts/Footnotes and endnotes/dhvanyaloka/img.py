# usage: img.py PDF K[,K..] OUT.jpg [y0 y1]  (y0,y1 = fractions of page height to crop; default whole page)
import pymupdf,sys
d=pymupdf.open(sys.argv[1]); pages=[int(x) for x in sys.argv[2].split(',')]; out=sys.argv[3]
y0,y1=(float(sys.argv[4]),float(sys.argv[5])) if len(sys.argv)>5 else (0.0,1.0)
LONG=1500
clips=[]
for K in pages:
    r=d[K-1].rect; clips.append(pymupdf.Rect(r.x0,r.y0+r.height*y0,r.x1,r.y0+r.height*y1))
W=sum(c.width for c in clips); H=max(c.height for c in clips)
zoom=LONG/max(W,H)
pix=[d[K-1].get_pixmap(matrix=pymupdf.Matrix(zoom,zoom),clip=c,colorspace=pymupdf.csRGB,alpha=False) for K,c in zip(pages,clips)]
o=pymupdf.Pixmap(pymupdf.csRGB,pymupdf.IRect(0,0,sum(p.width for p in pix),max(p.height for p in pix)),False); o.clear_with(255)
x=0
for p in pix: p.set_origin(x,0); o.copy(p,p.irect); x+=p.width
o.save(out,jpg_quality=75)
import os; print(out,o.width,'x',o.height,os.path.getsize(out)//1024,'KB')
