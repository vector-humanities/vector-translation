# Brief: [author, title], [range] (shared by all parts in this batch)

Read this brief in full before starting. Then read the models listed below.

## Source
- Page images: `[path]/page_NNN.jpg` (NNN = image number). [Single pages / two-page spreads; reading order.]
- Page mapping: [formula, tested].
- Crop and enlarge hard passages into your own scratch folder, then read the crop. [Command.]
- [Do not use the OCR / The OCR may be used as a draft, checked against the image.]

## Boundaries: headings, not page numbers
Your range runs from your first heading to the next part's first heading, wherever on the page each falls. The image ranges below are approximate; look a page or two either side to find the headings. Report where your first and last headings actually stand.

| Part | First heading | Approx. images | Files |
|---|---|---|---|
| A | | | `partA-literal.md`, `partA-readable.md` |

## Models
- Register: the approved sample page, `[path]`. Match it.
- Literal style: `[path, section]`.

## Two outputs, section by section, literal first
1. **Literal** (`partX-literal.md`): close, sentence by sentence, keeping the author's sentence boundaries. No glosses, no joining, no added names. Translator's notes inline as [form].
2. **Readable** (`partX-readable.md`): in the register of the model page. It contains only what the literal contains, except glosses in marked notes and insertions in marked brackets.

## Conventions (binding; from `conventions.md`)
- Page markers `[p. N]` exactly where page N begins, even mid-sentence.
- Translator's notes: [form, prefix]. Labels unique to your section: `[^cCsS-k]`. Definitions at the end of each section.
- The author's own notes: [form].
- Insertions: [brackets].
- Emphasis: [rule]. Citations: [rule]. Quotations of other authors: [rule]. Verse and third-language quotations: [rule].
- Give an attribution, date or identification in a note only if you can name its source; otherwise leave it out and list it in your editor's notes.

## Glossary (binding)
Use the renderings in `glossary.csv`. Extract for this range:

| Source | English |
|---|---|
| | |

If you meet a term that is not in the glossary and recurs, choose a rendering, use it throughout, and list it in your editor's notes.

Section titles (use exactly): [list].

Headings (both versions; the book is typeset from the readable files by Vector Book): a file that opens a chapter or a text starts with one level-one heading carrying its attributes, `# Title {num="Chapter 1" orig="Original title" run="Short running head"}`; sections within it are `## N. Title`. A file with no level-one heading continues the chapter before it, so later sections of a text carry only `##` headings. A translator's note on a title goes on the heading: `# Title[^label] {…}`. Section breaks are a paragraph of `· · ·` or `* * *` alone, never `***` or `---`.

## Banned (both versions)
[Paste the list from `AGENTS.md`: dashes, words, constructions.] No commentary of your own on how important or striking something is.

## Output
- Append each section to your files as soon as it is finished.
- End each file with `#### Notes for the editor`: exact positions of your first and last headings; uncertain readings (page, source text, your reading); apparent misprints, kept as printed; new terms fixed; unverified attributions; illegible text.
- Before finishing: run `python3 tools/vt_check.py` on both files and fix what it reports.
- Do not edit any other file.

## CHANGE log
Dated, binding changes made after launch go here. Each supersedes anything above it.
