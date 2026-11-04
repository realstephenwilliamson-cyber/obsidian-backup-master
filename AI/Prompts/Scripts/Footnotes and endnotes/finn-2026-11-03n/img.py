import pymupdf, sys
d = pymupdf.open('/home/claude/finn/finn.pdf')
for a in sys.argv[1:]:
    K, *rest = a.split(':'); K = int(K)
    p = d[K - 1]; r = p.rect
    if rest:
        y0, y1 = map(float, rest[0].split('-')); clip = pymupdf.Rect(0, y0, r.width, y1)
    else: clip = r
    pix = p.get_pixmap(dpi=int(rest[1]) if len(rest) > 1 else 130, clip=clip)
    out = f'/home/claude/finn/img/K{K}' + (f'_{int(clip.y0)}' if rest else '') + '.png'; pix.save(out); print(out, pix.width, pix.height)
