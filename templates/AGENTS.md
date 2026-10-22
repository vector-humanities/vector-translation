# Instructions for agents: [author, title]

This repository holds a vector translation of [author, title, edition]. Read this file, then `STATUS.md`, then the method (https://github.com/vector-humanities/vector-translation/blob/main/method/method.md) before changing anything.

## Ground rules
1. **The translator decides.** Terms, register, conventions and contents are the translator's decisions. Propose; do not settle them. Raise questions in an issue or in your report.
2. **Translate from the images.** Source: `source/[...]`. [OCR status.] Page mapping: [formula]. Section boundaries follow the headings on the page.
3. **Literal is the master.** Every change to the readable version must be supported by the literal, and the literal by the image. The readable version contains nothing absent from the literal except marked glosses and marked insertions. If you change one, check the other.
4. **Change lists for checks.** When checking rather than translating, return a change list (format below); do not edit. Only the coordinator writes to the master files.
5. **Never fabricate.** No invented citations, page numbers, dates or identifications. An attribution that cannot be verified against a named source is deleted, not hedged. Every note, find or record that depends on a source gives its citation and page, and a URL where one exists, so that it can be checked against the original.
6. **Check after every write.** Run `python3 tools/vt_check.py` on what you changed. Rebuild the book after changes and check for missing glyphs.
7. **Log.** A dated line in `STATUS.md` for any meaningful change.
8. **Nothing private in the repository.** No working log, correspondence, email addresses or local paths. Third-party copyrighted texts only in `corpus/texts/` of a private repository, for research and checking; never quoted at length in the translation or apparatus, never in a public repository; removed, history included, on the translator's sign-off and only after two separate commands (method §2a). Notes, quotations, tables and finds made from them stay with the translation.

## Text conventions
[From `conventions.md`: page markers, notes and prefix, the author's notes, insertions, emphasis, citations, quotations, verse, labels, figures.]

## Terminology (binding)
`glossary.csv` is binding. Before introducing a rendering for a term already there, use the glossary's. After any merge, count competing renderings (`vt_check.py --glossary glossary.csv`).

## Register and style (readable version)
- [Register, with a pointer to the approved sample page.] [Spelling.]
- No em or en dashes in running prose (number ranges such as pp. 7–35 are fine). Use commas or restructure.
- Do not use: *legible/legibility*; *honest/honesty* as filler; *load-bearing*; *gestures toward/at*; *the seam*; *quietly*; *substrate*; "the tension between X and Y" as filler; "not X but Y" framing of our own; "chosen, not found" and its variants.
- No aphoristic closers, chiasmus, "worse than" comparisons, or sentences that restate the significance of the one before. In notes, state the fact.
- These bans apply to the translator's English. Where the author's own sentence has the form (a "not merely ... but" in the source), translate it.

## Change list format
```
### readable | p. 123
OLD: <exact text, matching once>
NEW: <replacement>
SRC: <source wording>   (terms and external checks)
WHY: <reason>           (read-through and attribution checks)
```
Multi-line text in `~~~` fences. Apply with `tools/vt_apply.py` (dry run, then `--write`).
