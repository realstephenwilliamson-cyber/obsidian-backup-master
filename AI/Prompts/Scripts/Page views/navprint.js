module.exports = (c, pre) => { const q = s => [...c.querySelectorAll(s)];
  const d = q(`.${pre}-nav`)[0]; if (!d) return "NO NAV";
  return [`summary: ${d.querySelector("summary").textContent} open=${d.open}`, ...q(`.${pre}-nav-row`).map(r => `  [${(r.querySelector(`.${pre}-nav-label`) || {}).textContent}] ${[...r.querySelectorAll(`.${pre}-nav-item`)].map(i => (i.classList.contains("is-on") ? "*" : "") + i.textContent).join(" | ").slice(0, 400)}`)].join("\n"); };
