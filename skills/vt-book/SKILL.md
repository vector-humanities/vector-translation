---
name: vt-book
description: Stage 7 of a vector translation. Hand the translation to Vector Book, the Vector Humanities book design tool, following its handover policy: write the book.toml manifest's translation tables, keep the text in the form Vector Book reads, build and check from the first merged chapter, run the design samples for the translator, and apply proof corrections. Use when setting up, rebuilding or proofing the book of a vector translation.
---

# Book

Method §9; rule 18. Tool: Vector Book (https://github.com/vector-humanities/vector-book), called by path. Policy: its `docs/handover.md`. Keys: its `docs/config.md`; text conventions: its `docs/conventions.md`.

## Set up
1. Copy `templates/book.toml` to the book folder root. Fill the translation tables only: `[book]` (title, subtitle, author, original title, credit line, affiliation, `credits` with edition, library and identifier, image credit, rights line, conventions note), `[sources]` (front, body = `text/readable/*.md`, back, glossary, overlays) and `[markers]` (page pattern; strip patterns for image numbers). Leave `[design]`, `[cover]`, `[back]` and `[frontispiece]` to the design side, with the starter's defaults.
2. Add `*/build/` (or `build/`) to the repository's `.gitignore`. Commit `book/`.
3. Write `HANDOVER.md` in the book folder for the design side: state of the text, what is provisional, questions. Make a `proof/` folder for corrections coming back.

## Text form
- At most one level-one heading per file: the file that opens a chapter or text starts `# Title {num="…" orig="…" run="…"}`; a file without one continues the chapter before it. Sections are `## N. Title`. A translator's note on a title goes on the heading (`# Title[^label] {…}`).
- Section breaks: a paragraph of `· · ·` or `* * *` alone; never `***` or `---`, which set only as a small space.
- Footnote labels unique across the book; `[p. N]` markers; figures as image line plus `**Figure N.**` caption with `Key:` or `Labels:`.

## Build
From the first merged chapter and after every merge:

```bash
path/to/vector-book/vbook check <book> --report
path/to/vector-book/vbook sweep <book>
```

`book/BUILD.md` must report notes set equal to notes defined, figures set equal to figures in the sources, and no missing glyphs. Send any fault to the design side; do not work round it in the text unless the fault is in the text.

## Design
`vbook samples <book>` sets the book in each template. The translator chooses; log the choice in `STATUS.md` and ask the design side to set `[design]`.

## Proof
Text faults go in `proof/` as change lists (method §7), applied with `tools/vt_apply.py` to the literal and readable masters together, then rebuild. Layout faults go to the design side.

## Gate
The book is final when the translator signs off the text in `STATUS.md` and `BUILD.md` reports no faults.
