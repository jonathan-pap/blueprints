# PBIP file format — atomic task index

> Each task below loads ONE small file (≤2 KB). Pick by intent. Do not load this whole folder.

## Identify

- `what-is-pbip.md` — one-paragraph definition + folder shape
- `thick-vs-thin.md` — which kind do I have, how to tell
- `what-is-platform-file.md` — `.platform` file role and rules

## Convert

- `pbix-to-pbip.md` — Save As workflow in PBI Desktop
- `extract-pbix.md` — programmatic ZIP extraction (Python + bash)
- `pbix-encoding-table.md` — which file is UTF-8 vs UTF-16LE vs binary

## Modify

- `rename-table.md` — exact files to touch in cascade
- `rename-measure.md` — exact files to touch in cascade
- `rename-column.md` — exact files to touch in cascade
- `fork-project.md` — duplicate a project safely

## Verify

- `post-rename-checklist.md` — what to grep for after a rename
- `validate-utf8-no-bom.md` — one-line check + fix
