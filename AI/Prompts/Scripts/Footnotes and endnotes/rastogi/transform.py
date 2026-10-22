# Rastogi, Krama Tantricism I: footnotes for the notes that are wholly text in the PDF layer (Stephen's option 3).
# Many notes are Devanagari quotations kept as image fragments; a note is converted only if (1) its label "N." is text
# in the layer, (2) nothing between its label and the next text label (or the end of the notes) is an image, (3) the
# md has one paragraph run starting with that label whose words match the layer's note, and (4) the page's body has
# exactly one <sup>N</sup>. Pages that already have footnotes are left alone.
import sys, os, re, json, glob, difflib, collections, unicodedata, pymupdf
VAULT = r'C:\Vaults\Obsidian Vault'
ORIG = os.path.join(VAULT, r'.work\backup-footnotes-2026-10-18\Rastogi\Library\Trika\The Krama Tantricism of Kashmir, Volume I (Rastogi)')
PDF = os.path.join(VAULT, r'Library\Trika\Rastogi - The Krama Tantricism of Kashmir, Volume I (1979).pdf')
HERE = os.path.dirname(os.path.abspath(__file__))
LAY = json.load(open(os.path.join(HERE, 'layer.json'), encoding='utf-8'))
MARK = re.compile(r'^\*\[(?:p|PDF)\.? ([^\]]*)\]\* \^pg(\d+)$')

def norm(w):
    w = unicodedata.normalize('NFKD', w); w = ''.join(c for c in w if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]', '', w)

def layer_notes(doc, K):
    """the notes zone of page K: list of elements in y order: ('label', n, words) for a text note, ('image',)."""
    lines = [l for l in LAY[K - 1]['lines'] if l['y'] > 60]
    small = [l for l in lines if all(w['sz'] < 8.6 for w in l['w']) and not all(w['sup'] for w in l['w'])]
    if not small: return None
    body = [l for l in lines if any(w['sz'] >= 8.9 and not w['sup'] for w in l['w'])]
    top = min(l['y'] for l in small)
    if body and max(l['y'] for l in body) > top: top = max(l['y'] for l in body) + 1   # notes are below the body
    zone = [l for l in small if l['y'] >= top]
    imgs = [i['bbox'] for i in doc[K - 1].get_image_info() if i['bbox'][1] >= top - 2 and (i['bbox'][3] - i['bbox'][1]) < 200]
    el = []
    for l in zone:
        ws = [w['t'] for w in sorted(l['w'], key=lambda w: w['x'])]
        el.append((l['y'], 'line', l['x'], ' '.join(ws)))
    for b in imgs: el.append((b[1], 'image', b[0], ''))
    el.sort()
    notes = []; cur = None
    first_line = next((e for e in el if e[1] == 'line'), None)
    starts_unlabelled = bool(el) and (el[0][1] == 'image' or (first_line is not None and el[0] is first_line and not re.match(r'^\d{1,2}\.', first_line[3])))
    for y, kind, x, t in el:
        if kind == 'image':
            if cur: cur['image_after'] = True; cur = None
            notes.append(dict(n=None, image=True)); continue
        m = re.match(r'^(\d{1,2})\.\s*(.*)$', t)
        if m:
            cur = dict(n=int(m.group(1)), words=m.group(2).split(), image_after=False); notes.append(cur)
        elif cur is not None:
            cur['words'] += t.split()
    if notes: notes[0]['_page_starts_unlabelled'] = starts_unlabelled
    return notes

def continues_from_previous(doc, K):
    """does page K's notes zone begin with text or an image that has no label (a note running on from page K-1)?"""
    nt = layer_notes(doc, K)
    return bool(nt) and nt[0].get('_page_starts_unlabelled', False)

def paras(lines):
    out, cur, start = [], [], None
    for i, l in enumerate(lines):
        if l.strip():
            if not cur: start = i
            cur.append(l)
        elif cur: out.append((start, i, '\n'.join(cur))); cur = []
    if cur: out.append((start, len(lines), '\n'.join(cur)))
    return out

