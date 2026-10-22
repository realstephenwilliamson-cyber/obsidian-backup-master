# Dhvanyaloka: remove the quote marks before a footnote reference where the printed page shows none there (or fewer),
# from the visual check of the printed lines (qresult1/2.json). Works on the notes as they are in the vault now.
import os, re, json, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
VAULT = r'C:\Vaults\Obsidian Vault'
FOLDER = os.path.join(VAULT, r'Library\Trika\The Dhvanyaloka of Anandavardhana with the Locana (Anandavardhana)')
cases = {c['n']: c for c in json.load(open(os.path.join(HERE, 'quotecases.json'), encoding='utf-8')) if c.get('n')}
res = json.load(open(os.path.join(HERE, 'qresult1.json'), encoding='utf-8')) + json.load(open(os.path.join(HERE, 'qresult2.json'), encoding='utf-8'))
rep = collections.Counter(); files = {}; changes = []
for r in res:
    c = cases.get(r['n'])
    if not c: rep['no case'] += 1; continue
    if not r.get('certain', False): rep['uncertain: left'] += 1; continue
    if re.search(r'between', r.get('note') or '') or r['n'] in (264, 269, 295, 302): rep['punctuation between: left'] += 1; continue
    printed = r.get('printed_quotes') or ''
    mdq = c['quotes']
    if printed == mdq: rep['real quote: left'] += 1; continue
    # the printed marks must be the md marks with some removed (same order)
    it = iter(mdq)
    if not all(ch in it for ch in printed): rep['printed marks not in md: left'] += 1; continue
    fn = c['f']
    if fn not in files: files[fn] = open(os.path.join(FOLDER, fn), encoding='utf-8').read()
    old = c['word'] + mdq + '[^' + c['id'] + ']'
    if files[fn].count(old) != 1: rep['not found once: left'] += 1; continue
    files[fn] = files[fn].replace(old, c['word'] + printed + '[^' + c['id'] + ']')
    rep['fixed'] += 1; changes.append((fn, c['id'], old, c['word'] + printed))
os.makedirs(os.path.join(HERE, 'qout'), exist_ok=True)
for fn, t in files.items():
    t = re.sub(r'^(text_source: .*?)("?)$', lambda m: m.group(1) + ('' if 'quote marks' in m.group(1) else '; misread quote marks at the calls removed after a visual check 18 Oct 2026') + m.group(2), t, count=1, flags=re.M)
    open(os.path.join(HERE, 'qout', fn), 'w', encoding='utf-8', newline='\n').write(t)
json.dump(changes, open(os.path.join(HERE, 'quotefix_log.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(dict(rep), 'files', len(files))
