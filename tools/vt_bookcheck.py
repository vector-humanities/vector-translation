#!/usr/bin/env python3
"""Post-design check: compare the typeset book with the translation's own text.

    python3 tools/vt_bookcheck.py <book>                      # report to stdout
    python3 tools/vt_bookcheck.py <book> --write              # also write <book>/proof/check-NN.md

Reads <book>/book.toml (the Vector Book manifest) for the source files, in the
order Vector Book sets them, and for the PDF. Extracts the PDF's text with
pdftotext (poppler) and checks, independently of Vector Book:

  body       every word of the text appears in the book, in order; runs of
             missing or changed words are reported with file and source page
  notes      every translator's note appears in the book
  headings   every heading appears

Running heads, margin numbers, note numbers and other furniture show up as
extra words in the book and are ignored. Hyphens, ligatures, quotation marks,
case and emphasis are normalised before comparing, so a word broken across a
line end matches. Findings are written in the return format (vector-book
docs/handover.md, Returns), as LAYOUT items addressed to the book side.
Standard library only; needs pdftotext on the PATH.
"""
import argparse
import datetime
import difflib
import glob
import re
import subprocess
import sys
import tomllib
import unicodedata
from pathlib import Path

WORKING = re.compile(r"<!-- working -->.*?<!-- /working -->", re.S)
COMMENT = re.compile(r"<!--.*?-->", re.S)
NOTEDEF = re.compile(r"^\[\^([^\]\s]+)\]:[ \t]*(.*(?:\n(?:[ \t]+.*|))*)", re.M)
NOTEREF = re.compile(r"\[\^[^\]\s]+\]")
ATTRS = re.compile(r"\{[^{}]*=[^{}]*\}")
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def norm_words(text):
    text = unicodedata.normalize("NFKC", text).replace("*", "")
    text = re.sub("[-­‐‑][ \t]*\n[ \t]*", "", text)   # word broken at a line end
    text = re.sub("[-­‐‑]", "", text)
    text = re.sub("[‘’‚‛′']", "", text)
    return re.findall(r"[^\W\d_]+|\d+", text.lower())   # digits apart, so note numbers do not stick to words


def source_files(root, cfg):
    s = cfg.get("sources", {})
    files = []
    for group in ("front", "body", "back"):
        pats = s.get(group, ["text/*.md"] if group == "body" else [])
        for pat in pats:
            files += [Path(p) for p in sorted(glob.glob(str(root / pat)))]
    return files


def tokens_with_pages(files, page_re, strip_res):
    """Body words with (file, page) for each, plus notes and headings."""
    words, where, notes, heads = [], [], [], []
    for f in files:
        t = WORKING.sub("", f.read_text(encoding="utf-8"))
        t = COMMENT.sub("", t)
        for m in NOTEDEF.finditer(t):
            notes.append((f, m.group(1), m.group(2)))
        t = NOTEDEF.sub("", t)
        for r in strip_res:
            t = re.sub(r, " ", t)
        t = NOTEREF.sub("", t)
        t = IMAGE.sub(" ", t)
        t = LINK.sub(r"\1", t)
        t = ATTRS.sub("", t)
        page = None
        for line in t.splitlines():
            if line.lstrip().startswith("#"):
                h = line.lstrip("# ").strip()
                if h:
                    heads.append((f, page, h))
            parts = re.split(page_re, line)
            # re.split with one group gives text, number, text, number, ...
            for k, part in enumerate(parts):
                if k % 2 == 1:
                    page = part
                    continue
                part = part.lstrip("#|> ")
                for w in norm_words(part):
                    words.append(w)
                    where.append((f, page))
    return words, where, notes, heads


def pdf_words(pdf):
    try:
        out = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("pdftotext not found (poppler)")
    return norm_words(out)


