# lead-g6.py (SDK 1): the lead's moves for group 6: the first note's text of PDF 670 (n. 2391) and 691 (n. 2450) left at the end of
# the block before; with the readers' added numbers 2392 and 2451 folded in.
import json
B = chr(92)
L = {
 'c103': ([669, 670], [
   ('2389 '+B+'[R.V., “become.”'+B+'] 365 έναγ.\n\n\n*[p. 662]*', '2389 '+B+'[R.V., “become.”'+B+'] 365\n\n\n*[p. 662]*'),
   ('2391 [[Matthew 19#^19-7|', '2391 έναγ. 2392 [[Matthew 19#^19-7|')]),
 'c104': ([690, 691], [
   ('scarcely any other peculiarities.—R.'+B+'] κατ λξιν.\n\n\n*[p. 683]*', 'scarcely any other peculiarities.—R.'+B+']\n\n\n*[p. 683]*'),
   ('2450 [[Galatians 01#^1-15|', '2450 κατ λξιν. 2451 [[Galatians 01#^1-15|')]),
}
for cid, (Ks, E) in L.items():
    json.dump({'case': cid, 'Ks': Ks, 'edits': [{'old': o, 'new': n, 'why': 'lead'} for o, n in E],
               'note': 'lead: move across blocks %d/%d (PDF text: %s)' % (Ks[0], Ks[1], 'n. 2391 έναγ.' if cid == 'c103' else 'n. 2450 κατ λξιν.')}, open('lead/%s.json' % cid, 'w', encoding='utf-8'), ensure_ascii=False)
# second round: two more leftovers (c101 n. 2370, c115 n. 2920); c102 and c110 accepted as read (the guard matched other
# references, "Matt. xix." and "Matt. xxiii."; no leftover before the block: checked by the lead). guard_ok: checked by the lead.
L2 = {
 'c101': ([661, 662], [
   (B+'[Slightly altered.'+B+'] '+B+'[ἐπιτρπων, “stewards,” answering here to “overseers,” in the worst sense.—R.'+B+']\n\n\n', B+'[Slightly altered.'+B+']\n\n\n'),
   ('2370 2371 Jer. ii. 12.', '2370 '+B+'[ἐπιτρπων, “stewards,” answering here to “overseers,” in the worst sense.—R.'+B+'] 2371 Jer. ii. 12.')]),
 'c115': ([845, 846], [
   (' 464 [[Luke 22#^22-4|Luke xxii. 4]]. '+B+'[The explanation is untenable. The “captains” (στρατηγο) were not “chiliarchs,” but the\n\n\n', ' 464\n\n\n'),
   ('2920 officers of the temple guard', '2920 [[Luke 22#^22-4|Luke xxii. 4]]. '+B+'[The explanation is untenable. The “captains” (στρατηγο) were not “chiliarchs,” but the officers of the temple guard')]),
}
for cid, (Ks, E) in L2.items():
    json.dump({'case': cid, 'Ks': Ks, 'edits': [{'old': o, 'new': n, 'why': 'lead'} for o, n in E], 'note': 'lead: move across blocks %d/%d' % tuple(Ks)}, open('lead/%s.json' % cid, 'w', encoding='utf-8'), ensure_ascii=False)
for cid in ('c102', 'c110'):
    r = json.load(open('read/%s.json' % cid, encoding='utf-8-sig')); r['guard_ok'] = True; r['note'] = 'lead: accepted as read; ' + r.get('note', '')
    json.dump(r, open('lead/%s.json' % cid, 'w', encoding='utf-8'), ensure_ascii=False)
r = json.load(open('lead/c103.json', encoding='utf-8')); r['guard_ok'] = True; json.dump(r, open('lead/c103.json', 'w', encoding='utf-8'), ensure_ascii=False)
