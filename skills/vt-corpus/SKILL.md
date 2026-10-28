---
name: vt-corpus
description: Stage 1a of a vector translation. Build a translation corpus before the pilot, from existing translations of the work, translations of the author's other works and circle, and scholarship quoting the author. Produces term tables merged with vt_corpus.py, a style note and a file of scholarly finds, which guide the glossary and register and serve as the reference for translation decisions, notes and the translation-choices appendix. Use after the source survey, and whenever a new source turns up.
---

# Translation corpus

Method §2a; rule 4a. Templates: `templates/corpus/`, `templates/BRIEF-corpus.md`. Tool: `tools/vt_corpus.py`.

## Steps
1. **List sources** in `corpus/SOURCES.md` (copy the template). Search the reference manager first, then catalogues and the web, for:
   - translations of the work, complete, partial or draft, in any language;
   - English translations of the author's other works;
   - English translations from the author's circle that share its vocabulary (correspondents, teachers, readers, opponents);
   - English scholarship that quotes the author, with page references;
   - translations of the authors the work quotes.
   Record for each: citation (from the reference manager; if a source is not there, say so), a URL, DOI or catalogue record, what it covers, where the text is held, rights. Every corpus entry cites a source ID and page, and a URL or DOI (with page) where one exists; entries without them are not used.
2. **Obtain texts.** Ask the translator before any download or purchase, naming the source and size. Full texts go in `corpus/texts/` in the translation's private repository, for research and checking; never in a public repository. They are removed, history included, when the translator signs off the translation, and only on two separate commands: after the first, list the files and commits affected and back the repository up outside itself; act only on a second command given after the translator has read the list. Delete the backup once the translator has checked the result. Only the full texts go: everything made from them stays with the translation: the term tables, the quotations recorded with their pages, the style note, the finds, and the notes drawn from them.
3. **Term list.** From the pilot and the survey, list the author's recurring terms (start with the candidates in the pilot notes). Put the list in the corpus brief.
4. **Launch** one sub-agent per source with `templates/BRIEF-corpus.md`. Each writes its own files, `corpus/terms-<ID>.csv`, `corpus/style/<ID>.md` and `corpus/finds/<ID>.md` (never a shared file, since agents run in parallel), and persists each entry as it goes. Group related short sources into one agent; run about five agents at a time.
5. **Merge.** `python3 tools/vt_corpus.py corpus/terms-*.csv -o corpus/terms.csv --report corpus/terms-report.md`. The report lists, for each source term, its renderings with counts and sources. Then assemble `style.md` and `finds.md` from the per-source files, and write `CORE-TERMS.md`: for each core term, the renderings in translations of the author kept apart from the same words in other authors.
6. **To the translator.** For each core term: the attested renderings, who uses which, and a recommendation with its reason. Also the style note, with the register page. The translator decides; record the decisions in `glossary.csv` with the attested alternatives in `competitors` and the reasons in `notes`.

## Uses later
- Briefs give the glossary and the style note, never corpus texts.
- The read-through flags passages of the readable version that match a corpus translation over more than a phrase.
- The external check and the attribution pass start from `finds.md`.
- Translator's notes may cite a precedent ("as in X's translation, p. N"); Appendix A records the alternatives and why they were not taken.
- New sources found later are added the same way, and the merge rerun.

## Limits
The corpus records alternatives; it does not supply defaults. An established rendering can be wrong for this author, and the translator may depart from it. Contexts in the tables are at most fifteen words. Nothing in the corpus is reproduced at length in the translation or its apparatus.
