# Builds the reference linker's Obsidian job from the pieces in this folder.
# python3 build.py <tag> <out.js>    e.g.  python3 build.py s70a-links-dry s70a-links-dry.js
# The job is dry unless window.B3APPLY === true when it runs (wrap it as in README.md to apply).
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
tag, out = sys.argv[1], sys.argv[2]
core = open(os.path.join(here, 'b3core.js'), encoding='utf-8').read().replace("if (typeof module !== 'undefined') module.exports = B3;\n", "")
vers = json.load(open(os.path.join(here, 'versif-eng.json')))
em = open(os.path.join(here, 'engmax.json')).read()
w = open(os.path.join(here, 'wrapper3.js'), encoding='utf-8').read()
job = ("(async () => {\n  // Reference linking (scripture, Zohar, Tantraloka, Avot); built from AI/Prompts/Scripts/Reference linker.\n"
       f"  const OUTTAG = '{tag}';\n  const VERSIF = " + json.dumps(vers, separators=(',', ':')) + ";\n  const ENGMAX = " + em + ";\n"
       + "\n".join("  " + l for l in core.split("\n")) + "\n" + w)
open(out, 'w', encoding='utf-8').write(job)
print('built', out, len(job))
