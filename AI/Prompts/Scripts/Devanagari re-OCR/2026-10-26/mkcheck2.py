# Container paths (/home/claude/dz/...) are those of the 26 Oct 2026 session; adjust before reuse.
import pymupdf as fitz, hashlib, random, re, json, sys, os
items=json.load(open('check2/items.json')) if os.path.exists('check2/items.json') else []
done={i['vol'] for i in items}
m=json.load(open('rb/post.json'))
for name,r in sorted(m.items()):
    v=name[-6:-4]
    if v in done: continue
    old=fitz.open(f'pdf/{name}'); new=fitz.open(f'rb/v{v}.fixed.pdf')
    same=sum(1 for i in range(len(old)) if [hashlib.md5(old.extract_image(x[0])['image']).hexdigest() for x in old[i].get_images()]==[hashlib.md5(new.extract_image(x[0])['image']).hexdigest() for x in new[i].get_images()])
    cand=[i for i in range(len(old)) if re.search(r'ि[^ऀ-ॿ \n.,;:|।॥()-]',old[i].get_text()) and len(re.findall('[ऀ-ॿ]',new[i].get_text()))>80]
    pick=random.Random(int('20261026'+v)).sample(cand,3)
    info=json.load(open('check2/info.json')) if os.path.exists('check2/info.json') else {}; info[v]=dict(images_identical=same,pages=len(old),checked=[p+1 for p in pick]); json.dump(info,open('check2/info.json','w'))
    print(v,'pages',len(old),'image-identical',same,'picked',[p+1 for p in pick],flush=True)
    for p in pick:
        fn=f'check2/v{v}-p{p+1}.png'; new[p].get_pixmap(dpi=200).save(fn)
        open(f'check2/v{v}-p{p+1}.new.txt','w').write(new[p].get_text()); open(f'check2/v{v}-p{p+1}.old.txt','w').write(old[p].get_text())
        items.append(dict(vol=v,page=p+1,image=fn,new_text=f'check2/v{v}-p{p+1}.new.txt',old_text=f'check2/v{v}-p{p+1}.old.txt'))
    json.dump(items,open('check2/items.json','w'),indent=1)
