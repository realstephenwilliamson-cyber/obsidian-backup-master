# nt_link.py (28 Oct 2026, third session after 28 Oct): link New Testament references in restored CCEL footnotes the way the
# books' existing footnotes are linked: [[Matthew 11#^11-28|Matt. xi. 28]], [[Matthew 11#^11-29|29]]; a range keeps its label
# ("John xxi. 1–11") and links its first verse; Old Testament references stay plain, as everywhere in these two books.
# The abbreviation -> note map is read from the existing links (notes.json); test() relinks every existing link group from its
# plain text and counts agreement.
import re, json, sys

ROM = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100}
def roman(s):
    s = s.lower(); v = 0
    for i, ch in enumerate(s):
        x = ROM[ch]; v += -x if i + 1 < len(s) and ROM[s[i + 1]] > x else x
    return v

def build_map(notes):
    M = {}
    for s in notes.values():
        for m in re.finditer(r'\[\[([1-3]?\s?[A-Z][A-Za-z ]+?) (\d{2,3})#\^(\d+)-(\d+)\|((?:[123] )?[A-Z][a-z]+\.?) ([ivxlc]+)\. (\d+)', s):
            base, cc, c, v, ab, rn, vv = m.groups()
            if roman(rn) == int(c) == int(cc) and v == vv: M.setdefault(ab, {}).setdefault(base, 0); M[ab][base] += 1
    return {ab: max(d, key=d.get) for ab, d in M.items()}

def link(text, M):
    abbrs = sorted(M, key=len, reverse=True)
    RNG = r'(?:[–-](?:[ivxlc]+\. )?\d+)?'
    head = re.compile(r'(?<![\w\[|])(' + '|'.join(re.escape(a) for a in abbrs) + r') ([ivxlc]+)\. (\d+)(' + RNG + r')')
    cont = re.compile(r', (?:([ivxlc]+)\. )?(\d+)(' + RNG + r')(?![\d]|\.\s*\d|\s*[ivxlc]+\.)')
    out = []; i = 0
    while True:
        m = head.search(text, i)
        if not m: out.append(text[i:]); return ''.join(out)
        out.append(text[i:m.start()])
        ab, rn, v, rng = m.groups(); c = roman(rn); base = M[ab]
        out.append(f'[[{base} {c:02d}#^{c}-{v}|{ab} {rn}. {v}{rng}]]'); j = m.end()
        while True:
            mm = cont.match(text, j)
            if not mm: break
            rn2, v2, rng2 = mm.groups()
            if rn2: c = roman(rn2); lab = f'{rn2}. {v2}{rng2}'
            else: lab = f'{v2}{rng2}'
            out.append(f', [[{base} {c:02d}#^{c}-{v2}|{lab}]]'); j = mm.end()
        i = j

def test(notes, M):
    ok = bad = 0; ex = []
    grp = re.compile(r'(?:\[\[[^\]|]+#\^\d+-\d+\|[^\]]+\]\](?:, (?=\[\[))?)+')
    for s in notes.values():
        for m in grp.finditer(s):
            g = m.group(0); pl = re.sub(r'\[\[[^\]|]+\|([^\]]+)\]\]', r'\1', g)
            r = link(pl, M)
            if r == g: ok += 1
            else:
                bad += 1
                if len(ex) < 12: ex.append((g, r))
    return ok, bad, ex

if __name__ == '__main__':
    notes = json.load(open(sys.argv[1])); M = build_map(notes)
    print(len(M), M)
    ok, bad, ex = test(notes, M); print('agree', ok, 'differ', bad)
    for g, r in ex: print('  ORIG', g[:150]); print('  MINE', r[:150])
