#!/usr/bin/env python3
"""Generate data/trials.json from data/trials.csv.

The CSV is the source of truth; never edit the JSON by hand. The build refuses to
run if validate.py reports errors.

Usage:
  python3 scripts/build_json.py          write data/trials.json
  python3 scripts/build_json.py --check  exit 1 if data/trials.json is stale
"""

import json
import sys

from trials_schema import COLUMNS, JSON_PATH, read_rows
from validate import validate


def render():
    _, rows = read_rows()
    trials = [dict(zip(COLUMNS, cells)) for cells in rows]
    # No timestamp: output depends only on the CSV, so git diffs stay meaningful.
    return json.dumps(trials, ensure_ascii=False, indent=2) + "\n"


def main():
    errors, _, _ = validate()
    if errors:
        print("data/trials.csv has validation errors; run scripts/validate.py", file=sys.stderr)
        return 1

    output = render()

    if "--check" in sys.argv:
        current = JSON_PATH.read_text(encoding="utf-8") if JSON_PATH.exists() else ""
        if current != output:
            print("data/trials.json is out of date; run scripts/build_json.py", file=sys.stderr)
            return 1
        print("data/trials.json is up to date")
        return 0

    JSON_PATH.write_text(output, encoding="utf-8")
    print(f"Wrote {JSON_PATH.relative_to(JSON_PATH.parent.parent)} ({output.count(chr(10) + '  {')} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
