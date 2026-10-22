# Vector translation: the method

How to make a book-length translation from page images with a coordinating agent and parallel sub-agents, under a human translator's direction. The procedure was first used on Kuki Shūzō, 偶然性の問題 (*The Problem of Contingency*, 1935), in October 2026 ([case study](case-kuki.md)). This version folds in the changes that run showed were needed; [rules.md](rules.md) gives each rule with the incident behind it.

The translator directs. The agents draft, check and assemble. Every decision about terms, register, conventions and what goes into the book is the translator's, and each is logged with its date.

---

## 1. Roles

| Role | Who | Does | Does not |
|---|---|---|---|
| Translator | The human translator | Decides key terms, register, conventions, contents and design; reads samples against the source; approves downloads, publishing and anything sent outside | Draft every sentence |
| Coordinator | The main agent session | Surveys the source; writes briefs; partitions the text; launches sub-agents; applies their change lists; runs the integrity checks; keeps `STATUS.md`; reports to the translator | Let sub-agents edit the master files; settle a term or convention |
| Translators | Sub-agents, one per part | Read the page images; write a literal and a readable version of their range; record uncertain readings, misprints and new terms | Edit outside their part; depart from the glossary |
| Checkers | Sub-agents, one per range | Compare versions, check terms or attributions against the source; return exact change lists | Edit the master files |

The coordinator is the only process that writes to the master files. Every other agent returns a change list, applied with `tools/vt_apply.py`, which refuses any edit whose old text does not match exactly once.

## 2. Source survey

Skill: `vt-survey`. Record: `templates/survey.md`.

1. **Edition.** Identify the edition and printing, its date, and its rights status in the jurisdictions that matter (see the language notes: Japan was life plus 50 for authors who died before 1968; Germany and the UK are life plus 70; the US turns on the publication date). Record the editorial apparatus of any modern edition separately, since it can be in copyright when the text is not.
2. **Images.** Obtain page images at full resolution (IIIF where the library offers it). Use OCR as the source only where it has been shown to be reliable for this script and typeface; otherwise keep it for searching.
3. **Page mapping.** Work out and test the formula from image number to printed page. Put it in every brief.
4. **Every page.** Make a contact sheet of every image and page through all of it before partitioning. List front matter (including unnumbered pages), every heading with its real page, figures, tables, verse, the author's own notes, and blank pages. Do not trust the printed contents.
5. **Existing translations and quotations.** Collect complete, partial and draft translations, translations into other languages, and scholarship that quotes the text with page references. Identify the standard scholarly edition for the concordance. These become the first sources of the translation corpus (2a).

## 2a. Translation corpus

Skill: `vt-corpus`. Templates: `templates/corpus/`, `templates/BRIEF-corpus.md`. Tool: `tools/vt_corpus.py`.

Before the pilot, build a corpus of how this author, and the author's circle, have already been translated. It guides word choice, register and the glossary, and it is the project's reference for scholarly finds and for the reasons behind translation decisions.

1. **Sources.** Existing translations of the work, in any language; English translations of the author's other works; translations from the author's circle that share its vocabulary (correspondents, teachers, readers); English scholarship that quotes the author; translations of the sources the author quotes. List each in `corpus/SOURCES.md` with its citation from the reference manager, a URL, DOI or catalogue record, and its rights.
2. **Terms.** One sub-agent per source records every rendering of the author's recurring terms in `corpus/terms-<source>.csv`: source term, rendering, translator, work, page, a context of at most fifteen words, note, source ID and a URL or DOI (with page) where one exists. `vt_corpus.py` merges the tables and counts each term's renderings across sources.
3. **Style.** `corpus/style.md`: how other translators handle sentence length, the author's punctuation, compounds, emphasis, quotations and notes, with an example of each.
4. **Finds.** `corpus/finds.md`: identifications of people, works and quotations; readings of difficult passages; errors and disagreements in other translations; anything a translator's note, the Preface or the translation-choices appendix may cite. Every entry in the corpus, in every file, carries its source ID and page, and a URL or DOI where one exists, so that it can be checked against the original after the texts are removed; a translator's note drawing on the corpus cites the source in full.
5. **Use.** Attested renderings fill the glossary's `competitors` and `notes` columns, so drift is counted against real alternatives. The core terms (§3.3) are fixed against the corpus. The style note goes to the translator with the register page. Briefs give the glossary and the style note, never the corpus texts. The external check (§7.4), the attribution pass (§7.3), the translator's notes and Appendix A draw on `finds.md`.
6. **Limits.** The corpus records attested alternatives with their reasons; it does not supply defaults. The translator decides each term, and may depart from an established rendering where the author's usage calls for it. Full texts of copyrighted sources are kept in the translation's private repository (`corpus/texts/`), for the translator's research and checking, and never in a public repository or the book; the tables, notes and short contexts are what the translation and its apparatus draw on. When the translator signs off the translation as satisfactory, `corpus/texts/` is removed, from the repository's history as well as its files; everything made from them stays with the translation: the term tables, the quotations recorded with their pages, the style note, the finds, and the notes drawn from them. Removal needs two separate commands from the translator. After the first, the coordinator lists the files and commits affected and backs the repository up outside itself; only a second command, given after the translator has read that list, carries it out. One command, or a confirmation in the same message as the first, is not enough. The backup is deleted once the translator has checked the result. The read-through flags any passage of the readable version that matches a corpus translation over more than a phrase.

