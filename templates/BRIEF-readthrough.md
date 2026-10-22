# Brief: read-through, readable against literal, [range]

Files: `[literal]` (the reference) and `[readable]`. Conventions as in `conventions.md`. Page images for disputes: `[path]`, mapping [formula].

## Task
Go paragraph by paragraph, aligning the versions by their `[p. N]` markers. Find places where the READABLE version:

1. **ADDS** a claim, example, name, date, qualification, contrast or interpretation absent from the literal: a gloss that belongs in a note; a reformulation that says more than the author; a contrast the author does not make; an inference word ("therefore", "thus") where the literal has a plain connective; a closing sentence that restates significance.
2. **DROPS** a sentence, clause, qualification, example, citation, page reference or emphasis present in the literal.
3. **CHANGES** a sense, a hedge, a modality, a term against the glossary, or the attribution of a view (the author's own against one the author reports).
4. Breaks a **RULE** of house style (the banned list in `AGENTS.md`).
5. Matches a **published translation** word for word over more than a phrase (flag as CHANGES with the source if known).

Joined sentences, reordered clauses and reformulations that restate the author without adding are the intended register: leave them. Do not propose stylistic preferences.

## Output (do not edit the translation files)
Write `fixes-X.md`, appending as you go:

```
### readable | p. N
OLD: <exact substring of the readable file, unique in the whole file (8 to 30 words)>
NEW: <corrected text, same register, minimal change>
WHY: <ADDS | DROPS | CHANGES | RULE: one line, citing the literal wording>
```

OLD must match character for character, including note markers, italics and page markers.

Then `## Literal problems` (page, issue, what the image shows) and `## Summary` (counts by type).
