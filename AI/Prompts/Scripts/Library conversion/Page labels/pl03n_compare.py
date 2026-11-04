# pl03n_compare.py (3 Nov 2026, night): joins the image key, two blind readings (read/r1*.json, read/r2*.json: [{img, printed, where}]) and the current markers of the staged notes; prints one line per page with DIFF where the readers differ. Paths are those of the cloud session (/home/claude/pl); change them to use it again.
import json, re, os, glob
V='/mnt/user-data/uploads/Obsidian Vault/'
key=json.load(open('/home/claude/pl/key/key.json'))
def load(n):
    out={}
    for f in sorted(glob.glob(f'/home/claude/pl/read/{n}*.json')):
        for e in json.load(open(f)): out[e['img'].replace('.png','')]=e
    return out
r1,r2=load('r1'),load('r2')
NOTES={'mal':['Library/Trika/Malini Vijayottara Tantra (Shastri)/'],'tt':['Library/Philosophy/Technics and Time (Stiegler)/'],'rb':['Library/Hinduism/The Ritual of Battle (Hiltebeitel)/'],'hir':['Library/Hinduism/Mudras - Yoga in Your Hands (Hirschi)/'],'cyr':['Library/Christianity/Commentary on John, vol. 1 (Cyril of Alexandria)/'],'cyc':['Library/Philosophy/Cyclonopedia - Complicity with Anonymous Materials (Negarestani)/']}
MK=re.compile(r'^\*\[(p\.|PDF) ([^\]]+)\]\* \^pg(\d+)\s*$')
cur={}
for b,ds in NOTES.items():
    for d in ds:
        for f in glob.glob(V+d+'*.md'):
            for l in open(f,encoding='utf-8').read().split('\n'):
                m=MK.match(l)
                if m: cur[(b,int(m.group(3)))]=(m.group(1)+' '+m.group(2), os.path.basename(f)[:28], l)
rows=[]
for img,(b,k,w,h) in key.items():
    img=img.replace('.png','')
    a=r1.get(img,{}).get('printed','?'); c=r2.get(img,{}).get('printed','?')
    rows.append((b,k,img,cur.get((b,k),('(not staged)','',''))[0],cur.get((b,k),('','',''))[1],a,c,r1.get(img,{}).get('where',''),r2.get(img,{}).get('where','')))
rows.sort()
json.dump(rows,open('/home/claude/pl/rows.json','w'),ensure_ascii=False,indent=0)
for r in rows:
    flag='' if str(r[5]).lower()==str(r[6]).lower() else '  <-- DIFF'
    print(f'{r[0]:4} K{r[1]:<4} {r[2]} cur={r[3]:<10} {r[4]:<28} | r1={r[5]!s:<10} r2={r[6]!s:<10}{flag}')
