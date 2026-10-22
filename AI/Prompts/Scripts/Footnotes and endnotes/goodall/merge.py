"""D31c: merge the new conversion (footnotes) into the current vault notes, keeping everything else as it is now.

For each current note: frontmatter, preamble (navigation, callouts), page markers and headings are kept verbatim;
each page's text comes from the new conversion; corrections found in the current text are carried over.
"""
import re, os, sys, glob, json, difflib, collections

CUR = "/mnt/user-data/uploads/Obsidian Vault/Library/Hinduism/Saivism and the Tantric Traditions (Goodall)"
NEW = "/home/claude/d31c/out/Library/Hinduism/Saivism and the Tantric Traditions (Goodall)"
FINAL = "/home/claude/d31c/final"
MARK = re.compile(r'^\*\[(?:p\. [^\]]+|PDF \d+)\]\* \^pg(\d+)[ \t]*$', re.M)
DATE_NOTE = "; footnotes re-converted 15 Oct 2026"

# stand-in letters seen in PyMuPDF output for this font, and the IAST letters they stand for (applied only when the current text has the IAST form)
STANDIN = set('ļțńşůőľŭŏ')
ACCEPTED = {('ļ', 'ḷ'), ('ț', 'ṭ')}   # stand-in letters whose correction in the current notes is right; ń→ṁ and ş→ṣ are not carried (see REPORT)
IAST = set('āīūṛṝḷḹṃṁḥṅñṭḍṇśṣĀĪŪṚṜḶḸṂṀḤṄÑṬḌṆŚṢ')

def split_pages(text):
    """-> (preamble, [(marker_line, K, block_text)]) ; block_text excludes the marker line."""
    ms = list(MARK.finditer(text))
    pre = text[:ms[0].start()] if ms else text
    pages = []
    for j, m in enumerate(ms):
        end = ms[j + 1].start() if j + 1 < len(ms) else len(text)
        pages.append((m.group(0), int(m.group(1)), text[m.end():end]))
    return pre, pages

def split_fm(text):
    m = re.match(r'^---\n.*?\n---\n', text, re.S)
    return (text[:m.end()], text[m.end():]) if m else ('', text)

def units(block):
    """Paragraph units of a page block (split on blank lines), stripped."""
    return [u for u in re.split(r'\n[ \t]*\n', block.strip('\n')) if u.strip()]

def norm(s):
    s = re.sub(r'\[\^[^\]]+\](?:: )?', '', s)          # footnote refs and definition labels
    s = re.sub(r'</?sup>', '', s)
    s = re.sub(r'^\d{1,3}\\\. ', '', s, flags=re.M)  # unreferenced-note prefix
    s = s.replace('\\', '')
    s = re.sub(r'[*_`]', '', s)
    return s

def words(s):
    return re.findall(r'\S+', norm(s))

def key(s):
    return re.sub(r'[\W_]+', '', norm(s)).lower()[:40]

def is_note_unit(u):
    return bool(re.match(r'^\[\^[^\]]+\]: ', u) or re.match(r'^\d{1,3}\\\. ', u))

def is_heading(u):
    return u.lstrip().startswith('#')

log = collections.defaultdict(list)
report = {}

