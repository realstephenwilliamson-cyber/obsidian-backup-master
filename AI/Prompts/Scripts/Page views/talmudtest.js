const fs = require("fs"); const obs = require("./obs.js");
const amud = process.argv[2] ?? "";
const extra = { "Texts/Talmud/Talmud page.md": `---\namud: "${amud}"\ncssclasses:\n  - wide\n---\n` };
const o = obs(extra, { current: "Texts/Talmud/Talmud page.md", today: process.argv[3] || "2026-10-23" });
o.run(fs.readFileSync("/home/claude/view/talmud-page/view.js", "utf8")).then(() => {
  const c = o.container, q = s => [...c.querySelectorAll(s)];
  console.log("errors:", q(".vp-view-error").map(e => e.textContent));
  console.log("bar:", q(".tp-bar button").map(b => b.textContent + (b.disabled ? "(off)" : "")).join(" | "));
  console.log(require("./navprint.js")(c, "tp"));
  console.log("head:", q(".tp-head")[0] && q(".tp-head")[0].textContent, "| lines:", q(".tp-line").length);
}).catch(e => console.error("THROWN", e));
