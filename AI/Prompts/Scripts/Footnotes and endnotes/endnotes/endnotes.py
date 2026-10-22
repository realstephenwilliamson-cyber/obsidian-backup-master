"""D31d: link endnote calls (<sup>N</sup>) to their endnotes, giving each endnote paragraph a block id.
Local only; writes to /home/claude/d31c2/endnotes/<book folder>/ the notes that change."""
import re, os, glob, json, collections, sys

UP = "/mnt/user-data/uploads/Obsidian Vault/Library/Philosophy/"
OUT = "/home/claude/d31c2/endnotes/"
SUFFIX = "; endnote calls linked 15 Oct 2026"
SUPD = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
MARK = re.compile(r'^\*\[(?:p\. [^\]]+|PDF \d+)\]\* \^pg\d+[ \t]*$')
LOG = collections.defaultdict(list)

def split_fm(text):
    m = re.match(r'^---\n.*?\n---\n', text, re.S)
    return (text[:m.end()], text[m.end():]) if m else ('', text)

def add_suffix(fm):
    return re.sub(r'^(text_source: .*)$', lambda m: (m.group(1)[:-1] + SUFFIX + '"') if m.group(1).endswith('"') else m.group(1) + SUFFIX, fm, count=1, flags=re.M)

def paragraphs(body):
    """Split into paragraph strings keeping the separators: returns list of [text, sep]."""
    parts = re.split(r'(\n[ \t]*\n+)', body)
    out = []
    for i in range(0, len(parts), 2):
        out.append([parts[i], parts[i + 1] if i + 1 < len(parts) else ''])
    return out

def add_id(par, bid):
    """Append ' ^bid' to the paragraph's last line; refuse when it already carries a block id."""
    if re.search(r'\s\^[\w-]+\s*$', par): return None
    return par.rstrip() + ' ^' + bid


def split_runon(par, start_n, log_key, where):
    """Split a paragraph holding several notes run together: '... modified. 49 Stiegler, ...' where 49 = start_n + 1."""
    pieces = []; cur = par; n = start_n
    while True:
        mm = re.search(r'(?<=[.)”’*\]]) ' + str(n + 1) + r' (?=[A-Z*“‘(\[])', cur)
        if not mm: break
        pieces.append(cur[:mm.start()]); cur = cur[mm.start() + 1:]; n += 1
    pieces.append(cur)
    if len(pieces) > 1: LOG[log_key].append((where, [p[:60] for p in pieces]))
    return pieces

