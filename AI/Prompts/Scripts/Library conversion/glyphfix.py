"""Recover characters for glyphs that a PDF's text layer leaves unmapped (U+FFFD).

Evidence used, all from the PDF itself:
  1. the embedded font's own symbol cmap (code 0xF0xx -> glyph): the code is the character, when the font's
     mapped glyphs agree with that rule;
  2. the glyph outline: a known letter of the same font (same shape) plus accent parts whose position and shape
     are measured (dot, macron, acute, grave, tilde, ring, diaeresis), or the same shape as a known glyph.
Results outside a whitelist of letters are dropped; unrecovered glyphs stay U+FFFD (later '[illegible]').
"""
import io, os, re, collections, unicodedata, itertools
import numpy as np
from PIL import Image, ImageDraw
import pymupdf as fitz
from fontTools.ttLib import TTFont
from fontTools.cffLib import CFFFontSet
from fontTools.pens.basePen import BasePen

WHITE = set('āīūṛṝḷḹṃṁḥṅñṭḍṇśṣĀĪŪṚṜḶḸṂṀḤṄÑṬḌṆŚṢēōĒŌáéíóúàèìòùâêîôûäëïöüÿçãõåÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÄËÏÖÜÇÃÕÅṅẏṙṫḋṡżŻ'
            'ǎěǐǒǔĂăĕĭŏŭ') | set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
ISO = {'r̥', 'r̥̄', 'l̥', 'l̥̄', 'R̥', 'm̐'}
DOTB = set('rRlLtTdDnNsShHmMkKzZ')


class FlatPen(BasePen):
    def __init__(self, gs=None):
        super().__init__(gs); self.contours = []; self.cur = None
    def _moveTo(self, p): self.cur = [p]
    def _lineTo(self, p): self.cur.append(p)
    def _curveToOne(self, p1, p2, p3):
        p0 = self.cur[-1]
        for i in range(1, 7):
            t = i / 6; u = 1 - t
            self.cur.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0], u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    def _qCurveToOne(self, p1, p2):
        p0 = self.cur[-1]
        for i in range(1, 6):
            t = i / 5; u = 1 - t
            self.cur.append((u*u*p0[0] + 2*u*t*p1[0] + t*t*p2[0], u*u*p0[1] + 2*u*t*p1[1] + t*t*p2[1]))
    def _closePath(self):
        if self.cur and len(self.cur) > 2: self.contours.append(self.cur)
        self.cur = None
    _endPath = _closePath


class Prog:
    """One embedded font program: outlines by glyph id."""
    def __init__(self, doc, xref):
        self.ok = False; self.sym = {}
        name, ext, typ, buf = doc.extract_font(xref)
        self.name = name.split('+')[-1]
        if not buf: return
        try:
            if ext in ('ttf', 'otf'):
                f = TTFont(io.BytesIO(buf)); self.upm = f['head'].unitsPerEm
                self.glyf = f['glyf']; self.order = f.getGlyphOrder(); self.kind = 'tt'
                glyf = self.glyf
                class _G:
                    def __init__(s, n): s.n = n
                    def draw(s, pen): glyf[s.n].draw(pen, glyf)
                class _GS(dict):
                    def __getitem__(s, n): return _G(n)
                    def __contains__(s, n): return n in glyf.glyphs
                self.gs = _GS()
                try:
                    for t in f['cmap'].tables:
                        if t.platformID == 3 and t.platEncID == 0:
                            for cp, gn in t.cmap.items():
                                if 0xF020 <= cp <= 0xF07E: self.sym.setdefault(f.getGlyphID(gn), chr(cp - 0xF000))
                except Exception: pass
            else:
                cff = CFFFontSet(); cff.decompile(io.BytesIO(buf), None); top = cff[cff.fontNames[0]]
                self.cs = top.CharStrings; self.charset = top.charset; self.kind = 'cff'
                fm = getattr(top, 'FontMatrix', [0.001]); self.upm = round(1 / fm[0]) if fm and fm[0] else 1000
            self.ok = True
        except Exception:
            pass

    def contours(self, gid):
        if not self.ok: return None
        try:
            pen = FlatPen(self.gs if self.kind == 'tt' else None)
            if self.kind == 'tt':
                if gid >= len(self.order): return None
                self.glyf[self.order[gid]].draw(pen, self.glyf)
            else:
                if gid >= len(self.charset): return None
                self.cs[self.charset[gid]].draw(pen)
            return [[(x * 1000 / self.upm, y * 1000 / self.upm) for x, y in c] for c in pen.contours]
        except Exception:
            return None


