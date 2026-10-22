import json,os,sys
L=json.load(open(os.path.expanduser('~/fnwork/dhv/layer.json'),encoding='utf-8'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for K in range(a,b+1):
    print('=== PDF',K)
    prev=None
    for l in L[K-1]['lines']:
        t=' '.join(w['t'] for w in l['w'])
        sz=l['w'][0]['sz']
        print(f"{l['y']:6.1f} {l['y']-prev if prev else 0:4.1f} x{l['x']:5.1f} s{sz} | {t[:80]}"); prev=l['y']
