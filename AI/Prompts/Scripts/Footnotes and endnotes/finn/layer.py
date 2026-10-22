import pymupdf as fitz, json, re
PDF="/mnt/user-data/uploads/Obsidian Vault/Library/Trika/KULACUDAMANI TANTRA and VAMAKESVARA TANTRA with the JAYARATHA COMMENTARY - Louise M. Finn - 1986.pdf"
d=fitz.open(PDF); out=[]
for pi,p in enumerate(d):
    lines=[]
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            sp=[s for s in l['spans'] if s['text'].strip()]
            if not sp: continue
            lines.append(dict(x=round(l['bbox'][0],1),y=round(l['bbox'][1],1),y1=round(l['bbox'][3],1),
                spans=[dict(t=s['text'],f='O' if 'Obl' in s['font'] else 'R',sz=round(s['size'],1),x=round(s['bbox'][0],1),x1=round(s['bbox'][2],1),y=round(s['bbox'][1],1)) for s in sp]))
    lines.sort(key=lambda L:(round(L['y']/4),L['x']))
    out.append(lines)
json.dump(out,open('layer.json','w'),ensure_ascii=False)
# stats
ml=nl=rf=0
for lines in out:
    for L in lines:
        if L['x']<50 and re.match(r'^\S{1,5}\.?$',L['spans'][0]['t'].strip()): ml+=1
        if any(s['f']=='O' for s in L['spans']): nl+=1
        rf+=sum(1 for s in L['spans'] if s['sz']<7 and re.search(r'\d',s['t']))
print('pages',len(out),'margin-ish',ml,'oblique lines',nl,'small digit spans',rf)
