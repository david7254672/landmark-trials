#!/usr/bin/env python3
"""Read and edit rows of data/trials.csv without hand-editing the file.

Rows are addressed by `src`. Writes preserve the file's formatting (LF line endings,
standard CSV quoting), so a one-field change is a one-line diff.

Usage:
  python3 scripts/rows.py list [--site "Bladder Cancer"] [--unverified]
  python3 scripts/rows.py show SRC
  python3 scripts/rows.py set SRC col=value [col=value ...]
  python3 scripts/rows.py set SRC --json patch.json      (object of col: value)
  python3 scripts/rows.py add --json row.json            (object of col: value)
  python3 scripts/rows.py style [--site "Bladder Cancer"] [SRC]

An entry is verified when it has `pe` and `pm` and no `flags`. `set` and `add` print
house-style warnings for the rows they touch; run validate.py afterwards as usual.
"""

import csv
import json
import os
import re
import sys

from trials_schema import COLUMNS, CSV_PATH, read_rows

RESULTS_MAX = 180


def load():
    header, rows = read_rows()
    if header != COLUMNS:
        sys.exit("data/trials.csv header does not match schema; run scripts/validate.py")
    return [dict(zip(COLUMNS, cells)) for cells in rows]


def save(rows):
    tmp = CSV_PATH.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(COLUMNS)
        writer.writerows([r[c] for c in COLUMNS] for r in rows)
    os.replace(tmp, CSV_PATH)


def find(rows, src):
    matches = [i for i, r in enumerate(rows) if r["src"] == src]
    if not matches:
        sys.exit(f"no row with src {src!r}")
    return matches[0]


def verified(r):
    return bool(r["pe"] and r["pm"] and not r["flags"])


def style_warnings(r):
    w = []
    if len(r["results"]) > RESULTS_MAX:
        w.append(f"results is {len(r['results'])} characters (max {RESULTS_MAX})")
    for col in COLUMNS:
        if re.search(r"[\r\n]", r[col]):
            w.append(f"{col} contains a line break")
    if re.search(r"95%\s*CI", r["results"], re.I):
        w.append('results says "95% CI"; use brackets only, e.g. HR 0.68 (0.49-0.94)')
    if re.search(r"\bmonths?\b|\byears?\b|\bversus\b", r["results"], re.I):
        w.append("results spells out months/years/versus; use mo, y, vs")
    if r["pm"] and (r["rf"] or r["link"]):
        w.append("rf/link filled although a PMID is present (fallbacks only)")
    return w


def parse_assignments(args):
    patch = {}
    if args[:1] == ["--json"]:
        with open(args[1], encoding="utf-8") as f:
            patch = json.load(f)
    else:
        for a in args:
            col, sep, val = a.partition("=")
            if not sep:
                sys.exit(f"expected col=value, got {a!r}")
            patch[col] = val
    bad = [c for c in patch if c not in COLUMNS]
    if bad:
        sys.exit(f"unknown column(s): {', '.join(bad)}")
    return {c: str(v).strip() for c, v in patch.items()}


def opt(args, name):
    if name in args:
        i = args.index(name)
        return args[i + 1]
    return None


def cmd_list(args):
    rows = load()
    site = opt(args, "--site")
    for r in rows:
        if site and r["tumour"] != site:
            continue
        if "--unverified" in args and verified(r):
            continue
        state = "verified" if verified(r) else ("flagged" if r["flags"] else "unverified")
        print(f"{r['src']}\t{r['trial']}\t{r['phase'] or '-'}\t{state}\t{r['pm'] or '-'}")


def cmd_show(args):
    rows = load()
    print(json.dumps(rows[find(rows, args[0])], ensure_ascii=False, indent=2))


def cmd_set(args):
    rows = load()
    i = find(rows, args[0])
    patch = parse_assignments(args[1:])
    if "src" in patch and patch["src"] != rows[i]["src"]:
        if any(r["src"] == patch["src"] for r in rows):
            sys.exit(f"src {patch['src']!r} already exists")
    before = dict(rows[i])
    rows[i].update(patch)
    save(rows)
    for c in COLUMNS:
        if before[c] != rows[i][c]:
            print(f"{c}: {before[c]!r}\n  -> {rows[i][c]!r}")
    for w in style_warnings(rows[i]):
        print(f"warning: {w}")


def cmd_add(args):
    rows = load()
    new = {c: "" for c in COLUMNS}
    new.update(parse_assignments(args))
    if any(r["src"] == new["src"] for r in rows):
        sys.exit(f"src {new['src']!r} already exists")
    same = [r["trial"] for r in rows if r["trial"].lower() == new["trial"].lower()]
    if same:
        print(f"warning: a row named {new['trial']!r} already exists")
    # Keep sites together: insert after the last row of the same tumour + subsite,
    # else the same tumour, else at the end.
    pos = len(rows)
    for key in (("tumour", "subsite"), ("tumour",)):
        hits = [i for i, r in enumerate(rows) if all(r[k] == new[k] for k in key)]
        if hits:
            pos = hits[-1] + 1
            break
    rows.insert(pos, new)
    save(rows)
    print(f"added {new['trial']!r} at data row {pos + 2}")
    for w in style_warnings(new):
        print(f"warning: {w}")


def cmd_style(args):
    rows = load()
    site = opt(args, "--site")
    srcs = [a for a in args if not a.startswith("--") and a != site]
    n = 0
    for r in rows:
        if (site and r["tumour"] != site) or (srcs and r["src"] not in srcs):
            continue
        for w in style_warnings(r):
            print(f"{r['src']}\t{r['trial']}\t{w}")
            n += 1
    print(f"{n} style warning(s)")


COMMANDS = {"list": cmd_list, "show": cmd_show, "set": cmd_set, "add": cmd_add, "style": cmd_style}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        sys.exit(__doc__)
    COMMANDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