## 3. Pilot and conventions

Skill: `vt-pilot`. Decision sheet: `templates/conventions.md`. Glossary: `templates/glossary.csv`.

1. **Pilot section.** The coordinator translates the opening section itself, literally and readably, to learn the text.
2. **Register on a page.** The translator revises one page of the readable version. That page, approved, becomes the register model in every brief.
3. **Core terms.** Fix the ontological and technical vocabulary against the translation corpus (2a), recording each established rendering and where translators disagree. The translator decides.
4. **Conventions, once.** Settle every item on the decision sheet before the first batch: how translator's additions and notes are marked, the author's own notes, citation form, emphasis, verse and quotations in other languages, quotations of other authors, dates, numbers, spelling. Each change after the first batch costs a retrofit.
5. **Glossary file.** Start `glossary.csv`. Briefs, checks and the book's glossary all read from it.

## 4. Project layout

- One file per section in `text/literal/` and `text/readable/`, numbered in reading order. Front matter, appendices and glossary are separate files. `tools/vt_assemble.py` builds the two master files and the book input from them.
- The literal version is the master. The readable version may contain nothing absent from the literal except marked glosses and marked insertions.
- Page markers `[p. N]` where each printed page begins, so that every passage has a stable reference (page plus paragraph) for change lists, notes and concordance anchors.
- `STATUS.md` holds the edition, the decisions log, provenance (which agent drafted each section, which checks it passed) and costs per stage.

## 5. Brief and batches

Skill: `vt-brief`. Template: `templates/BRIEF-translate.md`.

1. **Partition by headings**, using the survey: about ten spreads per part, six to eight parts per batch. A part runs from its first heading to the next part's first heading, wherever on the page each falls.
2. **The brief** gives source access and the page mapping, the boundaries, the approved register page and literal model, the two outputs (literal first), the conventions, unique footnote labels, the banned constructions, the glossary extract and exact section titles, and the editor's notes each agent returns. Agents append each section to their files as they finish it.
3. **Hard passages** (verse, classical quotation, logic notation, dense terminology) get two independent literal drafts and a third agent to compare them.
4. **Launch the batch together** as background agents. Forward boundary reports to neighbouring parts at once.
5. **Mid-run changes** go in a dated `CHANGE` section at the end of the brief, and every running agent is messaged.

## 6. Merge and integrity checks

Skill: `vt-merge`. Tools: `tools/vt_check.py`, `tools/vt_assemble.py`.

As each part returns, the coordinator strips the editor's notes into one notes file, writes the sections into `text/`, and runs the checks before anything else touches them:

