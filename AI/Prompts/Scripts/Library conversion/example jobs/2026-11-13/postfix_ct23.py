# Post-fixes to the converted Pelikan vols. 2 and 3 (13 Nov 2026), run once on conv.py's output (the folder holding both
# book folders). Each change must apply exactly once, or the script stops. The readings of the '#' misreads (italic letters
# in the margin abbreviations) were read off the page images.
import sys, re, os
D = sys.argv[1]
V2 = os.path.join(D, 'The Christian Tradition 2 - The Spirit of Eastern Christendom (Pelikan)')
V3 = os.path.join(D, 'The Christian Tradition 3 - The Growth of Medieval Theology (Pelikan)')


def edit(folder, prefix, pairs):
    fs = [f for f in os.listdir(folder) if f.startswith(prefix)]
    assert len(fs) == 1, (prefix, fs)
    p = os.path.join(folder, fs[0]); t = open(p, encoding='utf-8').read()
    for a, b in pairs:
        assert t.count(a) == 1, (fs[0], a, t.count(a))
        t = t.replace(a, b, 1)
    open(p, 'w', encoding='utf-8').write(t)


def page(folder, prefix, k, new):
    fs = [f for f in os.listdir(folder) if f.startswith(prefix)]
    p = os.path.join(folder, fs[0]); t = open(p, encoding='utf-8').read()
    m = re.search(r'(^\*\[[^\]]*\]\* \^pg%d\n)(.*?)(?=^\*\[[^\]]*\]\* \^pg\d+\n|\Z)' % k, t, re.S | re.M)
    assert m, (prefix, k)
    open(p, 'w', encoding='utf-8').write(t[:m.start(2)] + '\n' + new + '\n\n' + t[m.end(2):])


# vol. 2
page(V2, 'Christian Tradition 2 01 ', 1, '*\\[Spine.\\]*')
edit(V2, 'Christian Tradition 2 03 ', [('Ῥωμανὸς 6 Mehwdds cal i ᾿Ακάθιστος', 'Ῥωμανὸς ὁ Μελωδὸς καὶ ἡ ᾿Ακάθιστος')])
edit(V2, 'Christian Tradition 2 05 ', [('\nThe Councils and Thew Achievements\n', '\n### The Councils and Their Achievements\n')])
edit(V2, 'Christian Tradition 2 06 ', [('Bab.U\\#.6.20', 'Bab.Un.6.20'), ('Tim.J.Fp.36 (CSCO 75::177174:256\\])', 'Tim.I.Ep.36 (CSCO 75:177\\[74:256\\])')])   # '::' would be a Dataview field
edit(V2, 'Christian Tradition 2 07 ', [('ap.Niceph.An\\#irr.2.1', 'ap.Niceph.Antirr.2.1')])
edit(V2, 'Christian Tradition 2 08 ', [('Phot.Mys\\#.86', 'Phot.Myst.86')])
edit(V2, 'Christian Tradition 2 09 ', [('ap.Petr.Sic.H\\#s?.10', 'ap.Petr.Sic.Hist.10'), ('Mi#7.9.8', 'Mim.9.8')])
edit(V2, 'Christian Tradition 2 10 ', [('\\[\\#ewpia}', '\\[θεωρία\\]'), ('Sim.N.Th.£#4.8', 'Sim.N.Th.Eth.8'), ('Jer.CP.Ep.Ta\\#b.1.1', 'Jer.CP.Ep.Tüb.1.1')])
# vol. 3
page(V3, 'Christian Tradition 3 01 ', 1, '*\\[Spine.\\]*')
edit(V3, 'Christian Tradition 3 05 ', [('Isid.Sev.Se\\#t.t.x.1', 'Isid.Sev.Sent.1.1.1'), ('Ale.Tri\\#.3.2', 'Alc.Trin.3.2')])
edit(V3, 'Christian Tradition 3 06 ', [('Hine.R.De\\#.13', 'Hinc.R.Deit.13')])
edit(V3, 'Christian Tradition 3 07 ', [('Petr.Ab.Ep\\#.5', 'Petr.Ab.Ep.5'),
     ('\nThe Gross as the Redemption of Mankind Discipline, even', '\n### The Cross as the Redemption of Mankind\n\nDiscipline, even')])
edit(V3, 'Christian Tradition 3 08 ', [('Qcc\\#p.5.727-28', 'Occup.5.727-28'), ('Herm.Mag.Ep\\#.31', 'Herm.Mag.Epit.31')])
edit(V3, 'Christian Tradition 3 09 ', [('Gisl.Crisp.Si\\#z,', 'Gisl.Crisp.Sim.'), ('Rich.S.Vict.Sei\\#.8', 'Rich.S.Vict.Seir.8')])
edit(V3, 'Christian Tradition 3 10 ', [('Bonav.Sen\\#t.1.29.2.2', 'Bonav.Sent.1.29.2.2'), ('Bonav.I\\#in.4.t', 'Bonav.Itin.4.1'), ('Bonav.I\\#in.1.7', 'Bonav.Itin.1.7')])
print('post-fixes applied')
