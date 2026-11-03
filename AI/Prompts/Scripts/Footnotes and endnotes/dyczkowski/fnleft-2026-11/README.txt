fnleft-2026-11 scripts (3 Nov 2026, cloud chat; SDK 3 parts 1, 3 and 4). They ran in a Claude cloud workspace with the PDFs
staged under /mnt/user-data/uploads/Obsidian Vault/...; adapt the paths (P in tl.py, V in the others). Need PyMuPDF and Pillow.
Data and results: .work/edits/fnleft-2026-11/ (README.txt there).

Footnote starts read from strips (part 1, the leading \[illegible\]):
  tl.py        loads full.json (SDK 3's index: each item's PDF page or pages) and opens the volumes.
  sig.py       for one item: finds the line where the footnote's first words begin in the PDF text layer (exact, then
               diacritic-folded, longer keys until one line matches) and returns the tokens before them on that visual line.
  runsig.py    runs sig.py over all items -> sig.json; prints how it agrees with readings already made.
  strips.py    renders, for the items still to read, a 200 dpi strip around that line (two lines above), ten to a sheet with
               the item id above each; items the layer cannot place get the lower 60 % of the page -> sheets/, tasks.json.
  reader-brief-strips.txt   the readers' brief (two blind readers per item; copy what is printed between number and words).
  merge.py     two readers + the signal -> decisions.json, and a list of items for the lead to read on the page.
  look.py      renders a wider strip for given item ids, for the lead's own look.

Short spots on the page (parts 3 and 4: verse ranges, Sanskrit verse-end marks):
  p34_find.py, p34_items.py   find each garble in the notes and write a question per spot (words before it) -> items.json
  p34_render.py               a strip around the spot (text-layer match), or the whole page when the match fails
  spot-reader-brief.txt       the readers' brief.
Lesson (3 Nov): a strip or page found by a few words can show the wrong line (a verse ending in the same word); when two readers
agree but the text layer disagrees, look at the page.