- page markers continuous and in order (a gap is a missing page, a duplicate an overlap), checked on the body text only (`--body-until '^#+ Appendix'`); passages quoted in the apparatus carry no page markers, since on the first run quotations in the concordance appendix kept theirs and showed as duplicates;
- every footnote marker has exactly one definition, and every translator's note carries the agreed prefix;
- no banned characters or words (the check applies to the coordinator's own edits too);
- competing renderings of each glossary term counted;
- headings in the expected order.

Then run a read-through of that part, readable against literal (7.2), while the next parts are still running. Take a backup before every merge or bulk change.

## 7. Checking passes

Skill: `vt-check`. Templates: `templates/BRIEF-readthrough.md`, `BRIEF-terms.md`, `BRIEF-attribution.md`, `BRIEF-external.md`, `change-list.md`.

Checkers work in parallel over ranges and return change lists in this form (every OLD must match its file exactly once; multi-line text in `~~~` fences):

```
### readable | p. 123
OLD: <exact text>
NEW: <replacement>
SRC: <the source wording>    (terms and external passes)
WHY: <reason>                (read-through and attribution passes)
```

1. **Terminology pass**, whenever a core term changes: every candidate word checked against the image; only what translates the term in question is changed.
2. **Read-through**, readable against literal, per part: ADDS, DROPS, CHANGES (sense, hedge, modality, attribution of a view) and RULE (house style). Problems in the literal go in a separate list.
3. **Attribution pass**: every name, date and identification in the translator's notes checked against a named source or the reference manager. What cannot be verified is deleted, not hedged.
4. **External check**: every passage quoted in existing translations or scholarship compared, differences resolved against the image, attested alternatives recorded in the translation-choices appendix.
5. **Concordance** with the standard edition, from every page reference the literature gives with a quotation; anchors graded HIGH, MEDIUM, LOW; a locating rule of thumb, labelled not for citation.

## 8. Apparatus

Skill: `vt-apparatus`. Template: `templates/facts-sheet.md`.

- **Preface** written from a sourced fact sheet: every fact tied to a source and page, a list of disagreements between sources, a list of what could not be sourced (kept out of the preface). The translator sets scope and length.
- **Translator's Note**, signed by the translator: status, method, conventions, debts.
- **Appendices**: notes on translation choices for other translators; contents of the printing with real section pages; concordance; index of persons and works (built from the literal with the translator's notes excluded, pages checked by script); glossary.
- **Figures**: found from the contact sheet, cropped at full resolution, a gentle contrast curve that keeps marks, a manifest with placement, caption and an English key. Measure label positions for any English overlays when the figures are first cropped.

## 9. Book

Skill: `vt-book`. Tool: [Vector Book](https://github.com/vector-humanities/vector-book), following its handover policy, `docs/handover.md`. Template: `templates/book.toml`.

- **The book folder is the handover.** Vector Book reads the project in place: `book.toml` at the root names the front, body (`text/readable/*.md`) and back files, the glossary and the figures. The translation side writes `[book]`, `[sources]` and `[markers]`; the design side writes `[design]`, `[cover]`, `[back]` and `[frontispiece]`. Vector Book never edits the text; it writes `book/` (the PDF and `BUILD.md`, committed) and `build/` (ignored).
- **Text form.** At most one level-one heading per file, on the file that opens a chapter, with its attributes (`# Title {num="…" orig="…" run="…"}`), and a file without one continues the chapter before it; section breaks as a paragraph of `· · ·` or `* * *` alone; footnote labels unique across the book; `[p. N]` markers; figures as an image line and a `**Figure N.**` caption with `Key:` or `Labels:` before any key.
- **Build early.** Build from the first merged chapter and after every merge (`vbook check <book> --report`), so that tables that cannot break, missing glyphs and lost notes appear while there is little text. `vbook sweep` checks every character against the font stack.
- **Design.** `vbook samples` sets the book in each template; the translator chooses, and the choice goes in `[design]` and in `STATUS.md`. Covers can follow the typography of the edition translated; do not reproduce a publisher's name the edition does not carry.
- **Returns.** When the book side finds a fault it sends a return, `proof/return-NN.md`, in the format of Vector Book's `docs/handover.md` (Returns; blank in `templates/return.md`). Each item has a kind (MARKUP, TEXT, QUERY, SOURCES, LAYOUT, OTHER), a location (file and line, the source page, the PDF page) and the evidence, and may propose a change list. The translation side answers every item in the same file (FIXED, CHANGED-OTHERWISE, QUERY-TO-TRANSLATOR, DECLINED, NOTED): MARKUP and SOURCES items are applied; TEXT items are checked against the literal and the source first; QUERY and OTHER items go to the translator. Proposed change lists are applied straight from the return file with `vt_apply.py`, literal and readable together. Then the post-design check, `vbook check --report`, a commit, Status ANSWERED, and a message to the book side, which rebuilds and closes or reopens each item.
- **Post-design check.** `tools/vt_bookcheck.py <book>` compares the typeset PDF with the translation's own text, independently of Vector Book: every word in order, every note, every heading, with each difference located by file and source page. It runs when the translator asks, before every return is marked ANSWERED, and before the book is signed off. Findings go to the book side as `proof/check-NN.md` (`--write`), in the return format, as LAYOUT items.
- **Gate.** The book is final when the translator signs off the text in `STATUS.md`, `BUILD.md` reports no faults, the post-design check has no open findings, and every return is CLOSED.

## 10. Evaluation

- **Sample review**: the translator reads one page per chapter against the image and logs errors by type. This measures the pipeline rather than assuming it.
- **Provenance and costs** in `STATUS.md`, kept as the run goes, so the method can be described exactly in the Translator's Note.

## 11. Checklist

- [ ] Edition, printing, rights and image source recorded
- [ ] Page mapping worked out and tested
- [ ] Contact sheet of every image; front matter, headings, figures, author's notes, blank pages listed
- [ ] Existing translations and quoting scholarship collected; standard edition identified
- [ ] Translation corpus built: sources listed, term tables merged, style note, finds
- [ ] Pilot section; register approved on a page; core terms fixed; conventions sheet signed off
- [ ] `glossary.csv` started; project layout created; `STATUS.md` started
- [ ] Brief written; parts partitioned by headings; hard passages assigned double drafts
- [ ] Batch launched; boundary reports forwarded
- [ ] Each part checked on return (pages, notes, banned words, terms) and read through
- [ ] Terminology, attribution and external passes applied; concordance built
- [ ] Book built from the first chapter, rebuilt after each merge; glyph sweep clean
- [ ] Fact sheet, Preface, Translator's Note, appendices, index, figures
- [ ] Sample review by the translator; provenance and costs recorded
- [ ] On the translator's sign-off: `corpus/texts/` removed, history included
