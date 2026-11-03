# lead-g5.py (SDK 1): the lead's own edits for group 5: c080 (note 1540's text left at the end of the block before; 1546 lost),
# and c072 (repair: group 4 added note 1331's text in ^pg380 while its leftover copy stayed at the end of ^pg379).
import json
B = chr(92)
L = {
 'c080': ([436, 437], False, [
   ('1539 Ps. lxix. 21. '+B+'[ε τν δν.'+B+']\n\n\n*[p. 429]*', '1539 Ps. lxix. 21.\n\n\n*[p. 429]*'),
   ('1540 1541 [[1 Corinthians 14', '1540 '+B+'[ε τν δν.'+B+'] 1541 [[1 Corinthians 14'),
   ('Matt. x. 15]]. Deut. vi.', 'Matt. x. 15]]. 1546 Deut. vi. 4.')]),
 'c072': ([379, 380], True, [
   ('1330 μετ πολλ τ τραγδα. 205 μεθαρμζεται .\n\n\n*[p. 372]*', '1330 μετ πολλ τ τραγδα. 205\n\n\n*[p. 372]*')]),
}
for cid, (Ks, undo, E) in L.items():
    json.dump({'case': cid, 'Ks': Ks, 'undo_dup': undo, 'edits': [{'old': o, 'new': n, 'why': 'lead'} for o, n in E],
               'note': 'lead: blocks %d/%d' % tuple(Ks) + ('; removes the leftover copy that group 4 duplicated' if undo else '')}, open('lead/%s.json' % cid, 'w', encoding='utf-8'), ensure_ascii=False)
# second round (after the readers): two more leftovers (c083 note 1651, c093 note 2111), and c097 accepted as read (the guard's
# match "Luke ix." was another reference, not a leftover: checked by the lead).
L2 = {
 'c083': ([463, 464], [
   (' 251 '+B+'[ἐν τ ερ, is inserted here (not in Homily XL.) by Chrysostom, but does not occur in any of our mss. of\n\n\n*[p. 456]*', ' 251\n\n\n*[p. 456]*'),
   ('1651 the New Testament. 1652', '1651 '+B+'[ἐν τ ερ, is inserted here (not in Homily XL.) by Chrysostom, but does not occur in any of our mss. of the New Testament. 1652')]),
 'c093': ([590, 591], [
   (' '+B+'[The singular is retained here by the translator, though the Greek form is the same, τν ορανν.—R.'+B+']\n\n\n*[p. 583]*', '\n\n\n*[p. 583]*'),
   ('2111 2112 Matt. xvi. 20.', '2111 '+B+'[The singular is retained here by the translator, though the Greek form is the same, τν ορανν.—R.'+B+'] 2112 Matt. xvi. 20.')]),
}
for cid, (Ks, E) in L2.items():
    json.dump({'case': cid, 'Ks': Ks, 'edits': [{'old': o, 'new': n, 'why': 'first note of the page: its text moved from the end of the block before'} for o, n in E],
               'note': 'lead: move across blocks %d/%d' % tuple(Ks)}, open('lead/%s.json' % cid, 'w', encoding='utf-8'), ensure_ascii=False)
r = json.load(open('read/c097.json', encoding='utf-8-sig')); r['guard_ok'] = True; r['note'] = 'lead: accepted as read; ' + r.get('note', '')
json.dump(r, open('lead/c097.json', 'w', encoding='utf-8'), ensure_ascii=False)