def merge_page(name, K, cur_block, new_block):
    cu = units(cur_block); nu = units(new_block)
    heads = [(j, u) for j, u in enumerate(cu) if is_heading(u)]
    body_cur = [u for u in cu if not is_heading(u)]
    nu = [u for u in nu if not is_heading(u)]          # the new conversion's TOC headings are not wanted; the current ones are kept
    # --- corrections: word-level diff of the page text outside notes (new) vs current text outside note paragraphs
    new_body = [u for u in nu if not is_note_unit(u)]
    new_notes = [u for u in nu if is_note_unit(u)]
    cur_body = [u for u in body_cur if not is_note_unit(u)]
    cw = words('\n'.join(cur_body)); nw = words('\n'.join(new_body))
    sm = difflib.SequenceMatcher(a=nw, b=cw, autojunk=False)
    fixes = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal': continue
        a = nw[i1:i2]; b = cw[j1:j2]
        if tag == 'replace' and len(a) == len(b):
            for x, y in zip(a, b):
                if x == y: continue
                # the current text carries the note number that the new text links as a reference: expected
                if re.sub(r'\d+', '', x) == re.sub(r'\d+', '', y) and len(re.findall(r'\d', y)) != len(re.findall(r'\d', x)):
                    (log['digits_more_in_current'] if len(re.findall(r'\d', y)) > len(re.findall(r'\d', x)) else log['digits_fewer_in_current']).append((name, K, x, y)); continue
                xs = set(x); ys = set(y)
                if (xs & STANDIN) and len(x) == len(y) and all(a == b or (a, b) in ACCEPTED for a, b in zip(x, y)):
                    fixes.append((x, y)); continue
                if (xs & STANDIN) and len(x) == len(y):
                    log['correction_not_applied'].append((name, K, x, y)); continue
                if x.replace('rh', 'ṁ') == y or x.replace('ṃ', 'ṁ') == y:
                    log['current_error_not_carried'].append((name, K, x, y)); continue
                if '[[' in y and ']]' in y:
                    continue   # wikilinks are carried over separately
                log['unresolved'].append((name, K, 'replace', x, y))
            continue
        if tag == 'delete':      # new has words the current lacks (text the old conversion dropped, e.g. header-like lines)
            log['new_only'].append((name, K, ' '.join(a)[:160]))
        elif tag == 'insert':    # current has words the new body lacks: note text that is now a footnote, or text to carry over
            t = ' '.join(b)
            allnotes = re.sub(r'\s+', ' ', norm('\n'.join(ALL_NEW_NOTES[name])))
            probe = re.sub(r'^\d{1,3} ', '', re.sub(r'\s+', ' ', t))
            ws = probe.split(' ')
            if len(ws) >= 3 and (' '.join(ws[:5]) in allnotes or ' '.join(ws[1:6]) in allnotes or ' '.join(ws[-5:]) in allnotes): log['cur_only_note'].append((name, K, t[:100]))
            elif re.fullmatch(r'[\d ]+', t): log['cur_only_digits'].append((name, K, t))
            elif t.lower() in RUNHEADS: log['running_head_dropped'].append((name, K, t))
            else: log['unresolved'].append((name, K, 'insert', '', t[:200]))
        else:
            log['unresolved'].append((name, K, 'replace', ' '.join(a)[:200], ' '.join(b)[:200]))
    # apply the letter corrections to the new block (whole-word, first occurrence each)
    out_block = new_block
    for x, y in fixes:
        # x is a normalized token; find it in the raw new block allowing markdown marks inside
        pat = re.compile(r'(?<![\w])' + ''.join(re.escape(c) + r'[*\\]*' for c in x).rstrip('[*\\\\]*') + r'(?![\w])')
        m = pat.search(out_block)
        if m:
            raw = m.group(0)
            # rebuild with the corrected letters, keeping any markdown marks in place
            res = []; k = 0
            for c in raw:
                if k < len(x) and c == x[k]: res.append(y[k]); k += 1
                else: res.append(c)
            out_block = out_block[:m.start()] + ''.join(res) + out_block[m.end():]
            log['fixed'].append((name, K, x, y))
        else:
            log['fix_not_applied'].append((name, K, x, y))
    # --- wikilinks added in the current note (Tantrāloka links): put them on the same text in the new block
    for link, n_cur in collections.Counter(m.group(0) for m in re.finditer(r'\[\[[^\]|]+\|[^\]]+\]\]', cur_block)).items():
        alias = link.split('|', 1)[1][:-2]
        pat = re.compile(r'(?<!\[)(?<![\w|])' + re.escape(alias) + r'(?![\w\]])')
        while out_block.count(link) < n_cur:
            mm = pat.search(out_block)
            if not mm: log['wikilink_not_placed'].append((name, K, link)); break
            out_block = out_block[:mm.start()] + link + out_block[mm.end():]; log['wikilink_carried'].append((name, K, link))
    # --- put the current headings back
    ou = units(out_block)
    ou = [u for u in ou if not is_heading(u)]
    for j, h in heads:
        nxt = next((u for u in cu[j + 1:] if not is_heading(u)), None)
        pos = None
        if nxt is not None:
            kk = key(nxt)
            for q, u in enumerate(ou):
                if kk and key(u) == kk: pos = q; break
            if pos is None and kk:
                for q, u in enumerate(ou):
                    if key(u).startswith(kk[:12]): pos = q; break
        if pos is None:
            prv = next((u for u in reversed(cu[:j]) if not is_heading(u)), None)
            if prv is not None and key(prv):
                for q, u in enumerate(ou):
                    if key(u) == key(prv): pos = q + 1; break
        if pos is None:
            if j == 0 or all(is_heading(u) for u in cu[:j]): pos = 0
            else:
                pos = len([u for u in ou if not is_note_unit(u)])   # after the body text, before the notes
                log['heading_fallback'].append((name, K, h[:60]))
        ou.insert(pos, h)
    return '\n\n'.join(ou) + '\n\n'