# ------------------------------------------------------------------ Ricoeur
def ricoeur():
    book = "Politics, Economy, and Society (Ricoeur)"; src = UP + book + '/'
    notes_name = "Politics, Economy, and Society 27 - Notes"
    text = open(src + notes_name + '.md', encoding='utf-8').read()
    fm, body = split_fm(text)
    pars = paragraphs(body)
    # chapter sections
    endnotes = {}      # (chapter key, number) -> block id
    cur_ch = None; last_n = None
    new_pars = []
    for par, sep in pars:
        s = par.strip()
        m = re.match(r'^### (.*)$', s)
        if m:
            h = m.group(1)
            mm = re.match(r'^(\d{1,2})\. ', h)
            cur_ch = f'C{int(mm.group(1)):02d}' if mm else ('ed' if 'Editor' in h else None)
            last_n = None; new_pars.append([par, sep]); continue
        if cur_ch is None or MARK.match(s) or s.startswith('#'):
            new_pars.append([par, sep]); continue
        m = re.match(r'^(\d{1,3})[ \t](\S.*)$', s, re.S)
        start_n = int(m.group(1)) if m else (last_n or 0)
        pieces = split_runon(s, start_n, 'ricoeur_splits', cur_ch)
        for k, piece in enumerate(pieces):
            mp = re.match(r'^(\d{1,3})[ \t]', piece)
            if not mp:
                new_pars.append([piece, sep if k == len(pieces) - 1 else '\n\n']); continue      # continuation of a note across a page break
            num = int(mp.group(1))
            key = (cur_ch, num)
            if key in endnotes:
                LOG['ricoeur_duplicate_endnote'].append((cur_ch, num)); new_pars.append([piece, sep if k == len(pieces) - 1 else '\n\n']); continue
            bid = f'n-{cur_ch}-{num}'
            if last_n is not None and num != last_n + 1: LOG['ricoeur_sequence_gap'].append((cur_ch, last_n, num))
            last_n = num
            withid = add_id(piece, bid)
            if withid is None:
                LOG['ricoeur_already_has_id'].append((cur_ch, num)); new_pars.append([piece, sep if k == len(pieces) - 1 else '\n\n']); continue
            endnotes[key] = bid
            new_pars.append([withid, sep if k == len(pieces) - 1 else '\n\n'])
    new_notes = add_suffix(fm) + ''.join(p + s for p, s in new_pars)
    os.makedirs(OUT + book, exist_ok=True)
    open(OUT + book + '/' + notes_name + '.md', 'w', encoding='utf-8').write(new_notes)
    # body notes
    stats = collections.OrderedDict(); used = set()
    for f in sorted(glob.glob(src + 'Politics, Economy, and Society [0-9][0-9] - *.md')):
        name = os.path.basename(f)[:-3]
        if name == notes_name: continue
        t = open(f, encoding='utf-8').read()
        if '<sup>' not in t: continue
        mm = re.match(r'^Politics, Economy, and Society \d\d - (\d{1,2}) ', name)
        ch = f'C{int(mm.group(1)):02d}' if mm else ('ed' if "Editor's Introduction" in name else None)
        fm, body = split_fm(t)
        found = linked = 0; unmatched = []; last = None
        def rep(m):
            nonlocal found, linked, last
            lab = m.group(1)
            if not lab.isdigit(): unmatched.append((lab, 'not a number')); return m.group(0)
            found += 1; num = int(lab)
            if ch is None: unmatched.append((lab, 'no Notes section for this note')); return m.group(0)
            key = (ch, num)
            if key not in endnotes: unmatched.append((lab, 'no endnote with this number in section ' + ch)); return m.group(0)
            if last is not None and num != last + 1 and num != last: LOG['ricoeur_call_out_of_sequence'].append((name, last, num))
            last = num; linked += 1; used.add(key)
            return f'[[{notes_name}#^{endnotes[key]}|{lab.translate(SUPD)}]]'
        body2 = re.sub(r'<sup>([^<]*)</sup>', rep, body)
        stats[name] = dict(calls=found, linked=linked, unmatched=unmatched)
        if linked:
            open(OUT + book + '/' + name + '.md', 'w', encoding='utf-8').write(add_suffix(fm) + body2)
    uncalled = sorted(k for k in endnotes if k not in used)
    return dict(book=book, notes_note=notes_name, endnotes=len(endnotes), per_note=stats, endnotes_without_call=uncalled)

