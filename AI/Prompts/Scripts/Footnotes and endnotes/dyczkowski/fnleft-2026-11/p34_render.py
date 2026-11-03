import json, re, unicodedata, pymupdf, os
from PIL import Image, ImageDraw, ImageFont
items=json.load(open('items.json'))
V='/mnt/user-data/uploads/Obsidian Vault/'
PD={'02':'Dyczkowski - Tantraloka, vol. %s.pdf'}
def pdf(it):
    if it['part']==4: return V+'Library/Trika/Dyczkowski - Kubjika, Kali, Tripura and Trika (Nepal Research Centre 22, 2000).pdf'
    return V+'Library/Trika/Dyczkowski - Tantraloka translation/Dyczkowski - Tantraloka, vol. %s.pdf'%it['vol']
fold=lambda s: ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if c.isascii() and c.isalnum())
docs={}; os.makedirs('img',exist_ok=True); font=ImageFont.load_default(size=22)
for it in items:
    w=[x for x in it['before'].split(' ') if x not in ('|','||','॥')][-3:]; it['before3']=' '.join(w)
    d=docs.setdefault(pdf(it), pymupdf.open(pdf(it))); pg=d[it['K']-1]
    L=[]
    for b in pg.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            t=''.join(s['text'] for s in l['spans'])
            if t.strip(): L.append((t,l['bbox']))
    key=fold(' '.join(w))[-14:]; hits=[bb for t,bb in L if key and key in fold(t)]
    if len(hits)==1:
        x0,y0,x1,y1=hits[0]; h=min(max(y1-y0,9),16); r=pg.rect
        clip=pymupdf.Rect(r.x0+20, max(r.y0,y0-3*h), r.x1-20, min(r.y1,y1+3*h)); dpi=170; it['how']='strip'
    else:
        clip=pg.rect; dpi=110; it['how']='page'
    pix=pg.get_pixmap(dpi=dpi, clip=clip); im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    sh=Image.new('RGB',(im.width,im.height+30),'white'); dr=ImageDraw.Draw(sh); dr.rectangle([0,0,im.width,28],fill=(225,225,225)); dr.text((8,2),'CASE '+it['id'],fill='black',font=font); sh.paste(im,(0,30))
    sh.save('img/%s.png'%it['id'])
json.dump(items,open('items.json','w'),ensure_ascii=False,indent=0)
import collections; print(collections.Counter(it['how'] for it in items)); print([it['id'] for it in items if it['how']=='page'])
