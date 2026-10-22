#!/usr/bin/env python3
"""Assemble a master file from section files.

    python3 tools/vt_assemble.py text/readable/ --front front/ --back back/ -o build/readable.md

Section files are joined in filename order (number them 00-, 01-, ...),
front matter before and back matter after, each separated by a blank line.
Lines between <!-- working --> and <!-- /working --> are dropped, so working
headers and editor's notes can stay in the section files without reaching
the master. Standard library only.
"""
import argparse
import re
import sys
from pathlib import Path

WORKING = re.compile(r"<!-- working -->.*?<!-- /working -->\n?", re.S)


def parts(folder):
    if not folder:
        return []
    return sorted(p for p in Path(folder).glob("*.md") if p.is_file())


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sections", help="folder of section files")
    ap.add_argument("--front", help="folder of front-matter files")
    ap.add_argument("--back", help="folder of back-matter files")
    ap.add_argument("-o", "--out", required=True)
    args = ap.parse_args()

    files = parts(args.front) + parts(args.sections) + parts(args.back)
    if not files:
        sys.exit("no .md files found")
    chunks = [WORKING.sub("", f.read_text(encoding="utf-8")).strip() for f in files]
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text("\n\n".join(chunks) + "\n", encoding="utf-8")
    print(f"{args.out}: {len(files)} files")
    for f in files:
        print(f"  {f}")


if __name__ == "__main__":
    sys.exit(main())