S = 0.1   # pixels per font unit (1000 units per em -> 100 px)
X0, Y1, W, H = -200, 1300, 220, 200


def raster(contours, dx=0):
    acc = np.zeros((H, W), bool)
    for c in contours:
        im = Image.new('1', (W, H), 0)
        ImageDraw.Draw(im).polygon([((x + dx - X0) * S, (Y1 - y) * S) for x, y in c], fill=1)
        acc ^= np.array(im, bool)
    return acc


def bbox(c):
    xs = [p[0] for p in c]; ys = [p[1] for p in c]
    return min(xs), min(ys), max(xs), max(ys)


def parts(contours):
    bb = [bbox(c) for c in contours]
    def inside(a, b): return a[0] >= b[0] - 1 and a[1] >= b[1] - 1 and a[2] <= b[2] + 1 and a[3] <= b[3] + 1 and a != b
    outer = [i for i in range(len(contours)) if not any(inside(bb[i], bb[j]) for j in range(len(contours)) if j != i)]
    ps = [[i] for i in outer]
    for i in range(len(contours)):
        if i in outer: continue
        for p in ps:
            if inside(bb[i], bb[p[0]]): p.append(i); break
    return [dict(cont=[contours[i] for i in p], bb=bb[p[0]], holes=len(p) - 1) for p in ps]


def iou(a, b):
    u = (a | b).sum()
    return (a & b).sum() / u if u else 0


def classify_mark(m, base_bb):
    x0, y0, x1, y1 = m['bb']; w, h = x1 - x0, max(1, y1 - y0)
    r = raster(m['cont']); ink = r.sum()
    area = max(1, (w * S) * (h * S)); fill = ink / area
    bx0, by0, bx1, by1 = base_bb
    if y0 >= by1 - 0.15 * (by1 - by0) and (y0 + y1) / 2 > by1 * 0.85: pos = 'above'
    elif y1 <= by0 + 30 and (y0 + y1) / 2 < by0: pos = 'below'
    else: return None
    if m['holes']: return '\u030A' if pos == 'above' else '\u0325'
    if fill >= 0.7 and 0.6 <= w / h <= 1.6: return '\u0307' if pos == 'above' else '\u0323'
    if fill >= 0.85 and w / h > 2.0: return '\u0304' if pos == 'above' else '\u0331'
    if pos != 'above': return None
    ys, xs = np.nonzero(r)
    if len(xs) < 5: return None
    xa, xb = xs.min(), xs.max(); hp = max(1, ys.max() - ys.min())
    third = (xb - xa + 1) / 3
    yc = lambda lo, hi: ys[(xs >= lo) & (xs < hi)].mean() if ((xs >= lo) & (xs < hi)).any() else None
    L, Cm, R = yc(xa, xa + third), yc(xa + third, xa + 2 * third), yc(xa + 2 * third, xb + 1)
    if None not in (L, Cm, R):
        if Cm - (L + R) / 2 > 0.2 * hp: return None          # cup: breve or caron (not told apart)
        if (L + R) / 2 - Cm > 0.2 * hp: return '\u0302'      # circumflex
    if w / h > 1.8: return '\u0303'
    top = xs[ys <= ys.min() + hp / 3].mean(); bot = xs[ys >= ys.max() - hp / 3].mean()
    if top - bot > 0.15 * w * S: return '\u0301'
    if bot - top > 0.15 * w * S: return '\u0300'
    return None


def compose(base, marks):
    if not marks: return base if base not in 'ıȷ' else None
    if base in 'ıȷ':
        if all(mk in ('\u0323', '\u0325', '\u0331') for mk in marks): return None
        base = {'ı': 'i', 'ȷ': 'j'}[base]
    s = unicodedata.normalize('NFC', base + ''.join(sorted(marks, key=lambda m: 0 if m in ('̣', '̥', '̱') else 1)))
    if s in WHITE or unicodedata.normalize('NFD', s) in {unicodedata.normalize('NFD', x) for x in ISO}: return s
    return None


DEBUG = False
SUSPECT = set('ƒŠšŸžŽ˜™©®µ¶†‡ˆ‰‹›•–—¨¯´¸¹²³¼½¾¿×÷ÐðÞþ‘’“”„')
PUNCT = set('‘’“”')


def _nm(basefont):
    return basefont.split('+')[-1].replace('-Identity-H', '')


