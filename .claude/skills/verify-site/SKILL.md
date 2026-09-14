---
name: verify-site
description: Batch-verify existing entries in data/trials.csv against their primary publications, site by site - add PMIDs and primary endpoints, correct sourced errors, flag what can't be confirmed. Use when David asks to verify a tumour site, capture references, "do bladder", or continue reference capture from STATUS.md.
---

# Verify a site

An entry is **verified** when it has `pe` and `pm` and no `flags`. This skill works
through the unverified entries of one site in batches, to the standard in `CLAUDE.md`.
Read `CLAUDE.md` and `STATUS.md` first. `STATUS.md` records the site order and entries
already done.

## 1. Pick the batch

```bash
python3 scripts/rows.py list --site "<Tumour site>" --unverified
python3 scripts/rows.py style --site "<Tumour site>"
```

Take up to **10 entries** per batch, in CSV order unless David names them. Tell David
the batch before starting.

## 2. For each entry

1. `python3 scripts/rows.py show "<src>"` to read the whole row.
2. **Identify the primary publication.** Use PubMed `search_articles` (trial name, then
   drug + comparator + disease), web search if keywords miss, and confirm with
   `get_article_metadata`. Use the first full report of the primary endpoint, not a
   design paper, subgroup or secondary analysis, or abstract. Every PMID must come back
   from a tool; never guess one.
3. **Read the evidence.** Read the abstract, and the PMC full text when the row quotes
   figures the abstract doesn't give. Check for later updates (longer follow-up, final
   OS) with a search on the trial name sorted by date.
4. **Compare field by field**: phase, population and n, arms, each figure in `results`
   (value, CI, p, timepoint label), whether the trial was positive, and the `comment`
   claims.
5. **Classify** the entry as one of the outcomes below and act on it.

| Outcome | Action |
|---|---|
| **Confirmed** | Add `pm` and `pe`; tidy to house style (abbreviations, CI in brackets, timepoint labels, months rounded to the nearest month outside `pe`, ≤180-character `results`) without changing any figure otherwise |
| **Corrected** | Change only what the paper contradicts or omits in a way that misleads (wrong figure, wrong arm, missing negative result, missing deaths). Add `pm` and `pe`. Record the before → after in `STATUS.md` |
| **Updated** | Later follow-up changes the figures: update them and state the follow-up (`at median 5 y`). `pm` stays the primary paper; put the update PMID in `comment` |
| **Flagged** | Can't confirm something (no full text, abstract only, conflicting reports): fill what is confirmed and write the specific open issue in `flags`, e.g. `12-mo DFS 19% not in abstract; check full text` |
| **Needs David** | Anything that is a judgement, not a sourced fact: removing a row, splitting or merging rows, moving it to another site/setting/line, an unidentifiable trial, clearing a flag without new evidence, or a figure that is right but whose framing he may prefer. **Don't apply these.** Collect them for the report |

Apply edits with `rows.py`, never by hand-editing the CSV:

```bash
python3 scripts/rows.py set "<src>" pm=12345678 "pe=PFS HR 0.66 (95% CI 0.51-0.87)"
python3 scripts/rows.py set "<src>" --json <scratchpad>/patch.json   # for long text
```

Resolve every style warning it prints for the row.

## 3. Commit

After each entry (or a run of Confirmed entries):

```bash
python3 scripts/validate.py --quiet     # must be 0 errors
python3 scripts/build_json.py
git add data/trials.csv data/trials.json
```

- **Confirmed** entries can share one commit: `Bladder: add PMIDs and primary endpoints
  for POUT, NIAGARA, CheckMate 274 (confirmed accurate)`.
- **Corrected / Updated / Flagged** entries get one commit each, naming the change and
  the source: `Bladder: correct ABC 2003 absolute benefit 7% -> 5% (PMID 12801735)`.
- Never leave data changes uncommitted at the end of a batch.

## 4. Report the batch

Give David a table: entry, outcome, what changed, and PMID. List the **Needs David** items
separately, each with the evidence and a recommended decision. Then stop and wait
before the next batch.

## 5. Update STATUS.md

At the end of the session:

- Update the counts at the top (`python3 scripts/validate.py --quiet` prints rows, with PMID
  and flagged).
- Add the verified entries under a `Verified so far (<site>)` table with a one-line outcome
  each.
- Add corrections to **Corrections applied** in the existing before → after style, with PMID.
- Record decisions David made as `— David's decision`.
- Move the site on in **Open items** / **Planned order**.

Commit `STATUS.md` on its own: `STATUS: <site> batch N verified; <counts>`.

## Pitfalls seen so far

- Merged rows: one row can carry two different studies (the Sylvester meta-analyses).
  Check that every figure comes from the same paper.
- Conference and press-release figures often differ slightly from the paper (ATOMIC).
  Use the paper.
- Figures attributed to a subgroup can be the overall result, or the reverse (VESPER).
- Arms drift in transcription (FLOT65+ FOLFOX → FLO; COMPETE dotatate → edotreotide).
- Phase is often wrong (TheraP, nadofaragene, ABACUS). Take it from the paper.
- Results quoted without the toxicity signal (SWOG S1605 deaths, PANOPTIMOX
  neurotoxicity) should get that signal added.
