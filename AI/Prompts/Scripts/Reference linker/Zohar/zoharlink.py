#!/usr/bin/env python3
"""Zohar reference linker (library + command line).

Turns plain Zohar folio references in Obsidian note text into links to the
Pritzker notes of the vault, following the rule Stephen set on 26 Oct 2026:

  * A reference counts only when it is introduced by "Zohar" (italic or not)
    or "ZH" / "Zohar Hadash", or continues a list so introduced
    ("*Zohar* 1:76b, 97a; 2:3b" is three references).  A bare folio takes the
    last volume given earlier in the same list.
  * Where several notes carry the same folio, the composition named after the
    reference decides the target: the parenthesis right after the item
    ("(*ST*)") or a group parenthesis that covers it ("(both *ST*)",
    "(last two *Heikh*)", "(all *Tos*)").
  * With no composition named, the target is the sole note holding the block,
    or, where several hold it, the main-text (volumes 1-9) note.  A range
    ("2:176b-179a") prefers the note that holds its last folio too.
  * Otherwise the reference is left alone and listed: undecided (the text does
    not decide between holders) or noblock (no note holds the block, or the
    composition named is not in the vault: RM, TZ, Tiq, Tosafot ...).

Form of a link: `[[Zohar 2.06 - Parashat Va-Yetse#^z1-156a|1:156a]]`; the label
is exactly the printed text of the item and the italic "*Zohar*" stays outside.
Where a note already writes non-italic links with the word in the label
(`[[...|Zohar 2:176b]]`, `[[...|Zohar III, 137b]]`) the same form is kept.

Nothing else on a line is changed.  Frontmatter, headings, code, existing links
and link labels are never touched.

Standard library only.  See README.md for the commands.
"""
import json
import os
import re
import sys

# ----------------------------------------------------------------------------
# Composition table
# ----------------------------------------------------------------------------

# family -> list of note-number prefixes ("11.09") whose notes may be the target
COMPOSITIONS = {
    "ST": ["11.09"],
    "Tos": ["11.08", "12.12"],
    "Mat": ["11.07"],
    "MhN": ["10.03", "10.04", "10.05", "10.06", "10.07", "10.08", "10.09",
            "10.10", "10.11", "11.03", "11.04", "11.05"],
    "MhN-Rut": ["11.04"],
    "MhN-Eikhah": ["11.05"],
    "MhN-ShS": ["11.03"],
    "ShS": ["11.06"],
    "Heikh": ["12.04", "12.05"],
    "Piq": ["12.06"],
    "RR": ["12.07"],
    "SO": ["12.08"],
    "QhM": ["12.09"],
    "MY": ["12.10"],
    "IR": ["8.09"],
    "IZ": ["9.15"],
    "SdTs": ["5.06"],
    "SdM": ["5.03", "5.04"],   # Sava de-Mishpatim: 2:94b-114a sits in 5.03; 5.04 carries the title
    "Yan": ["9.09"],
    "RavM": ["9.04"],
}

# token regex (applied to the parenthesis text with asterisks removed) -> family
COMP_TOKENS = [
    (r"\bST\b|Sitrei Torah", "ST"),
    (r"\bTos\b|Tosefta\b", "Tos"),
    (r"\bMat\b|Matnitin", "Mat"),
    (r"\bM[hn][Nn]\b|Midrash ha-Ne[’'ʾ]lam", "MhN"),
    (r"\bRut\b|\bRuth\b", "Rut"),            # qualifier of MhN
    (r"\bEikhah\b|\bEikha\b", "Eikhah"),      # qualifier of MhN
    (r"\bShS\b|Shir ha-Shirim", "ShS"),
    (r"\bHeikh\b|Heikhalot", "Heikh"),
    (r"\bPiq\b|Piqqudin", "Piq"),
    (r"\bRR\b|Raza de-Razin", "RR"),
    (r"\bSO\b|Sitrei Otiyyot", "SO"),
    (r"\bQhM\b|Qav ha-Middah", "QhM"),
    (r"Merkevet Ye[hḥ]ezqel|Merkavat Ye[hḥ]ezqel", "MY"),
    (r"\bIR\b|Idra Rabba", "IR"),
    (r"\bIZ\b|Idra Zuta", "IZ"),
    (r"\bSdTs\b|Sifra di-Tsni[’'ʿ]?uta", "SdTs"),
    (r"Sava de-Mishpatim", "SdM"),
    (r"\bYanuqa\b", "Yan"),
    (r"Rav Metivta", "RavM"),
]

