#!/usr/bin/env python3
"""Draw a random sample of proposed links and lay out what a checker needs:
the citing line, the reference and its composition, whether the target block
exists, and the target text right after the block (so the checker can judge
whether it plausibly holds the passage cited).

usage: selfcheck.py META CUR.json LINKS.json N SEED OUT.md

The verdicts are written by the person or agent reading OUT.md, not by this
script; it only gathers the evidence and lists shared names, verse
references and words between the citing line and the target excerpt.
"""
import json
import random
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zoharlink as Z  # noqa: E402

STOP = set("""the of and to in a is that it as for on with by this his he be are was or from at an which not
but their they them its one all who have has so into what there when then upon see also cf above below note
zohar rabbi said says because these those than other here where only even now such being come out about
you your our we us i me my our him her she will would should may can does do did been were had had""".split())


def target_excerpt(text, block, length=20000):
    """The folio side's own text.  The block id sits at the head of the printed
    page on which the folio begins; the folio itself runs from its inline
    marker ("\\[80a\\]") to the next inline folio marker, across page heads."""
    m = re.match(r"(z[123]|zh)-(\d+[a-d])", block)
    if not m:
        return None
    fol = m.group(2)
    bl = re.search(r"\^" + re.escape(block) + r"\s*$", text, re.M)
    if not bl:
        return None
    mm = re.compile(r"\\\[" + re.escape(fol) + r"\\\]").search(text, max(0, bl.start() - 3000))
    pos = mm.end() if mm and mm.start() < bl.start() + 6000 else bl.end()
    nxt = re.compile(r"\\\[\d{1,3}[a-d]\\\]|^\[\^", re.M)
    end = min(len(text), pos + length)
    for mm in nxt.finditer(text, pos):
        if re.search(re.escape(fol), mm.group(0)):
            continue
        end = mm.start()
        break
    return text[pos:end]


def words(s):
    return set(w.lower() for w in re.findall(r"[A-Za-z’'ʿ\-]{4,}", s)) - STOP


def main(argv):
    meta, cur_path, links_path, n, seed, out_md = argv[1:7]
    index = Z.Index(meta)
    cur = json.load(open(cur_path, encoding="utf-8"))
    links = json.load(open(links_path, encoding="utf-8"))
    random.seed(int(seed))
    sample = random.sample(range(len(links)), int(n))
    L = ["# Self-check sample (seed %s, %s of %d proposed links)\n" % (seed, n, len(links))]
    for k, idx in enumerate(sample, 1):
        r = links[idx]
        line = cur[r["path"]].split("\n")[r["line"] - 1]
        plain, _, _, _ = Z.plain_view(line)
        i = plain.find(r["label"])
        ctx = plain[max(0, i - 220):i] + "<<" + r["label"] + ">>" + plain[i + len(r["label"]):i + len(r["label"]) + 160]
        tpath = next((p for p in index.blocks if Z.Index.basename(p) == r["target"]), None)
        has_block = bool(tpath) and r["block"] in index.blocks[tpath]
        excerpt = target_excerpt(cur.get(tpath, ""), r["block"]) if tpath in cur else None
        shared = sorted(w for w in words(ctx) & words(excerpt or "") if not Z.holds_divine_name(w))
        verses = sorted(set(re.findall(r"[A-Z][a-z]+ \d+:\d+", ctx)) & set(re.findall(r"[A-Z][a-z]+ \d+:\d+", excerpt or "")))
        L.append("## %d. #%d %s L%d (%s)\n" % (k, idx, r["path"], r["line"], r["set"]))
        L.append("- reference: `%s` -> `[[%s#^%s|%s]]`; composition: %s; rule: %s" % (
            r["label"], r["target"], r["block"], r["label"], r["composition"] or "none", r["rule"]))
        L.append("- block present in target: %s%s" % (has_block, "" if tpath in cur else " (target text not in cur.json)"))
        if Z.holds_divine_name(line):
            L.append("- citing line: " + Z.hidden(r["path"], r["line"]))
        else:
            L.append("- citing line: `%s`" % ctx.replace("`", "'"))
        if excerpt:
            ex = excerpt.replace("`", "'").replace("\n", " ")[:700]
            if Z.holds_divine_name(ex):
                L.append("- the folio's text (%d chars): %s" % (len(excerpt), Z.hidden(tpath, 0).replace(" L0", ", the folio %s" % r["block"])))
            else:
                L.append("- the folio's text (first 700 chars of %d): `%s`" % (len(excerpt), ex))
        else:
            L.append("- the folio's text: (not available)")
        L.append("- shared names/words: %s; shared verses: %s" % (", ".join(shared[:12]) or "none", ", ".join(verses) or "none"))
        L.append("- verdict: ")
        L.append("")
    open(out_md, "w", encoding="utf-8").write("\n".join(L))
    print("wrote", out_md)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
