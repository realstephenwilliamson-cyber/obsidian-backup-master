const fs = require("fs");
const obs = require("./obs.js");
const ref = process.argv[2] ?? "", tr = process.argv[3] ?? "", greek = process.argv[4] === "1";
const extra = { "Texts/Bible/New Testament/New Testament page.md": `---\nref: "${ref}"\ntranslation: ${tr || "bsb"}\n${greek ? "greek: true\n" : ""}cssclasses:\n  - wide\n---\n`,
  "Journal/2026/2026-10-22.md": "# x\n- question:: who are [[Matthew 05#^5-3|the poor in spirit]]?\n- claim:: [[NRSVue Matthew 05#^5-5|Mt 5:5]] quotes Ps 37.\n- see [[Matthew 05#^5-9|peacemakers]]\n" };
const o = obs(extra, { current: "Texts/Bible/New Testament/New Testament page.md" });
const code = fs.readFileSync("/home/claude/view/nt-page/view.js", "utf8");
const t0 = Date.now();
o.run(code).then(() => {
  const c = o.container, q = s => [...c.querySelectorAll(s)];
  fs.writeFileSync("nt-out.html", c.innerHTML);
  console.log("ms:", Date.now() - t0, "errors:", q(".vp-view-error").map(e => e.textContent));
  console.log("bar:", q(".nt-bar button").map(b => b.textContent + (b.disabled ? "(off)" : "") + (b.className ? "{" + b.className + "}" : "") + "[" + b.getAttribute("aria-label") + "]").join(" | "), "input:", q(".nt-input")[0] && q(".nt-input")[0].getAttribute("value"));
  console.log(require("./navprint.js")(c, "nt"));
  console.log("notices:", q(".nt-notice").map(e => e.textContent));
  console.log("head:", q(".nt-head")[0] && q(".nt-head")[0].textContent);
  console.log("verses:", q(".nt-verse").length, "headings:", q(".nt-heading").map(e => e.textContent), "notes:", q(".nt-note").length);
  q(".nt-verse").slice(0, 3).forEach(e => console.log("  V:", e.innerHTML.slice(0, 700)));
  q(".nt-note").slice(0, 3).forEach(e => console.log("  N:", e.textContent.slice(0, 150)));
  console.log("compare:", q(".nt-compare")[0] && q(".nt-compare")[0].textContent);
  for (const s of ["nt-inner", "nt-left", "nt-outer", "nt-right"]) { const e = q("." + s)[0]; console.log("\n==", s, "\n" + (e ? [...e.children].map(x => "  [" + x.className + "] " + x.textContent.replace(/\s+/g, " ").slice(0, 300)).join("\n") : "-")); }
  console.log("\nfoot:", q(".nt-foot")[0] && q(".nt-foot")[0].textContent);
}).catch(e => console.error("THROWN", e));
