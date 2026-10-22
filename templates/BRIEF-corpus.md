# Brief: translation corpus, [source]

Source: [citation]. Held at: `corpus/texts/[file]` in the private repository, or [library]. Covers: [which works or passages].

You are building one source's part of the translation corpus for a translation of [author, title]. Read the source, find how it renders the terms below, and record what it does. Do not translate anything yourself and do not judge which rendering is right.

## Terms
| Source term | Notes for finding it |
|---|---|
| | |

Also record any other recurring term of the author's that the source renders in a marked way.

## Output (append each entry as you find it)
1. `corpus/terms-[source-id].csv`, columns `source_term,rendering,translator,work,year,language,page,context,note,source_id,url`:
   - `source_id`: this source's ID in `corpus/SOURCES.md`; `url`: a URL to the page (archive, publisher) or a DOI, where one exists, otherwise empty;
   - `context`: the rendering in its sentence, at most fifteen words, in quotation marks;
   - `note`: where the source gives the original word, explains its choice, or renders the same term two ways.
2. `corpus/style.md`, under a heading for this source: sentence length and joining; the author's punctuation (dashes, exclamations); compounds and coinages; emphasis; quotations and the original-language words kept; notes and brackets. One short example of each, with page.
3. `corpus/finds.md`, under a heading for this source: identifications of people, works and quotations; readings of difficult passages; points where the source disagrees with another translation or with the original; errors you can show. Each with page, and the evidence.

## Rules
- Quote at most fifteen words at a time. Never copy longer passages into any file.
- Give the source ID and a page for every entry, in every file, and a URL or DOI (with page) where one exists. If you cannot find a page, leave the entry out.
- Do not fabricate. If unsure whether a word renders the term, say so in `note`.
- End with `## Summary` in `finds.md`: entries recorded, terms not found in this source.
