# Landmark Trials — status

Last updated: 13 September 2026

## Where things stand

- **903 entries**, 25 tumour sites. Migrated from a 25-sheet workbook where section headings
  carried the setting and line; those are now real fields.
- **28 entries carry a PMID** (was 9). The rest have no reference yet.
- **64 entries flagged** for review (was 84).
- **1 entry has no results text** (was 26) — STOP MDS, which could not be identified.
- 69 spelling corrections applied and approved. Five name-level fixes among them:
  ABCSG-16, ToGA, Joudi, fedratinib, "Periop chemo".

## Verified so far (bladder)

| Entry | Outcome |
|---|---|
| Sylvester meta-analyses | Split into two rows — the CIS meta-analysis (PMID 15947584) and the progression meta-analysis (PMID 12394686) had been merged into one |
| Joudi | Accurate; BCG-naive arm added (PMID 16818189) |
| KEYNOTE-057 | Accurate; 41% labelled as the 3-month CR (PMID 34051177) |
| SWOG S1605 | Failed efficacy threshold and three treatment-related deaths were missing (PMID 37596191) |
| Boorjian / nadofaragene | Accurate; phase corrected 2 → 3 (PMID 33253641) |
| BOND-003 Cohort C | Added — was absent (PMID 42508433) |
| ABC 2003 meta-analysis | Absolute benefit corrected 7% → 5% (PMID 12801735) |
| AMBASSADOR | Accurate; coprimary endpoint design noted (PMID 39282902) |
| CREST | Identified and filled — sasanlimab + BCG I+M, EFS HR 0.68, 36-mo EFS 82.1 vs 74.8% (PMID 40450141) |
| LAURA (lung) | PFS HR 0.16 confirmed; primary NEJM PMID pinned (38828946) |

## Results pass — completed 13 September 2026

All 26 blank-results entries worked through. 21 filled with a PMID, 4 filled with a
status (not yet reported / terminated), 1 unresolved.

**Filled with primary publication:** CREST, TEXT (via SOFT-TEXT combined), ATOMIC, COMMIT,
REAL-2, FIRST-MIND, LAURA, FREEDOM-2, MOMENTUM, MASTER, LYNX, BELLINI, CANOVA, SEQTOR,
OCLURANDOM, COMPETE, GARNET, Schram/zenocutuzumab, ROAR. Plus two column-shift repairs
(STIM-1, SELECT-D) where the results text was sitting in the population field.

**Filled with status, no efficacy data:**
- SWOG S1207 — negative (5-y IDFS 74.8 vs 73.9%, HR 0.93), SABCS 2022 abstract only, no
  indexed publication
- RENAISSANCE — not yet reported; design paper PMID 29282088
- SURGIGAST — terminated for inadequate accrual; no efficacy data will come
- PACIFICA — ongoing, completion listed Dec 2026

## Open items

- **STOP MDS** — no trial by this name in registries or literature. The text in the
  population field was a study-design description and has been moved to intervention.
  Name or source needs confirming; may be a transcription of something else.
- **REAL-2 setting mismatch** — the row sits under Neoadjuvant/adjuvant with intervention
  "Periop Chemo (ECX/EOX)", but REAL-2 studied first-line advanced esophagogastric disease.
  Left unchanged and flagged — may be deliberate shorthand for justifying X/O substitution.
- **POTOMAC** — HR 0.68 unconfirmed. Primary publication is Lancet 2025;406:2221-34.
- **IMvigor011** — numbers don't match the published description. Possibly IMvigor010
  ctDNA-positive subgroup figures. Flagged, not corrected.
- **Bladder, still unverified**: VESPER, ABACUS, PURE-01, POUT, Coleman, CheckMate 274,
  NIAGARA, EV-303/KEYNOTE-905, EV-304/KEYNOTE-B15, Herr, Harland.
- **Every other site** — no verification started.

## Corrections applied during this pass

- COMMIT intervention rewritten: the FOLFOX/bev-alone arm closed after 20 patients, so the
  reported comparison is atezolizumab alone vs FFX/bev/atezo, not "FOLFOX-bev +/- atezo"
- FIRST-MIND intervention rewritten: both arms received tafasitamab, randomisation was
  ± lenalidomide; phase set to 1b
- COMPETE intervention corrected: 177Lu-**edotreotide**, not dotatate
- Trial name "??" resolved to OCLURANDOM
- Unnamed dostarlimab dMMR row named GARNET (cohorts A1 + F)
- ATOMIC: published NEJM figures (86.3/76.2) used in preference to the widely quoted
  ASCO 2025 presentation figures (86.4/76.6)

## Planned order

1. ~~Finish the 26 entries with no results~~ — done
2. Build the entry-generation and batch-verification skills
3. Reference capture site by site, starting with GU and heme
