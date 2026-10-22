import re,glob,json,os
def load():
    P={}  # pdf page index (1-based K) -> dict(file, start line idx, end idx)
    files=sorted(glob.glob('/home/claude/finn/md/The Kulacudamani Tantra [0-9]*.md'))
    for f in files:
        L=open(f,encoding='utf-8').read().split('\n')
        marks=[(i,int(m.group(1))) for i,l in enumerate(L) for m in [re.match(r'^\*\[(?:p|PDF)\.? [^\]]*\]\* \^pg(\d+)$',l)] if m]
        for j,(i,k) in enumerate(marks):
            e=marks[j+1][0] if j+1<len(marks) else len(L)
            P[k]=dict(file=os.path.basename(f),start=i,end=e,lines=L[i+1:e])
    return P
if __name__=='__main__':
    P=load(); print(len(P), min(P), max(P))
    runs=0
    for k,p in P.items():
        paras=[l for l in p['lines'] if l.strip()]
        num=[bool(re.match(r'^[\dOolIS]{1,4}\\?\.\s*$',x.strip())) for x in paras]
        r=max((len(m.group(0)) for m in re.finditer('1+',''.join('1' if n else '0' for n in num))),default=0)
        if r>=2: runs+=1
    print('pages with runs of >=2 number-only paragraphs:',runs)
