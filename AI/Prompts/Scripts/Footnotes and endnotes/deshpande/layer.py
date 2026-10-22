# Dump a PDF text layer: per page, lines with words (text, x0, x1, size, y-origin). usage: layer.py PDF OUT.json
import pymupdf,sys,json
d=pymupdf.open(sys.argv[1]); out=[]
for p in d:
    L=[]
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            ws=[dict(t=s['text'].strip(),x=round(s['bbox'][0],1),x1=round(s['bbox'][2],1),y0=round(s['bbox'][1],1),y1=round(s['bbox'][3],1),sz=round(s['size'],1),it=('Ital' in s['font'] or 'Obl' in s['font']),sup=bool(s['flags']&1),f=s['font']) for s in l['spans'] if s['text'].strip()]
            if ws: L.append(dict(y=round(l['bbox'][1],1),y1=round(l['bbox'][3],1),x=round(l['bbox'][0],1),x1=round(l['bbox'][2],1),w=ws))
    L.sort(key=lambda l:(l['y'],l['x']))
    out.append(dict(W=round(p.rect.width,1),H=round(p.rect.height,1),lines=L))
json.dump(out,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False)
print(len(out),'pages')