# compositions named in the sources that the vault does not hold as notes
RM_NAME = r"Ra[’'ʿ]?a?y[ao]\s+Meh?e?i?mna"      # Ra'aya Meheimna and its spellings
ABSENT_TOKENS = [
    (r"\bRM\b|%s" % RM_NAME, "RM"),
    (r"\bTZ\b|Ti[qk]{1,2}unei ha-Zohar|Ti[qk]{1,2}unei Zohar", "TZ"),
    (r"\bTiq\b|\bTiqqunim\b|\bTikkunim\b", "Tiq"),
    (r"\bTosafot\b", "Tosafot"),
]

GROUP_NUM = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
             "seven": 7, "eight": 8, "nine": 9, "ten": 10, "2": 2, "3": 3,
             "4": 4, "5": 5}

ROMAN = {"I": 1, "II": 2, "III": 3}

# ----------------------------------------------------------------------------
# Regexes
# ----------------------------------------------------------------------------

LINK_RE = re.compile(r"\[\[([^\]\|]+?)(?:\\?\|([^\]]*?))?\]\]")
CODE_RE = re.compile(r"`[^`]*`")

# introducers.  group 'zh' = Zohar Hadash, 'z' = main Zohar
INTRO_RE = re.compile(
    r"(?P<intro>(?P<zh>\*?(?:Z[ḤḥH]|Zohar\s+[Ḥḥ]adash)\*?)|(?P<z>\*?Zohar\*?))"
    r"(?P<sep>,?\s+)")

VOL = r"(?:(?P<vol>[1-3]|I{1,3})\s?[:.,]\s?)"
ITEM_Z = re.compile(
    VOL + r"?(?P<f>(?!0)\d{1,3})(?P<l>[ab])"
    r"(?:(?P<dash>[–\-])(?:(?P<f2>(?!0)\d{1,3})(?P<l2>[ab])|(?P<l3>[ab])))?"
    r"(?![\w])")
ITEM_ZH = re.compile(
    r"(?P<f>(?!0)\d{1,3})(?P<l>[a-d])"
    r"(?:(?P<dash>[–\-])(?:(?P<f2>(?!0)\d{1,3})(?P<l2>[a-d])|(?P<l3>[a-d])))?"
    r"(?![\w])")
PAREN_RE = re.compile(
    r"\s*(?:\((?P<p>[^()]*(?:\([^()]*\)[^()]*)*)\)|\\\[(?P<b>[^\[\]]*)\\\])")
SEP_RE = re.compile(r"(?:,\s+and\s+|,\s+|;\s+|\s+and\s+|\s*&\s*|\s+)")
# words that, right before "Zohar", mean another work (Nitsotsei Zohar, Tiqqunei Zohar)
NOT_INTRO_BEFORE = re.compile(
    r"(Nitsotsei|Ti[qk]{1,2}unei|Ti[qk]{1,2}une|Or|Peirush|Sefer|ha|de|Matoq)\s*\*?\s*$")
GROUP_RE = re.compile(
    r"^\s*(?:the\s+)?(?P<w>both|all|last|latter|first)\b\s*(?P<n>two|three|four|five|six|seven|eight|nine|ten|\d)?",
    re.I)


# The four-letter divine name, in Hebrew (with or without points) or in Latin
# letters (written as character classes, so the name itself never stands in this file).  House rule: never written into a new file; a line that holds it is
# referred to by path and line number, and its edits are given by offset.
DIVINE_NAME_RE = re.compile(
    r"\u05d9[\u0591-\u05c7]*\u05d4[\u0591-\u05c7]*\u05d5[\u0591-\u05c7]*\u05d4"
    r"|\b[Y][\-\s]?[H][\-\s]?[VW][\-\s]?[H]\b|\b[JI][H][V][H]\b|\b[Y]ah[wv]eh\b|\b[J]eho[v]ah\b|\b[J]ah[w]eh\b",
    re.I)


def holds_divine_name(s):
    return bool(DIVINE_NAME_RE.search(s))