class DocFonts:
    """Font programs of a document grouped into classes that share one glyph-id space (same name and the same
    glyph list), so that a glyph id seen in the text layer can be tied to its outline without guessing."""
    def __init__(self, doc):
        self.doc = doc; self.progs = {}; self.cls = {}; self.members = collections.defaultdict(list); self.page_names = {}

    def prog(self, xref):
        if xref not in self.progs: self.progs[xref] = Prog(self.doc, xref)
        return self.progs[xref]

    def cls_of(self, xref, name):
        if xref not in self.cls:
            p = self.prog(xref)
            if not p.ok: fp = (name, 'x', xref)
            elif p.kind == 'tt': fp = (name, 'tt', len(p.order))
            else: fp = (name, 'cff', tuple(p.charset))
            self.cls[xref] = fp; self.members[fp].append(xref)
        return self.cls[xref]

    def names(self, pn):
        """name -> class for the fonts of page pn (None when two different classes share the name there)."""
        if pn not in self.page_names:
            d = collections.defaultdict(set)
            for f in self.doc[pn].get_fonts():
                nm = _nm(f[3]); d[nm].add(self.cls_of(f[0], nm))
            self.page_names[pn] = {k: (next(iter(v)) if len(v) == 1 else None) for k, v in d.items()}
        return self.page_names[pn]

    def name_char(self, c, gid):
        """The character the font's own glyph name stands for ('sacute' -> ś), or None for made-up names."""
        from fontTools import agl
        for xr in self.members.get(c, []):
            p = self.prog(xr)
            if not p.ok: continue
            try: nm = p.order[gid] if p.kind == 'tt' else p.charset[gid]
            except Exception: continue
            if re.match(r'^(glyph|cid|g|index)\d+$|^uni[EF][0-9A-F]{3}$|^\.notdef$', nm or ''): return None
            u = agl.toUnicode(nm)
            return unicodedata.normalize('NFC', u) if u else None
        return None

    def outline(self, c, gid):
        for xr in self.members.get(c, []):
            o = self.prog(xr).contours(gid)
            if o: return o
        return None


