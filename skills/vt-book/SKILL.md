---
name: vt-book
description: Stage 7 of a vector translation. What the method requires of the typeset book: build it from the first merged chapter, rebuild after every merge, run a glyph sweep, offer the translator design samples, and follow the edition's own typography for covers. Use when setting up or rebuilding the book for a vector translation. The typesetting pipeline itself is a separate Vector Humanities tool.
---

# Book

Method §9; rule 18.

The typesetting pipeline (Markdown through Pandoc to Typst, with templates, covers and figure overlays, first built for the Kuki book) is being set up as its own Vector Humanities tool. Use it when it is available; until then, the Kuki project's build is the reference. This skill sets out what the translation method needs from any build.

## Requirements
1. **Build early.** Set up the build from the first merged chapter and rebuild after every merge, so that layout faults appear while there is little text: tables that cannot break across pages, notes inside captions, emphasis lost in conversion, missing glyphs.
2. **Glyph sweep.** Produce a test page setting every distinct non-ASCII character in the text once, build it, and check the PDF's fonts page by page for fallback or missing-glyph fonts (`pdffonts`). Fix the font stack before the full build.
3. **Design samples.** Offer the translator two or three sample spreads (title page, a text page with notes, a figure page, a glossary page). The translator chooses.
4. **Covers** may follow the typography of the edition translated. Do not reproduce a publisher's name the edition does not carry.
5. **Front matter** credits the image source as the library requires, and states that the translation is a vector translation, with the translator's name.
6. **Check** the built book after each rebuild: page count, notes count against the text, figures placed, no missing glyphs. Log in `STATUS.md`.
