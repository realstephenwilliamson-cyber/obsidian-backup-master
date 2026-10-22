---
type: prompt
updated: 2026-10-05
---
# Sync and size check

> **Retired 21 Oct 2026**: the size figures are in the [[Monthly check-up]]'s report, and its follow-up prompt does the Sync-plan comparison on request. Kept in `AI/Archive/`.

**Use when:** before turning Obsidian Sync back on, before adding a large batch of files, or if Sync warns about storage.

**Before you start:** in a new Cowork task, connect the vault folder. It only reads; any change it suggests is yours to make in Obsidian's settings.

````text
Check my Obsidian vault (C:\Vaults\Obsidian Vault) against my Obsidian Sync plan and tell me what to set. This is read-only.

FIRST read, in the vault:
- AI/Prompts/House rules for AI work.md
- Vault Guide.md → Sync and backups

1. Measure the vault's size from the files themselves:
   - totals by type (PDF, DjVu, .txt, audio, images, Markdown, other) and by top folder;
   - the 25 largest files;
   - files over 200 MB, the Plus per-file limit, and files over 5 MB, the Standard limit;
   - the size of .trash, .work, .smart-env and other hidden folders. These don't sync (the .obsidian settings folder can, depending on Sync settings), but they take disk space.
2. Look up Obsidian's current Sync plan limits on obsidian.md (storage, per-file size, version history) and cite the pages. Don't rely on the Guide's figures if the site says otherwise. I'm on Sync Plus.
3. Work out:
   - what the remote vault will hold if I sync everything now;
   - the headroom left for version history. Sync keeps older versions of notes for 12 months and of attachments for two weeks (obsidian.md/help/Obsidian+Sync/Version+history), so a re-uploaded PDF counts twice for about two weeks;
   - what each option saves: turning off PDFs, audio or "other types" (the .txt e-texts and .docx originals) in Selective sync, or excluding a folder.
4. Recommend settings in plain steps: which Selective sync toggles, which folders to exclude, and whether to wait for old attachment versions to expire, or to use a purge option if Sync offers one. Check the current help pages for both and give me the menu path.

Report a short table of the sizes and one clear recommendation with the numbers behind it. Do not change any Obsidian setting yourself.
````

**Afterwards:** make the changes in Settings → Sync, then let the first sync finish on the laptop before opening the vault on the phone.
