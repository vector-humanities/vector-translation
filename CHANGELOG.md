# Changes

## 2026-11-27 (0.1.2)
- From the November work on Kuki: rules 22 to 26 (one English word per source term; read both versions against the page images after the checks; doubts on the full-resolution image and symbols by shape; notes from primary sources and printed editions, no hedges; edit the masters). Method §2 (positional reading by macOS Vision for search), §7 (pass 6, page reading), §8 (Translator's Preface, Translator's Note as the only discussion of the two versions, chronology, concordance only once checked), §9 (front matter in roman numerals, epigraph). Conventions rows 21 to 23. `vt_check.py --glossary` reports renderings shared by two source terms and counts renderings that differ only by case separately. Kuki case study brought up to date.

## 2026-11-05
- The readable version is renamed the translation, everywhere: `text/readable/` becomes `text/translation/`, the change-list target `readable` becomes `translation`, and brief part files `partX-readable.md` become `partX-translation.md`. The two versions are the translation and the literal version. `vt_apply.py` still accepts `readable` as a target, in change lists and in `--target`. Kuki's repository keeps its old names.
- Figures are listed in `figures/figures.csv` (`templates/figures.csv`; method §8), the form tools read for the bench and the book; captions stay in the translation, labels in `figures/overlays.json`.
