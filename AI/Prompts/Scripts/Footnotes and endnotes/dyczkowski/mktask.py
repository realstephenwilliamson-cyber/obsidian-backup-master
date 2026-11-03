# mktask.py ID [EXTRA] (2 Nov 2026, night 3): prints the reader task for one note from reader-task-n3.txt and the pre-pass data.
import sys, json, re
H = '/home/claude/dyfn'; nid = sys.argv[1]; extra = sys.argv[2] if len(sys.argv) > 2 else ''
t = open(f'{H}/scripts/reader-task-n3.txt', encoding='utf-8').read().split('\n\n', 1)[1]
p = json.load(open(f'{H}/work/{nid}/pre.json')); nums = sorted(d['n'] for pg in p['pages'] for d in pg['defs'])
path = [l.strip().split('=', 1)[1] for l in open(f'{H}/paths.txt') if l.startswith(nid + '=')][0]
gaps = sorted(set(range(nums[0], nums[-1] + 1)) - set(nums)) if nums else []
flags = ''
if gaps: flags = 'pages.txt flags gaps: no definition numbered %s. At each gap the OCR probably lost or garbled the footnote\'s number (it then stands as a plain paragraph, or run together with the one before): look closely and split or label it.' % ', '.join(map(str, gaps))
off = [f for f in p['flags'] if 'between' in f]
if off: flags += ' Also a paragraph numbered off the sequence: ' + '; '.join('line %d (%s)' % (f['line'], f['number']) for f in off) + ' — decide on the page what it is.'
t = (t.replace('__ID__', nid).replace('__VOL__', nid[1:3]).replace('__NOTE__', path.split('/')[-1][:-3])
     .replace('__RANGE__', 'footnotes %d–%d in the note\'s numbering' % (nums[0], nums[-1])).replace('__REAL__', str(len(p['real_defs_before'])))
     .replace('__PAGES__', '%d pages with footnotes, PDF %d–%d' % (len(p['pages']), p['pages'][0]['pdf'], p['pages'][-1]['pdf']))
     .replace('__FLAGS__', (flags + ' ' + extra).strip()))
print(t)
