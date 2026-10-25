# Last slips pass, 23 Oct 2026, evening (see the note "Viveka English scripts"). Written for a cloud workspace: /home/claude/p4/ for the work,
# /home/claude/pf/ for proof.py, crops.py, the sheets and the reads; the library copy from a read-only bundle job (.work/pe-proof4/lib-bundle.json).
from slips_common import *
# Verse-number daṇḍas the OCR read as I| Il |I |l l| (or a lone I/i at the end): normalise to the line's own form (|| or ॥).
JUNK=r"(?:I\||Il|\|I|\|l|l\||II|I|i|l)"
DD=r"(?:\|\||॥)"
RX=re.compile(rf"(?P<a>{DD}|{JUNK})(?P<sp1>\s*)(?P<n>\d+)(?P<sp2>\s*)(?P<b>{DD}|{JUNK})(?=\s*$|\s)")
edits=[]; c=collections.Counter(); ex=[]
for p,t in sorted(T.items()):
    off=0
    for ln in t.split("\n"):
        s=ln.lstrip()
        if s and not s.startswith(("#","*[p.","^","*[PDF")) and not P.english_line(ln):
            for m in RX.finditer(ln):
                a,b=m.group("a"),m.group("b")
                ja=not re.fullmatch(DD,a); jb=not re.fullmatch(DD,b)
                if not (ja or jb): continue
                if ja and jb:
                    if len(a)!=2 or len(b)!=2: continue   # both sides junk: only two-character forms, made ||
                    good="||"
                else: good=b if ja else a
                # a lone I/i/l on one side only at the end of the line
                if (ja and a in ("I","i","l")) or (jb and b in ("I","i","l") and ln[m.end():].strip()): continue
                new=(good if ja else a)+m.group("sp1")+m.group("n")+m.group("sp2")+(good if jb else b)
                st=off+m.start(); edits.append({"path":p,"s":st,"e":off+m.end(),"w":m.group(0),"prop":new,"kind":"J"})
                c["both" if ja and jb else (a if ja else b)]+=1
                if len(ex)<10: ex.append((m.group(0),new))
        off+=len(ln)+1
print(len(edits),c); print(ex)
json.dump(edits,open("danda.json","w"),ensure_ascii=False)
