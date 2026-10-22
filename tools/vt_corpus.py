#!/usr/bin/env python3
"""Merge translation-corpus term tables and report each term's renderings.

    python3 tools/vt_corpus.py corpus/terms-*.csv -o corpus/terms.csv --report corpus/terms-report.md
    python3 tools/vt_corpus.py corpus/terms-*.csv --glossary glossary.csv

Each input has the columns of templates/corpus/terms.csv:
source_term,rendering,translator,work,year,language,page,context,note,source_id,url

Every entry needs a source ID and a page, so that it can be checked against
the original; the URL is reported when missing. The merged table drops exact duplicate rows. The report lists, for each source
term, every rendering with the number of entries and the works that use it.
With --glossary, it also shows the glossary's agreed rendering for the term and
the attested renderings not yet listed among its competitors. Contexts longer
than fifteen words are reported, since the corpus quotes no more than that.
Standard library only.
"""
import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

COLS = ["source_term", "rendering", "translator", "work", "year", "language", "page", "context", "note", "source_id", "url"]


def read(paths):
    rows, seen, problems = [], set(), []
    for p in paths:
        with open(p, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            missing = [c for c in ("source_term", "rendering", "work", "page") if c not in (r.fieldnames or [])]
            if missing:
                problems.append(f"{p}: missing columns {missing}")
                continue
            for i, row in enumerate(r, 2):
                row = {c: (row.get(c) or "").strip() for c in COLS}
                if not row["source_term"] or not row["rendering"]:
                    problems.append(f"{p}:{i}: empty term or rendering")
                    continue
                if not row["page"]:
                    problems.append(f"{p}:{i}: no page")
                if not row["source_id"]:
                    problems.append(f"{p}:{i}: no source ID")
                if not row["url"]:
                    problems.append(f"{p}:{i}: no URL (give one where it exists)")
                if len(row["context"].split()) > 15:
                    problems.append(f"{p}:{i}: context over fifteen words")
                key = tuple(row[c] for c in COLS)
                if key in seen:
                    continue
                seen.add(key)
                rows.append(row)
    return rows, problems


def glossary(path):
    g = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            comp = {c.strip().lower() for c in (r.get("competitors") or "").split(";") if c.strip()}
            g[(r.get("source") or "").strip()] = ((r.get("english") or "").strip(), comp)
    return g


def report(rows, gloss):
    by = defaultdict(lambda: defaultdict(list))
    for r in rows:
        by[r["source_term"]][r["rendering"]].append(r)
    out = ["# Translation corpus: renderings by term", ""]
    for term in sorted(by):
        out.append(f"## {term}")
        agreed, comp = gloss.get(term, ("", set())) if gloss else ("", set())
        if gloss:
            out.append(f"Glossary: {agreed or 'not yet in the glossary'}")
        for rend, rs in sorted(by[term].items(), key=lambda kv: -len(kv[1])):
            works = sorted({f"{r['work']} ({r['translator'] or 'n.n.'})" for r in rs})
            out.append(f"- **{rend}**: {len(rs)}; " + "; ".join(works))
        if gloss:
            new = [rd for rd in by[term] if rd.lower() != agreed.lower() and rd.lower() not in comp]
            if new:
                out.append(f"Attested, not in competitors: {'; '.join(sorted(new))}")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("tables", nargs="+")
    ap.add_argument("-o", "--out", help="merged terms.csv")
    ap.add_argument("--report", help="write the report here (default: print it)")
    ap.add_argument("--glossary", help="glossary.csv to compare with")
    args = ap.parse_args()

    rows, problems = read(args.tables)
    gloss = glossary(args.glossary) if args.glossary else None
    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            w.writerows(sorted(rows, key=lambda r: (r["source_term"], r["rendering"], r["work"], r["page"])))
        print(f"{args.out}: {len(rows)} rows from {len(args.tables)} tables")
    text = report(rows, gloss)
    if args.report:
        Path(args.report).write_text(text + "\n", encoding="utf-8")
        print(f"{args.report}: {len({r['source_term'] for r in rows})} terms")
    else:
        print(text)
    for p in problems:
        print(f"  CHECK {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
