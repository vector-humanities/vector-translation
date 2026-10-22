# Rules from practice

Each rule below comes from something that went wrong, or had to be corrected, in the first vector translation (Kuki Shūzō, *The Problem of Contingency*, October 2026). The incident is given so that the rule can be judged, and dropped if a new text makes it irrelevant.

## Source

**1. Translate from the images unless the OCR has been tested.**
The OCR of the pre-war vertical Japanese was unusable: 偶然 (contingency) came out as 借然, 必ず as 流す. It was kept for searching only. For a new script or typeface, test the OCR on a sample page against the image before deciding what it is good for.

**2. Survey every page before partitioning.**
The printed contents gave wrong section pages throughout, which cost three rounds of boundary corrections between parts. The author's own preface stood on an unnumbered page before the contents and was found only at the book-design stage. A contact sheet of every image in the first hour would have shown both.

**3. Set boundaries by headings, not page numbers.**
Headings fall partway down pages. Each part runs from its first heading to the next part's first heading; page numbers in a brief are approximate and say so.

## Terms and register

**4. Collect existing translations before the pilot, and fix the core terms against them.**
Two distinct Japanese terms (存在 and 有) were both rendered "being" for two chapters, the default of the English philosophical corpus. A specialist's draft of the opening section showed the distinction (existence and being). The correction then needed a terminology pass over the whole book, with every occurrence checked against the image.

**5. Count competing renderings after every merge.**
Drift is visible in counts before it is visible in reading. `vt_check.py --glossary` reports each glossary term's rendering and its listed competitors.

**6. Agree the register on a page, not a description.**
A list of style rules produced varied results across agents. One page revised by the translator and given as the model does better.

**7. The readable version adds nothing absent from the literal.**
The read-through of the whole book found 106 faults in the readable version. None reversed the argument; most were added inference words ("therefore" where the source has "and"), dropped hedges and moved emphasis. Glosses go in marked notes, insertions in marked brackets, and nothing else is added.

**8. Never drop the literal version, and make it the master.**
The literal version was skipped for one chapter to save time and had to be restarted. Every later correction to the readable text was found by comparing it with the literal.

**9. Run the read-through per part, as parts return.**
On the first run it came at the end, as a separate stage over the whole book. Run per part, it finds faults while the brief can still be corrected for the parts not yet drafted.

**10. Literal and readable versions from one agent are not independent.**
Both versions come from the same reading, so comparing them cannot catch a misreading they share. Hard passages (verse, classical quotation, logic notation) get two independent literal drafts and a third agent to compare them.

## Conventions

**11. Decide every convention once, before the first batch.**
On the first run the following changed mid-run, and each change needed retrofitting across finished parts: footnotes or inline glosses; the brackets for insertions; citation form; era dates; how verse and classical Chinese are presented. `templates/conventions.md` lists them.

**12. Mark everything the translator adds.**
Glosses had begun to sit unmarked or inline in the author's sentences. All translator's notes now carry a fixed prefix ("Tr."), and every insertion into the author's text stands in marked brackets (on the first run, 〔 〕, the Japanese editorial convention).

**13. Footnote labels unique per section, one definition each.**
Labels collided when parts were merged. Labels now carry chapter and section (`c3s8-4`), and the check counts definitions per marker.

## Agents and checks

**14. Delete an attribution that cannot be verified.**
Agents supplied names, dates and identifications in notes that could not be traced. The attribution pass checks each one against a named source or the reference manager; one that fails is deleted, not hedged, since a hedged date still lodges in the reader's head.

**15. Scripts check everyone, the coordinator included.**
A footnote-matching regular expression in one of the coordinator's own scripts ate newlines and merged note definitions into paragraphs; banned words entered through the coordinator's edits. The integrity checks run after every write, whoever made it.

**16. One change-list applier, with a dry run.**
Four ad hoc appliers grew up during the run. `tools/vt_apply.py` is the single one: it reports every match before writing and refuses an edit whose old text does not match exactly once.

**17. Persist as you go.**
Agents append each section to their output file on completion, so that an interrupted agent loses one section, not a part.

## Book and publication

**18. Build the book from the first merged chapter.**
Problems appeared late: tables that could not break overprinted the glossary page, notes inside captions were dropped, bold became italic, and characters were missing from the font stack. Each would have shown in a one-chapter build.

**19. Keep the private log out of the repository, and scan before every push.**
The first push of the Kuki repository included the private working log, email addresses and local paths. They were removed and the history rewritten. Correspondence and contacts stay in a private log outside the repository.

**20. Third-party scholarship stays out of public repositories.**
Copyrighted secondary material used for checking is kept privately and never committed to a public repository.
