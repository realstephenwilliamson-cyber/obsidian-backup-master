# filter09.py (2 Nov 2026, vol. 6 Chapter Nine): drops the starts found by fnstarts2.py whose first token is plainly not a
# misread superscript: a numbered-list or reference token ("12)", "9/2)", "(26)", "6.", "9,203.", "21/50-58", "(1992:"),
# a token opening with "(" or a dash, or a token that is a word. Usage: filter09.py STARTS.json OUT.json
import sys, json, re
S = json.load(open(sys.argv[1], encoding='utf-8'))
BAD = [re.compile(r'^\(?\d[\d/,\-–:.]*[).,:]+\)?:?$'),   # 12)  9/2)  6.  103.  9,131)  82):  186,
       re.compile(r'^[‘“]?\('),                            # (26)  (+  (4  (a  ‘(Impurity
       re.compile(r'^\d+/\d'),                             # 21/50-58  1/25  9/234
       re.compile(r'^[—–-]$'), re.compile(r'^\s*[A-Za-z]{3,}'), re.compile(r'^[‘“][‘“]?[a-z]{3,}')]
drop = 0
for k in S:
    keep = []
    for s in S[k]['starts']:
        t = s['tok']
        if any(b.search(t) for b in BAD): s['dropped_by_filter'] = True; drop += 1; print('drop', k, repr(t), s['raised'], s['ocr'][:60]); continue
        keep.append(s)
    S[k]['starts'] = keep
json.dump(S, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('dropped', drop, 'kept', sum(len(S[k]['starts']) for k in S))
