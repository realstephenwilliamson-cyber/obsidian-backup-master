#!/usr/bin/env python3
"""Validate zoharlink.py against the S2 batch of 26 Oct 2026.

Runs the linker over the pre-S2 note text (pre.json) and compares the links it
makes with the links S2 created from plain text (s2-patch-1.json).  Only new
links count: a link in S2's new line whose label was plain text in the old
line.  Sets: M1 = main-Zohar links in the 14 vol. 11 notes; J1-02 = Zohar
Hadash links in any note.

usage: validate_s2.py META PRE.json S2-PATCH.json OUT.md [OUT.json]
"""
import json
import re
import sys
import os
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zoharlink as Z  # noqa: E402


def s2_new_links(patch, pre):
    """(path, line) -> list of S2 new links with plain positions; also the
    lines whose plain text S2 changed (skipped)."""
    out = {}
    bad = []
    for path, v in patch.items():
        for ln, old, new in v["changes"]:
            po, lo, io = plain_links(old)
            pn, lnk, _ = plain_links(new)
            if po != pn:
                bad.append((path, ln))
                continue
            rows = []
            for st, en, tgt, lab in lnk:
                if not any(io[st:en]):
                    note, blk = tgt.split("#^", 1) if "#^" in tgt else (tgt, None)
                    rows.append({"pstart": st, "label": lab, "target": note, "block": blk})
            out[(path, ln)] = rows
    return out, bad


def plain_links(s):
    out, links, inlink = [], [], []
    i = 0
    for m in Z.LINK_RE.finditer(s):
        out.append(s[i:m.start()])
        inlink.extend([False] * (m.start() - i))
        lab = m.group(2) if m.group(2) is not None else m.group(1)
        st = sum(len(x) for x in out)
        out.append(lab)
        inlink.extend([True] * len(lab))
        links.append((st, st + len(lab), m.group(1), lab))
        i = m.end()
    out.append(s[i:])
    inlink.extend([False] * (len(s) - i))
    return "".join(out), links, inlink


