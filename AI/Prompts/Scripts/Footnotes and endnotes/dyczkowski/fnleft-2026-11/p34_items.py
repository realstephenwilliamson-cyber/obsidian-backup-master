import re, json, glob
from find import note
KD='/mnt/user-data/uploads/Obsidian Vault/Library/Trika/Kubjika, Kali, Tripura and Trika (Dyczkowski)/'
clean=lambda s: re.sub(r'\s+',' ', re.sub(r'\[\^\d+\]|\\\[illegible\\\]|[*#]|\\(?=[\[\]])','',s)).strip()
def around(t, i, j, nb=5, na=4):
    b=clean(t[max(0,i-200):i]).split(' ')[-nb:]; a=clean(t[j:j+150]).split(' ')[:na]
    return ' '.join(b), ' '.join(x for x in a if x)
items=[]
P3=[('07 02','(179cd- 18180)'),('07 02','(40cd- 4lab)'),('10 05','(137cd- 14140)'),('10 17','(40cd- 44270)'),('08 06','(330cd- 331lab)'),
    ('05 01','(221cd- \n\n223ab)'),('06 04','(80cd- \n\n8lab)'),('11 12','(110cd - 3)'),('09 20','(90cd - 95ab)'),('09 20','(15 - 43)')]
for n,(c,s) in enumerate(P3,1):
    p=note(c); t=open(p,encoding='utf-8').read(); i=t.find(s); assert t.count(s)==1,(c,s)
    K=int(re.findall(r'\^pg(\d+)',t[:i])[-1]); b,a=around(t,i,i+len(s))
    items.append({'id':'r%02d'%n,'part':3,'vol':c[:2],'path':p.split('Obsidian Vault/')[1],'K':K,'old':s,'before':b,'after':a,
      'q':'Copy exactly what is printed between the words "%s" and the words "%s" (a verse range in parentheses is expected there).'%(b,a)})
n=0
for f in ['Kubjika, Kali, Tripura and Trika 01 - Part 1.md','Kubjika, Kali, Tripura and Trika 02 - Part 2.md']:
    t=open(KD+f,encoding='utf-8').read()
    for m in re.finditer(r'[^\s]*\\\\[^\s]*', t):
        # token containing the double backslash
        n+=1; i,j=m.start(),m.end(); K=int(re.findall(r'\^pg(\d+)',t[:i])[-1]); b,a=around(t,i,j,4,3)
        items.append({'id':'k%02d'%n,'part':4,'path':'Library/Trika/Kubjika, Kali, Tripura and Trika (Dyczkowski)/'+f,'K':K,'old':m.group(0),'before':b,'after':a,
          'q':'Copy exactly what is printed between the words "%s" and %s. Verse-end marks (| or ||), verse numbers and brackets count.'%(b,('the words "%s"'%a) if a else 'the end of that line')})
json.dump(items,open('items.json','w'),ensure_ascii=False,indent=0)
print(len(items))
for x in items[:12]+items[-3:]: print(x['id'],x['K'],repr(x['old']),'|',x['before'],'|',x['after'])
