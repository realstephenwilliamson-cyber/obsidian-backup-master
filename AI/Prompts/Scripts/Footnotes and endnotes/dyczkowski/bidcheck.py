# bidcheck.py ID ... (2 Nov 2026, night 3): when review.py reports block_ids False, show whether only the whitespace after a
# block id changed (a moved paragraph leaves an empty page) or an id was lost, added or reordered.
import re, sys, difflib
for nid in sys.argv[1:]:
    a = open(f'/home/claude/dyfn/src/{nid}.md', encoding='utf-8').read(); b = open(f'/home/claude/dyfn/work/{nid}/out.md', encoding='utf-8').read()
    ra = [x.strip() for x in re.findall(r'\^[A-Za-z0-9-]+\s*$', a, re.M)]; rb = [x.strip() for x in re.findall(r'\^[A-Za-z0-9-]+\s*$', b, re.M)]
    print(nid, 'ids', len(ra), len(rb), 'same ids in the same order' if ra == rb else [o for o in difflib.SequenceMatcher(None, ra, rb).get_opcodes() if o[0] != 'equal'][:5])
