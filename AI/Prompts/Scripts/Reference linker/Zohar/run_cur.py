#!/usr/bin/env python3
"""Run the Zohar reference linker over the current vault text and write the
proposal batch.

usage: run_cur.py META CUR.json OUTDIR

Reads CUR.json ({vault path: note text}) and writes to OUTDIR:
  proposals.json  {path: {"changes": [[line, oldLine, newLine], ...]}}
  links.json      one row per new link: path, line, set, label, target, block,
                  composition, rule   (set = A-outside-11 | B-vol11-left | B-zh-left)
  undecided.json  references the rule does not decide (path, line, text, why)
  noblock.json    references no note holds a block for (same shape)
  stephen.json    links that would fall in Stephen's own notes (Study/Concepts,
                  Study/Hubs, Notes): listed, not proposed
  counts.json     the counts used by report.md

Skipped altogether: AI/, Templates/, Journal/, Projects/ and the vault's own
index notes (see zoharlink.SKIP_NOTES).
"""
import json
import os
import sys
import collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zoharlink as Z  # noqa: E402

EXCLUDE_PREFIXES = ("AI/", "Templates/", "Journal/", "Projects/")
STEPHEN_PREFIXES = ("Study/Concepts/", "Study/Hubs/", "Notes/")


def which_set(path, block):
    if block.startswith("zh-"):
        return "B-zh-left"
    if "/Zohar 11 - " in path:
        return "B-vol11-left"
    return "A-outside-11"


def main(argv):
    meta, cur_path, outdir = argv[1:4]
    index = Z.Index(meta)
    cur = json.load(open(cur_path, encoding="utf-8"))
    os.makedirs(outdir, exist_ok=True)
    proposals, links, und, nob, steph = {}, [], [], [], []
    problems = []
    skipped = []
    c = collections.Counter()
    # label style per note, falling back to the note's folder (the book)
    folder_counts = collections.Counter()
    for path, text in cur.items():
        w, wo = Z.label_style_counts(text)
        folder = path.rsplit("/", 1)[0] if "/" in path else ""
        folder_counts[(folder, "intro")] += w
        folder_counts[(folder, "item")] += wo
    styles = {}
    for path, text in cur.items():
        s = Z.label_style(text)
        if s is None:
            folder = path.rsplit("/", 1)[0] if "/" in path else ""
            w, wo = folder_counts[(folder, "intro")], folder_counts[(folder, "item")]
            s = "intro" if w > wo else "item"
        styles[path] = s
    for path in sorted(cur):
        if path.startswith(EXCLUDE_PREFIXES) or path in Z.SKIP_NOTES:
            skipped.append(path)
            continue
        ch, lk, u, nb = Z.link_note(path, cur[path], index, style=styles[path])
        for r in lk:
            r["set"] = which_set(path, r["block"])
        if path.startswith(STEPHEN_PREFIXES):
            steph += lk
            continue
        for ln, old, new, edits in ch:
            probs = Z.check_proposal(old, new, index)
            for a, b, rep in edits:
                lab = rep.rsplit("|", 1)[-1][:-2].replace("\\|", "|")
                if old[a:b] != lab.replace("\\|", "|") and old[a:b] != lab:
                    probs.append("offset edit does not match its label at %d-%d" % (a, b))
            if probs:
                problems.append({"path": path, "line": ln, "problems": probs})
        if ch:
            plain, by_offset = Z.split_changes(ch)
            proposals[path] = {"changes": plain}
            if by_offset:
                proposals[path]["changes_by_offset"] = by_offset
                c["lines given by offset (divine name)"] += len(by_offset)
        links += lk
        und += u
        nob += nb
    for rows in (und, nob):
        for r in rows:
            r["set"] = which_set(r["path"], r["block"])
            r.pop("pstart", None)
    for r in links:
        r.pop("pstart", None)
        r.pop("text", None)
    # counts
    for r in links:
        c["links/" + r["set"]] += 1
        c["links/folder/" + top(r["path"])] += 1
        c["links/rule/" + r["rule"].split(";")[0].split(" (")[0]] += 1
    for r in und:
        c["undecided/" + r["set"]] += 1
    for r in nob:
        c["noblock/" + r["set"]] += 1
        if r.get("sole_holder"):
            c["noblock-with-sole-holder/" + r["set"]] += 1
    c["notes changed"] = len(proposals)
    c["lines changed"] = sum(len(v["changes"]) + len(v.get("changes_by_offset", [])) for v in proposals.values())
    c["stephen links"] = len(steph)
    c["notes skipped (AI, Templates, Journal, Projects, index notes)"] = len(skipped)
    c["proposals failing check"] = len(problems)
    dump = lambda name, obj: json.dump(obj, open(os.path.join(outdir, name), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    dump("proposals.json", proposals)
    dump("links.json", links)
    dump("undecided.json", und)
    dump("noblock.json", nob)
    dump("stephen.json", steph)
    dump("counts.json", {"counts": dict(sorted(c.items())), "problems": problems, "skipped": skipped})
    for k, v in sorted(c.items()):
        print("%6d  %s" % (v, k))
    return 0


def top(path):
    parts = path.split("/")
    if len(parts) == 1:
        return parts[0]
    if parts[0] == "Texts" and parts[1] == "Zohar" and len(parts) > 3:
        return "Texts/Zohar/" + parts[2]
    return "/".join(parts[:2])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
