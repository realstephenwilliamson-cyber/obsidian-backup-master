# compare.py (27 Oct 2026, Dyczkowski footnotes night 1): compares a blind checker's answers with the converted notes (the key from
# sample.py). Printed footnote numbers on a page are matched to the note's definitions on that page in order. A call agrees when
# the last three words before it agree; a definition when its first three words agree (fuzzy, for OCR slips).
# Usage: compare.py KEY.json ANSWERS.json REPORT.json
import sys, json, re, difflib
keyf, ansf, repf = sys.argv[1:4]
K = json.load(open(keyf, encoding='utf-8')); A = json.load(open(ansf, encoding='utf-8'))
A = {a['task']: a for a in (A if isinstance(A, list) else A.get('answers', A.get('tasks', [])))}
W = lambda s: re.findall(r'[^\W\d_]+', (s or '').lower())
def same(a, b, k=3):
    a, b = W(a)[-k:], W(b)[-k:]
    if not a or not b: return False
    return a == b or difflib.SequenceMatcher(None, ' '.join(a), ' '.join(b)).ratio() > 0.85
def samestart(a, b, k=3):
    a, b = W(a)[:k], W(b)[:k]
    return bool(a) and bool(b) and (a == b or difflib.SequenceMatcher(None, ' '.join(a), ' '.join(b)).ratio() > 0.8)
rows, agree, total = [], 0, 0
for tid, k in K.items():
    a = A.get(tid)
    if not a: rows.append({'task': tid, 'error': 'no answer'}); total += len(k['sampled']); continue
    if 'carry_expected' in k:
        total += 1; ok = samestart(a.get('carry') or '', k['carry_expected'])
        agree += ok; rows.append({'task': tid, 'n': k['carry_of'], 'carry_ok': ok, 'checker_carry': a.get('carry'), 'ours_carry': k['carry_expected'][:60], 'ok_call': ok, 'ok_def': ok})
        continue
    fns = [f for f in a.get('footnotes', []) if str(f.get('printed', '')).isdigit()]
    def clean(s): return re.sub(r'\\\[illegible\\\]|\[illegible\]|&lt;sup&gt;.*?&lt;/sup&gt;|<sup>.*?</sup>', ' ', s or '')
    def r5(x, y):
        x, y = ' '.join(W(clean(x))[:5]), ' '.join(W(clean(y))[:5])
        return difflib.SequenceMatcher(None, x, y).ratio() if x and y else 0
    # printed number of each of our definitions on the page, by the first words; then by the page's dominant offset
    pmap = {}
    for n in k['defs_on_page']:
        ours = k['def_starts'].get(str(n), k['def_starts'].get(n, ''))
        best = max(fns, key=lambda f: r5(f.get('first', ''), ours), default=None)
        if best and r5(best.get('first', ''), ours) > 0.6: pmap[n] = int(best['printed'])
    offs = [n - p for n, p in pmap.items()]
    off = max(set(offs), key=offs.count) if offs else None
    for n in k['sampled']:
        total += 1; p = pmap.get(n, (n - off) if off is not None else None)
        call = next((c for c in a.get('calls', []) if str(c.get('printed')) == str(p)), None)
        fn = next((f for f in fns if str(f.get('printed')) == str(p)), None)
        ours_b = k['calls'].get(str(n), k['calls'].get(n, ''))
        ok_call = bool(call) and (same(call.get('before', ''), ours_b) or (not W(call.get('before', '')) and not W(ours_b)[-1:]))
        ok_def = n in pmap
        if ok_call and ok_def: agree += 1
        rows.append({'task': tid, 'n': n, 'printed': p, 'by_words': n in pmap, 'ok_call': ok_call, 'ok_def': ok_def,
                     'checker_before': (call or {}).get('before'), 'ours_before': ours_b[-60:],
                     'checker_first': (fn or {}).get('first'), 'ours_first': (k['def_starts'].get(str(n)) or k['def_starts'].get(n) or '')[:60],
                     'special': n in k['special'], 'carry': a.get('carry')})
json.dump({'agree': agree, 'total': total, 'rows': rows}, open(repf, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('agree %d / %d' % (agree, total))
for r in rows:
    if not (r.get('ok_call') and r.get('ok_def')): print(json.dumps(r, ensure_ascii=False)[:400])
