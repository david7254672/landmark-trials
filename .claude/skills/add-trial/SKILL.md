---
name: add-trial
description: Draft and add a new landmark trial entry to data/trials.csv from its primary publication. Use when David names a trial (or several) to add, says an entry is missing, or asks to "add", "create" or "generate" an entry.
---

# Add a trial entry

The goal is one row in house style, sourced from the **primary peer-reviewed
publication**, committed on its own. Read `CLAUDE.md` (columns, house style,
verification standard) before the first entry of a session.

## 1. Check it isn't already there

```bash
python3 scripts/rows.py list --site "<Tumour site>"
```

Also grep the CSV for the trial name without punctuation (e.g. `KEYNOTE-905`, `EV-303`,
`keynote 905`) and for the drug. If a row exists, this is a verification job, not an
addition: use the `verify-site` workflow for that row instead, and tell David.

## 2. Find the primary publication

- PubMed `search_articles`: trial name in [Title/Abstract], then drug + comparator +
  disease + `Randomized Controlled Trial[Publication Type]`.
- If keyword searches miss, search the web for the trial name + journal, then confirm
  the PMID with `lookup_article_by_citation` or `get_article_metadata`. (FLOT65+ was only
  found this way.)
- Pick the **first full report of the primary endpoint**, not a design paper, secondary
  analysis, or conference abstract. Record later updates (longer follow-up, final OS)
  separately; they go in `comment`.
- Read the abstract with `get_article_metadata`. If the paper is in PMC, fetch the full
  text for figures the abstract omits.
- **Never infer or guess a PMID.** Every PMID written must have come back from a tool.

If there is no peer-reviewed publication, stop and tell David what exists (abstract,
press release, registry entry). Only add it if he says so, with a flag such as
`Abstract only (ASCO 2026); no peer-reviewed publication as of <Mon YYYY>`.

## 3. Draft the row

Write a JSON object to the scratchpad, filling every column that applies:

| Column | How to fill |
|---|---|
| `tumour` | One of the 25 values in `scripts/trials_schema.py` |
| `subsite`, `setting`, `line`, `subgroup` | Copy the vocabulary of neighbouring rows in the same site (`rows.py list --site`); don't invent a new term when an existing one fits |
| `trial` | Trial name as commonly cited; first author + "et al" if unnamed |
| `phase` | From the paper, e.g. `Phase 3` |
| `population` | Who was randomised, key eligibility, `n=` |
| `intervention` | Arms, experimental first: `Sasanlimab + BCG vs BCG` |
| `results` | ≤180 characters. Primary endpoint first, then key secondaries, then notable toxicity. `PFS 39.1 vs 5.6 mo, HR 0.16 (0.10-0.24), p<0.001`. Label timepoints and follow-up. Negative trials start `Primary endpoint not met: ` |
| `comment` | Take-home, caveats (single arm, crossover, control arm), later-update PMIDs |
| `pe` | Primary endpoint as reported; may spell out `(95% CI ...)` |
| `pm` | Primary publication PMID, bare number |
| `extra` | Teaching points only if they don't fit `comment`; usually blank |
| `rf`, `link` | Blank when there is a PMID |
| `src` | `new entry, <Mon YYYY>`. `src` must be unique: if another row already has that value, add the trial name, e.g. `new entry, Sep 2026 (NIAGARA)` |
| `flags` | Anything you couldn't confirm. Blank only if every figure was checked against the paper |

Use the `mo`, `y`, `vs`, `NS`, `HR`, `ORR`, `PFS`, `OS`, `DFS`, `EFS` abbreviations.
No line breaks in any cell.

## 4. Show David before writing

Show the draft row as a compact field list, with the PMID, journal and year. Point out
any judgement calls (which endpoint went first, placement under setting/line, anything
flagged). Wait for approval, unless David has already said to add without review in this
session.

## 5. Write, validate, build, commit

```bash
python3 scripts/rows.py add --json <scratchpad>/row.json
python3 scripts/validate.py --quiet
python3 scripts/build_json.py
git add data/trials.csv data/trials.json
git commit -m "<Site>: add <TRIAL> (PMID <pm>)" -m "<one or two lines: population, arms, headline result>"
```

Fix any style warnings `rows.py` prints before committing. Validation must report 0
errors. One trial per commit.

## 6. Log it

Add the entry to `STATUS.md` (the verified table or the list of additions for its site)
and update the counts at the top. Commit `STATUS.md` separately at the end of the session
if several entries were added.
