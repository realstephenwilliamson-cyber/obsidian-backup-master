import json,sys,os
man=json.load(open('/home/claude/d09/rb/manifest.json'))
done=set(json.load(open('/home/claude/d09/rb/committed.json'))) if os.path.exists('/home/claude/d09/rb/committed.json') else set()
L=[]
for rel,r in man.items():
    if 'after' not in r or rel in done: continue
    b,a=r['before'],r['after']
    line=(f"**Text layer** (15 Oct 2026, decision D09 a/b): the OCR text layer was redone (OCRmyPDF --redo-ocr, sandwich renderer, English and Sanskrit) "
          f"to remove the stray glyph the old layer put after the vowel sign ि; the page images are unchanged. Stray glyphs after ि: {b['junk']} before, {a['junk']} now"
          + (f"; Devanagari letters read into English lines: {b['deva_in_latin']} before, {a['deva_in_latin']} now." if (b['deva_in_latin'] or a['deva_in_latin']) else "."))
    L.append(dict(target=rel,parts=r['parts'],size=r['size'],sha256=r['sha256'],line=line))
json.dump(L,open('/mnt/user-data/outputs/fx/pdfrep.json','w'),ensure_ascii=False,indent=0)
print(len(L),'entries',sum(x['size'] for x in L)//1_000_000,'MB'); [print(' ',x['target'].split('/')[-1],x['parts']) for x in L]