def run():
    doc = pymupdf.open(PDF)
    rep = collections.Counter(); log = []; newfiles = {}
    for f in sorted(glob.glob(os.path.join(glob.escape(ORIG), '*.md'))):
        fn = os.path.basename(f)
        L = open(f, encoding='utf-8').read().split('\n')
        marks = [(i, m.group(1), int(m.group(2))) for i, l in enumerate(L) for m in [MARK.match(l)] if m]
        used = set(re.findall(r'\[\^([^\]\s]+)\]', '\n'.join(L)))
        out = L[:marks[0][0]] if marks else L
        changed = False
        for mi, (li, plabel, K) in enumerate(marks):
            le = marks[mi + 1][0] if mi + 1 < len(marks) else len(L)
            sec = L[li:le]
            if any('[^' in x for x in sec): rep['page already has footnotes'] += 1; out += sec; continue
            notes = layer_notes(doc, K)
            if not notes: out += sec; continue
            body_calls = collections.Counter(re.findall(r'<sup>(\d{1,2})</sup>', '\n'.join(sec)))
            P = paras(sec[1:])
            new_sec = list(sec)
            seen_n = collections.Counter(nt['n'] for nt in notes if nt.get('n'))
            last_text = [nt for nt in notes if nt.get('n') is not None]
            last_n = last_text[-1]['n'] if last_text and notes[-1] is last_text[-1] else None
            runs_on = K + 1 <= len(LAY) and continues_from_previous(doc, K + 1)
            for nt in notes:
                if nt.get('n') is None: continue
                n = nt['n']; rep['text notes in layer'] += 1
                if n == last_n and runs_on: rep['last note runs on to the next page'] += 1; continue
                if seen_n[n] != 1: rep['label repeated on page'] += 1; continue
                if nt['image_after']: rep['image follows (note may continue in an image)'] += 1; continue
                if body_calls[str(n)] != 1: rep['call not exactly once'] += 1; continue
                # the md paragraph that starts with the label, plus following paragraphs while they improve the match
                lw = [norm(w) for w in nt['words'] if norm(w)]
                cand = [k for k, (a, b, t) in enumerate(P) if re.match(r'^\s*%d\\?\.\s' % n, t)]
                if len(cand) != 1: rep['md label paragraph not found once'] += 1; continue
                k = cand[0]; take = [k]
                def ratio(ks):
                    mw = [norm(w) for q in ks for w in P[q][2].split() if norm(w)]
                    if mw and re.fullmatch(r'\d+', P[ks[0]][2].split()[0].replace('\\.', '').replace('.', '')): pass
                    return difflib.SequenceMatcher(None, lw, mw, autojunk=False).ratio()
                r = ratio(take)
                while k + len(take) < len(P) and not re.match(r'^\s*\d{1,2}\\?\.\s', P[k + len(take)][2]):
                    r2 = ratio(take + [k + len(take)])
                    if r2 > r + 0.02: take.append(k + len(take)); r = r2
                    else: break
                if r < 0.85: rep['md note text does not match the layer'] += 1; log.append((fn, K, n, round(r, 2))); continue
                lab = str(n) if str(n) not in used else '%d-p%s' % (n, re.sub(r'[^\w]', '', plabel))
                used.add(lab)
                txt = ' '.join(P[q][2].replace('\n', ' ').strip() for q in take)
                txt = re.sub(r'^\s*%d\\?\.\s+' % n, '', txt)
                # write: the definition replaces the note's paragraphs; the call replaces <sup>n</sup>
                a0 = P[take[0]][0] + 1; b0 = P[take[-1]][1] + 1           # +1: P indexes sec[1:]
                for q in range(a0, b0): new_sec[q] = None
                new_sec[a0] = '[^%s]: %s' % (lab, txt)
                for q in range(1, len(new_sec)):
                    if new_sec[q] and '<sup>%d</sup>' % n in new_sec[q]:
                        new_sec[q] = new_sec[q].replace('<sup>%d</sup>' % n, '[^%s]' % lab); break
                rep['footnotes'] += 1; changed = True
            out += [x for x in new_sec if x is not None]
        if changed:
            txt = '\n'.join(out)
            SUF = '; footnotes for the notes that are wholly text in the PDF layer 18 Oct 2026'
            txt = re.sub(r'^(text_source: )(.*)$', lambda m: m.group(1) + (m.group(2)[:-1] + SUF + '"' if m.group(2).endswith('"') else m.group(2) + SUF), txt, count=1, flags=re.M)
            newfiles[fn] = txt
    return newfiles, rep, log

if __name__ == '__main__':
    newfiles, rep, log = run()
    print(dict(rep))
    os.makedirs(os.path.join(HERE, 'out'), exist_ok=True)
    for fn, t in newfiles.items(): open(os.path.join(HERE, 'out', fn), 'w', encoding='utf-8', newline='\n').write(t)
    json.dump(log, open(os.path.join(HERE, 'log.json'), 'w'), indent=0)
    print('files', len(newfiles))
