# S8 decision 8 (26 Oct 2026, second session): a new text layer for scanned two-page spreads (Gonda, Abbinnett) without touching the page images.
# Each spread's image is split at the gutter; each half is deskewed (and upscaled if asked) and read by Tesseract as a text-only PDF page;
# that page is placed back on the original PDF page with the exact affine map (crop, scale, rotation), as a Form XObject named /OCR-…
# (GlyphLessFont, so fixlayer.py works on it). The old text layers are removed first (strip.py).
# Usage: python3 spread.py in.pdf out.pdf --lang Latin+san [--tessdata DIR] [--up 2] [--sauvola] [--single 1,2,81] [--jobs 2] [--pages 5,8]
import sys, os, argparse, subprocess, json, math, re, shutil, tempfile
from concurrent.futures import ThreadPoolExecutor
import numpy as np, cv2, pymupdf, pikepdf

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('dst')
ap.add_argument('--lang', default='eng'); ap.add_argument('--tessdata', default=None)
ap.add_argument('--up', type=float, default=1.0); ap.add_argument('--sauvola', action='store_true')
ap.add_argument('--single', default=''); ap.add_argument('--jobs', type=int, default=2); ap.add_argument('--pages', default='')
ap.add_argument('--work', default='/home/claude/s8/work/spread'); ap.add_argument('--psm', default=''); ap.add_argument('--keep-others', action='store_true')
a = ap.parse_args()
single = {int(x) for x in a.single.split(',') if x}; only = {int(x) for x in a.pages.split(',') if x}
W = os.path.join(a.work, os.path.basename(a.src).replace('.pdf', '')); os.makedirs(W, exist_ok=True)

def page_image(doc, i):
    pg = doc[i]; imgs = pg.get_images(full=True)
    if len(imgs) != 1: raise RuntimeError(f'page {i+1}: {len(imgs)} images')
    xref = imgs[0][0]; pix = pymupdf.Pixmap(doc, xref)
    if pix.alpha: pix = pymupdf.Pixmap(pix, 0)
    if pix.n not in (1, 3): pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    g = arr[:, :, 0] if pix.n == 1 else cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    rects = pg.get_image_rects(xref, transform=True); rect, mat = rects[0]
    return g.copy(), rect, mat, pg.rect, pg.rotation

def ink(g):
    b = cv2.adaptiveThreshold(g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 31, 15)
    return b

