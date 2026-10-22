import json,sys,os,re
res=open(sys.argv[1],encoding='utf-8').read()
L=json.load(open('/mnt/user-data/outputs/fx/pdfrep.json'))
c=json.load(open('/home/claude/d09/rb/committed.json'))
ok=[x for x in L if '["replaced","'+x['target'].split('/')[-1]+'"' in res]
for x in ok:
    c.append(x['target'])
    for p in x['parts']:
        f='/mnt/user-data/outputs/d09/'+p
        if os.path.exists(f): os.remove(f)
json.dump(c,open('/home/claude/d09/rb/committed.json','w'))
print('recorded',len(ok),'of',len(L),'; total committed',len(c)); print(res[-300:])
