# Change list format

Every checker returns its findings in this form. The coordinator applies them with `tools/vt_apply.py` (dry run first, then `--write`).

```
### readable | p. 123
OLD: <exact text, matching the target file exactly once>
NEW: <replacement>
SRC: <the source wording>     (terms and witness checks)
WHY: <reason>                 (read-through and attribution passes)
ORIGIN: internal | witness <ID>
```

- The word after `###` names the target file (`readable`, `literal`, or any name passed with `--target`). After the `|`, a page or note label for the reader.
- OLD must match character for character, including note markers, italics and page markers, and be unique in the file. Quote enough words to make it unique (8 to 30).
- An empty NEW deletes the OLD text.
- `ORIGIN` says where the change came from: `internal` for any check the agents ran on their own output (including second drafts, "same model" or "other model"), or `witness <ID>` for a witness recorded in `checks/witness-<ID>.md`. `vt_apply.py` reports applied changes by origin; an entry without `ORIGIN` is counted as "unmarked".
- Multi-line text goes in fences on the lines after the label:

```
OLD:
~~~
first line
second line
~~~
NEW:
~~~
replacement
~~~
```

Run:

```
python3 tools/vt_apply.py fixes-*.md --target readable=text/readable.md --target literal=text/literal.md
python3 tools/vt_apply.py fixes-*.md --target readable=text/readable.md --target literal=text/literal.md --write
```
