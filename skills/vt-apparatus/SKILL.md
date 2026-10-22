---
name: vt-apparatus
description: Stage 6 of a vector translation. Build the scholarly apparatus: a sourced fact sheet and Preface, the Translator's Note, appendices (translation choices, contents of the printing, concordance, index of persons and works), the glossary, and the figures with captions and English keys. Use once the text is translated and checked.
---

# Apparatus

Method §8; rule 14. Template: `templates/facts-sheet.md`.

## Preface
1. A sub-agent compiles the fact sheet: every fact tied to a source and page, disagreements between sources listed, unsourced claims listed separately. The reference manager is the first source for citations.
2. The translator sets the Preface's scope and length.
3. Draft from the fact sheet only. Nothing from the "could not be sourced" list goes in.

## Translator's Note
Drafted for the translator to revise and sign: the text and printing; status (what has and has not been checked); the method in a paragraph; the conventions; debts to earlier translators and scholars. The translator's wording is final.

## Corpus
Translator's notes, the fact sheet and Appendix A draw on `corpus/finds.md` and the corpus tables, citing source and page.

## Appendices
- **A. Notes on translation choices**, for other translators: the core terms and why, attested alternatives from the corpus and the external check, conventions and their reasons, misprints kept.
- **B. Contents of the printing** with the real section pages (from the survey).
- **C. Concordance** with the standard edition (from `vt-check`).
- **D. Index of persons and works**, built by script from the literal with the translator's notes excluded; pages checked by script.
- **Glossary** from `glossary.csv`.

## Figures
A sub-agent finds every figure from the contact sheet, crops each at full resolution (IIIF region where available), applies a gentle contrast curve that keeps marks, and writes `figures/FIGURES.md`: figure number, page, crop region, placement in the text, draft caption, English key to the labels. Measure label positions for English overlays at this stage, at the book's type size. The author's own references to figures stay as written, with the figure number added in the insertion brackets. Credit the image source as the library requires.
