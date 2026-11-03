# multi.py OUT SCALE PDF:Y0:Y1 [...]: stack several page crops (300 dpi images) into one image, each labelled
import sys
from PIL import Image, ImageDraw
out, sc = sys.argv[1], float(sys.argv[2]); parts = []
for a in sys.argv[3:]:
    k, y0, y1 = map(int, a.split(':')); im = Image.open('/home/claude/lost/ch05/img300/p-%03d.png' % k).convert('L')
    im = im.crop((100, y0, im.width - 100, y1)); im = im.resize((int(im.width * sc), int(im.height * sc)))
    lab = Image.new('L', (im.width, 22), 200); ImageDraw.Draw(lab).text((4, 4), 'PDF %d  y %d-%d' % (k, y0, y1), fill=0)
    parts += [lab, im]
W = max(p.width for p in parts); H = sum(p.height for p in parts); o = Image.new('L', (W, H), 255); y = 0
for p in parts: o.paste(p, (0, y)); y += p.height
o.save(out)