def gutter(g):
    h, w = g.shape; b = ink(g)
    prof = b[int(h * 0.08):int(h * 0.92), :].sum(axis=0).astype(float)
    k = max(3, w // 150); prof = np.convolve(prof, np.ones(k) / k, mode='same')
    lo, hi = int(w * 0.38), int(w * 0.62)
    return lo + int(np.argmin(prof[lo:hi]))

def skew(g):
    b = ink(g); s = 1000 / max(b.shape); small = cv2.resize(b, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    h, w = small.shape; c = (w / 2, h / 2)
    def score(t):
        M = cv2.getRotationMatrix2D(c, t, 1.0); r = cv2.warpAffine(small, M, (w, h), flags=cv2.INTER_NEAREST)
        p = r.sum(axis=1).astype(float); return float(np.var(p))
    best = max(np.arange(-6, 6.01, 0.5), key=score)
    best = max(np.arange(best - 0.5, best + 0.501, 0.1), key=score)
    return float(round(best, 2))

def process(g, up, ang):
    if up != 1.0: g = cv2.resize(g, None, fx=up, fy=up, interpolation=cv2.INTER_CUBIC)
    h, w = g.shape; c = (w / 2, h / 2); M = cv2.getRotationMatrix2D(c, ang, 1.0)
    cos, sin = abs(M[0, 0]), abs(M[0, 1]); nw, nh = int(h * sin + w * cos), int(h * cos + w * sin)
    M[0, 2] += nw / 2 - c[0]; M[1, 2] += nh / 2 - c[1]
    r = cv2.warpAffine(g, M, (nw, nh), flags=cv2.INTER_CUBIC, borderValue=255) if ang else g
    if not ang: M = np.array([[1, 0, 0], [0, 1, 0]], float)
    return r, M

def ocr(img, base):
    png = base + '.png'; cv2.imwrite(png, img)
    env = dict(os.environ, OMP_THREAD_LIMIT='1')
    if a.tessdata: env['TESSDATA_PREFIX'] = a.tessdata
    cmd = ['tesseract', png, base, '-l', a.lang, '--dpi', '300', '-c', 'textonly_pdf=1']
    if a.sauvola: cmd += ['-c', 'thresholding_method=2']
    if a.psm: cmd += ['--psm', a.psm]
    cmd += ['pdf', 'txt']
    subprocess.run(cmd, env=env, capture_output=True, check=True)
    return base + '.pdf'

def affine_from_points(src, dst):
    # solve [x' y'] = [x y 1] @ [[a b],[c d],[e f]]
    A = np.array([[x, y, 1] for x, y in src], float); B = np.array(dst, float)
    sol, *_ = np.linalg.lstsq(A, B, rcond=None); (a_, b_), (c_, d_), (e_, f_) = sol
    return [a_, b_, c_, d_, e_, f_]

def work_page(i):
    doc = pymupdf.open(a.src)
    g, rect, mat, prect, rot = page_image(doc, i)
    if rot: raise RuntimeError(f'page {i+1} rotated {rot}')
    Hi, Wi = g.shape
    halves = [(0, Wi)] if ((i + 1) in single or prect.width < prect.height * 1.1) else None
    if halves is None:
        x = gutter(g); halves = [(0, x), (x, Wi)]
    out = []
    for k, (x0, x1) in enumerate(halves):
        crop = g[:, x0:x1]; ang = skew(crop) if crop.shape[1] > 50 else 0.0
        proc, M = process(crop, a.up, ang)
        base = os.path.join(W, f'p{i+1:04d}{"LR"[k] if len(halves) > 1 else "S"}')
        tp = ocr(proc, base)
        tpd = pymupdf.open(tp); mb = tpd[0].rect; Hr, Wr = proc.shape
        sx, sy = Wr / mb.width, Hr / mb.height   # processed pixels per text-PDF point
        Minv = cv2.invertAffineTransform(M)
        def to_page(u, v):
            px, py = u * sx, Hr - v * sy                                      # text-PDF user space -> processed pixel (y down)
            ox, oy = Minv[0, 0] * px + Minv[0, 1] * py + Minv[0, 2], Minv[1, 0] * px + Minv[1, 1] * py + Minv[1, 2]
            ox, oy = ox / a.up + x0, oy / a.up                                 # -> original image pixel
            X, Y = rect.x0 + ox / Wi * rect.width, rect.y0 + oy / Hi * rect.height   # -> PyMuPDF page coords (y down)
            return X, prect.height - Y                                         # -> PDF user space (y up)
        pts = [(0, 0), (mb.width, 0), (0, mb.height), (mb.width, mb.height)]
        out.append(dict(pdf=tp, cm=affine_from_points(pts, [to_page(*p) for p in pts]), ang=ang, cut=(x0, x1), words=len(open(base + '.txt').read().split())))
    return i, out

doc = pymupdf.open(a.src); n = doc.page_count
for i in range(n):
    pg = doc[i]
    if pg.rotation or len(pg.get_images()) != 1: print('WARN page', i + 1, 'rotation', pg.rotation, 'images', len(pg.get_images()))
todo = [i for i in range(n) if not only or (i + 1) in only]
res = {}
with ThreadPoolExecutor(a.jobs) as ex:
    for i, out in ex.map(work_page, todo):
        res[i] = out; print('page', i + 1, [(o['cut'], o['ang'], o['words']) for o in out], flush=True)
json.dump({str(k): v for k, v in res.items()}, open(os.path.join(W, 'layout.json'), 'w'), indent=0)

# strip old text, then graft
tmp = os.path.join(W, 'stripped.pdf')
if a.keep_others:
    # strip only the pages read here (BT..ET blocks and OCR form XObjects), keep every other page's layer
    dst = pikepdf.open(a.src)
    for i in res:
        pg = dst.pages[i]; xo = pg.obj.Resources.get('/XObject', {})
        ocr = [k for k, v in xo.items() if v.get('/Subtype') == '/Form' and b'BT' in v.read_bytes() and b' Do' not in v.read_bytes()]
        c = pg.obj.Contents; streams = list(c) if isinstance(c, pikepdf.Array) else [c]
        for st in streams:
            d = st.read_bytes(); nd = re.sub(rb'(?<![A-Za-z])BT(?![A-Za-z]).*?(?<![A-Za-z])ET(?![A-Za-z])', b'', d, flags=re.S)
            for k in ocr: nd = re.sub(re.escape(str(k).encode()) + rb'\s+Do', b'', nd)
            if nd != d: st.write(nd)
        for k in ocr: del xo[k]
else:
    subprocess.run(['python3', '/home/claude/s8/strip.py', a.src, tmp], check=True)
    dst = pikepdf.open(tmp)
for i, outs in sorted(res.items()):
    page = pikepdf.Page(dst.pages[i])
    for o in outs:
        src = pikepdf.open(o['pdf']); fx = pikepdf.Page(src.pages[0]).as_form_xobject()
        loc = dst.copy_foreign(fx); name = page.add_resource(loc, pikepdf.Name.XObject, prefix='OCR-')
        cm = ' '.join(f'{v:.6f}' for v in o['cm'])
        page.contents_add(pikepdf.Stream(dst, f'q {cm} cm {name} Do Q\n'.encode()), prepend=False)
dst.save(a.dst)
print('saved', a.dst)
