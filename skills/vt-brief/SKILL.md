---
name: vt-brief
description: Stage 3 of a vector translation. Partition the text by headings, write the shared translation brief, assign double drafts for hard passages, and launch a batch of parallel translation sub-agents. Use when the pilot and conventions are settled and parts are ready to be drafted.
---

# Brief and batches

Method §5; rules 2, 3, 10, 17. Template: `templates/BRIEF-translate.md`.

## Partition
- From the survey's heading list, cut parts of about ten spreads, six to eight parts per batch. A part runs from its first heading to the next part's first heading.
- Mark hard passages (verse, third-language quotation, logic or notation, dense terminology) for two independent literal drafts and a third comparing agent.

## Write the brief
Copy the template to `batches/N/BRIEF.md` and fill every bracket: source access, page mapping, the boundaries table, the register page and literal model, the conventions, footnote labels, the glossary extract for the range, exact section titles, the banned list from `AGENTS.md`, the editor's notes required. The brief must be complete without this conversation: a sub-agent reads only the brief and the files it names.

## Launch
- Launch all parts of the batch together as background sub-agents. Each prompt: "Read `batches/N/BRIEF.md` in full and follow it. You are part X." plus the part's first heading and approximate images.
- Tell each to append each section to its files on completion.
- Record in `STATUS.md`: batch, parts, start time.

## During the run
- Forward each boundary report to the neighbouring part at once.
- If a decision changes, append a dated `CHANGE` section to the brief and message every running agent. Resume finished agents with a message if their part is affected.
- As each part returns, go to `vt-merge` for that part.
