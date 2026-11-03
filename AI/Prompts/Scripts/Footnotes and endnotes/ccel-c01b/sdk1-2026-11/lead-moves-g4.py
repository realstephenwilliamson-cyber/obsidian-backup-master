import json
B = chr(92)
L = {
 'c065': ([298, 299], [
   (B+'[οτω is omitted; so the Vulgate.—R.'+B+'] '+B+'[πολιτεα.'+B+']\n\n\n*[p. 291]*', B+'[οτω is omitted; so the Vulgate.—R.'+B+']\n\n\n*[p. 291]*'),
   ('1020 1021 Confined', '1020 '+B+'[πολιτεα.'+B+'] 1021 Confined')]),
 'c067': ([341, 342], [
   ('1170 ὅσιον. φιλοσοφαν .\n\n\n*[p. 334]*', '1170 ὅσιον.\n\n\n*[p. 334]*'),
   ('1171 1172 [[Luke 09#^9-62|', '1171 φιλοσοφαν . 1172 [[Luke 09#^9-62|')]),
 'c075': ([387, 388], [
   ('1359 Matt. x. 4. κορυφαο.\n\n\n*[p. 380]*', '1359 Matt. x. 4.\n\n\n*[p. 380]*'),
   ('1360 1361 [[Acts 04#^4-13|', '1360 κορυφαο. 1361 [[Acts 04#^4-13|')]),
}
for cid, (Ks, E) in L.items():
    json.dump({'case': cid, 'Ks': Ks, 'edits': [{'old': o, 'new': n, 'why': 'first note of the page: its text moved from the end of the block before'} for o, n in E],
               'note': 'lead: move across blocks %d/%d, checked on the PDF text of both pages' % tuple(Ks)}, open('lead/%s.json' % cid, 'w', encoding='utf-8'), ensure_ascii=False)