def hidden(path, line_no):
    """Placeholder used instead of quoting a line that holds the divine name."""
    return "(text not quoted: the line holds the divine name; see %s L%d)" % (path, line_no)


# ----------------------------------------------------------------------------
# Index of blocks
# ----------------------------------------------------------------------------

class Index:
    """Which note holds which folio block; which notes are main text."""

    def __init__(self, meta_path):
        meta = json.load(open(meta_path, encoding="utf-8"))
        self.blocks = {}      # note path -> set of ids
        self.holders = {}     # id -> [note paths]
        for path, ids in meta["blocks"].items():
            s = set(ids)
            self.blocks[path] = s
            for i in ids:
                if re.match(r"^(z[123]|zh)-\d+[a-d]$", i):
                    self.holders.setdefault(i, []).append(path)
        for i in self.holders:
            self.holders[i].sort()
        self.folio_notes = set(meta.get("folioNotes", []))

    @staticmethod
    def note_number(path):
        m = re.search(r"/Zohar (\d{1,2}\.\d{2}) - ", path)
        return m.group(1) if m else None

    @staticmethod
    def is_main_text(path):
        """Volumes 1-9 of the Pritzker edition: the running text."""
        n = Index.note_number(path)
        return bool(n) and int(n.split(".")[0]) <= 9

    def notes_of(self, family):
        nums = COMPOSITIONS.get(family, [])
        return [p for p in self.blocks if self.note_number(p) in nums]

    @staticmethod
    def basename(path):
        b = path.rsplit("/", 1)[-1]
        return b[:-3] if b.endswith(".md") else b


# ----------------------------------------------------------------------------
# Parenthesis classification
# ----------------------------------------------------------------------------

def _find_token(rx, t):
    """Abbreviations (ST, Tos, MhN ...) match case-sensitively; a full name
    ("idra rabba", "ra'aya meheimna") matches in any case."""
    for alt in rx.split("|"):
        flags = 0 if alt.startswith("\\b") and len(alt) <= 14 else re.I
        for m in re.finditer(alt, t, flags):
            yield m


def composition_before(before):
    """A composition named right before the introducer, by its full name:
    "the Idra Rabba (Zohar 3:127b-145a", "*Idra Zuta, Zohar 3:292b*",
    "the *Saba* (Zohar II, 100b)".  Returns (kind, family) or (None, None)."""
    tail = before[-60:]
    glue = r"\*?[,:]?\s*[(\[]?\s*\*?$"
    for rx, fam in NAME_TOKENS:
        if re.search(r"(?<![A-Za-z-])(?:%s)%s" % (rx, glue), tail, re.I):
            return "comp", fam
    for rx, fam in ABSENT_NAME_TOKENS:
        if re.search(r"(?<![A-Za-z-])(?:%s)%s" % (rx, glue), tail, re.I):
            return "absent", fam
    return None, None


# full names that may stand right before the introducer
NAME_TOKENS = [
    (r"Sitrei Torah", "ST"), (r"Tosefta", "Tos"), (r"Matnitin", "Mat"),
    (r"Midrash ha-Ne[’'ʾ]lam", "MhN"), (r"Heikhalot", "Heikh"), (r"Piqqudin", "Piq"),
    (r"Raza de-Razin", "RR"), (r"Sitrei Otiyyot", "SO"), (r"Qav ha-Middah", "QhM"),
    (r"Merkevet Ye[hḥ]ezqel", "MY"), (r"Idra Rabba", "IR"), (r"Idra Zuta", "IZ"),
    (r"Sifra di-Tsni[’'ʿ]?uta", "SdTs"), (r"Tsni[’'ʿ]?uta de-Sifra", "SdTs"),
    (r"Sava de-Mishpatim", "SdM"), (r"Sa[bv]a", "SdM"), (r"Yanuqa", "Yan"), (r"Rav Metivta", "RavM"),
]
ABSENT_NAME_TOKENS = [
    (RM_NAME, "RM"),
    (r"Ti[qk]{1,2}unei (?:ha-)?Zohar", "TZ"), (r"Ti[qk]{1,2}unim", "Tiq"), (r"Tosafot", "Tosafot"),
]