def contains(hay, needle):
    if not needle:
        return True
    n = len(needle)
    first = needle[0]
    for i in range(len(hay) - n + 1):
        if hay[i] == first and hay[i:i + n] == needle:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("book", help="book folder with book.toml")
    ap.add_argument("--pdf", help="PDF to check (default: [book] output in book.toml)")
    ap.add_argument("--write", action="store_true", help="write proof/check-NN.md in the book folder")
    ap.add_argument("--context", type=int, default=6, help="words of context around each finding")
    args = ap.parse_args()

    root = Path(args.book)
    cfg = tomllib.loads((root / "book.toml").read_text(encoding="utf-8"))
    pdf = Path(args.pdf) if args.pdf else root / cfg.get("book", {}).get("output", "book/book.pdf")
    markers = cfg.get("markers", {})
    page_re = re.compile(markers.get("page", r"\[p\. (\d+)\]"))
    strip_res = markers.get("strip", [])

    files = source_files(root, cfg)
    if not files:
        sys.exit("no source files found from book.toml")
    words, where, notes, heads = tokens_with_pages(files, page_re, strip_res)
    book = pdf_words(pdf)
    book_text = " " + " ".join(book) + " "

    items = []
    sm = difflib.SequenceMatcher(None, words, book, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ("delete", "replace") and i2 > i1:
            f, page = where[i1]
            lost = " ".join(words[i1:i2])
            before = " ".join(words[max(0, i1 - args.context):i1])
            after = " ".join(words[i2:i2 + args.context])
            got = " ".join(book[j1:j2][:40]) if op == "replace" else ""
            items.append(("Text missing or changed in the book" if op == "delete" else "Text changed in the book",
                          f, page,
                          f"Expected: …{before} [{lost}] {after}…" + (f" Book has: [{got}]" if got else "")))
    for f, label, body in notes:
        nw = norm_words(NOTEREF.sub("", body))
        if not contains(book, nw):
            head, tail = nw[:6], nw[-6:]
            state = "split or altered" if contains(book, head) or contains(book, tail) else "missing"
            items.append((f"Note {label} {state}", f, None, "Note: " + " ".join(nw[:20]) + ("…" if len(nw) > 20 else "")))
    for f, page, h in heads:
        hw = norm_words(h)
        if hw and f" {' '.join(hw)} " not in book_text:
            items.append(("Heading missing or altered", f, page, f"Heading: {h}"))

    rel = lambda p: str(p.relative_to(root)) if p.is_relative_to(root) else str(p)
    lines = [f"Post-design check of `{rel(pdf)}` against the translation's text: {len(words)} words, {len(notes)} notes, {len(heads)} headings; {len(items)} findings."]
    for k, (title, f, page, ev) in enumerate(items, 1):
        lines += ["", f"## R{k} · LAYOUT · {title}", "",
                  f"- Where: `{rel(f)}`" + (f", after [p. {page}]" if page else ""),
                  "- Found by: vt_bookcheck.py (translation side)",
                  f"- Evidence: {ev}",
                  "- Response:",
                  "- Book side:"]
    report = "\n".join(lines)
    print(report)

    if args.write:
        proof = root / "proof"
        proof.mkdir(exist_ok=True)
        n = len(list(proof.glob("check-*.md"))) + 1
        out = proof / f"check-{n:02d}.md"
        head = [f"# Check {n:02d}: {cfg.get('book', {}).get('title', root.name)}", "",
                "| | |", "|---|---|",
                f"| Book | {root.name} |", f"| Round | {n:02d} |",
                f"| Date | {datetime.date.today().isoformat()} |",
                f"| PDF | `{rel(pdf)}` |",
                f"| Direction | translation side to book side |",
                f"| Status | {'OPEN' if items else 'CLOSED (no findings)'} |", "",
                "Format: Vector Book `docs/handover.md`, Returns. The book side answers each item; the translation side closes it after the rebuild.", ""]
        out.write_text("\n".join(head) + report + "\n", encoding="utf-8")
        print(f"\nwrote {rel(out)}")
    return 1 if items else 0


if __name__ == "__main__":
    sys.exit(main())
