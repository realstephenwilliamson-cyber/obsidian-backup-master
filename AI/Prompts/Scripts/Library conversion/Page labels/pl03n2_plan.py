# pl03n2_plan.py (3 Nov 2026, night, second round): the books and PDF pages read for the 66 held entries and the leftovers; prints pages and image tokens per book. Rendering and shuffling as in pl03n_render.py (seed 20261104, batches of 60).
import json
src=json.load(open('src.json'))
B={'w':"The Self's Awareness of Itself (Watson)",'isv':"The Isvarapratyabhijnakarika of Utpaladeva with the Author's (Utpaladeva)",'tz':"The Doctrine of Magic Female Spirits' (Torzsok)",
'mal':'Malini Vijayottara Tantra (Shastri)','ab':"Abhinavabharati - Abhinavagupta's Commentary on Bharata's (Pande)",'bif':'Bifurcate (Stiegler)','ver':'The Books of Contemplation (Verman)',
'idel':'Ben - Sonship and Jewish Mysticism (Idel)','vin':'The Vinasikhatantra (Goudriaan)','weiss':'The Emergence of Modern Hinduism (Weiss)','dmt':'The Devi Mahatmyam (text)',
'kin':'Tantric Visions of the Divine Feminine (Kinsley)','pb':'Prabuddha Bharata, January 2016 (Narasimhananda)','lut':"Hanuman's Tale (Lutgendorf)",'gan':'Ganapati - Song of the Self (Grimes)',
'cob':'Devi-Mahatmya (Coburn)','cy2':'Commentary on John, vol. 2 (Cyril of Alexandria)','vas':'The Yoga of the Malinivijayottaratantra (Vasudeva)','hir':'Mudras - Yoga in Your Hands (Hirschi)',
'cyc':'Cyclonopedia - Complicity with Anonymous Materials (Negarestani)','cy1':'Commentary on John, vol. 1 (Cyril of Alexandria)'}
def R(*a):
    out=[]
    for x in a:
        if isinstance(x,tuple): out+=list(range(x[0],x[1]+1))
        else: out.append(x)
    return out
P={'w':R((1,13),19,20),
'isv':R((1,42),51,52,53,(58,64),71,(79,82),85,91,114,118,126,(137,140),149,180,207,(214,218),232,235,270,272,312,333,334),
'tz':R((90,94),(120,130),(141,146),(154,158),(164,166),200,201),
'mal':R((224,227)),
'ab':R(26,27,28,(40,43),(48,50),(108,110),(119,122),(126,134),(170,173)),
'bif':R((1,12),(304,308),(325,330)),
'ver':R((1,15),(129,131)),
'idel':R((1,7)),
'vin':R((1,16),(72,75),(166,175)),
'weiss':R((220,222)),
'dmt':R(1,2,3,39,40,41),
'kin':R((56,62),(72,77),(86,89),(96,98),(147,149),(163,165),(243,246)),
'pb':R(),
'lut':R((1,20)),
'gan':R(1,(10,15),(38,46),(74,77),(80,84),(118,123),(152,160),165,166),
'cob':R((1,23),(384,386)),
'cy2':R((1,29),(756,764)),
'vas':R((5,12),(39,44),(51,57),(79,83),(118,123),(158,162)),
'hir':R((25,28),(38,46),(53,56),(141,143),(155,163),(178,180),(201,208),(220,223),(227,230),232,233),
'cyc':R((9,11),(17,24),(38,41),(200,202),(233,235),(238,240),244,245),
'cy1':R((1,18),72,73)}
json.dump({'books':B,'pages':P},open('plan2.json','w'),indent=0)
import fitz,warnings; warnings.filterwarnings('ignore')
V='/mnt/user-data/uploads/Obsidian Vault/'
tot=0;n=0
for b,ks in P.items():
    if not ks: continue
    d=fitz.open(V+src[B[b]]); r=d[ks[0]-1].rect; w,h=r.width/72*110,r.height/72*110
    t=len(ks)*w*h/750; tot+=t; n+=len(ks); print(b,len(ks),d.page_count,int(w),int(h),int(t))
print('pages',n,'tokens per reader',int(tot))