def classify_paren(text):
    """Return (kind, family, group_n) for the text inside a parenthesis.

    kind: 'comp' (a composition in the vault), 'absent' (a composition the
    vault lacks), 'ambiguous' (two compositions, text does not say which),
    None (nothing deciding: Hash, SA, 'standard edition', 'Vol. 5, n. 3' ...).
    group_n: None for an immediate parenthesis, an integer for "both"/"last N",
    -1 for "all".
    """
    t = text.replace("*", "")
    group = None
    gm = GROUP_RE.match(t)
    if gm:
        w = gm.group("w").lower()
        n = gm.group("n")
        if n:
            group = GROUP_NUM[n.lower()]
        elif w == "both":
            group = 2
        elif w == "all":
            group = -1
        else:
            group = None  # "last" / "first" without a number: no group
        if w == "first":
            group = ("first", group)
    found = []
    for rx, fam in COMP_TOKENS:
        for m in _find_token(rx, t):
            found.append((m.start(), fam))
    absent = []
    for rx, fam in ABSENT_TOKENS:
        for m in _find_token(rx, t):
            absent.append((m.start(), fam))
    found.sort()
    fams = []
    for _, f in found:
        if f not in fams:
            fams.append(f)
    # MhN qualifiers
    quals = [f for f in fams if f in ("Rut", "Eikhah")]
    core = [f for f in fams if f not in ("Rut", "Eikhah")]
    if "MhN" in core and "ShS" in core:
        core = ["MhN-ShS" if f == "MhN" else f for f in core if f != "ShS"]
    if quals:
        q = quals[0]
        if "MhN" in core:
            core = ["MhN-" + q if f == "MhN" else f for f in core]
        else:
            core = ["MhN-" + q] + core
    if not core:
        if absent:
            return "absent", absent[0][1], group
        return None, None, group
    if len(core) == 1:
        return "comp", core[0], group
    if re.search(r"in fact|actually|really|correctly", t):
        return "comp", core[-1], group
    if re.search(r"label|mistaken|erroneous|wrongly", t):
        return "comp", core[0], group
    return "ambiguous", "/".join(core), group


# ----------------------------------------------------------------------------
# Line parsing
# ----------------------------------------------------------------------------

class Ref:
    __slots__ = ("kind", "vol", "f", "l", "f2", "l2", "label", "pstart", "pend",
                 "rstart", "rend", "inlink", "incode", "paren", "paren_kind",
                 "paren_fam", "group", "comp", "comp_src", "intro", "intro_italic",
                 "intro_pstart", "intro_rstart", "first", "bracketed")

    def __init__(self):
        for s in self.__slots__:
            setattr(self, s, None)

    @property
    def block(self):
        if self.kind == "zh":
            return "zh-%d%s" % (self.f, self.l)
        return "z%d-%d%s" % (self.vol, self.f, self.l)

    @property
    def end_folio(self):
        """The folio number the range ends on; '244b-45a' means 245a."""
        if self.f2 is None:
            return self.f
        f2 = self.f2
        if f2 < self.f:
            d = 10 ** len(str(f2))
            f2 = self.f - self.f % d + f2
            if f2 < self.f:
                f2 += d
        return f2

    @property
    def end_block(self):
        if self.f2 is None and self.l2 is None:
            return None
        f2 = self.end_folio
        if self.kind == "zh":
            return "zh-%d%s" % (f2, self.l2)
        return "z%d-%d%s" % (self.vol, f2, self.l2)

    @property
    def text(self):
        return ("ZḤ " if self.kind == "zh" else "Zohar ") + self.label


def plain_view(line):
    """Plain text of a line (links replaced by their labels) with maps back.

    Returns (plain, raw_index, inlink, incode) where raw_index[i] is the raw
    offset of plain char i, and inlink/incode flag plain chars that sit inside
    an existing link or inline code.
    """
    spans = []
    for m in LINK_RE.finditer(line):
        spans.append((m.start(), m.end(), "link", m))
    for m in CODE_RE.finditer(line):
        if not any(a <= m.start() < b for a, b, _, _ in spans):
            spans.append((m.start(), m.end(), "code", m))
    spans.sort()
    plain = []
    rawidx = []
    inlink = []
    incode = []
    pos = 0
    for a, b, kind, m in spans:
        if a < pos:
            continue
        seg = line[pos:a]
        plain.append(seg)
        rawidx.extend(range(pos, a))
        inlink.extend([False] * len(seg))
        incode.extend([False] * len(seg))
        if kind == "link":
            lab = m.group(2) if m.group(2) is not None else m.group(1)
            # raw offset of the label inside the link
            off = m.start() + line[m.start():m.end()].find(lab)
            plain.append(lab)
            rawidx.extend(range(off, off + len(lab)))
            inlink.extend([True] * len(lab))
            incode.extend([False] * len(lab))
        else:
            seg = line[a:b]
            plain.append(seg)
            rawidx.extend(range(a, b))
            inlink.extend([False] * len(seg))
            incode.extend([True] * len(seg))
        pos = b
    seg = line[pos:]
    plain.append(seg)
    rawidx.extend(range(pos, len(line)))
    inlink.extend([False] * len(seg))
    incode.extend([False] * len(seg))
    rawidx.append(len(line))
    return "".join(plain), rawidx, inlink, incode