def main(argv):
    meta, pre_path, patch_path, out_md = argv[1:5]
    out_json = argv[5] if len(argv) > 5 else None
    index = Z.Index(meta)
    pre = json.load(open(pre_path, encoding="utf-8"))
    patch = json.load(open(patch_path, encoding="utf-8"))
    s2, bad = s2_new_links(patch, pre)
    vol11 = lambda p: "/Zohar 11 - " in p

    # run the linker over every note of pre.json
    mine = {}        # (path, line) -> list of link rows
    und, nob = [], []
    for path in sorted(pre):
        ch, lk, u, nb = Z.link_note(path, pre[path], index)
        for r in lk:
            mine.setdefault((r["path"], r["line"]), []).append(r)
        und += u
        nob += nb

    def s2set(path, blk):
        if blk and blk.startswith("zh-"):
            return "J1-02"
        if vol11(path):
            return "M1"
        return "other"

    # ---- compare
    stats = collections.Counter()
    diffs = []       # same position, different target/label
    s2_only = []     # S2 linked, I did not
    mine_only = []   # I linked on an S2 line, S2 did not
    for key, rows in s2.items():
        path, ln = key
        myrows = {r["pstart"]: r for r in mine.get(key, [])}
        for r in rows:
            st = s2set(path, r["block"])
            if st == "other":
                stats["s2-other"] += 1
                continue
            stats["s2-" + st] += 1
            m = myrows.get(r["pstart"])
            if m is None:
                # maybe my label starts at the intro (intro style): look for a row covering
                m = next((x for x in mine.get(key, []) if x["pstart"] <= r["pstart"] < x["pstart"] + len(x["label"])), None)
            if m is None:
                # why not?  find my verdict for this reference
                why = "not parsed as a reference"
                for u in und:
                    if u["path"] == path and u["line"] == ln and u["pstart"] == r["pstart"]:
                        why = "undecided: " + u["why"]
                for u in nob:
                    if u["path"] == path and u["line"] == ln and u["pstart"] == r["pstart"]:
                        why = "noblock: " + u["why"]
                s2_only.append({"set": st, "path": path, "line": ln, "s2": r, "why": why})
                stats["s2only-" + st] += 1
            elif m["target"] == r["target"] and m["block"] == r["block"] and m["label"] == r["label"]:
                stats["same-" + st] += 1
                m["_matched"] = True
            else:
                diffs.append({"set": st, "path": path, "line": ln, "s2": r, "mine": m})
                stats["diff-" + st] += 1
                m["_matched"] = True
        for m in mine.get(key, []):
            if m.get("_matched"):
                continue
            st = s2set(path, m["block"])
            if st == "other":
                continue
            mine_only.append({"set": st, "path": path, "line": ln, "mine": m})
            stats["mineonly-" + st] += 1
    # my links on lines S2 did not touch (vol 11 main / zh anywhere)
    mine_offline = []
    for key, rows in mine.items():
        if key in s2:
            continue
        for m in rows:
            st = s2set(key[0], m["block"])
            if st == "other":
                continue
            mine_offline.append({"set": st, "path": key[0], "line": key[1], "mine": m})
            stats["mine-offline-" + st] += 1
    # my leftovers in kind
    my_und = [u for u in und if s2set(u["path"], u["block"]) != "other"]
    my_nob = [u for u in nob if s2set(u["path"], u["block"]) != "other"]

    def fmt_ctx(path, ln, pstart, width=70):
        raw = pre[path].split("\n")[ln - 1]
        if Z.holds_divine_name(raw):
            return Z.hidden(path, ln)
        plain, _, _, _ = Z.plain_view(raw)
        a = max(0, pstart - width)
        return plain[a:pstart] + "<<" + plain[pstart:pstart + 12] + ">>" + plain[pstart + 12:pstart + 12 + width]

    L = []
    L.append("# Validation of zoharlink.py against S2 (26 Oct 2026)\n")
    L.append("Linker run over pre.json (the %d notes as they were before S2); S2's new links read from s2-patch-1.json: a link in the new line whose label was plain in the old line.\n" % len(pre))
    L.append("Lines skipped because S2 changed their plain text (not new links; see report.md): %d\n" % len(bad))
    for p, ln in bad:
        L.append("- %s L%d" % (p, ln))
    L.append("\n## Counts\n")
    L.append("| set | S2 new links | identical | different | S2 only | linker only (on S2's lines) | linker only (lines S2 left) |")
    L.append("|---|---|---|---|---|---|---|")
    for st in ("M1", "J1-02"):
        L.append("| %s | %d | %d | %d | %d | %d | %d |" % (
            st, stats["s2-" + st], stats["same-" + st], stats["diff-" + st], stats["s2only-" + st],
            stats["mineonly-" + st], stats["mine-offline-" + st]))
    L.append("\nS2 new links outside both sets (main-Zohar links outside vol. 11, e.g. the Glossary/other notes): %d (not compared).\n" % stats["s2-other"])
    L.append("Linker leftovers on pre.json in the same scope: undecided %d (M1 %d, J1-02 %d), noblock %d (M1 %d, J1-02 %d).\n" % (
        len(my_und), sum(1 for u in my_und if not u["block"].startswith("zh-")), sum(1 for u in my_und if u["block"].startswith("zh-")),
        len(my_nob), sum(1 for u in my_nob if not u["block"].startswith("zh-")), sum(1 for u in my_nob if u["block"].startswith("zh-"))))

    L.append("\n## Differences (same reference, different link)\n")
    for d in diffs:
        L.append("- **%s** %s L%d: S2 `%s#^%s|%s`; linker `%s#^%s|%s` (%s). Context: `%s`" % (
            d["set"], d["path"].split("/")[-1], d["line"], d["s2"]["target"], d["s2"]["block"], d["s2"]["label"],
            d["mine"]["target"], d["mine"]["block"], d["mine"]["label"], d["mine"].get("rule"),
            fmt_ctx(d["path"], d["line"], d["s2"]["pstart"])))
    L.append("\n## S2 linked, linker did not\n")
    for d in s2_only:
        L.append("- **%s** %s L%d: S2 `%s#^%s|%s`; linker: %s. Context: `%s`" % (
            d["set"], d["path"].split("/")[-1], d["line"], d["s2"]["target"], d["s2"]["block"], d["s2"]["label"], d["why"],
            fmt_ctx(d["path"], d["line"], d["s2"]["pstart"])))
    L.append("\n## Linker linked on S2's lines, S2 did not\n")
    for d in mine_only:
        m = d["mine"]
        L.append("- **%s** %s L%d: `%s#^%s|%s` (%s). Context: `%s`" % (
            d["set"], d["path"].split("/")[-1], d["line"], m["target"], m["block"], m["label"], m.get("rule"),
            fmt_ctx(d["path"], d["line"], m["pstart"])))
    L.append("\n## Linker links on lines S2 did not change (same scope)\n")
    for d in mine_offline:
        m = d["mine"]
        L.append("- **%s** %s L%d: `%s#^%s|%s` (%s). Context: `%s`" % (
            d["set"], d["path"].split("/")[-1], d["line"], m["target"], m["block"], m["label"], m.get("rule"),
            fmt_ctx(d["path"], d["line"], m["pstart"])))
    open(out_md, "w", encoding="utf-8").write("\n".join(L) + "\n")
    if out_json:
        json.dump({"stats": dict(stats), "diffs": diffs, "s2_only": s2_only, "mine_only": mine_only,
                   "mine_offline": mine_offline, "my_undecided": my_und, "my_noblock": my_nob},
                  open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(dict(stats), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
