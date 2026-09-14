# Landmark Trials

A hematologist-oncologist's personal quick-reference of landmark clinical trials
(~900 entries, 25 tumour sites), used at point of care. Entries must be **accurate
and succinct**. Every entry should eventually carry a PMID.

`STATUS.md` is the working log: current counts, what has been verified, open items
and the planned order of work. Read it before starting, and update it at the end of
a working session.

## Layout

```
data/trials.csv      source of truth - edit this, nothing else
data/trials.json     generated from the CSV for the phone web app; never edit by hand
scripts/validate.py  checks the CSV (exit 1 on errors)
scripts/build_json.py  CSV -> JSON (refuses to build if validation fails; --check for staleness)
scripts/trials_schema.py  column list, required fields, allowed tumour/phase values
.claude/skills/      project skills (none yet)
STATUS.md            working log
```

Scripts are Python 3 standard library only (no Node on this machine).

## Columns

18 columns, in this order. The order is part of the schema.

| Column | Meaning |
|---|---|
| `tumour` | Tumour site. One of 25 fixed values (see `trials_schema.py`). Required |
| `subsite` | Disease within the site, e.g. NMIBC, ER+, Follicular lymphoma, MDS |
| `setting` | Disease setting, e.g. Metastatic, Adjuvant, CRPC, Relapsed/refractory |
| `line` | Line of therapy or treatment context, e.g. 1st line, Later line, Transplant-eligible |
| `subgroup` | Biomarker or drug-class grouping, e.g. EGFR, ALK, Targeted therapy |
| `trial` | Trial name, or first author for unnamed studies ("Herr et al"). Required |
| `phase` | Phase 1, 1b, 1b/2, 1/2, 2, 2/3, 3, or Meta-analysis. Blank = not yet recorded |
| `population` | Who was studied, including n where known. Required |
| `intervention` | Arms compared, e.g. "BCG (I+M) +/- Durva". Required |
| `results` | The point-of-care summary: key efficacy figures and notable toxicity. Required |
| `comment` | Interpretation, take-home message, caveats, later-update PMIDs |
| `pe` | Primary endpoint result as reported in the primary publication |
| `pm` | PMID of the primary publication (bare number) |
| `rf` | Free-text citation - fallback only when there is no PMID |
| `extra` | Additional teaching points that don't fit `comment` |
| `link` | URL - fallback only when there is no PMID |
| `src` | Provenance: workbook `Sheet!row` from the migration, `(split)` if a row was divided, or `new entry, <Mon YYYY>` for additions. Required, unique |
| `flags` | Open review issues, `;`-separated. Blank = nothing outstanding |

`setting`, `line` and `subgroup` came from section headings in the original 25-sheet
workbook, so usage is not fully consistent: in myeloma, "1st line" sits in `setting`
with transplant eligibility in `line`; elsewhere "1st line" is in `line`. Leave as is
unless David decides a rule.

## House style

The recently verified entries (see `STATUS.md`) are the standard. Older rows that
don't match are brought into line when their site is verified, not in bulk.

- Abbreviations: `mo`, `y`, `vs`, `NS`, `HR`, `OR`, `ORR`, `CR`, `PFS`, `OS`, `DFS`, `EFS`
- Figures in `results`: `PFS 39.1 vs 5.6 mo, HR 0.16 (0.10-0.24), p<0.001` - CI in
  brackets without "95% CI"
- `pe` may spell out `(95% CI ...)`
- Separate findings with `; `. No line breaks inside a cell
- `results` 180 characters or fewer; move interpretation to `comment`
- Label timepoints: `3-mo CR`, `5-y OS`, `at median 25.8 mo follow-up`
- Negative trials say so: `Primary endpoint not met: ...`
- Unreported trials get a status in `results` (not yet reported / terminated / ongoing)
  rather than a blank

## Verification standard

- Verify against the **primary peer-reviewed publication**. Use published figures in
  preference to conference presentation figures.
- `pm` is the PMID of the primary publication. Look it up; never infer or guess one.
- An entry counts as **verified** when it has `pe` and `pm` and no `flags`.
- **Later updates** (longer follow-up, final OS): update the entry's figures, state the
  follow-up in `results` (e.g. "at median 5 y"), keep `pm` as the primary publication,
  and add the update's PMID to `comment` (e.g. "5-y OS update: PMID 12345678").
- If something cannot be confirmed, **flag it** in `flags` - don't guess and don't
  silently leave it. Abstract-only results are recorded with a flag saying so.
- Never change trial content without a source. Record corrections in `STATUS.md`.

## Workflow for every data change

1. Edit `data/trials.csv` (keep it UTF-8, 18 columns, standard CSV quoting)
2. `python3 scripts/validate.py` - must report 0 errors
3. `python3 scripts/build_json.py` - regenerates `data/trials.json`
4. Commit the CSV and JSON together with a **descriptive message** naming the entries
   and what changed and why, e.g. "Bladder: correct ABC 2003 absolute benefit 7% -> 5%
   (PMID 12801735)". One logical change per commit; never leave data changes uncommitted.

When a new tumour site or phase value is genuinely needed, add it to
`scripts/trials_schema.py` in the same commit.

## Open decisions

- **Stable ID column** - `src` is the only unique field but won't stay meaningful as
  rows are added. Decide before building the phone app.
- **`setting` / `line` rule** - see Columns above.