HEADWORD_RE = re.compile(r"(?:^|\]\s+|\s{2,})\*\*\*([^*]+?)\*\*\*")   # glossary entry head


def parse_line(line):
    """Find every Zohar / Zohar Hadash reference in a line.

    A glossary line that opens with a bold-italic headword naming a composition
    ("***Qav ha-Middah*** ... *Zohar Hadash* 56d-58d") names that composition
    for every reference on the line that has none of its own.

    Returns a list of lists: one list of Ref per introduced run (a "list" in the
    source), in order of appearance.  Items already inside links are included
    (they carry the volume) but flagged inlink.
    """
    plain, rawidx, inlink, incode = plain_view(line)
    runs = []
    pos = 0
    n = len(plain)
    while pos < n:
        m = INTRO_RE.search(plain, pos)
        if not m:
            break
        kind = "zh" if m.group("zh") else "z"
        start = m.start("intro")
        # guards on what precedes the introducer
        before = plain[:start]
        prev = before[-1:] if before else ""
        if prev and (prev.isalnum() or prev in "-’'_/"):
            pos = m.end("intro")
            continue
        if before.endswith("[") and not m.group("intro").startswith("*"):
            pos = m.end("intro")      # a folio marker such as "**[ZH 3a]** ^zh-3a"
            continue
        if kind == "z" and NOT_INTRO_BEFORE.search(before[-25:]):
            pos = m.end("intro")
            continue
        tiq = False
        if kind == "zh" and (re.search(r"Ti[qk]{1,2}unei\s*(?:ha-)?\*?\s*$", before[-25:]) or
                             re.search(r"Ti[qk]{1,2}un[^;.]{0,40}\b(?:of|in)\s+\*?$", before[-70:])):
            tiq = True       # "Tiqqunei Zohar Hadash 24c", "the Tiqqunim of Zohar Hadash 26a"
        if any(incode[start:m.end()]):
            pos = m.end("intro")
            continue
        intro_text = m.group("intro")
        italic = intro_text.startswith("*") or intro_text.endswith("*") or \
            (before.rstrip().endswith("*") and not before.rstrip().endswith("**"))
        # a comma between Zohar and the item only with a Roman volume ("Zohar, I, 186a")
        sep = m.group("sep")
        p = m.end()
        item_re = ITEM_ZH if kind == "zh" else ITEM_Z
        refs = []
        vol = None
        first = True
        while True:
            im = item_re.match(plain, p)
            if not im:
                break
            if kind == "z":
                v = im.group("vol")
                if first:
                    if v is None:
                        break
                    if sep.startswith(",") and v not in ROMAN:
                        break
                if v is not None:
                    vol = ROMAN.get(v, None) or int(v)
            r = Ref()
            r.kind = kind
            r.vol = vol
            r.f = int(im.group("f"))
            r.l = im.group("l")
            if im.group("f2"):
                r.f2 = int(im.group("f2"))
                r.l2 = im.group("l2")
            elif im.group("l3"):
                r.f2 = None
                r.l2 = im.group("l3")
            r.pstart, r.pend = im.start(), im.end()
            r.label = plain[r.pstart:r.pend]
            r.inlink = any(inlink[r.pstart:r.pend])
            r.incode = any(incode[r.pstart:r.pend])
            r.rstart = rawidx[r.pstart]
            r.rend = rawidx[r.pend - 1] + 1
            r.intro = intro_text
            r.intro_italic = italic
            r.intro_pstart = start
            r.intro_rstart = rawidx[start]
            r.first = first
            r.bracketed = (r.pstart > 0 and plain[r.pstart - 1] == "[")
            p = r.pend
            if plain.startswith("*", p) and not plain.startswith("**", p):
                p += 1          # closing italic: "*ZH 17d* (*MhN*)"
            # parenthesis right after the item
            pm = PAREN_RE.match(plain, p)
            if pm:
                ptext = pm.group("p") if pm.group("p") is not None else pm.group("b")
                r.paren = ptext
                r.paren_kind, r.paren_fam, r.group = classify_paren(ptext)
                p = pm.end()
            if tiq:
                r.paren_kind, r.paren_fam = "absent", "Tiq"
                r.group = None
                r.paren = r.paren or "Tiqqunim named before the introducer"
            refs.append(r)
            first = False
            sm = SEP_RE.match(plain, p)
            if not sm:
                break
            p = sm.end()
        if refs:
            runs.append(refs)
            pos = refs[-1].pend
        else:
            pos = m.end("intro")
    # apply the compositions: immediate first, then group coverage
    for refs in runs:
        for r in refs:
            if r.paren is not None and r.group is None and r.paren_kind in ("comp", "absent", "ambiguous"):
                r.comp = r.paren_fam
                r.comp_src = r.paren_kind
        for k, r in enumerate(refs):
            if r.paren is None or r.group is None:
                continue
            if r.paren_kind is None:
                continue
            fam, kind_ = r.paren_fam, r.paren_kind
            g = r.group
            if isinstance(g, tuple):          # ("first", n)
                n = g[1] if g[1] and g[1] > 0 else len(refs)
                targets = [x for x in refs[:n]]
            else:
                targets = []
                j = k
                while j >= 0:
                    x = refs[j]
                    if x.comp is not None and j != k:
                        break
                    if x.comp is None:
                        targets.append(x)
                    if g != -1 and len(targets) >= g:
                        break
                    j -= 1
            for x in targets:
                if x.comp is None:
                    x.comp = fam
                    x.comp_src = kind_ + "-group"
    for refs in runs:
        r0 = refs[0]
        pk, pf = composition_before(plain[:r0.intro_pstart])
        if pk:
            for r in refs:
                if r.comp is None:
                    r.comp = pf
                    r.comp_src = pk + "-before"
    heads = [(hm.end(), hm.group(1)) for hm in HEADWORD_RE.finditer(plain)]
    for refs in runs:
        if not heads:
            break
        prior = [h for h in heads if h[0] <= refs[0].intro_pstart]
        if not prior:
            continue
        hk, hf, _ = classify_paren(prior[-1][1])
        if hk in ("comp", "absent"):
            for r in refs:
                if r.comp is None:
                    r.comp = hf
                    r.comp_src = hk + "-headword"
    return runs