def build_map(doc, pages=None, log=None, df=None):
    """Return ({(class, gid): char}, DocFonts): unmapped glyphs recovered, and wrongly mapped glyphs of old
    transliteration fonts corrected, both from the embedded font outlines."""
    df = df or DocFonts(doc)
    known = collections.defaultdict(collections.Counter); bad = collections.Counter(); occ = {}; ctx = collections.defaultdict(list)
    rng = list(pages if pages is not None else range(len(doc)))
    for pn in rng:
        try: tr = doc[pn].get_texttrace()
        except Exception: continue
        nmap = None
        for sp in tr:
            if not any(c[0] == 0xFFFD or c[0] > 127 for c in sp['chars']) and not re.search('Accent', sp['font']) and nmap is not None and False: continue
            if nmap is None: nmap = df.names(pn)
            c_ = nmap.get(sp['font'])
            if c_ is None: continue
            chs = sp['chars']
            for ci_, c in enumerate(chs):
                if c[1] is None or c[1] < 0: continue
                k_ = (c_, c[1])
                if c[0] == 0xFFFD and len(ctx[k_]) < 40:   # the word around it, for the ligature test
                    gap_ = 0.1 * (sp['size'] or 10)
                    a_ = ci_
                    while a_ > 0 and chr(chs[a_ - 1][0]).isalpha() and chs[a_][3][0] - chs[a_ - 1][3][2] < gap_: a_ -= 1
                    b_ = ci_ + 1
                    while b_ < len(chs) and chr(chs[b_][0]).isalpha() and chs[b_][3][0] - chs[b_ - 1][3][2] < gap_: b_ += 1
                    w_ = ''.join('\x00' if chs[q][0] == 0xFFFD and chs[q][1] == c[1] else chr(chs[q][0]) for q in range(a_, b_))
                    if len(w_) >= 3: ctx[k_].append(w_)
                lo = occ.setdefault(k_, [])
                if len(lo) < 3 and (not lo or lo[-1][0] != pn): lo.append((pn, c[2], sp['size'], c[3]))
                if c[0] == 0xFFFD: bad[k_] += 1
                elif c[0] > 32: known[k_][chr(c[0])] += 1
    suspects = collections.defaultdict(list)
    for (c_, g), cnt in known.items():
        cl = cnt.most_common(1)[0][0]
        if not cl.isascii() and (cl.isalpha() or cl in SUSPECT): suspects[c_].append((g, cl, sum(cnt.values())))
    accents = {c_ for c_, _ in known if re.search(r'Accent', c_[0])}
    out = {}
    if not bad and not suspects and not accents: return out, df
    famk = lambda x: re.sub(r'(Accents?|Expert|Exp|OS)(?=[-,]|$)', '', x)
    for C in set(c_ for c_, _ in bad) | set(suspects) | accents:
        fn = C[0]; kind = C[1]
        if kind == 'x': continue
        kn = {g: cnt.most_common(1)[0][0] for (c_, g), cnt in known.items() if c_ == C}
        sym = {}
        for xr in df.members.get(C, []):
            for g, ch in df.prog(xr).sym.items(): sym.setdefault(g, ch)
        agree = [kn[g] == sym[g] for g in kn if g in sym]
        sym_ok = len(agree) >= 5 and sum(agree) / len(agree) >= 0.9
        for g, claimed, n in [(g_, c__, 0) for (c_, g_), cnt in known.items() if c_ == C for c__ in [cnt.most_common(1)[0][0]]]:
            cnt = known[(C, g)]
            if claimed.isalnum() and len(cnt) > 1 and cnt[claimed] >= 0.6 * sum(cnt.values()) and all(k == claimed or k in SUSPECT for k in cnt) and sym_ok and sym.get(g) == claimed:
                out[(C, g)] = claimed; log is not None and log.append((fn, g, sum(cnt.values()) - cnt[claimed], claimed, 'majority, was ' + ''.join(k for k in cnt if k != claimed)))
        if sym_ok:   # letters the text layer gives as quote marks ('“omānanda'): the font's own cmap says which letter
            for g, claimed, n in suspects.get(C, []):
                if claimed in SUSPECT and not claimed.isalpha() and g in sym and sym[g].isalnum():
                    out[(C, g)] = sym[g]; kn[g] = sym[g]; log is not None and log.append((fn, g, n, sym[g], 'cmap, was ' + claimed))
        refs = []
        if not re.search(r'Accent', fn):   # an accents font's letters are stand-ins for accented ones
            for g, ch in kn.items():
                if len(ch) == 1 and (ch.isascii() and ch.isalnum() or ch in PUNCT):
                    nc = df.name_char(C, g)
                    if (nc and nc != ch) or sum(known[(C, g)].values()) < 2: continue   # a label the font contradicts, or seen once
                    o = df.outline(C, g)
                    if o: refs.append((ch, raster(o), o, g))
        if len(refs) < 10:   # borrow letter shapes from the family font (accents-only or old-style-figure companions)
            for (c2, g2), cnt2 in known.items():
                if c2 != C and c2[1] != 'x' and famk(c2[0]) == famk(fn) and not re.search(r'SC(?=[-,]|$)', c2[0]) and not re.search('Accent', c2[0]):
                    ch2 = cnt2.most_common(1)[0][0]
                    if len(ch2) == 1 and ch2.isascii() and ch2.isalnum() and not any(r_[0] == ch2 for r_ in refs):
                        o2 = df.outline(c2, g2)
                        if o2: refs.append((ch2, raster(o2), o2, None))
        for ch0, rr0, rc0, _g0 in list(refs):   # dotless i and j (for i and j with an accent above)
            if ch0 in 'ij':
                P0 = parts(rc0)
                if len(P0) == 2:
                    big = max(P0, key=lambda p: (p['bb'][3] - p['bb'][1]))
                    refs.append(({'i': 'ı', 'j': 'ȷ'}[ch0], raster(big['cont']), big['cont'], None))
        if not refs: continue

        def derive(g, n):
            c = df.outline(C, g)
            if not c: return None
            P = parts(c)
            if len(P) > 4: return None
            best = None
            order = sorted(range(len(P)), key=lambda i: -(P[i]['bb'][2] - P[i]['bb'][0]) * (P[i]['bb'][3] - P[i]['bb'][1]))
            cands = [set(range(len(P)))]
            for k in range(1, min(3, len(P))):
                for drop in itertools.combinations(order[1:], k): cands.append(set(range(len(P))) - set(drop))
            scores = {}
            for ki, keep in enumerate(cands):
                cont = [cc for i in keep for cc in P[i]['cont']]
                kb = bbox([p for cc in cont for p in cc])
                for ch, rr, rc, rg in refs:
                    if rg == g: continue
                    rb = bbox([p for cc in rc for p in cc])
                    dx = ((rb[0] + rb[2]) - (kb[0] + kb[2])) / 2
                    sc = iou(raster(cont, dx), rr)
                    scores.setdefault(ki, {})
                    if sc > scores[ki].get(ch, (0,))[0]: scores[ki][ch] = (sc, rb[3] - rb[1])
                    if best is None or sc > best[0]: best = (sc, ch, keep, kb, ki)
            if not best or best[0] < 0.8: return None
            sc, ch, keep, kb, ki = best
            if fn.startswith('Fd') and (sc < 0.88 or n < 2): return None   # OCR-made (ClearScan) shapes: only clear, repeated glyphs
            if not fn.startswith('Fd') and sc < 0.95: return None   # real fonts: a known letter's outline is reused almost exactly
            if sc < 0.98:
                # a clear winner: no other letter close; the other case of the same letter decided by height
                other = [v[0] for c2, v in scores[ki].items() if c2.lower() != ch.lower()]
                if other and sc - max(other) < 0.04: return None
                twin = ch.swapcase()
                if twin in scores[ki] and scores[ki][twin][0] >= sc - 0.06:
                    hb = kb[3] - kb[1]
                    ch = min((ch, twin), key=lambda c2: abs(scores[ki][c2][1] - hb))
            marks = []; mparts = [P[i] for i in range(len(P)) if i not in keep]
            for m_ in mparts:
                mk = classify_mark(m_, kb)
                if mk is None: return None
                marks.append(mk)
            if marks == ['̇', '̇'] and abs(mparts[0]['bb'][1] - mparts[1]['bb'][1]) < 40: marks = ['̈']
            if '̣' in marks and ch not in DOTB: return None
            if ch in PUNCT:
                return (ch, float(sc), ch, []) if not marks and sc >= 0.98 else None
            res = compose(ch, marks)
            if res and (marks or sc >= 0.98): return res, float(sc), ch, marks
            return None

        # 1. unmapped glyphs: the font's symbol cmap (when the mapped glyphs agree with it), else the outline
        for (c_, g), n in bad.items():
            if c_ != C: continue
            if sym_ok and g in sym:
                out[(C, g)] = sym[g]; log is not None and log.append((fn, g, n, sym[g], 'cmap')); continue
            r = derive(g, n)
            if r: out[(C, g)] = r[0]; log is not None and log.append((fn, g, n, r[0], round(r[1], 2)))
        # 2. glyphs mapped to the wrong character (old transliteration fonts: 'â' for ṃ, 'ƒ' for ḥ): remapped only
        #    when the outline is an exact known letter plus measured accents and disagrees with the text layer
        cand = suspects.get(C, []) if C not in accents else [(g, cnt.most_common(1)[0][0], sum(cnt.values())) for (c_, g), cnt in known.items() if c_ == C]
        for g, claimed, n in cand:
            r = derive(g, n)
            if DEBUG: print('suspect', fn, g, claimed, n, r)
            if not r: continue
            res, sc, base, marks = r
            if res == unicodedata.normalize('NFC', claimed) or res in PUNCT: continue
            if not re.search('Accent', fn) and df.name_char(C, g) == unicodedata.normalize('NFC', claimed): continue   # the font's glyph name agrees with the text layer
            if unicodedata.name(claimed, 'X').split()[0] in ('GREEK', 'CYRILLIC', 'HEBREW', 'ARABIC', 'ARMENIAN', 'GEORGIAN', 'COPTIC', 'SYRIAC', 'DEVANAGARI'): continue   # other scripts share Latin shapes
            if not marks: continue
            if sc < 0.97: continue
            cd = unicodedata.normalize('NFD', claimed)
            if cd[0].lower() == {'ı': 'i', 'ȷ': 'j'}.get(base, base).lower():
                if not set(marks) <= {'\u0304'} or '\u0304' in cd[1:]: continue   # same letter: only a measured macron overrides another accent
            out[(C, g)] = res; log is not None and log.append((fn, g, n, res, 'was ' + claimed, round(sc, 2)))
    # unmapped ligatures (TeX fonts: 'classi?cation', '?nished'): the glyph is the ligature that turns its words into
    # English words - decided once per glyph, from all its words, and only when nearly all of them agree
    words = _words()
    for k, n in bad.items():
        if k in out or len(ctx.get(k, [])) < 3: continue
        best = None
        for lig in ('fi', 'fl', 'ff', 'ffi', 'ffl'):
            ok_ = sum(1 for w in ctx[k] if w.replace('\x00', lig).lower() in words)
            if best is None or ok_ > best[0]: best = (ok_, lig)
        if best and best[0] >= 0.8 * len(ctx[k]) and best[0] >= 3:
            out[k] = best[1]; log is not None and log.append((k[0][0], k[1], n, best[1], 'ligature by words'))
            occ.pop(k, None); occ[k] = None
    # every mapping is checked against the page as MuPDF renders it: the outline we read for this glyph id must be
    # the ink actually printed at one of its occurrences (guards against glyph ids that do not index the outline table)
    for k in list(out):
        if occ.get(k, 0) is None: continue   # decided by its words, not its outline
        res_ = [_rendered_match(doc, df, k, o_) for o_ in occ.get(k, [])]
        ok = bool(res_) and sum(res_) * 2 > len(res_)
        if not ok:
            del out[k]
            if log is not None:
                for e in log:
                    if e[0] == k[0][0] and e[1] == k[1]: log.remove(e); break
    return out, df


