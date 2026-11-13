# Post-fixes to the converted Pelikan vol. 1 notes (13 Nov 2026), run once on conv.py's output folder.
# usage: postfix_ct1.py <out folder of the book>. Each change must apply exactly once, or the script stops.
import sys, re, os
D = sys.argv[1]


def edit(name, fn):
    p = os.path.join(D, name + '.md'); t = open(p, encoding='utf-8').read(); t2 = fn(t)
    assert t2 != t, name
    open(p, 'w', encoding='utf-8').write(t2)


def once(t, a, b):
    assert t.count(a) == 1, (a, t.count(a))
    return t.replace(a, b, 1)


def page(t, k, new):
    """Replace the text of PDF page k (between its marker and the next marker) with new."""
    m = re.search(r'(^\*\[[^\]]*\]\* \^pg%d\n)(.*?)(?=^\*\[[^\]]*\]\* \^pg\d+\n|\Z)' % k, t, re.S | re.M)
    assert m, k
    return t[:m.start(2)] + '\n' + new + '\n\n' + t[m.end(2):]


# 1. Chapter 4's section headings: 'Christ as Homoousios' was read 'Christ as Homooustos'; 'The Three and the One'
#    (top of p. 211) was dropped as a running head, which has the same words.
def ch4(t):
    t = once(t, '\nChrist as Homooustos\n', '\n### Christ as Homoousios\n')
    return once(t, '\nThe form in which the homoousios was vindicated',
                '\n### The Three and the One\n\nThe form in which the homoousios was vindicated')
edit('Christian Tradition 1 08 - Chapter 4. The Mystery of the Trinity', ch4)


# 2. Covers and endpapers: OCR noise replaced by a bracketed description (the page markers stay).
def fm(t):
    t = page(t, 1, '*\\[Front cover; the symbol is described on the colophon page.\\]*')
    t = page(t, 3, '*\\[Endpaper, blank.\\]*')
    return page(t, 4, '*\\[Endpaper, blank.\\]*')
edit('Christian Tradition 1 01 - Front matter', fm)


def bm(t):
    t = page(t, 424, "*\\[Endpaper: a previous reader's pencilled list of names with dates; not transcribed.\\]*")
    t = page(t, 425, '*\\[Endpaper, blank.\\]*')
    t = page(t, 427, '*\\[Endpaper, blank.\\]*')
    return page(t, 428, '*\\[Back cover.\\]*')
edit('Christian Tradition 1 15 - Back matter', bm)


# 3. 't' and 'i' read as '#' (the converter escaped them): Clem.Str. (Stromateis), Sibylline, 'to'; a lone '#' is a pencil mark.
def ch1(t):
    t = once(t, 'Clem. S\\#r.6.18.168.3', 'Clem. Str.6.18.168.3')
    t = once(t, 'the S\\#bylline Oracles', 'the Sibylline Oracles')
    return once(t, '\n\\#\n', '\n')
edit('Christian Tradition 1 05 - Chapter 1. Praeparatio Evangelica', ch1)
edit('Christian Tradition 1 10 - Chapter 6. Nature and Grace', lambda t: once(t, 'he was bound \\#o them', 'he was bound to them'))
print('post-fixes applied')