# ----------------------------------------------------------------------------
# Resolution
# ----------------------------------------------------------------------------

def resolve(ref, index):
    """Return (status, note_path, rule) for a Ref.

    status: 'link', 'undecided', 'noblock'.
    """
    blk = ref.block
    holders = index.holders.get(blk, [])
    end = ref.end_block
    comp = ref.comp
    if ref.comp_src and ref.comp_src.startswith("absent"):
        return ("noblock", None, "composition %s not in the vault" % comp)
    if ref.comp_src and ref.comp_src.startswith("ambiguous"):
        return ("undecided", None, "parenthesis names two compositions (%s)" % comp)
    if comp is None:
        if not holders:
            return ("noblock", None, "no note holds %s" % blk)
        main = [h for h in holders if index.is_main_text(h)]
        cands = main if main else holders
        if end:
            both = [h for h in cands if end in index.blocks[h]]
            if len(both) == 1:
                if len(cands) == 1:
                    return ("link", both[0], "sole holder" if len(holders) == 1 else "main text (no composition named)")
                return ("link", both[0], "range: holds first and last folio")
        if len(holders) == 1:
            return ("link", holders[0], "sole holder")
        if len(main) == 1:
            return ("link", main[0], "main text (no composition named)")
        names = ", ".join(index.note_number(h) or index.basename(h) for h in cands)
        return ("undecided", None, "%s held by %s; no composition named" % (blk, names))
    cands = [h for h in index.notes_of(comp) if blk in index.blocks[h]]
    if len(cands) == 1:
        return ("link", cands[0], "composition %s" % comp)
    if not cands:
        who = ", ".join(index.note_number(h) or index.basename(h) for h in holders) or "no note"
        return ("noblock", None, "%s named, but its note(s) hold no %s (%s holds it)" % (comp, blk, who)
                if holders else "%s named, and no note holds %s" % (comp, blk))
    if end:
        both = [h for h in cands if end in index.blocks[h]]
        if len(both) == 1:
            return ("link", both[0], "composition %s; range decides between its notes" % comp)
    names = ", ".join(index.note_number(h) for h in cands)
    return ("undecided", None, "%s named, held by %s" % (comp, names))


