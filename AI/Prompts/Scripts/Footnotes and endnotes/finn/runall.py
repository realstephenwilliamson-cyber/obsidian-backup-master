import sys, json, collections
sys.path.insert(0,'/home/claude/finn')
from transform import do_page, P
R={}; last=None; st=collections.Counter(); skips=[]
for K in sorted(P):
    try: r,last2,info=do_page(K,last,set())
    except Exception as e: skips.append((K,'ERR '+repr(e)[:80])); continue
    if info.get('skip'): skips.append((K,info['skip']))
    last=last2 if last2 is not None else last
    if not r: continue
    R[K]=r
    st['pages']+=1; st['notes']+=len(r['lab_idx']); st['defs']+=len(r['out_defs']); st['visible_notes']+=sum(1 for t in r['out_tail'] if True)
    for v in r['refs'].values(): st['ref_'+v]+=1
    st['labels_placed']+=len(r['placed']); st['floating_pages']+=1 if r['floating'] else 0
    st['notes_missing_in_md']+=sum(1 for j in r['lab_idx'] if not any(c==('N',j) for c in r['cls']))
print(st); print(len(skips),'skips'); print(collections.Counter(s for _,s in skips)); print(skips[:30])
import pickle; pickle.dump(R,open('/home/claude/finn/R.pkl','wb'))
