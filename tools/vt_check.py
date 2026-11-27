#!/usr/bin/env python3
"""Integrity checks for vector translation files.

Run after every merge and every bulk edit, whoever made it:

    python3 tools/vt_check.py text/translation.md --glossary glossary.csv
    python3 tools/vt_check.py text/literal.md --skip-pages 12 --no-footnotes

Checks:
  pages      [p. N] markers continuous and in order (gaps, duplicates, reversals)
  footnotes  every [^label] marker has exactly one definition, every definition
             is used, and every definition begins with the translator's prefix
  banned     em and en dashes (an en dash between digits is allowed) and the
             banned words and constructions (built-in list, extendable with --banned)
  glossary   for each glossary row, counts of the agreed English and of each
             listed competitor, to show drift; then any English rendering
             given for more than one source term. Renderings that differ only
             by case (Ground, ground) are reported as kept apart by case and
             counted case-sensitively, so a translation that marks a term with
             a capital must not open a sentence with the lower-case term.

Exit status 1 if pages, footnotes or banned report a fault. Glossary counts are
information only. Standard library only.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

PAGE = re.compile(r"\[p\.[ \t]*(\d+)\]")
MARK = re.compile(r"\[\^([^\]\s]+)\](?!:)")
DEF = re.compile(r"^\[\^([^\]\s]+)\]:[ \t]*(.*)$", re.M)

BANNED_WORDS = [
    r"\blegib\w*", r"\bhonest\w*", r"\bload-bearing\b", r"\bgestur\w* (?:toward|towards|at)\b",
    r"\bthe seams?\b", r"\bat the seams\b", r"\bquietly\b", r"\bsubstrate\b",
    r"\bthe tension between\b", r"\bchosen,? not found\b",
]
SOFT = [r"\bnot \w+(?: \w+)?, but\b", r"\bnot merely\b", r"\bworse than\b"]


def check_pages(text, skip):
    faults = []
    nums = [int(m.group(1)) for m in PAGE.finditer(text)]
    if not nums:
        return ["no [p. N] markers found"]
    seen = set()
    for a, b in zip(nums, nums[1:]):
        if b == a:
            faults.append(f"duplicate p. {b}")
        elif b < a:
            faults.append(f"p. {b} after p. {a}")
        else:
            missing = [n for n in range(a + 1, b) if n not in skip]
            if missing:
                faults.append(f"gap after p. {a}: missing {missing[0]}" + (f"-{missing[-1]}" if len(missing) > 1 else ""))
    for n in nums:
        if n in seen and f"duplicate p. {n}" not in faults:
            faults.append(f"p. {n} appears more than once")
        seen.add(n)
    return faults, (nums[0], nums[-1], len(nums))


def check_footnotes(text, prefix):
    faults = []
    defs = {}
    for m in DEF.finditer(text):
        defs.setdefault(m.group(1), []).append(m.group(2))
    body = DEF.sub("", text)
    marks = {}
    for m in MARK.finditer(body):
        marks[m.group(1)] = marks.get(m.group(1), 0) + 1
    for label, n in marks.items():
        if label not in defs:
            faults.append(f"[^{label}] has no definition")
        if n > 1:
            faults.append(f"[^{label}] marker used {n} times")
    for label, ds in defs.items():
        if len(ds) > 1:
            faults.append(f"[^{label}] defined {len(ds)} times")
        if label not in marks:
            faults.append(f"[^{label}] defined but never used")
        if prefix and not ds[0].startswith(prefix):
            faults.append(f"[^{label}] does not begin {prefix!r}")
    return faults, (len(marks), len(defs))


def check_banned(text, extra):
    faults, warnings = [], []
    for i, line in enumerate(text.splitlines(), 1):
        if "—" in line:
            faults.append(f"line {i}: em dash")
        for m in re.finditer("–", line):
            before, after = line[m.start() - 1:m.start()], line[m.end():m.end() + 1]
            if not (before.isdigit() and after.isdigit()):
                faults.append(f"line {i}: en dash outside a number range")
        for pat in BANNED_WORDS + extra:
            for m in re.finditer(pat, line, re.I):
                faults.append(f"line {i}: {m.group(0)!r}")
        for pat in SOFT:
            for m in re.finditer(pat, line, re.I):
                warnings.append(f"line {i}: {m.group(0)!r} (check)")
    return faults, warnings


def count(text, phrase, case=False):
    phrase = phrase.strip()
    if not phrase:
        return 0
    return len(re.findall(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text, 0 if case else re.I))


def renderings(eng):
    """The English renderings in a glossary cell: notes in brackets dropped,
    alternatives split on ';'."""
    eng = re.sub(r"\([^)]*\)", "", eng)
    return [e.strip() for e in eng.split(";") if e.strip()]


def read_glossary(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def cased(rows):
    """Lower-cased renderings that the glossary gives in more than one case."""
    forms = {}
    for r in rows:
        for e in renderings(r.get("english", "")):
            forms.setdefault(e.lower(), set()).add(e)
    return {k for k, v in forms.items() if len(v) > 1}


def glossary_report(text, rows):
    case = cased(rows)
    out = []
    for r in rows:
        eng = r.get("english", "")
        first = (renderings(eng) or [eng])[0]
        comp = [c for c in r.get("competitors", "").split(";") if c.strip()]
        out.append((r.get("source", ""), first, count(text, first, first.lower() in case),
                    [(c.strip(), count(text, c, c.strip().lower() in case)) for c in comp]))
    return out


def shared_renderings(rows):
    """English renderings given for more than one source term, and those kept
    apart only by case."""
    by = {}
    for r in rows:
        for e in renderings(r.get("english", "")):
            by.setdefault(e, []).append(r.get("source", ""))
    shared = {e: s for e, s in by.items() if len(set(s)) > 1}
    lower = {}
    for e, s in by.items():
        lower.setdefault(e.lower(), []).append((e, s))
    by_case = {k: v for k, v in lower.items() if len(v) > 1}
    return shared, by_case


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--skip-pages", default="", help="comma-separated pages known to be blank or absent")
    ap.add_argument("--prefix", default="Tr.", help="translator's note prefix ('' to skip the check)")
    ap.add_argument("--no-pages", action="store_true")
    ap.add_argument("--no-footnotes", action="store_true")
    ap.add_argument("--banned", action="append", default=[], help="extra regular expression to ban (repeatable)")
    ap.add_argument("--glossary", help="glossary.csv with columns source,reading,english,competitors,...")
    ap.add_argument("--body-from", help="regular expression for the line where the body text starts (page check only)")
    ap.add_argument("--body-until", help="regular expression for the first line after the body text, e.g. '^# Appendix' (page check only)")
    args = ap.parse_args()
    skip = {int(x) for x in args.skip_pages.split(",") if x.strip()}

    bad = False
    for fp in args.files:
        text = Path(fp).read_text(encoding="utf-8")
        print(f"== {fp}")
        if not args.no_pages:
            body = text
            if args.body_from:
                m = re.search(args.body_from, body, re.M)
                body = body[m.start():] if m else body
            if args.body_until:
                m = re.search(args.body_until, body, re.M)
                body = body[:m.start()] if m else body
            res = check_pages(body, skip)
            if isinstance(res, list):
                faults, info = res, None
            else:
                faults, info = res
            if info:
                print(f"pages: p. {info[0]} to p. {info[1]}, {info[2]} markers")
            for f in faults:
                print(f"  PAGE  {f}")
            bad |= bool(faults)
        if not args.no_footnotes:
            faults, (nm, nd) = check_footnotes(text, args.prefix)
            print(f"footnotes: {nm} markers, {nd} definitions")
            for f in faults:
                print(f"  NOTE  {f}")
            bad |= bool(faults)
        faults, warnings = check_banned(text, args.banned)
        print(f"banned: {len(faults)} faults, {len(warnings)} to check")
        for f in faults:
            print(f"  BAN   {f}")
        for w in warnings:
            print(f"  WARN  {w}")
        bad |= bool(faults)
        if args.glossary:
            rows = read_glossary(args.glossary)
            print("glossary: agreed rendering, then competitors")
            for src, eng, n, comp in glossary_report(text, rows):
                extra = ", ".join(f"{c} {k}" for c, k in comp if k)
                print(f"  {src}  {eng} {n}" + (f"  | {extra}" if extra else ""))
            shared, by_case = shared_renderings(rows)
            for e, srcs in sorted(shared.items()):
                print(f"  SHARED  {e!r} renders {', '.join(sorted(set(srcs)))}")
            for k, forms in sorted(by_case.items()):
                print("  CASE    " + "; ".join(f"{e!r} {', '.join(s)}" for e, s in forms) + " (counted case-sensitively)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