# ----------------------------------------------------------------------------
# Note style (does the note put "Zohar" inside its link labels?)
# ----------------------------------------------------------------------------

def label_style_counts(text):
    """(links whose label carries the word Zohar/ZH, links whose label is the
    folio only) among the note's existing Zohar folio links."""
    with_intro = without = 0
    for m in LINK_RE.finditer(text):
        tgt, lab = m.group(1), m.group(2)
        if lab is None or "#^z" not in tgt:
            continue
        if re.match(r"\*?(Zohar|Z[Ḥḥ])\b", lab):
            with_intro += 1
        else:
            without += 1
    return with_intro, without


def label_style(text):
    """'intro' if the note's existing Zohar folio links carry the word in the
    label (`[[...|Zohar 2:176b]]`), 'item' if they carry the folio only, or None
    when the note has no such links."""
    with_intro, without = label_style_counts(text)
    if with_intro == 0 and without == 0:
        return None
    return "intro" if with_intro > without else "item"


# ----------------------------------------------------------------------------
# Driver over a note
# ----------------------------------------------------------------------------

# the vault's own index notes: their folio spans describe notes, they are not citations
SKIP_NOTES = {"Texts/Zohar/Zohar.md", "Texts/Zohar/Zohar folio index.md",
              "Texts/Zohar/Sefaria/Zohar (Soncino).md", "Vault Guide.md"}


def link_note(path, text, index, style=None, only_lines=None, scope=None):
    """Propose links for one note.

    Returns (changes, links, undecided, noblock) where changes is a list of
    [line_no, old, new] and links a list of row dicts.
    scope: optional function(ref) -> bool; refs for which it is False are
    ignored altogether (used to separate the vol. 11 run from the rest).
    """
    lines = text.split("\n")
    if path in SKIP_NOTES:
        return [], [], [], []
    if style is None:
        style = label_style(text) or "item"
    changes, links, undecided, noblock = [], [], [], []
    in_front = False
    in_code = False
    for i, line in enumerate(lines, 1):
        if i == 1 and line.strip() == "---":
            in_front = True
            continue
        if in_front:
            if line.strip() == "---":
                in_front = False
            continue
        if line.lstrip().startswith("```") or line.lstrip().startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.lstrip().startswith("#"):
            continue
        if only_lines is not None and i not in only_lines:
            continue
        if "Zohar" not in line and "ZḤ" not in line and "Zḥ" not in line and "ZH" not in line:
            continue
        runs = parse_line(line)
        if not runs:
            continue
        is_table = line.lstrip().startswith("|")
        edits = []  # (rstart, rend, replacement)
        for refs in runs:
            for r in refs:
                if scope is not None and not scope(r):
                    continue
                row = {"path": path, "line": i, "label": r.label, "block": r.block,
                       "composition": r.comp, "text": r.text, "pstart": r.pstart}
                if r.inlink or r.incode:
                    continue
                if r.bracketed:
                    row["why"] = "printed inside square brackets"
                    undecided.append(row)
                    continue
                status, note, rule = resolve(r, index)
                row["rule"] = rule
                if status == "link":
                    name = index.basename(note)
                    pipe = "\\|" if is_table else "|"
                    label = r.label
                    rs = r.rstart
                    if r.first and not r.intro_italic and style == "intro":
                        label = line[r.intro_rstart:r.rend]
                        rs = r.intro_rstart
                    new = "[[%s#^%s%s%s]]" % (name, r.block, pipe, label)
                    edits.append((rs, r.rend, new))
                    row.update({"target": name, "block": r.block, "label": label,
                                "pstart": r.pstart - (r.rstart - rs)})
                    links.append(row)
                elif status == "undecided":
                    row["why"] = rule
                    undecided.append(row)
                else:
                    row["why"] = rule
                    hs = index.holders.get(r.block, [])
                    if len(hs) == 1:
                        row["sole_holder"] = index.basename(hs[0])
                    noblock.append(row)
        if edits:
            edits.sort()
            out = []
            pos = 0
            ok = True
            for a, b, rep in edits:
                if a < pos:
                    ok = False
                    break
                out.append(line[pos:a])
                out.append(rep)
                pos = b
            if not ok:
                continue
            out.append(line[pos:])
            new = "".join(out)
            if new != line:
                changes.append([i, line, new, [[a, b, rep] for a, b, rep in edits]])
    return changes, links, undecided, noblock


