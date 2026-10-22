import json,sys,statistics as st
LAY=json.load(open(sys.argv[1],encoding='utf-8'))
def rows(i):
    R=[]
    for l in LAY[i]['lines']:
        if R and abs(l['y']-R[-1]['y'])<4: R[-1]['w']+=l['w']; R[-1]['y1']=max(R[-1]['y1'],l['y1'])
        else: R.append(dict(y=l['y'],y1=l['y1'],w=list(l['w'])))
    for r in R:
        r['w'].sort(key=lambda w:w['x']); r['sz']=st.median([w['sz'] for w in r['w']]); r['h']=r['y1']-r['y']
    return R
if __name__=='__main__':
    for K in [int(x) for x in sys.argv[2].split(',')]:
        R=rows(K-1); print('== PDF',K)
        prev=None
        for r in R:
            t=' '.join(w['t'] for w in r['w'])
            print(f"{r['y']:6.1f} pitch {r['y']-prev if prev else 0:5.1f} h {r['h']:4.1f} sz {r['sz']:4.1f} x {r['w'][0]['x']:5.1f} | {t[:70]}"); prev=r['y']
