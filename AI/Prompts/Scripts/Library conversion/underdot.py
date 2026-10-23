# underdot.py (22 Oct 2026, Lutgendorf): a text layer that draws the dot below a letter as a separate mark, read by PyMuPDF as "\_", put back on its letter.
# Usage: python3 underdot.py <folder of converted notes> [write]   (without "write" it only counts)
import glob, re, sys
DOT = dict(zip('dtnsrhlmDTNSRHLM', 'ḍṭṇṣṛḥḷṃḌṬṆṢṚḤḶṂ'))
def fix(t):
    head, body = (t.split('\n---\n', 1) if t.startswith('---\n') else ('', t))
    n0 = body.count('\\_')
    body = re.sub(r'(\w) ?\\_ ?n', lambda m: m.group(1) + 'ṅ', body)            # dot above, placed before the n: la \_ngot -> laṅgot
    body = re.sub(r'([dtnsrhlmDTNSRHLM])\\_ ?(?=\w|$|[\s,.;:)’”-])', lambda m: DOT[m.group(1)], body)   # dot below after the letter
    body = re.sub(r'(?:\\_ ?)+(?=\w)', '', body)    # stray dots left at the start of a word (their letter is elsewhere on the line): dropped
    body = re.sub(r' (?:\\_ ?)+', ' ', body)
    return (head + '\n---\n' + body if head else body), n0, body.count('\\_')
if __name__ == '__main__':
    tot0 = tot1 = 0; left = []
    for f in glob.glob(sys.argv[1] + '/*.md'):
        t = open(f, encoding='utf-8').read(); nt, a, b = fix(t); tot0 += a; tot1 += b
        left += re.findall(r'.{20}\\_.{15}', nt)
        if len(sys.argv) > 2 and sys.argv[2] == 'write': open(f, 'w', encoding='utf-8').write(nt)
    print('before', tot0, 'after', tot1); print(left[:12])
