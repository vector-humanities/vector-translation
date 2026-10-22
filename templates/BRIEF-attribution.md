# Brief: attribution pass, [range]

## Task
Check every factual claim in the translator's notes of your range: names, dates (birth, death, publication), identifications of persons, works and quotations, editions and page numbers.

For each, find a named source: the reference manager first, then an authority file (GND, VIAF, NDL, Library of Congress), a standard reference work, or the publisher's record. A search-result summary is not a source.

- **VERIFIED**: give the source.
- **CORRECTED**: give the source and the correction.
- **UNVERIFIED**: propose deleting the claim. Do not propose a hedge ("probably", "c.").

## Output (do not edit the translation files)
Write `attributions-X.md`, appending as you go:

```
### readable | [^label]
CLAIM: <the claim>
RESULT: VERIFIED | CORRECTED | UNVERIFIED
SOURCE: <named source, with page or URL>
OLD: <exact text>        (CORRECTED and UNVERIFIED only)
NEW: <replacement>
```

End with `## Summary` (counts by result).
