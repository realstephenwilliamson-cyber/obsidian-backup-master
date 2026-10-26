# Container paths (/home/claude/dz/...) are those of the 26 Oct 2026 session; adjust before reuse.
# Second pass for volumes already replaced once (26 Oct): the old file is the first fixed copy (post-first.json), the new one the re-fixed copy (post.json).
import json, sys
post = json.load(open('/home/claude/dz/rb/post.json')); first = json.load(open('/home/claude/dz/rb/post-first.json')); want = set(sys.argv[1:]); L = []
for name, r in sorted(post.items()):
    key = name.replace('Dyczkowski - Tantraloka, vol. ', 'v').replace('.pdf', '')
    if key not in want: continue
    L.append(dict(target='Library/Trika/Dyczkowski - Tantraloka translation/' + name, parts=r['parts'], size=r['size'], sha256=r['sha256'], old_size=first[name]['size'], old_sha256=first[name]['sha256'], line=''))
json.dump(L, open('/mnt/user-data/outputs/work/dzrep.json', 'w'), ensure_ascii=False, indent=0)
print(len(L), 'entries'); [print(' ', x['target'].split('/')[-1], x['parts'], x['size'], x['old_size']) for x in L]
