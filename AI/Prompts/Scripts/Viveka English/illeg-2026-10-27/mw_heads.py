# Builds mw-heads.json: the Monier-Williams headwords (Library/Sanskrit/Monier-Williams/monier-williams.tsv, column "headword")
# in IAST, with the anusvara written as Dyczkowski prints it (ṁ), lower case, letters only. Usage: python3 mw_heads.py <tsv>
import csv,json,unicodedata,collections,re,sys
NFC=lambda s: unicodedata.normalize("NFC",s)
mw=collections.Counter()
with open(sys.argv[1],encoding="utf-8") as f:
    r=csv.reader(f,delimiter="\t"); next(r)
    for row in r:
        if len(row)<3: continue
        h=NFC(row[2]).replace("ṃ","ṁ").replace("Ṃ","Ṁ").lower()
        h=re.sub(r"[^a-zāīūṛṝḷḹṅñṭḍṇśṣḥṁ]","",h)
        if h: mw[h]+=1
json.dump(sorted(mw),open("mw-heads.json","w"),ensure_ascii=False); print(len(mw))
