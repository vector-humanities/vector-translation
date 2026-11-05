---
name: vt-check
description: Stage 5 of a vector translation. Run checking passes with parallel checker sub-agents that return change lists: internal passes (read-through of the translation against the literal, terminology, attribution, concordance) and witness checks from outside the agents (earlier translations, human readers of the source, the translator's sample review), recorded apart. Apply the change lists with the dry-run applier. Use after parts are merged, when a core term changes, or before the apparatus.
---

# Checking passes

Method §7; rules 4, 7, 9, 14, 16. Templates: `BRIEF-readthrough.md`, `BRIEF-terms.md`, `BRIEF-attribution.md`, `BRIEF-external.md`, `change-list.md`.

Checkers never edit the translation. They return change lists; you apply them.

Keep the two kinds of check apart. **Internal** checks are those the agents run on their own output (passes 1, 2, 3 and 5, the integrity checks, and second drafts of hard passages, marked "same model" or "other model"). **Witness** checks are readings from outside the agents' series: human readers with the source, earlier translations, and the translator's sample review. Every change-list entry carries `ORIGIN: internal` or `ORIGIN: witness <ID>`.

## Passes
1. **Read-through** (per part, as parts return): the translation against the literal; ADDS, DROPS, CHANGES, RULE. Problems in the literal come back in a separate list; check them against the image yourself.
2. **Terminology** (whenever the translator changes a core term): every candidate English word checked against the image; only translations of that term change. Split the text into ranges across parallel checkers.
3. **Attribution** (before the apparatus is finished): every name, date and identification in the translator's notes checked against a named source. Unverified claims are deleted.
4. **Witness checks**: one record per witness, `checks/witness-NN.md` from `templates/witness.md`, saying what the witness did not see. Earlier translations and quotations come from the corpus (`corpus/finds.md`, `corpus/terms.csv`), aligned by page; human readers of the source are named with what they read; the translator's sample review (method §10) is recorded the same way. Differences are resolved against the image; changes carry `ORIGIN: witness <ID>`; attested alternatives go to the translation-choices appendix. Name the witnesses for each section in the `Witnessed by` column of the provenance table in `STATUS.md`.
5. **Concordance** (once): pages of the printing translated paired with the standard edition from every page reference the literature gives with a quotation; anchors graded HIGH, MEDIUM, LOW; check that both page series increase together; a locating rule of thumb, labelled not for citation.

## Applying
```
python3 tools/vt_apply.py fixes-*.md --target translation=<file> --target literal=<file>
```
Read the dry run. Refused entries (no match or several) go back to the checker or are fixed by hand. Entries that would reverse a decision in `STATUS.md` go to the translator. Then `--write`, then `vt_check.py`, then log counts by type and by origin (the dry run and the write both report applied changes per origin) in `STATUS.md`.

## Disputes
Where a checker and the draft disagree on a reading, look at the image yourself. If it is still unclear, put it to the translator with the source text, both readings and your view.
