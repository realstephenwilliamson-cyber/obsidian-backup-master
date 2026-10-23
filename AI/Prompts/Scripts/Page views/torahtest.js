const fs = require("fs");
const obs = require("./obs.js");
const ref = process.argv[2] ?? "", span = process.argv[3] ?? "";
const extra = { "Texts/Bible/Torah/Torah page.md": `---\nref: "${ref}"\nspan: ${span || '""'}\ncssclasses:\n  - wide\n---\n`,
  "Journal/2026/2026-10-22.md": "# x\n- question:: why does [[Torah 01 - Bereshit#^1-2|Gen 1:2]] put the spirit over the water?\n- [ ] question:: [[Torah 01 - Bereshit]] task\n- claim:: [[Isaiah 53#^53-4|Isa 53:4]] is read as the servant.\n" };
const o = obs(extra, { current: "Texts/Bible/Torah/Torah page.md", today: process.argv[4] || "2026-10-22" });
const code = fs.readFileSync("/home/claude/view/torah-page/view.js", "utf8");
const t0 = Date.now();
o.run(code).then(() => {
  const c = o.container, q = s => [...c.querySelectorAll(s)];
  fs.writeFileSync("torah-out.html", c.innerHTML);
  console.log("ms:", Date.now() - t0, "errors:", q(".vp-view-error").map(e => e.textContent));
  console.log("bar:", q(".tr-bar button").map(b => b.textContent + (b.disabled ? "(off)" : "") + "[" + b.getAttribute("aria-label") + "]").join(" | "), "input:", q(".tr-input")[0] && q(".tr-input")[0].getAttribute("value"));
  console.log(require("./navprint.js")(c, "tr"));
  console.log("notices:", q(".tr-notice").map(e => e.textContent));
  console.log("head:", q(".tr-head")[0] && q(".tr-head")[0].textContent);
  console.log("verses:", q(".tr-verse").length, "chapters:", q(".tr-chapter").map(e => e.textContent), "notes:", q(".tr-note").length);
  q(".tr-verse").slice(0, 3).forEach(e => console.log("  V:", e.textContent.slice(0, 150)));
  q(".tr-note").slice(0, 3).forEach(e => console.log("  N:", e.textContent.slice(0, 150)));
  console.log("compare:", q(".tr-compare")[0] && q(".tr-compare")[0].innerHTML);
  for (const s of ["tr-inner", "tr-left", "tr-outer", "tr-right"]) { const e = q("." + s)[0]; console.log("\n==", s, "\n" + (e ? [...e.children].map(x => "  [" + x.className + "] " + x.textContent.replace(/\s+/g, " ").slice(0, 260)).join("\n") : "-")); }
  console.log("\nfoot:", q(".tr-foot")[0] && q(".tr-foot")[0].textContent);
}).catch(e => console.error("THROWN", e));
