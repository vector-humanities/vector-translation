---
name: vt-merge
description: Stage 4 of a vector translation. Take a returned part, extract its editor's notes, run the integrity checks (page markers, footnotes, banned words, glossary drift), write it into the section files, and start its read-through. Use whenever a translation sub-agent finishes a part.
---

# Merge and integrity checks

Method §6; rules 5, 9, 13, 15. Tools: `tools/vt_check.py`, `tools/vt_assemble.py`.

## For each returned part
1. **Back up** the section folders.
2. **Editor's notes.** Move the part's `#### Notes for the editor` into `notes/batch-N-notes.md` under the part's name. Collect from them: uncertain readings, misprints kept as printed, new terms, unverified attributions, heading positions.
3. **Check the part files** before writing anything:
   ```
   python3 tools/vt_check.py partX-literal.md --no-footnotes
   python3 tools/vt_check.py partX-readable.md --glossary glossary.csv
   ```
   Pages continuous within the part and joining the previous part; one definition per note marker, every translator's note with its prefix; no banned characters or words; glossary counts with competitors. Fix or send back what fails.
4. **New terms** raised by the agent go to the translator as a short table, with your recommendation. Add the decisions to `glossary.csv`.
5. **Write** the sections into `text/literal/` and `text/readable/`. Run the checks again on the assembled text:
   ```
   python3 tools/vt_assemble.py text/readable --front front --back back -o build/readable.md
   python3 tools/vt_check.py build/readable.md --glossary glossary.csv
   ```
6. **Read-through.** Launch a checker on this part now with `templates/BRIEF-readthrough.md` (stage 5).
7. **Log** in `STATUS.md`: part merged, checks passed, provenance row.
8. **Rebuild the book** if one exists (`vt-book`).

The checks apply to every write, including yours. A fault introduced by the coordinator is still a fault.
