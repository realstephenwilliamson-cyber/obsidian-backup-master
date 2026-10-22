#!/usr/bin/env python3
"""Phase 4 converter: one PDF -> a book folder of Markdown notes with page anchors.
usage: conv.py JOB.json   (JOB: see make_job in run.py)
Writes OUT/<folder>/<notes>.md and OUT/<folder>/_report.json
"""
import sys, os, re, json, statistics, subprocess, tempfile, unicodedata, collections, datetime
import pymupdf as fitz
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glyphfix

HERE = os.path.dirname(os.path.abspath(__file__))
EN = set(open(os.path.join(HERE, 'en_words.txt'), encoding='utf-8').read().split())
IAST = set('āīūṛṝḷḹṃṁḥṅñṭḍṇśṣĀĪŪṚṜḶṂṀḤṄÑṬḌṆŚṢ')
DEVA = re.compile(r'[ऀ-ॿ]')
HEB = re.compile(r'[֐-׿]')
OPTS = {}   # job options read by the page readers (set in convert)
FIXMAP = str.maketrans({'ı': 'i', 'ş': 'ṣ', 'Ş': 'Ṣ', 'ņ': 'ṇ', 'Ņ': 'Ṇ', 'ț': 'ṭ', 'Ț': 'Ṭ', 'ţ': 'ṭ', 'Ţ': 'Ṭ',
                        'ļ': 'ḷ', 'Ļ': 'Ḷ', 'ř': 'ṛ', 'Ř': 'Ṛ'})
ROMAN = re.compile(r'^(?=[ivxlcdm]+$)m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$', re.I)


class RawdictError(Exception):
    pass


class Line:
    __slots__ = ('x0', 'y0', 'x1', 'y1', 'spans', 'size', 'text', 'kind', 'blk')

    def __init__(self, spans):
        self.spans = spans  # list of dict(text,size,flags,bbox,sup)
        self.x0 = min(s['bbox'][0] for s in spans); self.y0 = min(s['bbox'][1] for s in spans)
        self.x1 = max(s['bbox'][2] for s in spans); self.y1 = max(s['bbox'][3] for s in spans)
        sz = [(s['size'], len(s['text'].strip())) for s in spans if s['text'].strip() and not s['sup']]
        self.size = max(sz, key=lambda t: t[1])[0] if sz else spans[0]['size']
        self.text = ''.join(s['text'] for s in spans).strip()
        self.kind = 'body'; self.blk = None