# ------------------------------------------------------------------ Stiegler
def stiegler():
    book = "Nanjing Lectures 2016-2019 (Stiegler)"; src = UP + book + '/'
    p9 = "Nanjing Lectures 2016-2019 11 - Stiegler_2020_Nanjing-Lectures, part 9"
    p10 = "Nanjing Lectures 2016-2019 12 - Stiegler_2020_Nanjing-Lectures, part 10"
    endnotes = {}   # number -> (note name, block id)
    pending = None; cur = None; last_n = 0; seq_issues = []
    def process(name, body, start_at_notes):
        nonlocal pending, cur, last_n
        pars = paragraphs(body); out = []; active = not start_at_notes
        for par, sep in pars:
            s = par.strip()
            if not active:
                out.append([par, sep])
                if re.match(r'^\*\[p\. 345\]\* \^pg347', s): active = True
                continue
            if MARK.match(s) or s.startswith('#') or not s:
                out.append([par, sep]); continue
            m = re.fullmatch(r'(\d{1,3})\t?', s)
            if m:                                   # a number on a line of its own: the next paragraph is the note's text
                pending = int(m.group(1)); out.append([par, sep]); continue
            m0 = re.match(r'^(\d{1,3})[ \t](\S.*)$', s, re.S)
            start_n = int(m0.group(1)) if (m0 and pending is None) else (pending if pending is not None else last_n)
            pieces = split_runon(par, start_n, 'stiegler_splits', name[-7:])
            for k, piece in enumerate(pieces):
                psep = sep if k == len(pieces) - 1 else '\n\n'
                s = piece.strip()
                m = re.match(r'^(\d{1,3})[ \t](\S.*)$', s, re.S)
                glued = re.search(r'(?:^|\s)(\d{1,3})\t[ \t]*$', piece.rstrip('\n'))   # on the raw paragraph: strip() would eat the tab
                if m and pending is None:                # number and text in one paragraph
                    num = int(m.group(1)); text_par = piece
                elif pending is not None:
                    num = pending; text_par = piece; pending = None
                elif glued:                              # the number printed at the head of the line came last in the text layer: this paragraph is the note
                    num = int(glued.group(1)); text_par = piece
                else:
                    out.append([piece, psep]); continue    # continuation paragraph (quote, URL line)
                if num != last_n + 1: seq_issues.append((last_n, num))
                if num in endnotes:
                    LOG['stiegler_duplicate_endnote'].append(num); out.append([piece, psep]); continue
                bid = f'n-{num}'
                withid = add_id(text_par, bid)
                if withid is None: LOG['stiegler_already_has_id'].append(num); out.append([piece, psep]); continue
                endnotes[num] = (name, bid); last_n = max(last_n, num)
                out.append([withid, psep])
        return ''.join(p + s for p, s in out)
    texts = {}
    for name, start in ((p9, True), (p10, False)):
        t = open(src + name + '.md', encoding='utf-8').read(); fm, body = split_fm(t)
        texts[name] = (fm, process(name, body, start))
    LOG['stiegler_sequence_issues'] = seq_issues
    # body calls (parts 1-9); part 9 holds both calls and notes
    stats = collections.OrderedDict(); used = set(); last = 0
    os.makedirs(OUT + book, exist_ok=True)
    for f in sorted(glob.glob(src + 'Nanjing Lectures 2016-2019 [0-9][0-9] - *.md')):
        name = os.path.basename(f)[:-3]
        t = open(f, encoding='utf-8').read()
        if name in texts: fm, body = texts[name]
        else: fm, body = split_fm(t)
        if '<sup>' not in body:
            if name in texts: open(OUT + book + '/' + name + '.md', 'w', encoding='utf-8').write(add_suffix(fm) + body)
            continue
        found = linked = 0; unmatched = []
        def rep(m):
            nonlocal found, linked, last
            lab = m.group(1)
            if not lab.isdigit(): unmatched.append((lab, 'not a number')); return m.group(0)
            found += 1; num = int(lab)
            if num != last + 1:
                unmatched.append((lab, f'out of sequence (previous call {last})')); return m.group(0)
            last = num
            if num not in endnotes: unmatched.append((lab, 'no endnote with this number')); return m.group(0)
            nn, bid = endnotes[num]; linked += 1; used.add(num)
            return f'[[{nn}#^{bid}|{lab.translate(SUPD)}]]'
        body2 = re.sub(r'<sup>([^<]*)</sup>', rep, body)
        stats[name] = dict(calls=found, linked=linked, unmatched=unmatched)
        open(OUT + book + '/' + name + '.md', 'w', encoding='utf-8').write(add_suffix(fm) + body2)
    uncalled = sorted(k for k in endnotes if k not in used)
    return dict(book=book, notes_notes=[p9, p10], endnotes=len(endnotes), per_note=stats, endnotes_without_call=uncalled)

if __name__ == '__main__':
    res = dict(ricoeur=ricoeur(), stiegler=stiegler(), log={k: v for k, v in LOG.items()})
    json.dump(res, open('/home/claude/d31c2/endnotes_log.json', 'w'), ensure_ascii=False, indent=1)
    for b in ('ricoeur', 'stiegler'):
        r = res[b]; print('==', r['book'], 'endnotes', r['endnotes'], 'without call', len(r['endnotes_without_call']))
        for n, s in r['per_note'].items(): print('  ', n[-50:], 'calls', s['calls'], 'linked', s['linked'], 'unmatched', s['unmatched'][:4])
    for k, v in LOG.items(): print(k, len(v), v[:6])
