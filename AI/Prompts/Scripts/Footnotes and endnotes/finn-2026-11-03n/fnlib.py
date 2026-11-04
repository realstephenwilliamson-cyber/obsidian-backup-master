# fnlib.py (3 Nov 2026, night): build exact {id, path, old, new} edits for Finn's notes from span edits on the page blocks.
# Usage in a spec script: S = Spec('02'); S.sub(id, K, old, new) replaces 'old' (once within page K's block); S.para(id, K, first,
# n, new_label) turns the paragraph starting with 'first' (and the n-1 non-empty paragraphs after it) into one line '[^lab]: ...'
# (new_label None -> keep as one plain paragraph 'N\. ...'); S.move(...) etc. S.build() -> edits (old made unique in the file by
# context), and a simulation check: calls and definitions paired, a blank line before every definition run.
import re, glob, os, json
ROOT = '/home/claude/finn/md/'
VP = 'Library/Trika/The Kulacudamani Tantra and The Vamakesvara Tantra (Finn)/'
MARK = re.compile(r'(?m)^\*\[(?:p|PDF)\.? ([^\]]*)\]\* \^pg(\d+)$')
class Spec:
    def __init__(s, n):
        s.fn = os.path.basename(glob.glob(ROOT + 'The Kulacudamani Tantra %s - *.md' % n)[0]); s.path = VP + s.fn
        s.t = open(ROOT + s.fn, encoding='utf-8').read(); s.spans = []
        ms = list(MARK.finditer(s.t)); s.blk = {}
        for i, m in enumerate(ms): s.blk[int(m.group(2))] = (m.end(), ms[i + 1].start() if i + 1 < len(ms) else len(s.t))
    def find(s, K, old):
        a, b = s.blk[K]; sec = s.t[a:b]; c = sec.count(old)
        assert c == 1, (K, c, old[:80]); i = a + sec.index(old); return i, i + len(old)
    def sub(s, id, K, old, new):
        i, j = s.find(K, old); s.spans.append([i, j, new, id])
    def lines(s, K, first, n=1):
        """span of the paragraph beginning with 'first' and the n-1 non-empty lines after it; returns (i, j, [lines])"""
        a, b = s.blk[K]; sec = s.t[a:b]
        hits = [m.start() for m in re.finditer(r'(?m)^' + re.escape(first), sec)]; assert len(hits) == 1, (K, len(hits), first)
        i = a + hits[0]; out = []; j = i
        while len(out) < n:
            e = s.t.index('\n', j) if '\n' in s.t[j:] else len(s.t)
            ln = s.t[j:e]
            if ln.strip(): out.append(ln)
            if len(out) == n: j = e; break
            j = e + 1
        return i, j, out
    def para(s, id, K, first, n, lab, strip=r'^\s*[\dIlOS]{1,3}\\?[.,*»]?\s+', text=None, fix=None):
        i, j, ls = s.lines(K, first, n)
        body = ' '.join(x.strip() for x in ls)
        if strip: body = re.sub(strip, '', body, count=1)
        if fix:
            for o, nn in fix: assert body.count(o) == 1, (id, o); body = body.replace(o, nn)
        if text is not None: body = text
        new = ('[^%s]: ' % lab + body) if not str(lab).startswith('plain:') else (str(lab)[6:] + '\\. ' + body)
        s.spans.append([i, j, new, id]); return new
    def build(s):
        sp = sorted(s.spans)
        for x, y in zip(sp, sp[1:]): assert x[1] <= y[0], ('overlap', x[3], y[3])
        # final text
        u = s.t
        for i, j, new, id in sorted(sp, reverse=True): u = u[:i] + new + u[j:]
        # exact edits, old unique in the original, context not crossing a neighbour's span
        E = []
        for k, (i, j, new, id) in enumerate(sp):
            lo = sp[k - 1][1] if k else 0; hi = sp[k + 1][0] if k + 1 < len(sp) else len(s.t)
            a, b = i, j
            while s.t.count(s.t[a:b]) != 1 or b - a < 6:
                if a > lo: a -= 1
                if b < hi: b += 1
                if a <= lo and b >= hi and s.t.count(s.t[a:b]) != 1: raise SystemExit('not unique: ' + id)
            E.append(dict(id=id, path=s.path, old=s.t[a:b], new=s.t[a:i] + new + s.t[j:b]))
        # simulate as pf591 does
        v = s.t
        for e in E: assert s.t.count(e['old']) == 1 and v.count(e['old']) == 1, e['id']; v = v.replace(e['old'], e['new'], 1)
        assert v == u
        s.u = u; s.E = E; s.check(); return E
    def check(s):
        t = s.u
        calls = re.findall(r'\[\^([^\]]+)\](?!:)', t); defs = re.findall(r'(?m)^\[\^([^\]]+)\]:', t)
        cs, ds = set(calls), set(defs)
        prob = dict(no_def=sorted(cs - ds), no_call=sorted(ds - cs), dup_calls=sorted({c for c in calls if calls.count(c) > 1}),
                    dup_defs=sorted({d for d in defs if defs.count(d) > 1}))
        runs = []
        for m in re.finditer(r'(?m)^\[\^[^\]]+\]:', t):
            k = m.start()
            if k >= 2 and t[k - 1] == '\n' and t[k - 2] != '\n':
                prev = t[t.rfind('\n', 0, k - 1) + 1:k - 1]
                if not prev.startswith('[^'): runs.append(prev[-50:])
        # a text line right after a definition (would be absorbed into it)
        after = []
        for m in re.finditer(r'(?m)^\[\^[^\]]+\]:.*\n(?!\n|\[\^|$)(.+)', t): after.append(m.group(1)[:50])
        print(s.fn, 'calls', len(calls), 'defs', len(defs), {k: v for k, v in prob.items() if v}, 'def after text', runs, 'text after def', after[:5])
        s.prob = prob
    def save(s, out):
        json.dump(s.E, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0); print(len(s.E), 'edits ->', out)

def _lab(self, N, K):
    """label for footnote N on page block K: N if free in the file (original definitions and labels given so far), else N-pP"""
    if not hasattr(self, 'used'): self.used = set(re.findall(r'(?m)^\[\^([^\]]+)\]:', self.t))
    pp = re.sub(r'[^\w]', '', [m.group(1) for m in MARK.finditer(self.t) if int(m.group(2)) == K][0])
    lab = str(N) if str(N) not in self.used else '%s-p%s' % (N, pp)
    assert lab not in self.used, lab
    self.used.add(lab); return lab
Spec.L = _lab
