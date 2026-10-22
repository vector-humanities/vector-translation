---
name: vt-pilot
description: Stage 2 of a vector translation. Translate a pilot section, get the translator to approve the readable register on a sample page, fix core terms against existing translations, settle every convention on the decision sheet, and start the glossary. Use after the source survey and before writing any batch brief.
---

# Pilot and conventions

Method §3 and §4; rules 4, 6, 11, 12.

## Steps
1. **Pilot section.** Translate the opening section yourself, from the images: literal first, sentence by sentence, then readable. Note every term and convention question as it arises.
2. **Register page.** Give the translator one page of the readable pilot. Ask them to revise it. The revised page, approved, is the register model for every brief; save it as `models/register-page.md`. A description of the register is no substitute.
3. **Core terms.** For each recurring technical term, list the renderings in every existing translation and quotation collected in the survey, and where translators disagree. Recommend one rendering per term, keeping apart terms the source keeps apart. The translator decides. Record each in `glossary.csv` with its competitors (the renderings to count for drift) and the date.
4. **Conventions.** Copy `templates/conventions.md` into the project and go through every row with the translator. Recommend an option for each, with the reason. Nothing is left open before the first batch.
5. **Layout.** Create `text/literal/`, `text/readable/`, `front/`, `back/`, `notes/`, `STATUS.md` (from the template) and the project `AGENTS.md` (from the template, conventions filled in). Put the pilot in as the first section files.
6. **Check.** Run `tools/vt_check.py` on the pilot files.

## Ask the translator
- the register page (revise and approve);
- each core term, as a short table with your recommendation;
- each convention, with your recommendation.
Log every answer in `STATUS.md` with the date.