def split_changes(changes):
    """Separate a note's changes into the plain form [line, old, new] and, for
    lines that hold the divine name, the offset form
    {line, oldLen, oldSha1, edits: [[start, end, replacement], ...]}."""
    import hashlib
    plain, by_offset = [], []
    for ln, old, new, edits in changes:
        if holds_divine_name(old):
            by_offset.append({"line": ln, "oldLen": len(old),
                              "oldSha1": hashlib.sha1(old.encode("utf-8")).hexdigest(),
                              "edits": edits})
        else:
            plain.append([ln, old, new])
    return plain, by_offset


def check_proposal(old, new, index):
    """Sanity checks on one proposed line change: only links added, every new
    link resolvable.  Returns a list of problems (empty = fine)."""
    probs = []
    po = LINK_RE.sub(lambda m: m.group(2) if m.group(2) is not None else m.group(1), old)
    pn = LINK_RE.sub(lambda m: m.group(2) if m.group(2) is not None else m.group(1), new)
    if po != pn:
        probs.append("plain text differs")
    old_links = [m.group(0) for m in LINK_RE.finditer(old)]
    new_links = [m.group(0) for m in LINK_RE.finditer(new)]
    for l in old_links:
        if l not in new_links:
            probs.append("existing link changed: " + l)
    for m in LINK_RE.finditer(new):
        if m.group(0) in old_links:
            continue
        tgt = m.group(1)
        if "#^" not in tgt:
            probs.append("new link without block: " + m.group(0))
            continue
        name, blk = tgt.split("#^", 1)
        paths = [p for p in index.blocks if index.basename(p) == name]
        if len(paths) != 1 or blk not in index.blocks[paths[0]]:
            probs.append("unresolvable: " + m.group(0))
    if "[[[" in new and "[[[" not in old:
        probs.append("opening triple bracket")
    return probs


# ----------------------------------------------------------------------------
# Command line
# ----------------------------------------------------------------------------

def main(argv):
    if len(argv) < 3 or argv[1] not in ("run", "parse"):
        print(__doc__)
        print("usage: zoharlink.py run META NOTES.json OUTDIR [--vol11 both|only|none]")
        print("       zoharlink.py parse META 'line of text'")
        return 2
    if argv[1] == "parse":
        index = Index(argv[2])
        line = " ".join(argv[3:])
        for refs in parse_line(line):
            for r in refs:
                print(r.text, r.block, "comp=%s" % r.comp, "inlink=%s" % r.inlink, resolve(r, index))
        return 0
    meta, notes_path, outdir = argv[2], argv[3], argv[4]
    index = Index(meta)
    notes = json.load(open(notes_path, encoding="utf-8"))
    os.makedirs(outdir, exist_ok=True)
    proposals, links, und, nob = {}, [], [], []
    for path in sorted(notes):
        ch, lk, u, nb = link_note(path, notes[path], index)
        if ch:
            plain, by_offset = split_changes(ch)
            proposals[path] = {"changes": plain}
            if by_offset:
                proposals[path]["changes_by_offset"] = by_offset
        links += lk
        und += u
        nob += nb
    json.dump(proposals, open(os.path.join(outdir, "proposals.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(links, open(os.path.join(outdir, "links.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(und, open(os.path.join(outdir, "undecided.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(nob, open(os.path.join(outdir, "noblock.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("notes changed %d, links %d, undecided %d, noblock %d" % (len(proposals), len(links), len(und), len(nob)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
