"""Proofreading pass on the library copy of Dyczkowski's Tantrāloka (22 Oct 2026, night): the OCR dropped the initial Ś of
Śiva, Śakti, Śaiva and their compounds ("Lord iva", "Kula (akti)", "Kashmiri aiva authors"). This restores it in English
lines only, never in a quoted Sanskrit line, where "iva" is the particle "like" (or in a line of a mantra list or a figure).

  python3 proof.py <lib-in> <lib-out> <patch.json> <samples.json>

A word is changed only when
  - its line is English (at least two English function words, at least 8 % of its words, or a short line with one);
  - it is not between two Sanskrit-looking words (lowercase, IAST letters or a Sanskrit ending), as in a Sanskrit quotation
    run into an English line;
  - it is not "(iva)" glossing the particle ("so to speak (iva)", "seemingly (iva)");
  - it is not in a heading, a link, a page marker or a footnote number.
Case: Ś, except a word in parentheses after a lowercase word ("energies (akti)" -> "(śakti)"), as Dyczkowski prints glosses.
The patch has, per note, the length and FNV-1a hash (over UTF-16 code units, as in the vault's runner) before and after.
"""
import re, sys, json, glob, os, random, collections

L = r"A-Za-zÀ-ɏḀ-ỿ"
STOP = set("""the of and is to in that which as by with this it are for his from he who not be has its an a on or all one their they so
such was were also into through because when where there then than both each only must can may will would should these those him himself
itself i am we you""".split())
EN2 = STOP | set("lord supreme god nature consciousness light power form state principle will".split())
D = re.compile(r"[Ā-ɏḀ-ỿ]")
SKT_END = re.compile(r"(ah|am|aḥ|aṁ|ena|asya|āt|ād|eṣu|ānām|tvāt|ca|api|eva|tu|hi|iti|ity)$")
WORDS = {"iva": "Śiva", "ivas": "Śivas", "akti": "Śakti", "aktis": "Śaktis", "aiva": "Śaiva", "aivas": "Śaivas", "aivism": "Śaivism",
         "ivatanu": "Śivatanu", "ivatanuśāstra": "Śivatanuśāstra", "ivasūtra": "Śivasūtra", "ambhunātha": "Śambhunātha",
         "āmbhavopāya": "Śāmbhavopāya", "āktopāya": "Śāktopāya", "ivadrṣṭi": "Śivadrṣṭi", "ivadharmin": "Śivadharmin",
         "ivadharmiṇī": "Śivadharmiṇī", "ikhaṇdin": "Śikhaṇdin", "rīpūrvapañcikā": "Śrīpūrvapañcikā"}
TARGET = re.compile(rf"(?<![{L}\\])(" + "|".join(sorted(WORDS, key=len, reverse=True)) + rf")(?=[’']s|[^{L}]|$)")
PARTICLE = re.compile(r"(so to speak|seemingly|as it were|as if|as though|like)\s*$", re.I)

def line_at(t, s):
    a = t.rfind("\n", 0, s) + 1; b = t.find("\n", s); return a, t[a: b if b >= 0 else len(t)]

def english_line(l):
    ws = re.findall(rf"[{L}]+", l)
    if not ws: return False
    en = sum(1 for w in ws if w.lower() in STOP)
    return (en >= 2 and en / len(ws) >= 0.08) or (len(ws) <= 6 and en >= 1)

def skt(w):
    return bool(w) and w[0].islower() and w.lower() not in EN2 and bool(D.search(w) or SKT_END.search(w))

def u16(s):  # length in UTF-16 code units
    return len(s) + sum(1 for ch in s if ord(ch) > 0xFFFF)

def fnv(s):
    h = 0x811c9dc5
    b = s.encode("utf-16-le")
    for i in range(0, len(b), 2):
        h ^= b[i] | (b[i + 1] << 8); h = (h * 0x01000193) & 0xFFFFFFFF
    return h

def proof(t):
    edits, skipped = [], collections.Counter()
    for m in TARGET.finditer(t):
        w = m.group(1); a, l = line_at(t, m.start())
        if l.lstrip().startswith("#"): skipped["heading"] += 1; continue
        o = t.rfind("[[", 0, m.start()); c = t.rfind("]]", 0, m.start())
        if o > c and t.find("\n", o, m.start()) < 0: skipped["inside a link"] += 1; continue
        if not english_line(l): skipped["sanskrit line"] += 1; continue
        b = re.findall(rf"[{L}]+", t[max(0, m.start() - 40):m.start()]); n = re.findall(rf"[{L}]+", t[m.end():m.end() + 40])
        if skt(b[-1] if b else "") and skt(n[0] if n else ""): skipped["between Sanskrit words"] += 1; continue
        par = t[m.start() - 1:m.start()] == "(" and t[m.end():m.end() + 1] == ")"
        if par and PARTICLE.search(t[max(0, m.start() - 30):m.start() - 1]): skipped["the particle"] += 1; continue
        new = WORDS[w]
        if par and b and b[-1][0].islower() and w.startswith(("akti", "āmbhava", "ākto")): new = "ś" + new[1:]
        edits.append((m.start(), len(w), new, w))
    return edits, skipped

if __name__ == "__main__":
    src, dst, pout, sout = sys.argv[1:5]
    patch, samples, total = [], [], collections.Counter()
    for f in sorted(glob.glob(os.path.join(src, "**", "*.md"), recursive=True)):
        rel = os.path.relpath(f, src)
        t = open(f, encoding="utf-8").read()
        edits, sk = proof(t)
        total.update(sk)
        u = t
        for s, d, new, w in sorted(edits, reverse=True): u = u[:s] + new + u[s + d:]
        os.makedirs(os.path.dirname(os.path.join(dst, rel)), exist_ok=True)
        open(os.path.join(dst, rel), "w", encoding="utf-8").write(u)
        if not edits: continue
        for s, d, new, w in edits:
            total[w] += 1
            pg = list(re.finditer(r"\*\[p\. (\d+)\]\* \^pg(\d+)", t[:s]))
            samples.append({"file": rel, "word": w, "new": new, "page": pg[-1].group(1) if pg else None, "pdfpage": pg[-1].group(2) if pg else None,
                            "context": t[max(0, s - 90):s + d + 60].replace("\n", " ⏎ ")})
        hunks = [[u16(t[:s]), u16(t[s:s + d]), new] for s, d, new, w in edits]
        patch.append({"path": "Library/Trika/Tantraloka (Dyczkowski)/" + rel.replace(os.sep, "/"), "len0": u16(t), "h0": fnv(t), "len1": u16(u), "h1": fnv(u), "hunks": hunks})
    json.dump(patch, open(pout, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(samples, open(sout, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("notes", len(patch), "edits", sum(len(p["hunks"]) for p in patch))
    for k, v in total.most_common(): print(" ", v, k)
