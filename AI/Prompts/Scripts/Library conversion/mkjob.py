import json, sys, re, os, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
V = '/mnt/user-data/uploads/Obsidian Vault/'
CAT = None
def fm(path):
    global CAT
    if CAT is None:
        CAT = json.load(open(V + '.work/out/p4-catalog.json', encoding='utf-8'))
    if path in CAT:
        y = CAT[path]
        L = lambda v: [str(x) for x in v] if isinstance(v, list) else ([str(v)] if v else [])
        return dict(title=str(y.get('title') or ''), author=L(y.get('author')), translator=L(y.get('translator')), editor=L(y.get('editor')), year=y.get('year'), publisher=y.get('publisher') or '', ctype=y.get('type'))
    return fm_file(path)
def fm_file(path):
    import yaml
    t = open(V + path, encoding='utf-8').read()
    y = yaml.safe_load(re.match(r'---\n(.*?)\n---', t, re.S).group(1)) or {}
    L = lambda v: [str(x) for x in v] if isinstance(v, list) else ([str(v)] if v else [])
    return dict(title=str(y.get('title') or ''), author=L(y.get('author')), translator=L(y.get('translator')), year=y.get('year'), publisher=y.get('publisher') or '')
def byl(authors, c):
    b = ', '.join(authors)
    if c['translator']: b += (', translated by ' if b else 'Translated by ') + ', '.join(c['translator'])
    if c['publisher']: b += '. ' + str(c['publisher'])
    if c['year']: b += ', ' + str(c['year'])
    return b + '.'
SUFFIX = {'jr', 'jr.', 'sr', 'sr.', 'ii', 'iii', 'iv'}
PART = {'van', 'von', 'de', 'der', 'den', 'du', 'da', 'di', 'le', 'la', 'del', 'ibn', 'bar', 'ben'}
def surname(name):
    name = re.sub(r'\s*\([^)]*\)', '', name)
    t = name.replace(',', ' ').split()
    if not t: return ''
    if 'the' in [x.lower() for x in t]: return name.strip()                  # Maximus the Confessor
    if t[0].lower() in ('pope', 'saint', 'st.', 'st'): t = t[1:]
    if len(t) == 2 and re.fullmatch(r'[IVXL]+', t[1]): return ' '.join(t)   # Leo XIV
    while len(t) > 1 and t[-1].lower() in SUFFIX: t = t[:-1]
    out = [t[-1]]; k = len(t) - 2
    while k >= 1 and t[k].lower() in PART: out.insert(0, t[k]); k -= 1
    return ' '.join(out)
STOP = {'and', 'or', 'the', 'of', 'to', 'in', 'a', 'an', 'their', 'his', 'her', 'its', 'on', 'for', 'with', 'from', 'by'}
def short_title(title):
    t = re.sub(r'^\W+|\W+$', '', title)
    full = t
    t = re.split(r'(?<!\bSt)(?<!\bpp)(?<!\bvol)(?<!\bDr)(?<!\bMr)(?<!\bNo)(?<!\bno)(?<!\bVol)[:.]\s', t)[0]
    if t.count('(') > t.count(')'): t = t[:t.rfind('(')].strip()
    if len(t.split()) <= 2 and len(full) > len(t) + 3:      # 'Bernard Stiegler: A Glossary of Terms'
        t = t + ' - ' + re.sub(r'^[:.\s]+', '', full[len(t):])
    if len(t) > 60:
        w = t[:61].split()[:-1] if t[60:61] not in (' ', '') else t[:60].split()
        while w and w[-1].lower().strip(',;') in STOP: w = w[:-1]
        t = ' '.join(w).rstrip(',;')
    from conv import ascii_name
    return ascii_name(t, 60)
def trim_words(t, n):
    if len(t) <= n: return t
    w = t[:n + 1].split()[:-1] if t[n:n + 1] not in (' ', '') else t[:n].split()
    while len(w) > 1 and w[-1].lower().strip(',;') in STOP: w = w[:-1]
    return ' '.join(w).rstrip(',;')
def make(pdf, catalog, route, **kw):
    from conv import ascii_name
    c = fm(catalog)
    title = c['title']; authors = c['author'] if isinstance(c['author'], list) else [c['author']]
    who = authors or c['translator'] or c.get('editor') or []
    sur = kw.pop('author_short') if 'author_short' in kw else (surname(who[0]) if who else '')
    short = kw.pop('short', None) or short_title(title)
    folder_name = ascii_name(f'{short} ({ascii_name(sur)})' if sur else short, 80)
    subject = pdf.split('/')[1]
    prefix = kw.pop('prefix', None) or trim_words(short, 32)
    job = dict(pdf=V + pdf, pdf_vault=pdf, catalog=catalog[:-3], route=route, title=title.replace('"', "'"), authors=authors,
               byline=kw.pop('byline', None) or byl(authors, c),
               folder=f'Library/{subject}/{folder_name}', index_name=folder_name, prefix=prefix, out='/home/claude/p4/out', date='2026-10-07')
    job['ctype'] = c.get('ctype') or 'book'
    if 'single' not in kw:
        import pymupdf as fitz
        try: job['single'] = len(fitz.open(job['pdf'])) <= 40
        except Exception: job['single'] = False
    job.update(kw)
    return job
if __name__ == '__main__':
    pass
