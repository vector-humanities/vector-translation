#!/usr/bin/env python3
"""Apply a vector translation change list to the master files.

A change list is a sequence of entries:

    ### translation | p. 123
    OLD: <exact text>
    NEW: <replacement>
    SRC: <source wording>      (optional)
    WHY: <reason>              (optional)
    ORIGIN: internal | witness <ID>

Multi-line OLD or NEW text goes in ~~~ fences on the lines after the label:

    OLD:
    ~~~
    first line
    second line
    ~~~

The word after ### names the target, mapped to a file with --target name=path
(for example --target translation=text/translation.md --target literal=text/literal.md).
"readable", the old name for the translation (renamed 2026-11-05), is still
accepted, as a target in a change list and in --target.

Dry run by default: every entry is checked and reported, nothing is written.
With --write, entries whose OLD matches exactly once are applied in order,
and a timestamped backup of each changed file is written first.
Entries that match zero or several times are always refused.

ORIGIN records where a change came from: "internal" for checks the agents
ran on their own output, "witness <ID>" for a witness check. The report
counts applicable entries by origin; an entry without ORIGIN is "unmarked".

A Vector Book return file (proof/return-NN.md) can be given directly: the
entries under each item's "- Proposed:" line are read, and the rest ignored.
The Response lines in the return are still written by hand.

Standard library only.
"""
import argparse
import re
import shutil
import sys
import time
from pathlib import Path

HEAD = re.compile(r"^###[ \t]+(\S+)[ \t]*(?:\|[ \t]*(.*))?$")
FIELD = re.compile(r"^(OLD|NEW|SRC|JP|WHY|ORIGIN):[ \t]?(.*)$")


# Old target names, still accepted: "readable" was renamed "translation" on 2026-11-05.
ALIASES = {"readable": "translation"}


def target_name(name):
    name = name.lower()
    return ALIASES.get(name, name)


PROPOSED = re.compile(r"^([ \t]*)- Proposed:[ \t]*$", re.M)


def from_return(text):
    """Keep only the change-list entries under "- Proposed:" in a Vector Book return
    file (proof/return-NN.md), dedented, with every other line blanked so that line
    numbers still point into the return file."""
    lines, out, i = text.splitlines(), [], 0
    out = [""] * len(lines)
    while i < len(lines):
        m = PROPOSED.match(lines[i])
        if not m or i + 1 >= len(lines) or lines[i + 1].strip() != "~~~":
            i += 1
            continue
        indent = len(lines[i + 1]) - len(lines[i + 1].lstrip())
        j, inner, prev = i + 2, False, ""
        while j < len(lines):
            dl = lines[j][indent:] if lines[j][:indent].strip() == "" else lines[j].lstrip()
            if dl.strip() == "~~~":
                if inner:
                    inner = False
                elif FIELD.match(prev) and FIELD.match(prev).group(2).strip() == "":
                    inner = True
                else:
                    break
            out[j] = dl
            if dl.strip():
                prev = dl
            j += 1
        i = j + 1
    return "\n".join(out)


def parse(text):
    entries, cur, lines, i = [], None, text.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        m = HEAD.match(line)
        if m:
            cur = {"target": target_name(m.group(1)), "where": (m.group(2) or "").strip(), "line": i + 1}
            entries.append(cur)
            i += 1
            continue
        m = FIELD.match(line)
        if m and cur is not None:
            key, val = m.group(1), m.group(2)
            if val.strip() == "" and i + 1 < len(lines) and lines[i + 1].strip() == "~~~":
                j = i + 2
                body = []
                while j < len(lines) and lines[j].strip() != "~~~":
                    body.append(lines[j])
                    j += 1
                if j == len(lines):
                    sys.exit(f"line {i + 1}: unclosed ~~~ fence")
                cur[key] = "\n".join(body)
                i = j + 1
                continue
            cur[key] = val
        i += 1
    return entries


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("changes", nargs="+", help="change list file(s)")
    ap.add_argument("--target", action="append", default=[], metavar="NAME=PATH",
                    help="map a target name to a file (repeatable)")
    ap.add_argument("--write", action="store_true", help="apply the changes (default: dry run)")
    args = ap.parse_args()

    targets = {}
    for t in args.target:
        name, _, path = t.partition("=")
        if not path:
            sys.exit(f"--target needs NAME=PATH, got {t!r}")
        targets[target_name(name)] = Path(path)

    texts = {name: p.read_text(encoding="utf-8") for name, p in targets.items()}
    changed = set()
    ok = refused = 0
    by_origin = {}

    for cf in args.changes:
        raw = Path(cf).read_text(encoding="utf-8")
        if re.search(r"return-\d+\.md$", cf) or PROPOSED.search(raw) and "## R" in raw:
            raw = from_return(raw)
        for e in parse(raw):
            tag = f"{cf}:{e['line']} [{e['target']} | {e['where']}]"
            if e["target"] not in texts:
                print(f"REFUSED {tag}: no --target for {e['target']!r}")
                refused += 1
                continue
            if "OLD" not in e or "NEW" not in e:
                print(f"REFUSED {tag}: entry lacks OLD or NEW")
                refused += 1
                continue
            body = texts[e["target"]]
            n = body.count(e["OLD"]) if e["OLD"] else 0
            if n != 1:
                print(f"REFUSED {tag}: OLD matches {n} times")
                refused += 1
                continue
            texts[e["target"]] = body.replace(e["OLD"], e["NEW"], 1)
            changed.add(e["target"])
            ok += 1
            words = e.get("ORIGIN", "").split()
            origin = " ".join([words[0].lower()] + words[1:]) if words else "unmarked"
            by_origin[origin] = by_origin.get(origin, 0) + 1
            print(f"ok      {tag} ({origin})")

    print(f"\n{ok} applicable, {refused} refused")
    for origin in sorted(by_origin):
        print(f"  {origin}: {by_origin[origin]}")
    if not args.write:
        print("dry run: nothing written (use --write to apply)")
        return 1 if refused else 0

    stamp = time.strftime("%Y%m%d-%H%M%S")
    for name in sorted(changed):
        p = targets[name]
        backup = p.with_name(f"{p.name}.{stamp}.bak")
        shutil.copy2(p, backup)
        p.write_text(texts[name], encoding="utf-8")
        print(f"wrote {p} (backup {backup.name})")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
