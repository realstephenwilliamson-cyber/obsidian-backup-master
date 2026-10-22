// The week's parashah for a homily: the Torah portion, Rashi on it, Mei HaShiloach (vol. I) and the Zohar notes
// named for it. Found from the note's `parashah` property: a link such as [[Torah 02 - Noach]], or a name such as
// "Noach" or "Parashat Noah". Used by Templates/Homily (Polyphonic).md:  await dv.view("Templates/Views/homily-parashah")
// Added 6 Oct 2026 (phase 1 of the October plan) in place of four links built from paths that did not exist.
const p = dv.current()?.parashah;
const base = v => String(v?.path ?? v ?? "").replace(/^\[\[|\]\]$/g, "").split("|")[0].split("/").pop().replace(/\.md$/, "").trim();
const raw = base(p);
// a spelling-tolerant key: "Lech Lecha" = "Lekh Lekha", "Chayei Sara" = "Hayyei Sarah", "Miketz" = "Mi-Qets", "Lech-Lecha" = "Lech Lecha"
const key = s => String(s).toLowerCase()
  .replace(/^.*?\b(parashat|parshat)\s+/, "").replace(/^torah \d+ - /, "")
  .replace(/[\s-]+le(kh|ch|k)a$/, "")
  .replace(/q/g, "k").replace(/kh/g, "h").replace(/ch/g, "h").replace(/tz/g, "ts").replace(/[^a-z]/g, "")
  .replace(/(.)\1+/g, "$1").replace(/[aeiou]/g, "").replace(/h$/, "");
if (!raw) {
  dv.paragraph("Set this note's *parashah* property (for example `[[Torah 02 - Noach]]` or `Noach`) to see the week's texts here.");
} else {
  const torah = dv.pages('"Texts/Bible/Torah"').where(x => x.parasha_number && /^Torah \d\d - /.test(x.file.name)
    && (x.file.name === raw || key(x.parasha) === key(raw))).first();
  if (!torah) {
    dv.paragraph(`No Torah portion found for "${raw}". Use the name as in Texts/Bible/Torah (for example "Lech Lecha"), or a link to the note.`);
  } else {
    const num = torah.parasha_number;
    const rashi = dv.pages('"Texts/Bible/Torah/Rashi"').where(x => x.parasha_number === num).first();
    const mei = dv.pages('"Texts/Chasidut/Mei HaShiloach"').where(x => x.torah && base(x.torah) === torah.file.name);
    const zohar = dv.pages('"Texts/Zohar"').where(x => /\b(Parashat|Parshat)\b/.test(x.file.name) && key(x.file.name) === key(torah.parasha))
      .sort(x => x.file.name, "asc");
    const none = "*no note for this parashah in the vault*";
    dv.list([
      `**Torah:** ${torah.file.link}${torah.range ? " (" + torah.range + ")" : ""}`,
      `**Rashi:** ${rashi ? rashi.file.link : none}`,
      `**Mei HaShiloach:** ${mei.length ? mei.map(x => x.file.link).join(" · ") : none}`,
      `**Zohar:** ${zohar.length ? zohar.map(x => x.file.link).join(" · ") : none}`,
    ]);
  }
}