ALL_NEW_NOTES = {}
RUNHEADS = set()
def load_runheads():
    import fitz
    doc = fitz.open("/mnt/user-data/uploads/Obsidian Vault/Library/Hinduism/Saivism and the Tantric Traditions.pdf")
    for i in range(len(doc)):
        for b in doc[i].get_text('dict')['blocks']:
            if b.get('type') != 0: continue
            for l in b['lines']:
                t = ''.join(s['text'] for s in l['spans']).strip()
                if t and l['bbox'][3] <= 50 and not re.fullmatch(r'[\divxl]+', t): RUNHEADS.add(t.lower())

def main():
    os.makedirs(FINAL, exist_ok=True)
    load_runheads()
    cur_files = sorted(f for f in glob.glob(CUR + '/Saivism and the Tantric [0-9][0-9] - *.md') if '9789004432802' not in f)
    new_files = sorted(glob.glob(NEW + '/Saivism and the Tantric [0-9][0-9] - *.md'))
    assert len(cur_files) == 17 and len(new_files) == 17, (len(cur_files), len(new_files))
    counts = {}
    for cf, nf in zip(cur_files, new_files):
        name = os.path.basename(cf)[:-3]
        assert os.path.basename(cf)[:26] == os.path.basename(nf)[:26], (cf, nf)
        cur = open(cf, encoding='utf-8').read(); new = open(nf, encoding='utf-8').read()
        fm, body = split_fm(cur); _, nbody = split_fm(new)
        pre, cpages = split_pages(body); _, npages = split_pages(nbody)
        nmap = {K: blk for _, K, blk in npages}
        assert [K for _, K, _ in cpages] == [K for _, K, _ in npages], (name, 'page sets differ')
        ALL_NEW_NOTES[name] = [u for _, K, blk in npages for u in units(blk) if is_note_unit(u)]
        out = []
        for mark, K, cblk in cpages:
            out.append(mark + '\n\n' + merge_page(name, K, cblk, nmap[K]))
        fm2 = re.sub(r'^(text_source: .*)$', lambda m: m.group(1).rstrip('"') + DATE_NOTE + ('"' if m.group(1).endswith('"') else ''), fm, count=1, flags=re.M)
        text = fm2 + pre + ''.join(out)
        text = re.sub(r'\n{3,}', '\n\n', text).rstrip('\n') + '\n'
        # unique footnote ids and reference/definition balance
        defs = re.findall(r'^\[\^([^\]]+)\]: ', text, re.M)
        refs = re.findall(r'(?<!^)\[\^([^\]]+)\](?!:)', text, re.M)
        refs = [r for r in re.findall(r'\[\^([^\]]+)\](?!:)', text)]
        dup = [d for d, c in collections.Counter(defs).items() if c > 1]
        unref_def = sorted(set(defs) - set(refs)); undef_ref = sorted(set(refs) - set(defs))
        plain = re.findall(r'^(\d{1,3})\\\. ', text, re.M)
        counts[name] = dict(definitions=len(defs), references=len(refs), duplicate_ids=dup, defs_without_ref=unref_def, refs_without_def=undef_ref, notes_unreferenced=len(plain))
        # markers and headings identical?
        cm = MARK.findall(cur); tm = MARK.findall(text)
        ch = re.findall(r'^#+ .*$', cur, re.M); th = re.findall(r'^#+ .*$', text, re.M)
        counts[name]['markers_identical'] = [m.group(0) for m in MARK.finditer(cur)] == [m.group(0) for m in MARK.finditer(text)]
        counts[name]['headings_identical'] = ch == th
        counts[name]['preamble_identical'] = split_pages(split_fm(text)[1])[0] == pre
        open(os.path.join(FINAL, os.path.basename(cf)), 'w', encoding='utf-8').write(text)
    # index note: keep as is, with the text_source note
    idx = open(CUR + '/Saivism and the Tantric Traditions (Goodall).md', encoding='utf-8').read()
    idx2 = re.sub(r'^(text_source: .*)$', lambda m: m.group(1) + DATE_NOTE, idx, count=1, flags=re.M)
    open(os.path.join(FINAL, 'Saivism and the Tantric Traditions (Goodall).md'), 'w', encoding='utf-8').write(idx2)
    json.dump(dict(counts=counts, log={k: v for k, v in log.items()}), open('/home/claude/d31c/merge_log.json', 'w'), ensure_ascii=False, indent=1)
    for k, v in log.items(): print(k, len(v))
    for n, c in counts.items(): print(n[:40], c)

main()
