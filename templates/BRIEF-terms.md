# Brief: terminology pass, [term(s)], [range]

The translator has decided (date): [source term] = [English], [source term] = [English]. Earlier drafts used [old rendering] for both.

## Task
1. List every occurrence in your range, in both versions, of the candidate English words: [list].
2. For each, find the source word on the page image.
3. Change only what translates the term in question. Leave every other use of the English word as it is.
4. Where the new rendering clashes with another glossary term in the same sentence, propose a rewording and say why.

## Output (do not edit the translation files)
Write `changes-X.md`, appending as you go:

```
### readable | p. N
OLD: <exact text, unique in the file>
NEW: <replacement>
SRC: <the source word as printed>
```

Same for `### literal`. End with `## Clashes` and `## Summary` (counts per term, per version).
