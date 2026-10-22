---
name: vt-check
description: Stage 5 of a vector translation. Run checking passes with parallel checker sub-agents that return change lists: read-through of readable against literal, terminology pass, attribution pass, external check against existing translations, and the concordance with the standard edition. Apply the change lists with the dry-run applier. Use after parts are merged, when a core term changes, or before the apparatus.
---

# Checking passes

Method §7; rules 4, 7, 9, 14, 16. Templates: `BRIEF-readthrough.md`, `BRIEF-terms.md`, `BRIEF-attribution.md`, `BRIEF-external.md`, `change-list.md`.

Checkers never edit the translation. They return change lists; you apply them.

## Passes
1. **Read-through** (per part, as parts return): readable against literal; ADDS, DROPS, CHANGES, RULE. Problems in the literal come back in a separate list; check them against the image yourself.
2. **Terminology** (whenever the translator changes a core term): every candidate English word checked against the image; only translations of that term change. Split the text into ranges across parallel checkers.
3. **Attribution** (before the apparatus is finished): every name, date and identification in the translator's notes checked against a named source. Unverified claims are deleted.
4. **External** (once): every passage quoted by existing translations or scholarship compared, starting from the corpus (`corpus/finds.md`, `corpus/terms.csv`); differences resolved against the image; attested alternatives recorded for the translation-choices appendix.
5. **Concordance** (once): pages of the printing translated paired with the standard edition from every page reference the literature gives with a quotation; anchors graded HIGH, MEDIUM, LOW; check that both page series increase together; a locating rule of thumb, labelled not for citation.

## Applying
```
python3 tools/vt_apply.py fixes-*.md --target readable=<file> --target literal=<file>
```
Read the dry run. Refused entries (no match or several) go back to the checker or are fixed by hand. Entries that would reverse a decision in `STATUS.md` go to the translator. Then `--write`, then `vt_check.py`, then log counts by type in `STATUS.md`.

## Disputes
Where a checker and the draft disagree on a reading, look at the image yourself. If it is still unclear, put it to the translator with the source text, both readings and your view.