def _rendered_match(doc, df, key, oc):
    if not oc: return False
    C, g = key
    o = df.outline(C, g)
    if not o: return False
    pn, origin, size, bb = oc
    try:
        page = doc[pn]; z = 6
        xs = [origin[0] + x / 1000 * size for c in o for x, _ in c]; ys = [origin[1] - y / 1000 * size for c in o for _, y in c]
        clip = fitz.Rect(min(xs) - 1, min(ys) - 1, max(xs) + 1, max(ys) + 1) & page.rect
        if clip.is_empty or clip.width < 0.5 or clip.height < 0.5: return False
        pm = page.get_pixmap(matrix=fitz.Matrix(z, z), clip=clip, colorspace=fitz.csGRAY)
        ink = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width) < 128
        acc = np.zeros_like(ink)
        for c in o:
            im = Image.new('1', (pm.width, pm.height), 0)
            ImageDraw.Draw(im).polygon([((origin[0] + x / 1000 * size - clip.x0) * z, (origin[1] - y / 1000 * size - clip.y0) * z) for x, y in c], fill=1)
            acc ^= np.array(im, bool)
        if acc.sum() < 4: return False
        dil = ink.copy()   # one pixel of tolerance (anti-aliasing, rounding)
        dil[1:] |= ink[:-1]; dil[:-1] |= ink[1:]; dil[:, 1:] |= ink[:, :-1]; dil[:, :-1] |= ink[:, 1:]
        acd = acc.copy(); acd[1:] |= acc[:-1]; acd[:-1] |= acc[1:]; acd[:, 1:] |= acc[:, :-1]; acd[:, :-1] |= acc[:, 1:]
        prec = (acc & dil).sum() / acc.sum()
        ys_, xs_ = np.nonzero(acc); w_ = xs_.max() - xs_.min()
        win = np.zeros_like(ink); win[ys_.min():ys_.max() + 1, int(xs_.min() + 0.15 * w_):int(xs_.max() - 0.15 * w_) + 1] = True
        rec = (ink & acd & win).sum() / max(1, (ink & win).sum())   # inner columns only: neighbours' overhang left out
        return prec >= 0.85 and rec >= 0.7
    except Exception:
        return False


_MAPS = {}
_W = None


def _words():
    global _W
    if _W is None:
        _W = set(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'en_words.txt'), encoding='utf-8').read().split())
    return _W


def doc_map(doc):
    k = id(doc)
    if k not in _MAPS: _MAPS[k] = build_map(doc)
    return _MAPS[k]


def repair_page(page, doc, rawdict):
    """Replace characters in a rawdict by recovered or corrected ones (matched to glyphs by their origin)."""
    m, df = doc_map(doc)
    if not m: return 0
    nmap = df.names(page.number)
    pos = {}
    for sp in page.get_texttrace():
        c_ = nmap.get(sp['font'])
        if c_ is None: continue
        for c in sp['chars']:
            r = m.get((c_, c[1]))
            if r: pos[(round(c[2][0], 1), round(c[2][1], 1))] = r
    n = 0
    if not pos: return 0
    for b in rawdict['blocks']:
        for l in b.get('lines', []):
            for s in l['spans']:
                for ch in s['chars']:
                    if not ch['c'].isspace():
                        r = pos.get((round(ch['origin'][0], 1), round(ch['origin'][1], 1)))
                        if r: ch['c'] = r; n += 1
    return n
