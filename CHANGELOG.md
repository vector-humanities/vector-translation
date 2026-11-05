# Changes

## 2026-11-05
- The readable version is renamed the translation, everywhere: `text/readable/` becomes `text/translation/`, the change-list target `readable` becomes `translation`, and brief part files `partX-readable.md` become `partX-translation.md`. The two versions are the translation and the literal version. `vt_apply.py` still accepts `readable` as a target, in change lists and in `--target`. Kuki's repository keeps its old names.
- Figures are listed in `figures/figures.csv` (`templates/figures.csv`; method §8), the form tools read for the bench and the book; captions stay in the translation, labels in `figures/overlays.json`.
