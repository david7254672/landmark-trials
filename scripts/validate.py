#!/usr/bin/env python3
"""Validate data/trials.csv.

Errors (exit 1): the file is malformed or a row breaks a hard rule.
Warnings (exit 0): something worth a look that may be legitimate.

Usage: python3 scripts/validate.py [path/to/file.csv] [--quiet]
"""

import re
import sys
from collections import Counter, defaultdict

from trials_schema import COLUMNS, CSV_PATH, PHASES, REQUIRED, TUMOURS, read_rows

RESULT_PATTERN = re.compile(r"\bHR\s*[0-9]|\bp\s*[=<]\s*0?\.\d|\bORR\s+\d", re.I)


def validate(path=CSV_PATH):
    errors = defaultdict(list)
    warnings = defaultdict(list)

    try:
        header, rows = read_rows(path)
    except UnicodeDecodeError as e:
        errors["File is not valid UTF-8"].append(str(e))
        return errors, warnings, None

    if header != COLUMNS:
        errors["Header does not match schema"].append(
            f"expected {COLUMNS}\n      got      {header}"
        )
        return errors, warnings, None

    seen_src = Counter()
    seen_rows = Counter()
    seen_pmid = defaultdict(list)

    # Line numbers count data rows from 2 (the header is row 1), matching a spreadsheet view.
    for n, cells in enumerate(rows, start=2):
        if len(cells) != len(COLUMNS):
            errors["Wrong number of fields"].append(
                f"row {n}: {len(cells)} fields, expected {len(COLUMNS)}"
            )
            continue

        r = dict(zip(COLUMNS, cells))
        where = f"row {n} [{r['src'] or 'no src'}] {r['trial'] or '(no trial name)'}"

        for col, val in r.items():
            if val != val.strip():
                errors["Leading/trailing whitespace"].append(f"{where}: {col}")
            if "�" in val:
                errors["Unicode replacement character (encoding damage)"].append(f"{where}: {col}")

        # A blank required field is excused only by a flag that names it (e.g. "Missing
        # population") or marks the whole row UNIDENTIFIED; an unrelated flag doesn't count.
        flags = r["flags"].lower()
        for col in REQUIRED:
            if not r[col]:
                if col in flags or "unidentified" in flags:
                    warnings["Required field blank (flagged)"].append(f"{where}: {col}")
                else:
                    errors["Required field blank, not flagged"].append(f"{where}: {col}")
            elif f"missing {col}" in flags:
                warnings["Flag says field is missing but it is filled (stale flag?)"].append(
                    f"{where}: {col}"
                )

        if r["pm"]:
            if not re.fullmatch(r"[1-9]\d{0,8}", r["pm"]):
                errors["PMID is not a bare number"].append(f"{where}: {r['pm']!r}")
            else:
                seen_pmid[r["pm"]].append(where)

        if r["link"] and not re.match(r"https?://\S+$", r["link"]):
            errors["Link is not a URL"].append(f"{where}: {r['link']!r}")

        if r["tumour"] and r["tumour"] not in TUMOURS:
            errors["Unknown tumour site"].append(f"{where}: {r['tumour']!r}")

        if r["phase"] and r["phase"] not in PHASES:
            errors["Unknown phase value"].append(f"{where}: {r['phase']!r}")

        if r["pe"] and not (r["pm"] or r["rf"] or r["flags"]):
            warnings["Primary endpoint recorded without a PMID, reference or flag"].append(where)

        if RESULT_PATTERN.search(r["population"]):
            warnings["Population looks like results text (possible column shift)"].append(
                f"{where}: {r['population'][:70]!r}"
            )

        seen_src[r["src"]] += 1
        seen_rows[tuple(cells[:-1])] += 1  # ignore flags when looking for duplicates

    for src, count in seen_src.items():
        if src and count > 1:
            errors["Duplicate src"].append(f"{src!r} appears {count} times")

    for key, count in seen_rows.items():
        if count > 1:
            errors["Duplicate row"].append(f"{key[5] or '(no trial name)'} appears {count} times")

    for pmid, wheres in seen_pmid.items():
        if len(wheres) > 1:
            warnings["PMID used on more than one row"].append(f"{pmid}: " + "; ".join(wheres))

    stats = {
        "rows": len(rows),
        "with PMID": sum(1 for c in rows if len(c) == len(COLUMNS) and c[COLUMNS.index("pm")]),
        "flagged": sum(1 for c in rows if len(c) == len(COLUMNS) and c[COLUMNS.index("flags")]),
    }
    return errors, warnings, stats


def report(title, groups, quiet):
    total = sum(len(v) for v in groups.values())
    print(f"\n{title}: {total}")
    for label, items in sorted(groups.items()):
        print(f"  {label} ({len(items)})")
        if not quiet:
            for item in items:
                print(f"    - {item}")
    return total


def main():
    quiet = "--quiet" in sys.argv
    paths = [a for a in sys.argv[1:] if not a.startswith("--")]
    path = paths[0] if paths else CSV_PATH
    errors, warnings, stats = validate(path)
    if stats:
        print(
            f"{path}: {stats['rows']} rows, "
            f"{stats['with PMID']} with PMID ({stats['rows'] - stats['with PMID']} without), "
            f"{stats['flagged']} flagged"
        )
    n_err = report("ERRORS", errors, quiet)
    report("WARNINGS", warnings, quiet)
    print("\nFAIL" if n_err else "\nOK")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