# ---------------------------------------------------------------- text sources
def span_text(s):
    """Rebuild a span's text from its characters, adding a space where the gap between two characters is wide."""
    chars = s.get('chars')
    if not chars: return s.get('text', '')
    out = []; prev = None; size = s['size'] or 10
    gaps = sorted(chars[k + 1]['bbox'][0] - chars[k]['bbox'][2] for k in range(len(chars) - 1) if chars[k]['c'] != ' ' and chars[k + 1]['c'] != ' ')
    base = gaps[len(gaps) // 2] if gaps else 0
    thr = max(size * 0.08, base + size * 0.07)
    for ch in chars:
        c = ch['c']
        if prev is not None and c != ' ' and prev['c'] != ' ':
            gap = ch['bbox'][0] - prev['bbox'][2]
            if gap > thr: out.append(' ')
        out.append(c); prev = ch
    return ''.join(out)


ACC_MARK = {'¯': '̄', '´': '́', '˙': '̇', '˜': '̃', '`': '̀', 'ˆ': '̂', '¨': '̈',
            '˘': '̆', 'ˇ': '̌', '¸': '̧', '˚': '̊', 'ˊ': '́', 'ˋ': '̀', 'ˉ': '̄'}
DOT_BASES = set('rRlLtTdDnNsShHmMkKgGzZ')


_CED = {}


def _cedilla_is_dot(page, base, size, font):
    """Some fonts draw IAST's dot below with the glyph whose Unicode name is the cedilla: look at the ink under the letter."""
    key = (id(page.parent), font)
    if key in _CED: return _CED[key]
    try:
        y = base['origin'][1]; r = fitz.Rect(base['bbox'][0], y + 0.02 * size, base['bbox'][2], y + 0.4 * size)
        pm = page.get_pixmap(dpi=600, clip=r, colorspace=fitz.csGRAY)
        W, H = pm.width, pm.height; buf = pm.samples
        pts = [(i % W, i // W) for i in range(W * H) if buf[i] < 128]
        if len(pts) < 6: return None
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        area = (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1)
        res = len(pts) / area > 0.6
    except Exception:
        return None
    _CED[key] = res
    return res


def _ink_dot_below(page, base, size):
    try:
        y = base['origin'][1]; r = fitz.Rect(base['bbox'][0], y + 0.02 * size, base['bbox'][2], y + 0.4 * size)
        pm = page.get_pixmap(dpi=600, clip=r, colorspace=fitz.csGRAY)
        W, H = pm.width, pm.height; buf = pm.samples
        pts = [(i % W, i // W) for i in range(W * H) if buf[i] < 128]
        if len(pts) < 6: return False
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        w = max(xs) - min(xs) + 1; h = max(ys) - min(ys) + 1
        return len(pts) / (w * h) > 0.6 and 0.6 <= w / h <= 1.6
    except Exception:
        return False


def fix_accents(spans, page=None):
    """Accents drawn as separate glyphs (TeX '\\=a', '\\d{s}'): attach each to the letter it is drawn over or under,
    judged by position on the page, and drop the space that the separate glyph caused."""
    seq = [(si, ci, ch) for si, s in enumerate(spans) for ci, ch in enumerate(s.get('chars') or [])]
    # an accent glyph whose text layer says 'fi' (DeCaroli's linguistic-alternate font), drawn exactly over a letter:
    # read the ink under the letter; a round dot below the baseline is a dot below, anything else stays as it is
    if page is not None:
        for k in range(1, len(seq) - 1):
            si, ci, ch = seq[k]; b = seq[k - 1][2]; nx = seq[k + 1][2]
            if ch['c'] in ('f', '\ufb01') and b['c'] in DOT_BASES and abs(ch['bbox'][0] - b['bbox'][0]) < 0.6 and abs(ch['bbox'][2] - b['bbox'][2]) < 0.6 \
                    and (ch['c'] == '\ufb01' or (nx['c'] == 'i' and nx['bbox'][2] - nx['bbox'][0] < 0.2)):
                size = spans[si]['size'] or 10
                if _ink_dot_below(page, b, size):
                    was = ch['c']; ch['c'] = '\u0323'; ch['bbox'] = (b['bbox'][0] + 0.3 * (b['bbox'][2] - b['bbox'][0]),) + tuple(ch['bbox'][1:2]) + (b['bbox'][2] - 0.3 * (b['bbox'][2] - b['bbox'][0]),) + tuple(ch['bbox'][3:])
                    if was == 'f' and nx['c'] == 'i': nx['c'] = ''
    if not any(ch['c'] in ACC_MARK or '̀' <= ch['c'] <= 'ͯ' or ch['c'] == '.' for _, _, ch in seq): return
    drop = set(); touched = []
    for k, (si, ci, ch) in enumerate(seq):
        c = ch['c']; size = spans[si]['size'] or 10
        if c in ACC_MARK or '̀' <= c <= 'ͯ': mark = ACC_MARK.get(c, c); dot = False
        elif c == '.': mark = '̣'; dot = True
        else: continue
        x0, _, x1, _ = ch['bbox']; xc = (x0 + x1) / 2
        if x1 - x0 <= 0 and not ('̀' <= c <= 'ͯ'): continue
        best = None
        for d in (-1, 1, -2, 2, -3, 3):
            m = k + d
            if not 0 <= m < len(seq) or m in drop: continue
            b = seq[m][2]; bc = b['c']
            if not (bc.isalpha() or bc == 'ı'): continue
            if len(unicodedata.normalize('NFD', bc)) > 2: continue
            bx0, _, bx1, _ = b['bbox']; w = bx1 - bx0
            if w <= 0: continue
            if dot:
                if d not in (-1, 1) or bc not in DOT_BASES or not (bx0 + 0.15 * w <= xc <= bx1 - 0.15 * w): continue
                # a TeX dot below is the period glyph lowered under the letter; a sentence period stays on the baseline
                # (8 Oct 2026: Schweitzer's italic titles got 'Evangelieṇ' for 'Evangelien.')
                if ch['origin'][1] - b['origin'][1] < 0.1 * size: continue
            elif not (bx0 + 0.1 * w <= xc <= bx1 - 0.1 * w):
                continue
            best = m; break
        if best is None: continue
        b = seq[best][2]; base = b['c']
        if mark == '\u0327' and page is not None and base in DOT_BASES and _cedilla_is_dot(page, b, size, spans[si]['font']): mark = '\u0323'
        below = mark in ('̣', '̧', '̱')
        if not below and mark == '̄' and ch['origin'][1] - b['origin'][1] > 0.12 * size: mark = '̱'; below = True
        if not below: base = {'ı': 'i', 'ȷ': 'j'}.get(base, base)
        new = unicodedata.normalize('NFC', base + mark)
        if len(new) > 1 and not dot and mark not in ('̄', '́', '̇', '̃', '̀', '̂', '̈', '̱'): continue
        b['c'] = new; drop.add(k); touched.append(k)
    if not drop: return
    # spaces next to a removed accent glyph, between letters that touch: not real word spaces
    for k in touched:
        for d in (-1, 1):
            m = k + d
            if 0 <= m < len(seq) and seq[m][2]['c'] == ' ' and m not in drop:
                l_ = next((seq[j][2] for j in range(m - 1, -1, -1) if j not in drop and seq[j][2]['c'] != ' '), None)
                r_ = next((seq[j][2] for j in range(m + 1, len(seq)) if j not in drop and seq[j][2]['c'] != ' '), None)
                size = spans[seq[m][0]]['size'] or 10
                if l_ and r_ and l_['c'][-1:].isalpha() and r_['c'][:1].isalpha() and r_['bbox'][0] - l_['bbox'][2] < 0.12 * size:
                    drop.add(m)
    gone = {(seq[k][0], seq[k][1]) for k in drop}
    for si, s in enumerate(spans):
        if s.get('chars'):
            s['chars'] = [ch for ci, ch in enumerate(s['chars']) if (si, ci) not in gone]


DEVL = re.compile('[\u0900-\u0963\u0966-\u097F]')   # Devanagari without the dandas
SHORTW = set('a an as at be by do he if in is it me my no of on or so to up us we i o'.split())
PUNC = '.,;:()[]{}“”‘’"\'!?–—-*_'


def _good_latin(o):
    c = o.strip(PUNC)
    return bool(c) and c.isalpha() and not DEVL.search(c) and (c.lower() in english() or c.lower() in SHORTW)


def _junk(w, latin_line):
    c = w.strip(PUNC)
    if not c: return False
    if '[illegible]' in w or '�' in w: return True
    if latin_line:
        if DEVL.search(c): return True
        if re.search(r'\d', c) and re.search(r'[^\W\d_]', c): return True   # '0७10', '81101118'-like mixtures
        if re.fullmatch(r'\d+', c): return 'num'                            # replaced only by an English word
    else:
        if re.search(r'[A-Za-z]', c) and DEVL.search(c): return True
        if re.fullmatch(r'[A-Za-z]{1,3}', c): return 'lat'     # stray Latin letters inside a Devanagari line
    return False


def _en_rate(t):
    toks = [w for w in t.split() if w.strip(PUNC)]
    return sum(1 for w in toks if _good_latin(w)) / max(1, len(toks))


def latin_fix(doc, i, ls, langs, dpi=300, stats=None):
    """Fresh-OCR pages read with Latin+san: an English line in which the san model put Devanagari ('In ४ त ०४८६ form'
    for 'In their detailed form') is replaced by the same line read with Latin alone, when that reading has clearly more
    English words. Lines that are mostly Devanagari, and mixed lines that are not better in the Latin reading (a glossary
    line 'शब्द Sabda : words'), are kept."""
    def mixed(L):
        d = len(DEVL.findall(L.text)); a = len(re.findall(r'[A-Za-z]', L.text))
        return d >= 1 and a > d
    if not any(mixed(L) for L in ls): return ls
    le = ocr_page(doc, i, langs, dpi=dpi)
    # a line's band is the median top and bottom of its words (one stray tall box would otherwise make it span the page)
    def band(L):
        ys0 = sorted(sp['bbox'][1] for sp in L.spans); ys1 = sorted(sp['bbox'][3] for sp in L.spans)
        return ys0[len(ys0) // 2], ys1[len(ys1) // 2]
    def xr(L): return min(sp['bbox'][0] for sp in L.spans), max(sp['bbox'][2] for sp in L.spans)
    bl = [band(L) for L in ls]; be = [band(E) for E in le]
    # each English-only line belongs to the one Latin+san line it overlaps most (at least half of each line's height)
    own = {}
    for k, E in enumerate(le):
        best = None; e0, e1 = be[k]; ex0, ex1 = xr(E)
        for j, L in enumerate(ls):
            l0, l1 = bl[j]; lx0, lx1 = xr(L)
            h = min(l1, e1) - max(l0, e0)
            if h <= 0 or min(lx1, ex1) - max(lx0, ex0) <= 0: continue
            if h < 0.5 * (l1 - l0) or h < 0.5 * (e1 - e0): continue
            if best is None or h > best[0]: best = (h, j)
        if best: own.setdefault(best[1], []).append(k)
    def deva_junky(t):   # the Devanagari in this line is digits or one- or two-letter scraps, not words
        toks = [''.join(DEVL.findall(w)) for w in t.split() if DEVL.search(w)]
        return bool(toks) and sum(1 for w in toks if re.fullmatch('[\u0966-\u096F]+', w) or len(w) <= 2) >= 0.6 * len(toks)
    out = []
    def scrub(L):   # still an English line: Devanagari digits stand for an unread word, a lone danda is a stray mark
        if not (len(re.findall(r'[A-Za-z]', L.text)) > 3 * len(DEVL.findall(L.text))): return L
        for sp in L.spans:
            t = sp['text']; core = t.strip()
            if re.fullmatch('[\u0964\u0965]+', core): sp['text'] = ''
            elif re.fullmatch('[\u0966-\u096F\u0964\u0965.,:;-]*[\u0966-\u096F][\u0966-\u096F\u0964\u0965.,:;-]*', core):
                sp['text'] = t.replace(core, '[illegible]')
        L.text = ''.join(sp['text'] for sp in L.spans).strip()
        return L
    for j, L in enumerate(ls):
        if not mixed(L) or j not in own: out.append(scrub(L) if mixed(L) or re.search('[\u0964\u0965]', L.text) else L); continue
        cand = sorted(own[j], key=lambda k: xr(le[k])[0])
        etxt = ' '.join(le[k].text for k in cand)
        re_, rl = _en_rate(etxt), _en_rate(L.text)
        realword = any(len(re.findall('[\u0904-\u0939\u0958-\u0961\u0972-\u097F]', w)) >= 3 for w in L.text.split())   # a Devanagari word, as in a glossary line
        if not DEVL.search(etxt) and not realword and (re_ >= rl + 0.15 or (re_ >= rl - 0.05 and deva_junky(L.text))):
            out.extend(le[k] for k in cand)
            if stats is not None: stats[0] += 1
        else:
            out.append(scrub(L))
    return out


def merge_with_ocr(doc, i, ls, langs, deva_junk=False):
    """Scans whose own OCR layer is kept (its IAST is good) but whose junk words are replaced by a fresh OCR's word at
    the same place: a junk word ('81101118', '15' for 'is', Devanagari letters inside an English line, [illegible]) gives
    way only to an English dictionary word (or, in a Devanagari line, to a Devanagari word); Latin lines that are junk
    throughout where the fresh OCR reads Devanagari are replaced by the fresh line."""
    try: ocr = ocr_page(doc, i, langs, dpi=300)
    except Exception: return ls
    owords = [(sp['bbox'], sp['text'], L) for L in ocr for sp in L.spans if sp['text'].strip()]
    if not owords: return ls
    eng_words = [None]   # the page read with Latin alone, made only when needed
    out = []
    for L in ls:
        txt = L.text
        deva = len(DEVL.findall(txt)); lat = len(re.findall(r'[A-Za-z]', txt))
        latin_line = lat >= deva
        # whole line: Latin junk where the fresh OCR reads Devanagari
        ov = [L2 for L2 in ocr if min(L.y1, L2.y1) - max(L.y0, L2.y0) > 0.5 * min(L.y1 - L.y0, L2.y1 - L2.y0) and min(L.x1, L2.x1) - max(L.x0, L2.x0) > 0.5 * (L.x1 - L.x0)]
        if latin_line and ov:
            ws = re.findall(r'[A-Za-z]{3,}', txt)
            rate = sum(1 for w in ws if w.lower() in english()) / max(1, len(ws))
            od = ''.join(L2.text for L2 in ov)
            if len(DEVL.findall(od)) > 0.6 * max(1, len(od.replace(' ', ''))) and rate < 0.3 and not re.search(r'[āīūṛṭḍṇśṣṃḥ]', txt):
                # only the fresh words that lie within this line's own extent (table rows hold several old lines)
                inside = [(b, t_) for b, t_, L2 in owords if L2 in ov and L.x0 - 3 <= (b[0] + b[2]) / 2 <= L.x1 + 3]
                if inside:
                    nl = ' '.join(t_ for b, t_ in sorted(inside))
                    if L.spans:
                        L.spans = [dict(L.spans[0], text=nl, bbox=(L.x0, L.y0, L.x1, L.y1), sup=False)]
                        L.text = nl
                    out.append(L); continue
        for sp in L.spans:
            t = sp['text']
            if not t.strip() or sp.get('sup'): continue
            parts = re.split(r'(\s+)', t)
            x0, y0, x1, y1 = sp['bbox']; n = max(1, len(t)); pos = 0; changed = False
            for k, w in enumerate(parts):
                a = pos; pos += len(w)
                if not w.strip(): continue
                j = _junk(w, latin_line)
                if not j: continue
                wx0 = x0 + (x1 - x0) * a / n; wx1 = x0 + (x1 - x0) * pos / n
                cand = [(min(wx1, b[2]) - max(wx0, b[0]), ot) for b, ot, _ in owords
                        if min(y1, b[3]) - max(y0, b[1]) > 0.4 * min(y1 - y0, b[3] - b[1]) and min(wx1, b[2]) - max(wx0, b[0]) > 0.4 * (wx1 - wx0)]
                best = max(cand) if cand else None
                ot = best[1] if best else ''
                ob = next((b for b, t_, _ in owords if t_ == ot), None) if best else None
                latin_ok = _good_latin(ot) or (j is True and not DEVL.search(ot) and re.search(r'[A-Za-z0-9]', ot) and not re.search(r'[^\w.,;:()“”‘’"\'!?–—-]', ot))
                deva_ok = DEVL.search(ot) and not re.search(r'[A-Za-z]', ot)
                fffd_word = '\ufffd' in w and DEVL.search(w)   # a Devanagari word with unmapped glyphs, even inside an English line
                if best and (latin_line and (latin_ok or fffd_word and deva_ok) or (not latin_line and j in (True, 'lat') and deva_ok)):
                    lead = w[:len(w) - len(w.lstrip(PUNC))]; trail = w[len(w.rstrip(PUNC)):]
                    parts[k] = lead + ot.strip(PUNC) + trail; changed = True
                    # neighbouring pieces of the same word (the old layer split it differently): drop them
                    for d in (-2, 2):
                        m = k + d
                        if 0 <= m < len(parts) and parts[m].strip() and ob:
                            ma = sum(len(p_) for p_ in parts[:m]); mb = ma + len(parts[m])
                            mx0 = x0 + (x1 - x0) * ma / n; mx1 = x0 + (x1 - x0) * mb / n
                            if min(mx1, ob[2]) - max(mx0, ob[0]) > 0.6 * (mx1 - mx0) and _junk(parts[m], latin_line) is not False or \
                               (not latin_line and min(mx1, ob[2]) - max(mx0, ob[0]) > 0.6 * (mx1 - mx0)):
                                parts[m] = ''; parts[(k + m) // 2] = ''
                elif deva_junk and latin_line and j is True and DEVL.search(w):
                    # both readings put Devanagari here (an italic IAST word, say): try the page read with Latin alone
                    if eng_words[0] is None:
                        try: eng_words[0] = [(sp2['bbox'], sp2['text']) for L2 in ocr_page(doc, i, 'eng', dpi=300) for sp2 in L2.spans if sp2['text'].strip()]
                        except Exception: eng_words[0] = []
                    ce = [(min(wx1, b[2]) - max(wx0, b[0]), et) for b, et in eng_words[0]
                          if min(y1, b[3]) - max(y0, b[1]) > 0.4 * min(y1 - y0, b[3] - b[1]) and min(wx1, b[2]) - max(wx0, b[0]) > 0.4 * (wx1 - wx0)]
                    et = max(ce)[1] if ce else ''
                    if et and not DEVL.search(et) and re.search(r'[A-Za-z]', et):
                        lead = w[:len(w) - len(w.lstrip(PUNC))]; trail = w[len(w.rstrip(PUNC)):]
                        parts[k] = lead + et.strip(PUNC) + trail; changed = True
                    else:
                        parts[k] = '[illegible]'; changed = True   # Devanagari letters in an English/IAST line: the old OCR's junk
            if changed: sp['text'] = re.sub(r' {2,}', ' ', ''.join(parts))
        L.text = ''.join(s_['text'] for s_ in L.spans).strip()
        out.append(L)
    # Lines printed in Devanagari: the fresh OCR's line replaces what the old layer has there (often Latin junk), and is
    # added where the old layer has nothing (8 Oct 2026: the merged Paratrisika had a tenth of the fresh OCR's Devanagari)
    def band(X):
        ys0 = sorted(sp['bbox'][1] for sp in X.spans); ys1 = sorted(sp['bbox'][3] for sp in X.spans)
        return ys0[len(ys0) // 2], ys1[len(ys1) // 2]
    def xr(X): return min(sp['bbox'][0] for sp in X.spans), max(sp['bbox'][2] for sp in X.spans)
    dl = [L2 for L2 in ocr if len(DEVL.findall(L2.text)) >= 6 and len(DEVL.findall(L2.text)) > 0.5 * len(L2.text.replace(' ', ''))]
    if dl:
        drop = set(); add = []
        for D in dl:
            d0, d1 = band(D); dx0, dx1 = xr(D); hit = []
            for k, L in enumerate(out):
                if not L.spans: continue
                l0, l1 = band(L); lx0, lx1 = xr(L); h = min(l1, d1) - max(l0, d0)
                if h > 0.5 * min(l1 - l0, d1 - d0) and min(lx1, dx1) - max(lx0, dx0) > 0.3 * min(lx1 - lx0, dx1 - dx0): hit.append(k)
            if any(len(DEVL.findall(out[k].text)) > 0.5 * len(out[k].text.replace(' ', '')) and '\ufffd' not in out[k].text and '[illegible]' not in out[k].text
                   for k in hit): continue   # the layer has sound Devanagari here (unmapped glyphs or [illegible]: take the fresh line)
            if any(_en_rate(out[k].text) >= 0.6 and len(out[k].text) > 12 for k in hit): continue                       # real English: keep it
            drop.update(hit); add.append(D)
        if add:
            out = [L for k, L in enumerate(out) if k not in drop] + add
    return out


def lines_pymupdf(page, font_ok=None, bad_langs=None, doc=None, pno=None, bad_fonts=None):
    out = []
    # (on a rotated page PyMuPDF's mediabox clip cuts off text that lies inside the page: Sanderson's spreads lost a third)
    try: d = page.get_text('rawdict', flags=fitz.TEXT_PRESERVE_WHITESPACE | (0 if page.rotation else fitz.TEXT_MEDIABOX_CLIP))
    except (SystemError, ValueError): raise RawdictError(page.number)
    if any(ch['c'] == '\ufffd' or not ch['c'].isascii() for b in d['blocks'] for l in b.get('lines', []) for s in l['spans'] for ch in s['chars']):
        try: glyphfix.repair_page(page, page.parent, d)   # unmapped glyphs recovered from the embedded fonts
        except Exception as e: print('glyphfix', e, file=sys.stderr)
    # A page with /Rotate: the text layer's coordinates are those of the unrotated page, so they are turned into the page as
    # it is shown (8 Oct 2026: Hanneder's pages, rotated 180, came out bottom to top; pages rotated 90/270 were dropped as vertical text)
    RM = page.rotation_matrix if page.rotation else None
    rb = (lambda bb: tuple(fitz.Rect(bb) * RM)) if RM is not None else (lambda bb: bb)
    drops = []
    for bi, b in enumerate(d['blocks']):
        if b.get('type') != 0: continue
        for l in b['lines']:
            ddx, ddy = l['dir']
            if RM is not None: ddx, ddy = ddx * RM.a + ddy * RM.c, ddx * RM.b + ddy * RM.d
            if abs(ddy) > 0.2: continue  # vertical text (as shown on the page)
            if RM is not None:
                # judge accent positions on the page as shown: on a rotated page the raw boxes are turned, so a period after a
                # letter lay 'under' it (8 Oct 2026: Ruppel's vocabulary got '(ṃ)' for '(m.)')
                IRM = ~RM
                for s_ in l['spans']:
                    for ch in s_.get('chars') or []:
                        ch['bbox'] = tuple(fitz.Rect(ch['bbox']) * RM); ch['origin'] = tuple(fitz.Point(ch['origin']) * RM)
                fix_accents(l['spans'], page)
                for s_ in l['spans']:
                    for ch in s_.get('chars') or []:
                        ch['bbox'] = tuple(fitz.Rect(ch['bbox']) * IRM); ch['origin'] = tuple(fitz.Point(ch['origin']) * IRM)
            else:
                fix_accents(l['spans'], page)
            sp = []
            for s in l['spans']:
                if font_ok and not font_ok(s['font']): continue
                t = span_text(s)
                if not t: continue
                if sp:  # space between spans when there is a visible gap
                    gap = rb(s['bbox'])[0] - sp[-1]['bbox'][2]
                    if gap > (s['size'] or 10) * 0.08 and not sp[-1]['text'].endswith(' ') and not t.startswith(' '): sp[-1]['text'] += ' '
                if re.search('[\ufffd\ue000-\uf8ff]', t) and re.search(r'[^\s\ufffd\ue000-\uf8ff]', t) and len(s['chars']) > 1:
                    # split into words so that only the words with unknown glyphs are read again
                    groups, cur = [], []
                    for ch in s['chars']:
                        if ch['c'].isspace():
                            if cur: groups.append(cur); cur = []
                        else:
                            if cur and ch['bbox'][0] - cur[-1]['bbox'][2] > max(s['size'] * 0.25, 1.5): groups.append(cur); cur = []
                            cur.append(ch)
                    if cur: groups.append(cur)
                    for gi, g in enumerate(groups):
                        gt = span_text(dict(s, chars=g)) + (' ' if gi < len(groups) - 1 or t.endswith(' ') else '')
                        gb = (min(c['bbox'][0] for c in g), min(c['bbox'][1] for c in g), max(c['bbox'][2] for c in g), max(c['bbox'][3] for c in g))
                        sp.append(dict(text=gt, size=s['size'], flags=s['flags'], bbox=rb(gb), font=s['font'], sup=False))
                    continue
                sp.append(dict(text=t, size=s['size'], flags=s['flags'], bbox=rb(s['bbox']), font=s['font'], sup=False))
            if sp and ''.join(x['text'] for x in sp).strip():
                txt = ''.join(x['text'] for x in sp)
                heb = len(HEB.findall(txt)); lat = len(re.findall(r'[A-Za-z]', txt))
                if heb > 0.5 * (heb + lat) and len(sp) > 1:
                    sp = sp[::-1]
                    for x in sp: x['text'] = x['text'].strip() + ' '
                if OPTS.get('drop_nums') and re.fullmatch(r'\s*\d{1,3}\s*', ''.join(x['text'] for x in sp)) and sp[0]['size'] >= 16:
                    L0 = Line([sp[0]]); L0.blk = bi; out.append(L0); drops.append(L0); continue   # a drop number on a line of its own
                if OPTS.get('drop_nums') and len(sp) >= 2 and re.fullmatch(r'\s*\d{1,3}\s*', sp[0]['text']) and any(x['text'].strip() for x in sp[1:]) \
                        and sp[0]['size'] > 1.8 * max(x['size'] for x in sp[1:] if x['text'].strip()):
                    # a drop number (Lost Scriptures' fragment numbers) shares a line with the text beside its second line: own line
                    L0 = Line([sp[0]]); L0.blk = bi; out.append(L0); drops.append(L0); sp = sp[1:]
                    while not sp[0]['text'].strip(): sp = sp[1:]
                    sp[0] = dict(sp[0], text=sp[0]['text'].lstrip())
                LL = Line(sp); LL.blk = bi; out.append(LL)
    for L0 in drops:   # the drop number goes in front of the first line beside it; the lines beside it are not indented
        side = sorted([M for M in out if M is not L0 and M.x0 >= L0.x1 - 1 and M.x0 - L0.x1 < 25 and L0.y0 - 0.4 * (L0.y1 - L0.y0) <= M.y0 <= L0.y1], key=lambda M: M.y0)
        if not side: continue
        f = side[0]
        f.spans.insert(0, dict(L0.spans[0], text=L0.spans[0]['text'].strip() + ' ', size=f.size, bbox=(L0.x0, f.y0, L0.x1, f.y1)))
        f.text = ''.join(x['text'] for x in f.spans).strip()
        fx = min(M.x0 for M in side)
        for M in side: M.x0 = L0.x0 + (M.x0 - fx)     # an indent beside the number (a new verse) is kept
        out.remove(L0)
    # spans whose characters have no Unicode mapping (U+FFFD or private use): read them again by OCR
    for L in out:     # dingbat fonts (Bennett's ·inserted words·): a middle dot, never read again by OCR
        for x in L.spans:
            if re.match(r'(Wingdings|Webdings|ZapfDingbats|Dingbats)', x['font'].split('+')[-1]) and '\ufffd' in x['text']:
                x['text'] = x['text'].replace('\ufffd', '·'); x['font'] = 'dingbat'
    if doc is not None and (bad_langs or bad_fonts) or doc is not None and any('\ufffd' in x['text'] or re.search('[\ue000-\uf8ff]', x['text']) for L in out for x in L.spans):
        bf = {k: v for k, v in (bad_fonts or {}).items() if v != 'illegible' and not re.match(r'(Wingdings|Webdings|ZapfDingbats|Dingbats)', k.split('+')[-1])}
        for L in out:
            sp = L.spans
            def fffd_rich(x):
                t = x['text'].strip(); k = sum(1 for c in t if c == '\ufffd' or 0xE000 <= ord(c) <= 0xF8FF)
                return k >= 1 and (k >= 0.3 * len(t) or len(t) <= 3)
            bad = [x['font'] in bf or fffd_rich(x) for x in sp]
            if not any(bad): continue
            # extend to spans that continue the same word (touching, no space between)
            changed = True
            while changed:
                changed = False
                for k in range(len(sp) - 1):
                    a, b = sp[k], sp[k + 1]
                    touch = b['bbox'][0] - a['bbox'][2] < 0.15 * max(a['size'], 4) and not a['text'].endswith(' ') and not b['text'].startswith(' ')
                    if touch and bad[k] != bad[k + 1]:
                        if bad[k] and re.search(r'\S$', a['text']) or bad[k + 1] and re.match(r'^\S', b['text']):
                            if not bad[k]:
                                # take only the last word of a good span: split it
                                m = re.match(r'^(.*\s)(\S+)$', a['text'], re.S)
                                if m:
                                    w0 = fitz.Rect(a['bbox']); frac = len(m.group(1)) / max(1, len(a['text']))
                                    x_split = w0.x0 + (w0.x1 - w0.x0) * frac
                                    a2 = dict(a, text=m.group(2), bbox=(x_split, w0.y0, w0.x1, w0.y1))
                                    a['text'] = m.group(1); a['bbox'] = (w0.x0, w0.y0, x_split, w0.y1)
                                    sp.insert(k + 1, a2); bad.insert(k + 1, True); changed = True; break
                                bad[k] = True; changed = True
                            else:
                                m = re.match(r'^(\S+)(\s.*)$', b['text'], re.S)
                                if m:
                                    w0 = fitz.Rect(b['bbox']); frac = len(m.group(1)) / max(1, len(b['text']))
                                    x_split = w0.x0 + (w0.x1 - w0.x0) * frac
                                    b2 = dict(b, text=m.group(2), bbox=(x_split, w0.y0, w0.x1, w0.y1))
                                    b['text'] = m.group(1); b['bbox'] = (w0.x0, w0.y0, x_split, w0.y1)
                                    sp.insert(k + 2, b2); bad.insert(k + 2, False); bad[k + 1] = True; changed = True; break
                                bad[k + 1] = True; changed = True
            # OCR each run of bad spans once
            k = 0
            while k < len(sp):
                if not bad[k]: k += 1; continue
                j = k
                while j + 1 < len(sp) and bad[j + 1]: j += 1
                run = sp[k:j + 1]
                langs = collections.Counter(bf.get(x['font']) for x in run if bf.get(x['font']))
                lang = langs.most_common(1)[0][0] if langs else (bad_langs or 'Latin')
                txt = ''.join(x['text'] for x in run)
                lead = ' ' if txt.startswith(' ') else ''; trail = ' ' if txt.endswith(' ') else ''
                if not re.search(r'[\w\ufffd\ue000-\uf8ff]', txt):
                    k = j + 1; continue
                if lang == 'illegible':
                    new_t = '[illegible]'
                else:
                    r = fitz.Rect(run[0]['bbox'])
                    for x in run: r |= fitz.Rect(x['bbox'])
                    got = ocr_page(doc, pno, lang, dpi=400, clip=(r + (-2, -2, 2, 2)) & page.rect, psm=7)
                    new_t = ' '.join(x.text for x in got).strip() or '[illegible]'
                    confs = [sp_.get('conf', 0) for g in got for sp_ in g.spans]
                    words_ = re.findall(r'[A-Za-z]+', new_t)
                    plausible = words_ and all(w.lower() in english() for w in words_)
                    if not langs and not plausible and (not confs or sum(confs) / len(confs) < 45): new_t = '[illegible]'
                run[0]['text'] = lead + new_t + trail; run[0]['font'] = 'ocr-' + lang
                for x in run[1:]: x['text'] = ''
                k = j + 1
            L.spans = [x for x in sp if x['text']]
        for L in out: L.text = ''.join(s['text'] for s in L.spans).strip()
    # superscripts: flag bit 0, or clearly smaller and raised relative to the line
    for L in out:
        for s in L.spans:
            t = s['text'].strip()
            if not t: continue
            if (s['flags'] & 1) or (s['size'] < L.size * 0.8 and s['bbox'][3] < L.y1 - (L.y1 - L.y0) * 0.25):
                if re.fullmatch(r'(\d{1,4}|[*†‡§]{1,3}|[a-z])[.,]?', t) or re.fullmatch(r'(\d{1,3}|[a-z])(, ?(\d{1,3}|[a-z]))+', t): s['sup'] = True
    return merge_same_line(out)


LEGACY_LANGS = ('grc', 'heb', 'Latin', 'san', 'chi_sim')
ODD = re.compile(r'[\ufffd\ue000-\uf8ff¼½¾ØæðþÞÆ¹²³µ¶¿¡¤¦¬ºª]')
FWORDS = set('the of and to in a is that for it as was with be by on not he this are or his from at which but have an they'.split())


def legacy_fonts(doc, sample=60, langs=None):
    """Fonts whose text is not Unicode (old Greek/Hebrew/transliteration fonts that map letters to Latin codes):
    many odd characters, almost no English words. Returns {font: 'grc'|'heb'|'drop'} after test OCR of a few spans."""
    N = len(doc); idx = range(N) if N <= sample else sorted({int(k * N / sample) for k in range(sample)})
    st = collections.defaultdict(lambda: collections.Counter()); ex = collections.defaultdict(list); touch = collections.Counter()
    for i in idx:
        try: d_ = doc[i].get_text('rawdict', flags=fitz.TEXT_PRESERVE_WHITESPACE | fitz.TEXT_MEDIABOX_CLIP)
        except (SystemError, ValueError): continue   # a font whose ToUnicode gives an impossible code point: MuPDF cannot build this page's text
        try: glyphfix.repair_page(doc[i], doc, d_)   # judge the fonts after the glyph repair
        except Exception: pass
        for b in d_['blocks']:
            if b.get('type') != 0: continue
            for l in b['lines']:
                prev = None
                for sp in l['spans']:
                    t = span_text(sp)
                    if prev is not None and sp['bbox'][0] - prev['bbox'][2] < 0.15 * max(sp['size'], 4) and prev['font'] != sp['font']:
                        touch[(prev['font'], sp['font'])] += 1; touch[(sp['font'], prev['font'])] += 1
                    prev = sp
                    if not t.strip(): continue
                    st[sp['font']]['spans'] += 1
                    c = st[sp['font']]
                    c['chars'] += len(t.strip()); c['odd'] += len(ODD.findall(t))
                    ws = re.findall(r'[A-Za-z]+', t); c['words'] += len(ws)
                    c['fw'] += sum(1 for w in ws if w.lower() in FWORDS)
                    c['finalB'] += len(re.findall(r'[a-z]B\b', t))
                    if len(t.strip()) >= 4: ex[sp['font']].append((len(t.strip()), i, sp['bbox']))
    out = {}
    badset = set()
    for f in st:          # known legacy font families: Hebrew and Greek letters stored as Latin codes
        base = f.split('+')[-1]
        if re.match(r'(Davka|SPTiberian|BWHEBB|Ashkelon|SILEzra|HebraicaII|Hebrew-?Legacy)', base, re.I): out[f] = 'heb'
        elif re.match(r'(SGreek|SPIonic|BWGRKL|GraecaII|SuperGreek|GreekKeys|Ibycus)', base, re.I): out[f] = 'grc'
    for f, c in st.items():
        if f in out: continue
        if c['chars'] < 30: continue
        fwr = c['fw'] / max(1, c['words'])
        if fwr < 0.12 and (c['odd'] / c['chars'] > 0.02 or c['finalB'] / max(1, c['words']) > 0.02): badset.add(f)
    for f, c in st.items():   # fonts used inside the same words as a legacy font
        if f in badset or c['chars'] < 30: continue
        fwr = c['fw'] / max(1, c['words'])
        if fwr < 0.08 and (c['finalB'] / max(1, c['words']) > 0.01 or c['odd'] > 0) and sum(touch[(f, g)] for g in badset) >= 0.3 * c['spans']: badset.add(f)
    for f, c in st.items():
        if f in badset:
            best = None
            for lang in (langs or LEGACY_LANGS):
                confs = []
                for _, i, bb in sorted(ex[f], reverse=True)[:4]:
                    r = (fitz.Rect(bb) + (-2, -2, 2, 2)) & doc[i].rect
                    for L in ocr_page(doc, i, lang, dpi=400, clip=r, psm=7):
                        confs += [x.get('conf', 0) for x in L.spans]
                m = sum(confs) / len(confs) if confs else 0
                if best is None or m > best[1]: best = (lang, m)
            out[f] = best[0] if best and best[1] >= 45 else 'illegible'
    return out


def merge_same_line(lines):
    """PyMuPDF sometimes splits one printed line into several 'lines' (e.g. a superscript). Merge lines that overlap vertically and touch horizontally."""
    lines.sort(key=lambda L: (round(L.y0), L.x0))
    out = []
    for L in lines:
        if out:
            P = out[-1]
            ov = min(P.y1, L.y1) - max(P.y0, L.y0)
            h = min(P.y1 - P.y0, L.y1 - L.y0)
            if h > 0 and ov > 0.5 * h and 0 <= L.x0 - P.x1 < 1.0 * max(P.size, 6) and (P.blk == L.blk or L.x0 - P.x1 < 0.3 * max(P.size, 6)):
                if L.x0 - P.x1 > 0.08 * max(P.size, 6) and not P.spans[-1]['text'].endswith(' '): P.spans[-1]['text'] += ' '
                M = Line(P.spans + L.spans); M.blk = P.blk; out[-1] = M; continue
        out.append(L)
    return out


def wants_san(pg, ls):
    """A page to read again with +san: the text layer shows Devanagari, or (scans without a layer) the Latin reading has a
    line of low-confidence non-words, which is what Devanagari turns into (8 Oct 2026: Masson's notes came out as 'aaka msama')."""
    if len(DEVA.findall(pg.get_text())) >= 20: return True
    for L in ls:
        ws = re.findall(r'[A-Za-z]{2,}', L.text)
        cs = [s_['conf'] for s_ in L.spans if 'conf' in s_]
        # IAST lines (diacritics) are Latin text read with lower confidence, not Devanagari
        if not cs or len(re.findall('[āīūṛṝḷṭḍṇśṣṃṁḥñṅĀĪŪṚṬḌṆŚṢṂḤ]', L.text)) >= 2: continue
        mc = sum(cs) / len(cs); w3 = [w for w in ws if len(w) >= 3]
        # a prose line of non-words, or a short verse line read with very low confidence (Devanagari verse comes out as
        # 'amea RA AI T', conf 23-46: Ruppel's Reader)
        if (len(ws) >= 4 and mc < 60 and sum(1 for w in w3 if w.lower() in english()) < 0.4 * max(1, len(w3))) or (len(ws) >= 3 and mc < 50):
            return True
    return False


OCR_PREP = None   # job option ocr_prep ('norm-sauvola'); part of the cache key only when set


def ocr_page(doc, i, langs, dpi=300, clip=None, psm=3):
    page = doc[i]
    import hashlib
    key = hashlib.md5((f'{doc.name}|{i}|{langs}|{dpi}|{clip}|{psm}' + (f'|{OCR_PREP}' if OCR_PREP else '')).encode()).hexdigest()
    cdir = '/home/claude/p4/cache'; os.makedirs(cdir, exist_ok=True)
    cpath = os.path.join(cdir, key + '.tsv')
    if os.path.exists(cpath):
        stdout = open(cpath, encoding='utf-8').read()
    else:
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        if clip is not None and (fitz.Rect(clip).width < 1 or fitz.Rect(clip).height < 1): return []
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY, clip=clip, alpha=False)
        if pix.width < 2 or pix.height < 2: return []
        with tempfile.TemporaryDirectory() as td:
            png = os.path.join(td, 'p.png'); pix.save(png)
            extra = []
            if OCR_PREP == 'norm-sauvola':
                # Yellowed scans on a white canvas: Otsu splits canvas from paper and loses the text.
                # Stretch ink..paper to black..white, then Sauvola (local) thresholding.
                import numpy as np
                from PIL import Image
                a = np.array(Image.open(png)).astype(float); nw = a[a < 250]
                if nw.size:
                    paper, ink = np.percentile(nw, 75), np.percentile(nw, 2)
                    Image.fromarray(np.clip((a - ink) * 255 / max(1.0, paper - ink), 0, 255).astype('uint8')).save(png)
                extra = ['-c', 'thresholding_method=2']
            try:
                rr = subprocess.run(['tesseract', png, '-', '-l', langs, '--psm', str(psm)] + extra + ['tsv'], capture_output=True, text=True,
                                    timeout=300, env=dict(os.environ, OMP_THREAD_LIMIT='1'))
                stdout = rr.stdout
            except subprocess.TimeoutExpired:
                stdout = ''        # a page Tesseract cannot finish: left empty (reported as an OCR gap)
        open(cpath, 'w', encoding='utf-8').write(stdout)
    class _R: pass
    r = _R(); r.stdout = stdout
    rows = [l.split('\t') for l in r.stdout.splitlines()[1:]]
    words = collections.OrderedDict()
    sc = 72 / dpi
    ox, oy = (clip.x0, clip.y0) if clip else (0, 0)
    for w in rows:
        if len(w) < 12 or w[0] != '5': continue
        txt = w[11]
        if not txt.strip(): continue
        key = (int(w[2]), int(w[3]), int(w[4]))
        x, y, ww, hh, conf = int(w[6]), int(w[7]), int(w[8]), int(w[9]), float(w[10])
        words.setdefault(key, []).append(dict(text=txt, bbox=(ox + x * sc, oy + y * sc, ox + (x + ww) * sc, oy + (y + hh) * sc), conf=conf))
    out = []
    for key, ws in words.items():
        hs = sorted(w['bbox'][3] - w['bbox'][1] for w in ws)
        med = hs[len(hs) // 2]
        sp = []
        for j, w in enumerate(ws):
            t = w['text'] + (' ' if j < len(ws) - 1 else '')
            h = w['bbox'][3] - w['bbox'][1]
            sup = bool(re.fullmatch(r'\d{1,3}', w['text'])) and h < med * 0.7 and j > 0
            sp.append(dict(text=t, size=med * 0.75, flags=0, bbox=w['bbox'], font='ocr', sup=sup, conf=w['conf']))
        L = Line(sp); L.size = med * 0.75
        out.append(L)
    return out


# ---------------------------------------------------------------- page structure
def norm_hf(t):
    t = t.lower()
    t = re.sub(r'\d+', '#', t)
    t = re.sub(r'\b[ivxlc]+\b', '#', t)
    return re.sub(r'\W+', ' ', t).strip()


def page_number_token(t):
    t = t.strip()
    if re.match(r'^[A-Za-z] [A-Za-z] ', t) or re.search(r' [A-Za-z] [A-Za-z]$', t): return None   # letter-spaced words ('C H A P T E R')
    m = re.match(r'^\(?(\d{1,4}|[ivxlcdm]{1,7})\)?(\s|$)', t, re.I) or re.search(r'(^|\s)\(?(\d{1,4}|[ivxlcdm]{1,7})\)?$', t, re.I)
    if not m: return None
    v = m.group(1) if m.re.pattern.startswith('^') else m.group(2)
    if v.isdigit(): return int(v)
    if ROMAN.match(v): return v.lower()
    return None


def order_columns(lines, W):
    """Return lines in reading order; handles two-column pages."""
    if len(lines) < 8: return sorted(lines, key=lambda L: (L.y0, L.x0)), False
    mid = W / 2
    left = [L for L in lines if L.x1 < mid + W * 0.03 and (L.x1 - L.x0) < W * 0.5]
    right = [L for L in lines if L.x0 > mid - W * 0.03 and (L.x1 - L.x0) < W * 0.5]
    ok2 = False
    if len(left) >= 6 and len(right) >= 6 and len(left) + len(right) >= 0.6 * len(lines):
        ly0, ly1 = min(L.y0 for L in left), max(L.y1 for L in left)
        ry0, ry1 = min(L.y0 for L in right), max(L.y1 for L in right)
        ov = min(ly1, ry1) - max(ly0, ry0)
        cross = [L for L in lines if L.x0 < mid - W * 0.05 and L.x1 > mid + W * 0.05 and max(ly0, ry0) < L.y0 < min(ly1, ry1)]
        ok2 = ov > 0.5 * max(ly1 - ly0, ry1 - ry0) and len(cross) <= 1
    if ok2:
        col = set(map(id, left + right))
        full = [L for L in lines if id(L) not in col]
        if OPTS.get('col_segments'):
            # full-width lines above or below the right column cut the page into bands, each read left column then right;
            # the short last line of a full-width paragraph is then read in its place (Lost Scriptures: an introduction
            # running on above the two columns of fragments came out after them)
            r_top = min(L.y0 for L in right); r_bot = max(L.y1 for L in right)
            sep = sorted([L for L in full if L.y1 <= r_top + 2 or L.y0 >= r_bot - 2], key=lambda L: L.y0)
            sid = set(map(id, sep)); rest = sorted([L for L in full if id(L) not in sid], key=lambda L: L.y0)
            out = []
            for k in range(len(sep) + 1):
                lo = sep[k - 1].y0 if k > 0 else -1e9; hi = sep[k].y0 if k < len(sep) else 1e9
                out += sorted([L for L in left if lo <= L.y0 < hi], key=lambda L: L.y0) + sorted([L for L in right if lo <= L.y0 < hi], key=lambda L: L.y0)
                if k < len(sep): out.append(sep[k])
            return out + rest, True
        top_col = min(L.y0 for L in left + right)
        bot_col = max(L.y1 for L in left + right)
        above = sorted([L for L in full if L.y1 <= top_col + 2], key=lambda L: L.y0)
        below = sorted([L for L in full if L.y1 > top_col + 2], key=lambda L: L.y0)
        return above + sorted(left, key=lambda L: L.y0) + sorted(right, key=lambda L: L.y0) + below, True
    return sorted(lines, key=lambda L: (L.y0, L.x0)), False


def _split_gutter(L, W):
    """An OCR line that runs across a two-column block: cut it at the widest word gap near the middle of the page."""
    sps = sorted(L.spans, key=lambda s: s['bbox'][0]); best = None
    for k in range(1, len(sps)):
        a, b = sps[k - 1], sps[k]
        gap = b['bbox'][0] - a['bbox'][2]; m = (a['bbox'][2] + b['bbox'][0]) / 2
        if gap > 0.035 * W and a['bbox'][2] < 0.60 * W and b['bbox'][0] > 0.40 * W and (best is None or gap > best[0]): best = (gap, k)
    if not best: return None
    out = []
    for part in (sps[:best[1]], sps[best[1]:]):
        part = [dict(x) for x in part]; part[-1]['text'] = part[-1]['text'].rstrip()
        M = Line(part); M.kind = L.kind; M.blk = getattr(L, 'blk', None); M.size = L.size; out.append(M)
    return out


def order_gutter_bands(lines, W, H):
    """Pages that mix full-width paragraphs with two-column blocks whose OCR lines run across both columns
    (Macdonell's Vedic Reader: transliterated verse | translation, Samhita | Padapatha, with full-width notes between).
    Lines are cut at the gutter; each run of two-column lines is read left column, then right column; full-width
    lines stay in place (9 Oct 2026)."""
    ls = sorted(lines, key=lambda L: (L.y0, L.x0)); items = []
    for L in ls:
        sp = None if (L.y1 < 0.09 * H and re.search(r'\d', L.text)) else _split_gutter(L, W)   # a running head is not cut
        if sp: items.append(['split', sp, L])
        elif L.x1 < 0.53 * W: items.append(['left', L, L])
        elif L.x0 > 0.47 * W: items.append(['right', L, L])
        else: items.append(['full', L, L])
    hs = sorted(L.y1 - L.y0 for L in ls); lh = hs[len(hs) // 2] if hs else 10
    deva = lambda it: len(re.findall('[\u0900-\u097F]', it[2].text)) > 0.3 * max(1, len(re.findall(r'\w', it[2].text)))
    out = []; i = 0
    while i < len(items):
        if items[i][0] == 'full': out.append(items[i][1]); i += 1; continue
        j = i + 1
        # a run ends at a full-width line, a blank gap, or a change of script (Samhita|Padapatha above verse|translation)
        while j < len(items) and items[j][0] != 'full' and items[j][2].y0 - items[j - 1][2].y1 < 1.2 * lh and deva(items[j]) == deva(items[j - 1]): j += 1
        run = items[i:j]; i = j
        nl = sum(1 for it in run if it[0] in ('split', 'left')); nr = sum(1 for it in run if it[0] in ('split', 'right'))
        if nl < 2 or nr < 2: out += [it[2] for it in run]; continue
        a = next(k for k, it in enumerate(run) if it[0] in ('split', 'right'))
        h = max(4.0, run[a][2].y1 - run[a][2].y0)
        while a > 0 and run[a - 1][0] == 'left' and run[a - 1][2].y0 > run[a][2].y0 - 1.5 * h: a -= 1
        out += [it[2] for it in run[:a]]
        left, right = [], []
        for it in run[a:]:
            if it[0] == 'split': left.append(it[1][0]); right.append(it[1][1])
            elif it[0] == 'left': left.append(it[1])
            else: right.append(it[1])
        out += left + right
    return out


def order_ncols(lines, W, n):
    """Pages set in n equal columns (a three-column glossary): each line is cut at the column boundaries by its spans'
    centres, and the pieces are read column by column, top to bottom (8 Oct 2026: Ruppel's vocabulary list)."""
    out = []
    for L in lines:
        groups = collections.defaultdict(list)
        for sp in L.spans:
            xc = (sp['bbox'][0] + sp['bbox'][2]) / 2
            groups[min(n - 1, max(0, int(xc / (W / n))))].append(sp)
        if len(groups) == 1:
            out.append((next(iter(groups)), L))
        else:
            for k, sps in groups.items():
                M = Line(sps); M.kind = L.kind; M.blk = getattr(L, 'blk', None); out.append((k, M))
    return [L for k, L in sorted(out, key=lambda kl: (kl[0], kl[1].y0, kl[1].x0))]


# ---------------------------------------------------------------- inline text
def md_escape(t):
    t = t.replace('\\', '\\\\')
    t = re.sub(r'([\[\]*_`$^])', r'\\\1', t)
    t = t.replace('%%', '%&#37;').replace('==', '=\\=').replace('~~', '~\\~')
    t = re.sub(r'#(?=[^\s#\d])', r'\\#', t)
    t = re.sub(r'<(?=[A-Za-z/!])', '&lt;', t)
    return t


def note_md(L, italics, strip=False):
    """A footnote line as Markdown (italics kept); strip=True removes the leading note number."""
    t = line_markdown(L, italics, {}, [])
    if strip:
        t = re.sub(r'^\s*(?:\\?[^\w\s\\]){0,2}?(?:\d{1,3}|(?:\\\*|[†‡])+)(?:\\?[.)])?\s*', '', t, count=1)
        t = re.sub(r'^\s*<sup>[^<]*</sup>\s*', '', t)
    return t


def line_markdown(L, italics, page_notes, refs):
    """Render a line's spans with italics and footnote references."""
    parts = []
    for s in L.spans:
        t = s['text']
        if s['sup']:
            n = t.strip().rstrip('.,')
            if n in page_notes:
                refs.append(n); parts.append(('ref', n)); continue
            ns = [x.strip() for x in n.split(',')]
            if len(ns) > 1 and all(x in page_notes for x in ns):   # two notes on one word ("6, c")
                for x in ns: refs.append(x); parts.append(('ref', x))
                continue
            parts.append(('txt', md_escape(t.strip()) and '<sup>' + md_escape(t.strip()) + '</sup>', False)); continue
        it = italics and bool(s['flags'] & 2) and len(t.strip()) > 0
        parts.append(('txt', md_escape(t), it))
    # merge runs
    out = []; cur_it = False; buf = ''
    def flush():
        nonlocal buf
        if not buf: return
        if cur_it:
            m = re.match(r'^(\s*)(.*?)(\s*)$', buf, re.S)
            out.append(m.group(1) + ('*' + m.group(2) + '*' if m.group(2) else '') + m.group(3))
        else: out.append(buf)
        buf = ''
    for p in parts:
        if p[0] == 'ref':
            flush(); out.append('\x00REF' + p[1] + '\x00'); continue
        _, t, it = p
        if not t.strip(): buf += t; continue     # spaces do not end an italic run
        if it != cur_it: flush(); cur_it = it
        buf += t
    flush()
    return ''.join(out)


# ---------------------------------------------------------------- main conversion
def _yq(v):
    """Text for a double-quoted YAML value: backslash and quote escaped."""
    return str(v).replace('\\', '\\\\').replace('"', '\\"')


def convert(job):
    global OCR_PREP
    OCR_PREP = job.get('ocr_prep')
    OPTS.clear(); OPTS.update({k: job[k] for k in ('drop_nums', 'col_segments') if k in job})
    doc = fitz.open(job['pdf'])
    N = len(doc)
    route = job['route']
    langs = job.get('langs', 'Latin')
    font_re = re.compile(job['font_re']) if job.get('font_re') else None
    pages = []  # per page: dict(lines=[Line], W, H)
    ocr_conf = []
    stats_fill = [0]; stats_latin = [0]
    subj_ = job['pdf_vault'].split('/')[1]
    cand_langs = ('grc', 'heb', 'Latin', 'san') if subj_ in ('Trika', 'Hinduism', 'Sanskrit') else ('grc', 'heb', 'Latin', 'chi_sim')
    bad_fonts = legacy_fonts(doc, langs=cand_langs) if route == 'pymupdf' and job.get('legacy_fonts', True) else {}
    if job.get('force_bad_fonts'): bad_fonts = dict(bad_fonts, **job['force_bad_fonts'])   # {font: lang}: fonts the detection missed (Khalnayak, a Kruti-Dev-style Devanagari font)
    if bad_fonts: print(json.dumps({'legacy_fonts': bad_fonts}), flush=True)
    for i in range(N):
        pg = doc[i]; W, H = pg.rect.width, pg.rect.height
        ocr_r = next((r for r in job.get('ocr_ranges', []) if r[0] <= i + 1 <= r[1]), None)   # [first, last, langs]: pages whose text layer is junk
        if route == 'pymupdf' and ocr_r:
            ls = ocr_page(doc, i, ocr_r[2], dpi=300); stats_fill[0] += 1
        elif route == 'pymupdf':
            raw = pg.get_text(flags=fitz.TEXT_PRESERVE_WHITESPACE | (0 if pg.rotation else fitz.TEXT_MEDIABOX_CLIP))
            nonsp = len(re.sub(r'\s', '', raw))
            if nonsp > 200 and raw.count('\ufffd') > 0.05 * nonsp and not job.get('merge_ocr'):
                # most of the page has no Unicode mapping: read the whole page again by OCR (a merge job repairs it word by word instead)
                ls = ocr_page(doc, i, job.get('ocr_langs') or ('Latin' if job['pdf_vault'].split('/')[1] in ('Trika', 'Hinduism', 'Sanskrit') else 'eng'), dpi=300)
                stats_fill[0] += 1
            else:
                try: ls = lines_pymupdf(pg, bad_langs=job.get('bad_langs'), doc=doc, pno=i, bad_fonts=bad_fonts)
                except RawdictError:
                    # MuPDF cannot read this page's text layer (impossible code point in a font): read the page by OCR
                    ls = ocr_page(doc, i, job.get('ocr_langs') or ('Latin' if job['pdf_vault'].split('/')[1] in ('Trika', 'Hinduism', 'Sanskrit') else 'eng'), dpi=300)
                    stats_fill[0] += 1
                if job.get('merge_ocr') and nonsp < 30:
                    # no text layer on this page (a plate, a page the earlier OCR skipped): the fresh OCR as it is
                    fresh = ocr_page(doc, i, job['merge_ocr'], dpi=300)
                    if len(''.join(L.text for L in fresh).replace(' ', '')) > nonsp + 20: ls = fresh; stats_fill[0] += 1
                elif job.get('merge_ocr'): ls = merge_with_ocr(doc, i, ls, job['merge_ocr'], job.get('deva_junk', False))
        elif route == 'glyphless':
            ls = lines_pymupdf(pg, lambda f: f == 'GlyphLessFont')
        elif route == 'font':
            ls = lines_pymupdf(pg, lambda f: bool(font_re.search(f)))
            if job.get('fill_ocr'):
                other = lines_pymupdf(pg, lambda f: not font_re.search(f))
                def covered(o):
                    return any(min(o.y1, L.y1) - max(o.y0, L.y0) > 0.4 * (o.y1 - o.y0) and min(o.x1, L.x1) - max(o.x0, L.x0) > 0 for L in ls)
                ybot = max((L.y1 for L in ls), default=0)
                rest = [o for o in other if not covered(o) and len(o.text) > 3 and o.y0 > ybot - 2]
                if rest:
                    r = fitz.Rect(min(o.x0 for o in rest) - 4, min(o.y0 for o in rest) - 4, max(o.x1 for o in rest) + 4, max(o.y1 for o in rest) + 4) & pg.rect
                    got = ocr_page(doc, i, job['fill_ocr'], dpi=300, clip=r, psm=6)
                    ls = ls + got; stats_fill[0] += 1
        elif route == 'ocr':
            if job.get('psm') == 'best':
                # read the page both ways, auto layout (psm 3) and one block (psm 6); keep the one with more dictionary words,
                # unless the page is two-column (8 Oct 2026: psm 3 dropped whole lines on some scans, e.g. the Paramarthasara)
                la = ocr_page(doc, i, langs, dpi=job.get('dpi', 300), psm=3); lb = ocr_page(doc, i, langs, dpi=job.get('dpi', 300), psm=6)
                _en = english(); _wc = lambda X: sum(1 for x in X for w in re.findall(r'[A-Za-z]{3,}', x.text) if w.lower() in _en)
                ls = lb if (_wc(lb) > 1.02 * _wc(la) and not order_columns(la, W)[1]) else la
            else:
                ls = ocr_page(doc, i, langs, dpi=job.get('dpi', 300), psm=job.get('psm', 3))
            if job.get('latin_fix'): ls = latin_fix(doc, i, ls, job['latin_fix'], dpi=job.get('dpi', 300), stats=stats_latin)
            if job.get('san_pages') and wants_san(pg, ls):
                # Devanagari on this page: read it again with Latin+san and take only the lines that come out in Devanagari
                ls2 = ocr_page(doc, i, langs + '+san', dpi=job.get('dpi', 300))
                dl = [L for L in ls2 if len(DEVA.findall(L.text)) > 0.5 * max(1, len(L.text.replace(' ', '')))]
                if dl:
                    def ov(a, b): return min(a.y1, b.y1) - max(a.y0, b.y0) > 0.5 * min(a.y1 - a.y0, b.y1 - b.y0) and min(a.x1, b.x1) - max(a.x0, b.x0) > 0
                    ls = [L for L in ls if not any(ov(L, D) for D in dl)] + dl
                    stats_fill[0] += 1
            ocr_conf += [s['conf'] for L in ls for s in L.spans if 'conf' in s]
        else:
            raise SystemExit('unknown route ' + route)
        if job.get('deva_reocr') and route != 'ocr':
            ls = reocr_deva_lines(doc, i, ls)
        pd_ = dict(lines=ls, W=W, H=H)
        if route == 'font': pd_['num_lines'] = [L for L in lines_pymupdf(pg) if L.y1 < H * 0.16 or L.y0 > H * 0.86]
        pages.append(pd_)
        if job.get('progress') and i % 25 == 0: print(f'  page {i + 1}/{N}', flush=True)

    # --- body size (book-level mode, weighted by characters)
    cnt = collections.Counter()
    for p in pages:
        for L in p['lines']:
            lat = len(re.findall(r'[A-Za-zÀ-ɏḀ-ỿ]', L.text))
            if lat > 0.5 * max(1, len(L.text.replace(' ', ''))): cnt[round(L.size * 2) / 2] += lat
    body = cnt.most_common(1)[0][0] if cnt else 10
    tot_ = sum(cnt.values()) or 1
    size_steady = sum(v for k, v in cnt.items() if abs(k - body) <= 0.5) / tot_ > 0.6
    bold_ = sum(len(sp_['text']) for p in pages for L in p['lines'] for sp_ in L.spans if sp_.get('flags', 0) & 16)
    all_ = sum(len(sp_['text']) for p in pages for L in p['lines'] for sp_ in L.spans) or 1
    bold_common = bold_ / all_ > 0.4
    # --- running headers / footers
    zone = collections.Counter()
    def zone_lines(p):
        ls = sorted(p['lines'], key=lambda L: L.y0)
        if not ls: return [], []
        y_top = min(ls[0].y0, p['H'] * 0.15); y_bot = max(ls[-1].y1, p['H'] * 0.85)
        top = [L for L in ls[:3] if L.y1 < max(p['H'] * 0.12, y_top + p['H'] * 0.05)]
        bot = [L for L in ls[-3:] if L.y0 > min(p['H'] * 0.88, y_bot - p['H'] * 0.05)]
        return top, bot
    tails = collections.Counter()
    for p in pages:
        top, bot = zone_lines(p)
        for L in top: zone['t' + norm_hf(L.text)] += 1
        for L in bot: zone['b' + norm_hf(L.text)] += 1; tails[re.sub(r'^\W{0,2}\d+\.?\s*', '', L.text.strip())] += 1
    thr = max(3, int(0.015 * N))
    printed = [None] * N
    ebook = sum(1 for p in pages for L in p['lines'] if re.fullmatch(r'page_\d+', L.text.strip())) > 0.3 * N
    for i_, p in enumerate(pages):      # printer slugs and e-book chrome anywhere on the page
        for L in p['lines']:
            mpg_ = re.fullmatch(r'Page\s+(\d{1,4})', L.text.strip()) if ebook else None
            if mpg_:
                L.kind = 'hf'; printed[i_] = int(mpg_.group(1)); continue
            if re.search(r'\.indd\s+\d+|\b97[89]\s?\d{10}_', L.text) or re.match(r'^(< previous page|next page >|page_\d+|If you like this book, buy it!)', L.text.strip()) or re.fullmatch(r'Page \d{1,4} of \d{1,4}', L.text.strip()):
                L.kind = 'hf'
            elif re.fullmatch(r'\d{1,2}-[A-Z][a-z]{2}-\d{2}\s+\d{1,2}:\d{2}(:\d{2})?', L.text.strip()):
                L.kind = 'hf'      # printer's date-time stamp
    for i, p in enumerate(pages):
        top, bot = zone_lines(p)
        for z, L in [('t', L) for L in top] + [('b', L) for L in bot]:
            k = norm_hf(L.text)
            ltxt = re.sub(r'(?<=\d) (?=\d)', '', L.text.strip()) if re.fullmatch(r'[\d ]{3,9}', L.text.strip()) else L.text
            num = page_number_token(ltxt) if len(ltxt) < 120 else None
            pure_num = bool(re.fullmatch(r'[\(\[]?\s*(\d{1,4}|[ivxlcdmIVXLCDM]{1,7})\s*[\)\]]?', ltxt.strip()))
            note_like = z == 'b' and not pure_num and bool(re.match(r'^[\W]{0,2}\d{1,3}\.?\s+\S', L.text)) and L.size < body * 0.98 and tails[re.sub(r'^\W{0,2}\d+\.?\s*', '', L.text.strip())] < thr
            chrome = bool(re.match(r'^(< previous page|next page >|page_\d+|If you like this book, buy it!|Page \d+ of \d+$)', L.text.strip())) or bool(re.search(r'\.indd\s+\d+|\b97[89]\d{10}_', L.text))
            if chrome or (zone[z + k] >= thr or pure_num or (k in ('#', '# #'))) and not note_like:
                L.kind = 'hf'
                if num is not None and printed[i] is None: printed[i] = num
                mpg = re.fullmatch(r'Page\s+(\d{1,4})', L.text.strip())
                if mpg and printed[i] is None: printed[i] = int(mpg.group(1))
        if printed[i] is None and p.get('num_lines'):
            for L in p['num_lines']:
                if re.fullmatch(r'\s*\d{1,4}\s*', L.text): printed[i] = int(L.text); break
    if job.get('hf_top'):   # running heads that change with every text (Lost Scriptures): everything above this line, in points
        for p in pages:
            for L in p['lines']:
                if L.y1 <= job['hf_top']: L.kind = 'hf'
    runheads = None
    if job.get('head_re'):
        hre = re.compile(job['head_re'])
        runheads = [None] * N
        for i, p in enumerate(pages):
            top, _ = zone_lines(p)
            for L in top:
                t = re.sub(r'\s+', ' ', re.sub(r'\d+', '', L.text)).strip()
                if hre.match(t): runheads[i] = t.upper(); break
        first_lines = [' '.join(L.text for L in sorted(p['lines'], key=lambda L: L.y0)[:6]).lower() for p in pages]
        job['_first_lines'] = first_lines
    # --- chapter headings from large type, when the PDF has no usable outline
    job['_big_toc'] = []
    if route in ('pymupdf', 'font', 'glyphless') and not job.get('single') and not job.get('head_re') and job.get('big_heads', True):
        cand = []
        for i, p in enumerate(pages):
            ls = sorted([L for L in p['lines'] if L.kind != 'hf' and re.search(r'[A-Za-z]{2}', L.text)], key=lambda L: L.y0)
            if not ls: continue
            top = ls[0].y0; bottom = max(L.y1 for L in ls)
            upper = [L for L in ls if L.y0 < top + (bottom - top) * 0.4]
            if not upper: continue
            mx = max(L.size for L in upper)
            if mx < body * 1.3: continue
            hl = [L for L in upper if abs(L.size - mx) < 0.6]
            title = re.sub(r'\s+', ' ', ' '.join(L.text for L in hl)).strip()
            title = fix_spaced(title)
            if 2 < len(title) <= 120: cand.append((i, round(mx * 2) / 2, title))
        sizes = collections.Counter(c[1] for c in cand)
        chosen = None
        for sz in sorted(sizes, reverse=True):
            sel = [c for c in cand if c[1] >= sz]
            if len(sel) > 0.25 * N: break
            good = sum(1 for c in sel if re.search(r'[A-Za-z]{3,}', c[2]) and not re.search(r'[!,]{2}|\d{5}', c[2]))
            if len(sel) >= 4 and good >= 0.8 * len(sel) and len({c[2] for c in sel}) >= 4 and sel[0][0] < 0.3 * N:
                chosen = sz; break
        if chosen:
            job['_big_toc'] = [(1, t, i + 1) for i, sz, t in cand if sz >= chosen]
    # --- printed page numbers: PDF labels first, else header/footer numbers checked against neighbours
    def _lab(k):
        try: return re.sub(r'\\([0-7]{3})', lambda m: bytes([int(m.group(1), 8)]).decode('latin-1'), doc[k].get_label())   # 'Pr\\351sentation' (Persée PDFs) -> 'Présentation'
        except Exception: return ''
    labels = [_lab(i) for i in range(N)]
    use_labels = job.get('labels', 'auto')
    if use_labels == 'auto':
        use_labels = sum(1 for x in labels if x) > 0.8 * N and len(set(labels)) > 0.8 * N and sum(1 for i, x in enumerate(labels) if x == str(i + 1)) < 0.9 * N
        if any(re.search(r'[<>:]', x or '') for x in labels): use_labels = False
        both = [(labels[i], printed[i]) for i in range(N) if isinstance(printed[i], int) and labels[i] and labels[i].strip().isdigit()]
        if use_labels and len(both) > 0.3 * N and sum(1 for a, b in both if int(a) != b) > 0.5 * len(both):
            use_labels = False   # the labels disagree with the numbers printed on the pages
    pnum = [None] * N; psrc = [''] * N
    if use_labels:
        for i in range(N): pnum[i] = labels[i] or str(i + 1); psrc[i] = 'label' if labels[i] else 'pdf'
    else:
        off = [None] * N
        for i in range(N):
            if isinstance(printed[i], int): off[i] = printed[i] - (i + 1)
        ok = [False] * N
        for i in range(N):
            if off[i] is None: continue
            nb = [off[j] for j in range(max(0, i - 12), min(N, i + 13)) if j != i and off[j] is not None]
            if nb.count(off[i]) >= 1: ok[i] = True
        for i in range(N):
            if ok[i]: pnum[i] = str(printed[i]); psrc[i] = 'read'
            elif isinstance(printed[i], str): pnum[i] = printed[i]; psrc[i] = 'read'  # roman
        # fill gaps where both nearest read neighbours agree on the offset
        for i in range(N):
            if pnum[i] is not None: continue
            a = next((j for j in range(i - 1, max(-1, i - 16), -1) if ok[j]), None)
            b = next((j for j in range(i + 1, min(N, i + 16)) if ok[j]), None)
            if a is not None and b is not None and off[a] == off[b] and (i + 1 + off[a]) > 0:
                pnum[i] = str(i + 1 + off[a]); psrc[i] = 'inferred'
            else:
                pnum[i] = str(i + 1); psrc[i] = 'pdf'

    for i, p in enumerate(pages):
        top, bot = zone_lines(p)
        for L in top + bot:
            if L.kind == 'hf' or len(L.text) > 120: continue
            toks = re.findall(r'\b[\dIVXLCivxlc]+\b', L.text)
            if pnum[i] in toks and len(L.text) < 90: L.kind = 'hf'
    for k_, v_ in (job.get('pnum_override') or {}).items():   # {pdf page: printed page(s)}, e.g. a two-page spread "22–23"
        pnum[int(k_) - 1] = v_; psrc[int(k_) - 1] = 'given'
    # --- per page: footnotes and paragraphs
    toc = [tuple(x) for x in job['toc']] if job.get('toc') else (clean_toc(doc.get_toc(), N) if job.get('use_toc', True) else [])   # 'toc': [[level, title, pdf page]] from the printed Contents
    if job.get('ocr_ranges') and job.get('_big_toc'):   # big type on junk-layer pages is not a heading
        job['_big_toc'] = [t for t in job['_big_toc'] if not any(r[0] <= t[2] <= r[1] for r in job['ocr_ranges'])]
    if sum(1 for t in toc if t[0] == 1) < 2 and job.get('_big_toc') and not runheads:
        toc = [t for t in toc if t[0] != 1] + job['_big_toc']
    heads = collections.defaultdict(list)  # pdf page index -> [(level, title)]
    for lvl, title, pno in toc:
        if 1 <= pno <= N: heads[pno - 1].append((lvl, title.strip()))
    italics = route in ('pymupdf', 'font')
    page_md = []
    last_note = [None]
    DZ = json.load(open(job['dz'])) if job.get('dz') else None
    _dcache = {}
    def pg_drawings(k):
        if k not in _dcache:
            dr = doc[k].get_drawings() if route in ('pymupdf', 'font') else []
            if dr and doc[k].rotation:   # drawn rules in the page as shown, like the text (see lines_pymupdf)
                M = doc[k].rotation_matrix; dr = [dict(x, rect=x['rect'] * M) for x in dr]
            _dcache[k] = dr
        return _dcache[k]
    fn_pages = []
    stats = collections.Counter()
    for i, p in enumerate(pages):
        ls = [L for L in p['lines'] if L.kind != 'hf']
        if job.get('gutter_bands'): ls = order_gutter_bands(ls, p['W'], p['H']); twocol = False
        elif job.get('ncols'): ls = order_ncols(ls, p['W'], job['ncols']); twocol = False
        elif route == 'ocr' or not job.get('columns', True): twocol = False
        else: ls, twocol = order_columns(ls, p['W'])
        hebl = [L for L in ls if len(HEB.findall(L.text)) > 0.5 * max(1, len(re.findall(r'[A-Za-z\u0590-\u05FF]', L.text)))]
        latl = [L for L in ls if L not in hebl]
        side = False
        if len(hebl) >= 3 and len(latl) >= 3:
            hx = statistics.median((L.x0 + L.x1) / 2 for L in hebl); lx = statistics.median((L.x0 + L.x1) / 2 for L in latl)
            side = abs(hx - lx) > 0.25 * p['W']      # Hebrew in its own column (facing text), not alternating paragraphs
        if side:
            hid = set(map(id, hebl)); ls = hebl + [L for L in ls if id(L) not in hid]; stats['hebrew_side_pages'] += 1
        if twocol: stats['two_column_pages'] += 1
        # footnote zone: trailing lines smaller than body, in the lower part of the page
        notes_ls = []
        dzp = DZ['pages'].get(str(i + 1)) if DZ else None
        if dzp is not None:
            # notes found by the footnote rule; starts and numbers from the prepared data (Dyczkowski)
            if dzp['rule'] is not None:
                notes_ls = [L for L in ls if L.y0 > dzp['rule'] - 1]
                ls = [L for L in ls if L.y0 <= dzp['rule'] - 1]
        elif job.get('footnotes', True) and ls:
            up = collections.Counter()
            for L in ls:
                if L.y0 < p['H'] * 0.6:
                    up[round(L.size * 2) / 2] += len(re.findall(r'[A-Za-zÀ-ɏḀ-ỿ]', L.text))
            pbody = max(up, key=up.get) if up and sum(up.values()) > 200 else body
            ref = min(body, pbody) if pbody < body * 0.97 else body
            def is_small(L): return L.size < ref * 0.93
            fl = []
            for L in ls:
                if not is_small(L) or L.y0 < p['H'] * 0.45: continue
                below = [M for M in ls if M.y0 > L.y1 - 1 and not is_small(M) and min(M.x1, L.x1) - max(M.x0, L.x0) > 0 and len(M.text) > 3]
                if not below: fl.append(L)
            if fl:
                # keep only the smallest type at the bottom (block quotations are smaller than the body but larger than notes)
                fsz = min(L.size for L in fl if len(L.text) > 10) if any(len(L.text) > 10 for L in fl) else min(L.size for L in fl)
                if job.get('fn_max_size'):   # notes set in one known size, with other small type (a translation credit) below them
                    fl = [L for L in fl if L.size <= job['fn_max_size']]
                else:
                    k = len(fl)
                    while k > 0 and (fl[k - 1].size <= fsz + 0.7 or len(fl[k - 1].text) <= 10): k -= 1
                    fl = fl[k:]
            if fl:
                bl = [L for L in ls if L not in fl]
                if twocol:   # on a two-column page compare with the body lines of the notes' own column
                    fx = (min(L.x0 for L in fl) + max(L.x1 for L in fl)) / 2
                    bl = [L for L in bl if (L.x0 + L.x1) / 2 < p['W'] / 2] if fx < p['W'] / 2 else [L for L in bl if (L.x0 + L.x1) / 2 >= p['W'] / 2]
                lm = min((L.x0 for L in bl), default=None)
                if lm is not None and min(L.x0 for L in fl) > lm + max(4, body * 0.6):
                    fl = []          # indented on the left: a block quotation, not footnotes
            if fl:
                first = fl[0]
                above = [L for L in ls if L.y1 <= first.y0 + 1 and L not in fl]
                gap_above = first.y0 - max((L.y1 for L in above), default=0)
                has_rule = False
                try:
                    for dr in pg_drawings(i):
                        r_ = dr['rect']
                        if r_.height < 2 and 20 < r_.width < p['W'] * 0.95 and first.y0 - 25 < r_.y0 < first.y0 + 1: has_rule = True; break
                except Exception:
                    pass
                numbered = re.match(r'^\W{0,2}(\d{1,3}|[*†‡])', first.text) or first.spans[0]['sup'] or sum(1 for L in fl if re.match(r'^\W{0,2}\d{1,3}\s+\S', L.text)) >= 1 and len(fl) >= 2
                carried = page_md and page_md[-1]['notes'] and (has_rule or gap_above > body * 1.2)
                if numbered or carried:
                    fid = set(map(id, fl)); notes_ls = fl; ls = [L for L in ls if id(L) not in fid]
        notes = collections.OrderedDict(); cont = []
        curn = None
        bodyrefs = set()
        for L in ls:
            for sp_ in L.spans:
                if sp_['sup']: bodyrefs.add(sp_['text'].strip().rstrip('.,'))
            for m in re.finditer(r'(?<=[A-Za-zà-ÿ\.,;:!?\)\]’”\'"])(\d{1,3})(?=[\s,.;:)\]—–-]|$)', L.text):
                bodyrefs.add(m.group(1))
        dz_unc = set()
        for L in (notes_ls if dzp is not None else []):
            hit = next((st_ for st_ in dzp['starts'] if min(st_[1], L.y1) - max(st_[0], L.y0) > 0.4 * min(st_[1] - st_[0], L.y1 - L.y0)), None)
            if hit:
                curn = str(hit[2]); md_ = note_md(L, italics)
                tok = md_.split(' ', 1)
                if len(tok) == 2 and not re.search(r'[a-zāīūṛṝḷṃṁḥṅñṭḍṇśṣ]', tok[0]): md_ = tok[1]
                notes[curn] = [md_]
                if not hit[3]: dz_unc.add(curn)
            elif curn is None: cont.append(note_md(L, italics))
            else: notes[curn].append(note_md(L, italics))
        if job.get('fn_runin') and dzp is None and notes_ls:
            # several notes run on in one line, each opening with a raised number or letter (Lost Scriptures: "3Titus 3:1. 4Prov 7:3.")
            def is_lab(x, L):
                return (x['sup'] or x['size'] < L.size * 0.85) and re.fullmatch(r'\d{1,3}|[a-z]', x['text'].strip() or '#')
            for L in sorted(notes_ls, key=lambda L: (round(L.y0 / 3), L.x0)):
                pieces = []
                for x in L.spans:
                    if is_lab(x, L) or not pieces: pieces.append([x])
                    else: pieces[-1].append(x)
                for pc in pieces:
                    if not ''.join(x['text'] for x in pc).strip(): continue
                    PL = Line(pc)
                    if is_lab(pc[0], L) and len(pc) > 1:
                        curn = pc[0]['text'].strip(); notes[curn] = [note_md(Line(pc[1:]), italics)]
                    elif curn is None: cont.append(note_md(PL, italics))
                    else: notes[curn].append(note_md(PL, italics))
            notes_ls = []
        for L in (notes_ls if dzp is None else []):
            m = re.match(r'^\W{0,2}?(\d{1,3}|[*†‡]+)[.)]?\s*', L.text)
            first_sup = L.spans[0]['sup'] or (L.spans[0]['size'] < L.size * 0.85 and re.fullmatch(r'\d{1,3}', L.spans[0]['text'].strip() or 'x'))
            start = False
            if m and m.group(0).strip() != L.text.strip():
                n = m.group(1)
                if first_sup or n in bodyrefs: start = True
                elif curn is None and not cont: start = True
                elif curn is not None and n.isdigit() and curn.isdigit() and int(n) == int(curn) + 1: start = True
                elif curn is None and n.isdigit() and last_note[0] is not None and int(n) == last_note[0] + 1: start = True
            if start:
                curn = m.group(1); notes[curn] = [note_md(L, italics, strip=True)]
                if curn.isdigit(): last_note[0] = int(curn)
            elif curn is None:
                cont.append(note_md(L, italics))
            else:
                notes[curn].append(note_md(L, italics))
        # body paragraphs
        refs = []
        paras = []  # list of [text, kind]
        prev = None; prev_kind = 'p'; pending_head = None; cur_first_x0 = 0; cur_n = 0
        if job.get('entry_lines'):
            # glossaries: every line that starts at its column's left edge is an entry of its own (wrapped lines are indented)
            _nc = job.get('ncols', 1); _cw = p['W'] / _nc
            _band = lambda L: min(_nc - 1, int(((L.x0 + L.x1) / 2) / _cw))
            _cleft = {}
            for L in ls: _cleft[_band(L)] = min(_cleft.get(_band(L), 1e9), L.x0)
        gaps = [b.y0 - a.y1 for a, b in zip(ls, ls[1:]) if 0 <= b.y0 - a.y1 < body * 3]
        med_gap = statistics.median(gaps) if gaps else body * 0.3
        left = min((L.x0 for L in ls), default=0)
        right = max((L.x1 for L in ls), default=p['W'])
        cb = {}
        if twocol and job.get('col_bounds', True):
            # the column's own margins: a line ending short of the page's right margin is not a paragraph end in the left column
            lc = [L for L in ls if (L.x0 + L.x1) / 2 < p['W'] / 2 and L.x1 - L.x0 < p['W'] * 0.5]
            rc = [L for L in ls if (L.x0 + L.x1) / 2 >= p['W'] / 2 and L.x1 - L.x0 < p['W'] * 0.5]
            if len(lc) >= 4 and len(rc) >= 4:
                lb = (min(L.x0 for L in lc), max(L.x1 for L in lc)); rb_ = (min(L.x0 for L in rc), max(L.x1 for L in rc))
                for L in ls:
                    if L.x1 - L.x0 < p['W'] * 0.5: cb[id(L)] = lb if (L.x0 + L.x1) / 2 < p['W'] / 2 else rb_
        def lft(L): return cb.get(id(L), (left, right))[0]
        def rgt(L): return cb.get(id(L), (left, right))[1]
        hl = heads.get(i, [])
        for L in ls:
            t = line_markdown(L, italics, notes, refs)
            if not t.strip(): continue
            plain = re.sub(r'[\W_]+', '', L.text).lower()
            heading = None
            if pending_head is not None:
                lvl, tt, acc = pending_head
                if tt.startswith(acc + plain) and plain:
                    acc = acc + plain
                    pending_head = (lvl, tt, acc) if len(acc) < len(tt) else None
                    prev = L; continue
                pending_head = None
            for lvl, title in hl:
                tt = re.sub(r'[\W_]+', '', title).lower()
                core = re.sub(r'[\W_]+', '', re.sub(r'^\s*((chapter|part|book)\s+)?([0-9]+|[IVXLC]+)[.:)]?\s+', '', title, flags=re.I)).lower()
                if not tt or len(plain) < 4: continue
                hit = None
                for cand in {tt, core}:
                    if not cand: continue
                    if plain == cand or cand.endswith(plain) and len(plain) >= 8: hit = (cand, False); break
                    if cand.startswith(plain) and len(plain) >= 6: hit = (cand, True); break
                if not hit and job.get('fuzzy_heads') and re.match(r'^\W{0,2}[IVXLHl1]{1,6}[:.;]|^\W{0,2}[A-K]\.\s', L.text.strip()):
                    # a numbered heading printed differently from the Contents (Hock: "IH: ‘Lead me from untruth to truth ...")
                    lw = set(re.findall(r'[^\W\d_]{3,}', L.text.lower())); tw = set(re.findall(r'[^\W\d_]{3,}', title.lower()))
                    if len(lw) >= 2 and len(lw & tw) >= max(2, 0.6 * len(lw)): hit = (tt, False)
                if hit:
                    heading = (lvl, title)
                    if hit[1]: pending_head = (lvl, hit[0], plain)
                    break
            new = False
            letters = re.findall(r'[A-Za-zÀ-ɏḀ-ỿ]', L.text)
            headlike = (not heading and len(L.text) <= 100 and (L.x1 - L.x0) < (right - left) * 0.8 and len(letters) >= 3
                        and not re.search(r'[,;]$', L.text.strip())
                        and ((size_steady and L.size >= body * 1.12) or (not bold_common and all((sp_['flags'] & 16) for sp_ in L.spans if sp_['text'].strip()))
                             or (sum(1 for c in letters if c.isupper()) > 0.85 * len(letters) and len(letters) >= 6)))
            if prev is None: new = True
            else:
                gap = L.y0 - prev.y1
                col_jump = L.y0 < prev.y0 - body  # moved up: next column
                prev_full = prev.x1 >= rgt(prev) - p['W'] * 0.05 and not re.search(r'[.?!:"”’)]\s*$', prev.text)
                lf = lft(L)
                if heading or (prev_kind in ('h', 'hl')): new = True
                elif headlike: new = True
                elif gap > med_gap + body * 0.9 and not col_jump: new = True
                elif L.x0 > lf + body * 0.8 and abs(L.x0 - prev.x0) > body * 0.8 and not col_jump and L.x0 - lf < p['W'] * 0.25 and not prev_full: new = True
                elif L.x0 <= lf + body * 0.3 and prev.x0 > lf + body * 0.8 and cur_first_x0 <= lf + body * 0.3 and cur_n >= 2 and not col_jump: new = True  # hanging indent: next entry
                elif prev.x1 < rgt(prev) - (p['W'] * 0.12 if not cb else (rgt(prev) - lft(prev)) * 0.1) and re.search(r'[.?!:"”’)]\s*$', prev.text): new = True
                elif re.match(r'^\d{1,3}\.\s+[A-Z‘“"(]', L.text) and re.search(r'[.)”’]\s*$', prev.text) and L.x0 <= lf + body * 1.5: new = True   # numbered notes or list items
            if job.get('entry_lines') and prev is not None and not new and L.x0 <= _cleft.get(_band(L), L.x0) + body * 0.6: new = True
            if heading:
                lvl, title = heading
                if (lvl, title) in [(a, b) for a, b in hl]: hl = [x for x in hl if x != heading]
                paras.append(['#' * min(6, max(2, lvl + 1)) + ' ' + md_escape(title), 'h']); prev = L; prev_kind = 'h'; continue
            if prev is not None and not new and (len(HEB.findall(prev.text)) > 3) != (len(HEB.findall(L.text)) > 3): new = True
            if new: paras.append([t, 'p']); cur_first_x0 = L.x0; cur_n = 1
            elif re.search(r'(//?|\|\|?|।|॥)\s*[\d°\']*\s*$', paras[-1][0]) and job.get('verse_breaks', True): paras[-1][0] = paras[-1][0].rstrip() + '\n' + t.lstrip(); cur_n += 1
            else: paras[-1][0] = join_lines(paras[-1][0], t); cur_n += 1
            prev = L; prev_kind = 'hl' if headlike else 'p'
        # headings in the TOC for this page that were not matched: put them at the top of the page
        if job.get('skip_unmatched_sub'):   # a sub-heading not found on its page is left out rather than put at the top (the printed heading stays as text)
            stats['toc_subheading_skipped'] += sum(1 for lvl, _ in hl if lvl >= 2); hl = [x for x in hl if x[0] < 2]
        for k, (lvl, title) in enumerate(hl):
            paras.insert(k, ['#' * min(6, max(2, lvl + 1)) + ' ' + md_escape(title), 'h']); stats['toc_heading_unmatched'] += 1
        if dzp is not None and notes and dzp['rule'] is not None:
            try:
                import dzfn
                prs = dzfn.page_refs(doc[i], dzp['rule'])
            except Exception:
                prs = []
            nums = list(notes.keys())
            if prs and len(prs) == len(nums):
                done_all = True; newp = [list(x) for x in paras]
                for r_, n_ in zip(prs, nums):
                    key = r_['clean'].strip('()[].,;:’”‘“"\'')[-6:]
                    placed = False
                    for pi in range(len(newp)):
                        if newp[pi][1] != 'p': continue
                        t_ = newp[pi][0]
                        # the garbled word: its letters, then a run of junk characters
                        for m_ in re.finditer(r'(\S*?)((?:TM|™|\\\*|\\\^|\\\$|[°®%]|[0-9०-९]{1,4}|[’”"\'])+)(?=\s|$)', t_):
                            word_ = m_.group(1)
                            if not re.search(r'TM|™|\\\*|\\\^|\\\$|[°®%0-9०-९]', m_.group(2)): continue
                            if re.fullmatch(r'[0-9०-९]+', m_.group(2)) and re.search(r'(\d[.:,/-]?|\b(p|pp|vol|no|v|vv|ch)\.)$', word_): continue
                            if not word_ and re.fullmatch(r'[0-9०-९’”"\']+', m_.group(2)): continue     # a bare number: a verse number, not a mark
                            if key and key.lower() not in (word_ + m_.group(2)).lower() and r_['src'] == 'tess' and re.search(r'[A-Za-z]', word_):
                                continue
                            if not re.search(r'[A-Za-zāīūṛṝḷṃṁḥṅñṭḍṇśṣ]', word_): word_ = r_['clean']
                            newp[pi][0] = t_[:m_.start()] + word_ + '\x00REF' + n_ + '\x00' + t_[m_.end():]
                            placed = True; break
                        if placed: break
                    if not placed and r_['src'] == 'tess':
                        # the text layer lost the word itself ('state).593' read as '5131९).'): a token of digits and punctuation only
                        for pi in range(len(newp)):
                            if newp[pi][1] != 'p': continue
                            t_ = newp[pi][0]
                            m_ = re.search(r'(?<!\S)(?=\S*[0-9०-९])(?=\S*[०-९%°®™’”\*])[0-9०-९%°®™\)\]\.,;:’”"\'\\\*]{3,}(?=\s|$)', t_)
                            if m_:
                                newp[pi][0] = t_[:m_.start()] + r_['clean'] + '\x00REF' + n_ + '\x00' + t_[m_.end():]
                                placed = True; break
                    if not placed: done_all = False; break
                if done_all:
                    paras = newp; refs.extend(nums); stats['dz_pages_linked'] += 1
            stats['dz_notes'] += len(nums)
        # references printed as ordinary digits after a word ('importance.1 It'): link them when the note is on this page
        if notes and job.get('text_refs', True):
            pos = 0
            for n in [n for n in notes if n not in refs and n.isdigit()]:
                pat = re.compile(r'(?<=[A-Za-zà-ÿ\.,;:!?\)\]’”\'"])' + n + r'(?=[\s,.;:)\]—–-]|$)')
                done = False
                for pi in range(len(paras)):
                    if paras[pi][1] != 'p': continue
                    t = paras[pi][0]
                    for m in pat.finditer(t):
                        before = t[max(0, m.start() - 6):m.start()]
                        if re.search(r'\b(p|pp|vol|no|nos|ch|fig|n|nn|cf|l|ll|v|vv|art|sec|col)\.$', before, re.I): continue
                        if re.search(r'\d[.,:]$', before): continue
                        paras[pi][0] = t[:m.start()] + '\x00REF' + n + '\x00' + t[m.end():]
                        refs.append(n); done = True; stats['text_refs'] += 1
                        break
                    if done: break
        stats['footnotes'] += len(notes); stats['refs'] += len(refs)
        if notes: fn_pages.append(i)
        stats['notes_without_ref'] += len([n for n in notes if n not in refs])
        page_md.append(dict(paras=paras, notes=notes, cont=cont, refs=refs, unc=dz_unc))

    # --- join words hyphenated across pages; continuation of notes across pages
    for i in range(N - 1):
        a, b = page_md[i], page_md[i + 1]
        if a['paras'] and b['paras'] and a['paras'][-1][1] == 'p' and b['paras'][0][1] == 'p':
            ta, tb = a['paras'][-1][0], b['paras'][0][0]
            m = re.search(r'(\w+)-$', ta); m2 = re.match(r'^([a-zà-ÿāīūṛṝḷṃṁḥṅñṭḍṇśṣ]+)(.*)$', tb, re.S)
            if m and m2:
                joined = dehyph(m.group(1), m2.group(1))
                a['paras'][-1][0] = ta[:m.start()] + joined
                b['paras'][0][0] = m2.group(2).lstrip()
                if not b['paras'][0][0]: b['paras'].pop(0)
        if b['cont'] and a['notes']:
            last = next(reversed(a['notes']))
            a['notes'][last] += b['cont']; b['cont'] = []

    # --- fonts that print fi/fl/ff ligatures as W/X/V ('Wrst', 'reXect'): repair when the book shows it often
    if route in ('pymupdf', 'font') and job.get('ligfix', True):
        sample = ' '.join(t for pm in page_md[::max(1, N // 80)] for t, k in pm['paras'])
        bad = [m.group(0) for m in LIGTOK.finditer(sample) if lig_fix_token(m.group(0)) != m.group(0)]
        if len(bad) >= 8: job['_ligfix'] = True; stats['ligature_fix'] = len(bad)
        iso = re.findall(r'(?<!\S)[' + IASTC + r'](?!\S)', sample)
        if len(iso) >= 20: job['_spaced_iast'] = True; stats['spaced_iast_fix'] = len(iso)
    if route == 'pymupdf' and stats_fill[0] and not job.get('_ts_done'):
        job['text_source'] = job['text_source'] + f'; {stats_fill[0]} pages read by OCR (Tesseract) where the text layer has no Unicode'
        job['_ts_done'] = True
    # --- chapters
    chapters = make_chapters(toc, N, job, runheads)
    used_global = set()
    outdir = os.path.join(job['out'], job['folder'])
    os.makedirs(outdir, exist_ok=True)
    today = job.get('date', datetime.date.today().isoformat())
    notes_written = []; written = []
    for ci, ch in enumerate(chapters):
        a, b = ch['start'], ch['end']
        body_lines = []
        if ch.get('title_heading'):
            body_lines.append('# ' + md_escape(ch['title']))
            body_lines.append('')
        used = set()
        for i in range(a, b + 1):
            pm = page_md[i]
            body_lines.append(f'*[p. {pnum[i]}]* ^pg{i + 1}')
            body_lines.append('')
            labelmap = {}
            for n in pm['notes']:
                lab = n if n not in used else f'{n}-p{pnum[i]}'
                lab = re.sub(r'[^\w.-]', '', lab) or f'n{len(used)}'
                if lab in used: lab = f'{lab}-{i + 1}'
                used.add(lab); labelmap[n] = lab
            if pm['cont'] and not pm['paras']:
                pass
            for t, kind in pm['paras']:
                t = re.sub('\x00REF(.*?)\x00', lambda m: '[^' + labelmap.get(m.group(1), m.group(1)) + ']' if m.group(1) in labelmap else '<sup>' + m.group(1) + '</sup>', t)
                t = postfix(t, job)
                if kind == 'p': t = block_escape(t)
                body_lines.append(t); body_lines.append('')
            if pm['cont']:
                body_lines.append(postfix(join_all(pm['cont']), job)); body_lines.append('')
            for n, parts in pm['notes'].items():
                if n in pm['refs']:
                    body_lines.append(f'[^{labelmap[n]}]: ' + postfix(join_all(parts), job))
                else:  # no reference found on the page: keep the note as visible text (an unreferenced definition would be hidden)
                    body_lines.append(md_escape(n) + ('?' if n in pm.get('unc', ()) else '') + '\\. ' + postfix(join_all(parts), job)); body_lines.append('')
            if pm['notes']: body_lines.append('')
        nb_ = [k for k in range(a, b + 1) if psrc[k] != 'pdf']   # the range from printed numbers: an unnumbered title page at either end is not counted
        a2, b2 = (nb_[0], nb_[-1]) if nb_ else (a, b)
        pr = f"{pnum[a2].split('–')[0]}–{pnum[b2].split('–')[-1]}" if a2 != b2 else f'{pnum[a2]}'
        fm = ['---', 'type: book-chapter', f'work: "[[{job["catalog"]}]]"', f'book: "[[{job["folder"]}/{job["index_name"]}|{job["index_name"]}]]"',
              f'order: {ci + 1}', f'source_pdf: "{job["pdf_vault"]}"', f'pages: "{_yq(pr)}"', f'pdf_pages: "{a + 1}–{b + 1}"',
              f'text_source: "{job["text_source"]}"', f'converted: {today}', '---', '']
        if job.get('single'):
            fm1 = ['---', f'type: {job.get("ctype") or "article"}', f'title: "{job["title"]}"', f'author: {json.dumps(job["authors"], ensure_ascii=False)}',
                   f'work: "[[{job["catalog"]}]]"', f'source_pdf: "{job["pdf_vault"]}"', f'pages: "{_yq(pr)}"', f'pdf_pages: "1–{N}"',
                   f'text_source: "{job["text_source"]}"', f'converted: {today}', '---',
                   f'# {job["title"]}', '', job.get('byline', ''), '',
                   f'Converted from the PDF on {datetime.date.fromisoformat(today).strftime("%-d %b %Y")}. Each PDF page starts with `*[p. N]*`, the printed page number (or the PDF page where none is printed), ending in the block id `^pgK` for PDF page K. The PDF stays on the computer: open it from [[{job["catalog"]}|the catalog note]].', ''] + ([job['callout'], ''] if job.get('callout') else [])
            spath = os.path.join(job['out'], os.path.dirname(job['folder']), job['index_name'] + '.md')
            open(spath, 'w', encoding='utf-8').write('\n'.join(fm1 + body_lines).rstrip() + '\n')
            written.append((os.path.dirname(job['folder']) + '/' + job['index_name'] + '.md', spath))
            ch['pages'] = pr
            continue
        nav = []
        if ci > 0: nav.append(f'[[{chapters[ci - 1]["name"]}|← previous]]')
        nav.append(f'[[{job["index_name"]}|contents]]')
        if ci < len(chapters) - 1: nav.append(f'[[{chapters[ci + 1]["name"]}|next →]]')
        co = [job['callout'], ''] if job.get('callout') else []
        txt = '\n'.join(fm + [' · '.join(nav), ''] + co + body_lines).rstrip() + '\n'
        open(os.path.join(outdir, ch['name'] + '.md'), 'w', encoding='utf-8').write(txt)
        notes_written.append(ch['name']); written.append((job['folder'] + '/' + ch['name'] + '.md', os.path.join(outdir, ch['name'] + '.md')))
        ch['pages'] = pr
    # --- index note
    if job.get('single'): idx = None
    else:
      idx = ['---', 'type: book', f'title: "{job["title"]}"', f'author: {json.dumps(job["authors"], ensure_ascii=False)}', f'work: "[[{job["catalog"]}]]"',
           f'source_pdf: "{job["pdf_vault"]}"', f'pages: {N}', f'text_source: "{job["text_source"]}"', f'converted: {today}', '---',
           f'# {job["title"]}', '', job.get('byline', ''), '',
           f'Converted from the PDF on {datetime.date.fromisoformat(today).strftime("%-d %b %Y")} ({job["text_source"]}). Each PDF page starts with a line `*[p. N]*` giving the printed page number (or the PDF page where none is printed) and ending in the block id `^pgK`, K being the PDF page, so a link to PDF page K can be written `[[Chapter note#^pgK]]`. The PDF stays on the computer: open it from [[{job["catalog"]}|the catalog note]].', ''] + ([job['callout'], ''] if job.get('callout') else []) + [
           '## Contents', '']
    if idx is not None:
        gh = job.get('contents_heads', {})   # {chapter title: heading printed above it in the book's Contents (a Part)}
        for ch in chapters:
            kt = re.sub(r', part 1$', '', ch['title'])   # a long chapter split in parts keeps its heading before part 1
            if ch['title'] in gh or kt in gh: idx += ['', f'### {gh.get(ch["title"], gh.get(kt))}', '']
            idx.append(f'- [[{ch["name"]}|{md_escape(ch["title"])}]] (pp. {ch["pages"]})')
        open(os.path.join(outdir, job['index_name'] + '.md'), 'w', encoding='utf-8').write('\n'.join(idx).rstrip() + '\n')
        written.append((job['folder'] + '/' + job['index_name'] + '.md', os.path.join(outdir, job['index_name'] + '.md')))
    rep = dict(fn_pages=fn_pages, fill_ocr_pages=stats_fill[0], latin_fixed_lines=stats_latin[0], pdf=job['pdf_vault'], folder=job['folder'], pages=N, notes=len(chapters) + 1, body_size=body, stats=dict(stats),
               page_src=dict(collections.Counter(psrc)), labels_used=bool(use_labels), chapters=[(c['name'], c['start'] + 1, c['end'] + 1) for c in chapters],
               ocr_conf_mean=round(statistics.mean(ocr_conf), 1) if ocr_conf else None, pnum=pnum, written=written)
    json.dump(rep, open(os.path.join(outdir, '_report.json'), 'w'), ensure_ascii=False, indent=1)
    return rep


def join_all(parts):
    t = ''
    for p in parts: t = join_lines(t, p) if t else p
    return t.strip()


def dehyph(a, b):
    if f'{a}-{b}'.lower() in HYPH_SEEN: return f'{a}-{b}'
    w = (a + b).lower()
    if w in EN or w in WORDS_SEEN: return a + b
    if any(c in IAST for c in a + b) or a[:1].isupper(): return f'{a}-{b}'
    if a.lower() in EN and b.lower() in EN and len(a) > 2 and len(b) > 2: return f'{a}-{b}'
    return a + b


HYPH_SEEN = set(); WORDS_SEEN = set()


def join_lines(a, b):
    a = a.rstrip(); b = b.lstrip()
    if a.endswith('\u00ad'): a = a[:-1] + '-'
    m = re.search(r'(\w+)-$', a)
    m2 = re.match(r'^(\w+)', b)
    if m and m2 and b[:1].islower():
        return a[:m.start()] + dehyph(m.group(1), m2.group(1)) + b[m2.end():]
    m = re.search(r'(\w+)-\*$', a); m2 = re.match(r'^\*(\w+)', b)
    if m and m2 and m2.group(1)[:1].islower():   # a hyphenated word broken inside italics: '*Interpreta-*' '*tion*'
        return a[:m.start()] + dehyph(m.group(1), m2.group(1)) + b[m2.end():]
    if a.endswith('—') or a.endswith('/'): return a + b
    if re.search(r'\w-$', a) and re.match(r'^[A-Z]', b): return a + b          # 'anti-' + 'Semites'
    if a.endswith('*') and not a.endswith('**') and b.startswith('*') and not b.startswith('**') and re.search(r'\w\*$', a) and re.match(r'^\*\w', b):
        return a[:-1] + ' ' + b[1:]           # one italic phrase broken across lines
    return a + ' ' + b


def block_escape(t):
    m = re.match(r'^(\s*)(\d+)([.)])( |$)', t)
    if m: return m.group(1) + m.group(2) + '\\' + m.group(3) + t[m.end(3):]
    t = re.sub(r'^(\s*)(#|>|[-+] |=+$)', lambda m: m.group(1) + '\\' + m.group(2), t)
    return t


_DICT = None
def english():
    global _DICT
    if _DICT is None:
        _DICT = set()
        for f in ('/usr/share/dict/american-english-large', '/usr/share/dict/british-english-large'):
            try: _DICT |= {w.strip().lower() for w in open(f, encoding='utf-8', errors='ignore')}
            except OSError: pass
    return _DICT
LIG = {'W': 'fi', 'X': 'fl', 'V': 'ff', 'Y': 'ffi', 'Z': 'ffl'}
LIGTOK = re.compile(r"\b[A-Za-z]*[a-z][WXVYZ][a-z][A-Za-z]*\b|\b[WXVYZ][a-z]{2,}\b|\b[a-z]+[WXVYZ]\b")
def lig_fix_token(w):
    d = english()
    if w.lower() in d and not re.search(r'[a-z][WXVYZ]', w): return w
    cands = {w}
    for _ in range(2):
        cands |= {c[:i] + LIG[ch] + c[i + 1:] for c in list(cands) for i, ch in enumerate(c) if ch in LIG and (i == 0 or c[i - 1].islower() or i + 1 < len(c) and c[i + 1].islower())}
    good = [c for c in cands if c != w and c.lower() in d]
    if not good: return w
    c = min(good, key=len)
    return c[0].upper() + c[1:] if w[0] in LIG and w[0].isupper() and len(w) > 1 and w[1:].islower() and False else c
def lig_fix(t):
    t = LIGTOK.sub(lambda m: lig_fix_token(m.group(0)), t)
    return re.sub(r'(\d)V\.', r'\1ff.', t)


def lig_space_fix(t):
    """'fi rst', 'specifi c', 'Th e', 'eff ects': a space left after a ligature; join when the whole is a word."""
    d = english()
    def f(m):
        a, b = m.group(1), m.group(2); w = a + b
        if w.lower() not in d: return m.group(0)
        if a.lower() in d and b.lower() in d and len(a) >= 3 and len(b) >= 3: return m.group(0)
        return w
    return re.sub(r'\b([A-Za-z]*(?:fi|fl|ff|ffi|ffl|Th|th|Ff|Fi|Fl))\s([a-z]+)\b', f, t)


IASTC = 'āīūṛṝḷṃṁḥṅñṭḍṇśṣĀĪŪṚṆŚṢ'
def spaced_iast_fix(t):
    """Books whose diacritics come out as separate glyphs: 'Ī ś vara', 'M ī m ā m· s ā', 'Vai ś e s · ika'."""
    t = re.sub(r'([smtdnhrSMTDNHR]) ?· ?', lambda m: unicodedata.normalize('NFC', m.group(1) + '\u0323'), t)
    d = english(); out = []; opened = False
    for tok in t.split(' '):
        single = len(tok) == 1 and (tok in IASTC or (tok.isalpha() and tok.isascii() and tok not in 'aAiI'))
        if single:
            if tok.isupper() or not out:
                out.append(tok)
            elif opened or (re.search(r'[A-Za-z' + IASTC + r']$', out[-1] or ' ') and (any(c in IASTC for c in out[-1]) or len(out[-1]) <= 3)):
                out[-1] += tok
            else:
                out.append(tok)
            opened = True
        else:
            if out and opened and re.match(r'^[A-Za-z' + IASTC + r']', tok or ' ') and not (tok.lower().strip('.,;:') in d and len(tok) >= 3):
                out[-1] += tok
            else:
                out.append(tok)
            opened = False
    return ' '.join(out)


SPACING_ACC = {'¨': '\u0308', '´': '\u0301', 'ˆ': '\u0302', '˜': '\u0303', '¸': '\u0327', 'ˇ': '\u030C', '˘': '\u0306', '˙': '\u0307', '˚': '\u030A', '¯': '\u0304'}


def postfix(t, job):
    t = re.sub('[\u200b-\u200f\u2060\ufeff\u202a-\u202e\x00-\x08\x0b\x0c\x0e-\x1f]', '', t)
    t = t.replace('\u00ad ', '').replace('\u00ad', '')
    if HEB.search(t):  # dagesh and shin/sin dots extracted before their letter: put them after it
        t = re.sub(r'([\u05BC\u05C1\u05C2]+)([\u05D0-\u05EA])', r'\2\1', t)
    if job.get('fixmap'): t = t.translate(FIXMAP)
    if job.get('fixmap'):
        # 'ň' for ñ (layers that encode ñ with a caron n): doubled ñň/ňñ -> ñ; jň -> jñ; ň before c/j -> ñ (jṇ, ṇc, ṇj do not occur in Sanskrit)
        while True:
            t2 = re.sub('ñň|ňñ', 'ñ', t); t2 = re.sub('ÑŇ|ŇÑ', 'Ñ', t2)
            if t2 == t: break
            t = t2
        t = re.sub(r'([jJ])ň', r'\1ñ', t); t = t.replace('JŇ', 'JÑ'); t = re.sub(r'ň(?=[cjCJ])', 'ñ', t); t = re.sub(r'Ň(?=[CJ])', 'Ñ', t)
    if job.get('fixmap'):
        # vocalic r/l drawn with a separate ring below ('bhr ˚ gu', 'duṣkr ˚ tān', 'MAHĀ...EŚVAR ˚'): r̥ (only after a consonant
        # or at a word start, so an English 'for ˚parigraha' keeps its truncation sign)
        t = re.sub(r'(?:(?<=[^\W\daeiouAEIOUāīūĀĪŪ])|(?<=\b))([rRlL]) ?˚ ?(?=[^\W\d]|\]|\s|$)', lambda m: unicodedata.normalize('NFC', m.group(1) + '\u0325'), t)
    if job.get('fixmap'):
        # the same inside italics, where the ring splits the italic run: '*utsr* ˚ *ṣṭa*' -> '*utsr̥ṣṭa*'
        t = re.sub(r'(?:(?<=[^\W\daeiouAEIOUāīūĀĪŪ])|(?<=\b))([rRlL])\* ?˚ ?\*(?=[^\W\d])', lambda m: unicodedata.normalize('NFC', m.group(1) + '\u0325'), t)
    if job.get('fixmap') and not job.get('accents') and job.get('pdf_vault', '').split('/')[1:2] in (['Trika'], ['Hinduism'], ['Sanskrit']) \
            and (job.get('route') == 'ocr' or 'OCR' in job.get('text_source', '')) and re.search('[äåÄÅ]', t):
        # ä/å that Tesseract's Latin model reads for ā (tools/afix.py: German words kept, 'anä' -> 'and'); not in books with Vedic accents
        import afix; t = afix.fix_text(t)[0]
    if job.get('charmap'): t = t.translate(str.maketrans(job['charmap']))   # a book's own wrong letters, e.g. TAK: ň for ṇ, ŗ for ṛ (not general: elsewhere ň stands for ñ)
    if job.get('anusvara'):
        t = re.sub(r'ńh|ħ', 'ṁ', t)
        def fx(m):
            w = m.group(0)
            if not any(c in IAST for c in w.replace('ń', '')): return w
            w = re.sub(r'(rhn|rn|rh)$', 'ṁ', w) if len(w) > 3 else w
            return re.sub(r'rh|ń', 'ṁ', w)
        t = re.sub(r'[A-Za-zāīūṛṝḷṃṁḥṅñṭḍṇśṣĀĪŪṚṆŚṢħń]+', fx, t)
    if job.get('iast_umlaut') and not re.search(r'\b(und|der|die|des|für|zur|ist|nicht|auf)\b.*\b(und|der|die|des|für|zur|ist|nicht|auf)\b', t):
        t = t.translate(str.maketrans({'ä': 'ā', 'ü': 'ū', 'ï': 'ī', 'Ä': 'Ā', 'Ü': 'Ū', 'Ï': 'Ī', 'Ŝ': 'Ś', 'ŝ': 'ś', 'ã': 'ā'}))
    t = t.replace('\ufffd', '[illegible]')
    if job.get('_ligfix'): t = lig_fix(t)
    if re.search(r'(fi|fl|ff|Th|th) [a-z]', t): t = lig_space_fix(t)
    if job.get('_spaced_iast'): t = spaced_iast_fix(t)
    if re.search('[¨´ˆ˜¸ˇ˘˙˚¯]', t):  # spacing accents typeset after their letter ('naı¨ve', 'Rene´')
        t = re.sub(r'\b([A-Za-zı]+)([¨´ˆ˜¸ˇ˘˙˚¯]) ([a-z]+)', lambda m: m.group(0) if m.group(3) in english() else m.group(1) + m.group(2) + m.group(3), t)
        def comb(m):
            base, acc = m.group(1), m.group(2)
            if acc == '´' and base not in 'aeiouyAEIOUYcszCSZı': return m.group(0)
            if base == 'ı': base = 'i'
            return unicodedata.normalize('NFC', base + SPACING_ACC[acc])
        t = re.sub(r'([A-Za-zı])([¨´ˆ˜¸ˇ˘˙˚¯])(?=[\w\s.,;:!?)\]’”\'-]|$)', comb, t)
    t = re.sub(r'[ \t]{2,}', ' ', t)
    t = re.sub(r'(\[\^\w+\])\(', r'\1\\(', t)   # '[^10](1)' would read as a link to a note '1'
    return unicodedata.normalize('NFC', t)  # one encoding for each accented letter (search finds them all)


def reocr_deva_lines(doc, i, ls):
    """Replace the text of lines containing Devanagari by a fresh Tesseract 'san' reading of that line's image."""
    out = []
    for L in ls:
        if len(DEVA.findall(L.text)) >= 3 and len(DEVA.findall(L.text)) > 0.5 * len(re.findall(r'[A-Za-z\u0900-\u097F]', L.text)):
            r = fitz.Rect(L.x0 - 3, L.y0 - 3, L.x1 + 3, L.y1 + 3) & doc[i].rect
            got = ocr_page(doc, i, 'san', dpi=300, clip=r, psm=7)
            t = ' '.join(x.text for x in got).strip()
            if t:
                L.spans = [dict(text=t, size=L.size, flags=0, bbox=(L.x0, L.y0, L.x1, L.y1), font='ocr-san', sup=False)]
                L.text = t
        out.append(L)
    return out


def ascii_name(t, maxlen=90):
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = t.replace('’', "'").replace('‘', "'").replace('“', '').replace('”', '').replace('–', '-').replace('—', '-')
    t = re.sub(r'[\[\]#^|:*?"<>\\/]', ' ', t)
    t = re.sub(r'[^\x20-\x7e]', '', t)
    t = re.sub(r'\s+', ' ', t).strip(' .')
    if len(t) > maxlen: t = t[:maxlen].rsplit(' ', 1)[0].strip(' .,-')
    return t


def fix_spaced(title):
    """Letter-spaced capitals ('S E LECTE D B I B LIOG RAPHY'): rejoin and split again into words seen in the book."""
    toks = title.split()
    if len(toks) < 2 or sum(1 for t in toks if len(t) <= 2 and t.isupper()) < 0.4 * len(toks): return title
    s = ''.join(toks); low = s.lower(); n = len(s)
    best = [None] * (n + 1); best[0] = (0, [])
    for i in range(n):
        if best[i] is None: continue
        for j in range(i + 1, min(n, i + 25) + 1):
            w = low[i:j]
            ok = w in WORDS_SEEN and (len(w) > 1 or w in ('a', 'i'))
            if not ok and not re.fullmatch(r'\W+', w): continue
            sc = best[i][0] + (len(w) ** 2 if ok else 0)
            if best[j] is None or sc > best[j][0]: best[j] = (sc, best[i][1] + [s[i:j]])
    if best[n] is None: return title
    return re.sub(r'\s+([,.;:])', r'\1', ' '.join(best[n][1]))


def clean_toc(toc, N):
    """Drop machine-made bookmarks: one per page ('Text_0254', 'Page 12'), untitled entries, entries pointing outside the book."""
    toc = [[t[0], re.sub('[\x00-\x1f]', '', t[1]), t[2]] for t in toc]
    toc = [t for t in toc if 1 <= t[2] <= N and t[1].strip() and not re.fullmatch(r'(page|p\.?|untitled|bookmark)\s*\d*', t[1].strip(), re.I)]
    if not toc: return toc
    numbered = sum(1 for t in toc if re.search(r'[_ -]\d{2,}$', t[1].strip()))
    stems = {re.sub(r'[_ -]*\d+$', '', t[1].strip()).lower() for t in toc}
    if len(toc) > 0.4 * N and (numbered > 0.5 * len(toc) or len(stems) < 0.2 * len(toc)):
        return []
    return toc


def make_chapters(toc, N, job, heads=None):
    prefix = job['prefix']
    l1 = [(t.strip(), p - 1) for lvl, t, p in toc if lvl == 1 and 1 <= p <= N]
    chs = []
    if job.get('single'):
        chs = [dict(title='Text', start=0, end=N - 1)]
    elif len(l1) >= 2:
        l1.sort(key=lambda x: x[1])
        starts = []
        for t, p in l1:
            if starts and starts[-1][1] == p: starts[-1] = (starts[-1][0] + ' / ' + t, p); continue
            starts.append((t, p))
        if starts[0][1] > 0: starts.insert(0, ('Front matter', 0))
        # merge tiny front-matter sections (cover, title, copyright...) before the first real chapter
        merged = []
        for t, p in starts:
            merged.append([t, p])
        for k, (t, p) in enumerate(merged):
            end = merged[k + 1][1] - 1 if k + 1 < len(merged) else N - 1
            chs.append(dict(title=t, start=p, end=end))
        # fold the run of 1-3 page sections at the very start into one "Front matter" note
        fm = []
        while chs and chs[0]['end'] - chs[0]['start'] < 3 and len(chs) > 1 and not re.match(r'^\d|chapter|part', chs[0]['title'], re.I):
            fm.append(chs.pop(0))
        if fm:
            lab = ', '.join(c['title'] for c in fm)[:80]
            chs.insert(0, dict(title='Front matter' if lab == 'Front matter' else 'Front matter (' + lab + ')', start=fm[0]['start'], end=fm[-1]['end'], short='Front matter'))
    elif heads and any(heads):
        segs = []; cur = None
        for i, h in enumerate(heads):
            if h and h != cur:
                start = i
                words = h.lower()
                for back in (1, 2):
                    if i - back >= 0 and (segs and i - back > segs[-1][1] or not segs) and words.split(' chapter ')[-1] in job['_first_lines'][i - back] and not heads[i - back]:
                        start = i - back
                segs.append([h, start]); cur = h
        if not segs or segs[0][1] > 0: segs.insert(0, ['Front matter', 0])
        step = job.get('part_pages', 40)
        for k, (h, st) in enumerate(segs):
            en = segs[k + 1][1] - 1 if k + 1 < len(segs) else N - 1
            title = h.title() if h != 'Front matter' else h
            n = en - st + 1
            if n <= step * 1.5:
                chs.append(dict(title=title, start=st, end=en))
            else:
                parts = max(2, round(n / step)); size = -(-n // parts)
                for q in range(parts):
                    a = st + q * size; b = min(en, a + size - 1)
                    if a > en: break
                    chs.append(dict(title=f'{title}, part {q + 1}', start=a, end=b))
    else:
        step = job.get('part_pages', 40)
        k = 0
        for s in range(0, N, step):
            k += 1; e = min(N - 1, s + step - 1)
            if N - 1 - e < 10 and e != N - 1: e = N - 1
            chs.append(dict(title=f'Part {k}', start=s, end=e))
            if e == N - 1: break
    # long chapters: split into parts of about 40 pages
    if not job.get('single'):
        step = job.get('part_pages', 40); out = []
        for c in chs:
            n = c['end'] - c['start'] + 1
            if n <= job.get('max_chapter', 80) or re.match(r'Part \d+$', c['title']): out.append(c); continue
            parts = max(2, round(n / step)); size = -(-n // parts)
            for q in range(parts):
                a = c['start'] + q * size; b = min(c['end'], a + size - 1)
                if a > c['end']: break
                out.append(dict(c, title=f"{c.get('short') or c['title']}, part {q + 1}", short=None, start=a, end=b))
        chs = out
    for k, c in enumerate(chs):
        c['title'] = re.sub(r'\.(pdf|docx?|indd|rtf)\b', '', c['title'], flags=re.I)
        nm = c.get('short') or c['title']
        nm = re.sub(r'\.(pdf|docx?|indd|rtf)\b', '', nm, flags=re.I)
        c['name'] = ascii_name(f'{prefix} {k + 1:02d} - {nm}', 100) if not job.get('single') else ascii_name(f'{prefix} - Text', 100)
        c['title_heading'] = False
    return chs


def prescan_words(job):
    """Collect hyphenated forms seen mid-line and plain words, for line-end hyphen decisions."""
    doc = fitz.open(job['pdf'])
    for i in range(len(doc)):
        t = doc[i].get_text()
        for line in t.splitlines():
            for w in re.findall(r'\b\w+(?:-\w+)+\b', line.rstrip('-')[:-1] if line.endswith('-') else line):
                HYPH_SEEN.add(w.lower())
            for w in re.findall(r'\w+', line): WORDS_SEEN.add(w.lower())


if __name__ == '__main__':
    job = json.load(open(sys.argv[1]))
    if job['route'] != 'ocr': prescan_words(job)
    rep = convert(job)
    print(json.dumps({k: rep[k] for k in ('folder', 'pages', 'notes', 'body_size', 'stats', 'page_src', 'labels_used', 'ocr_conf_mean')}, ensure_ascii=False))
