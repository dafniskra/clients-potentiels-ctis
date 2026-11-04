# CTIS Sponsor Prospects

A prospecting dashboard built on the public **CTIS** register (EU Clinical Trials Information System). It finds **small trial sponsors** (biotechs, research centres, hospitals with 10 trials or fewer) that are likely to need an affordable clinical trial management tool, **France first**.

The dashboard is a self-contained HTML page with all data embedded: open `docs/index.html` in a browser (an internet connection is needed for the fonts and the charting library).

## Contents

```
data/CTIS_trials_20261104.csv   Raw CTIS register export (10,000 trials, 4 November 2026)
docs/index.html                 Generated dashboard (open in a browser)
docs/fusions_promoteurs.csv     Merged sponsor names, for review
scripts/build_dashboard.py      Builds docs/ from the CSV export
scripts/sponsor_groups.py       Sponsor merging rules
scripts/synonyms.py             Brand name ↔ molecule (INN) mappings
src/template.html               Dashboard template (HTML, CSS, JavaScript)
```

## Features

- **Default view**: small sponsors (10 trials or fewer in CTIS) with at least one trial in France, ranked by fit score.
- **KPIs and charts** recomputed from the filters: sponsors, trials, recruiting trials, countries covered; top prospects, top countries, therapeutic areas, phases.
- **Trial-level filters**: each sponsor is re-ranked on its matching trials only.
  - product or molecule (several terms separated by commas; brand names and molecules are linked);
  - country, therapeutic area, phase, status, sponsor type;
  - authorised in the last 6 / 12 / 24 months, year authorised, last update, population, trial size, geographic scope, number of countries, published results;
  - small sponsors only, new sponsors, minimum / maximum number of trials, first administration to humans, bioequivalence, and more.
- **Target segments (France)**: biotechs starting a trial, recruiting academic centres, new sponsors, multi-country small sponsors; plus small sponsors across Europe.
- **Sponsor detail**: how the fit score is built, contact links (Google, LinkedIn company and people searches, CTIS trial pages with the sponsor's public contact), merged entities, countries, areas, phases, products and latest trials.
- **CSV export** of the filtered view (sponsors or trials), comma-separated, UTF-8, with fit details and contact links.

## Rebuilding the dashboard

No dependencies: Python 3.9 or later is enough.

```bash
python3 scripts/build_dashboard.py
```

The script takes the most recent export in `data/` (`CTIS_trials_*.csv`) and rewrites `docs/index.html` and `docs/fusions_promoteurs.csv`. To use another file:

```bash
python3 scripts/build_dashboard.py path/to/export.csv
```

To update the data: export the trials from [euclinicaltrials.eu](https://euclinicaltrials.eu) in the same CSV format, save the file in `data/` as `CTIS_trials_YYYYMMDD.csv`, then run the script again. Also update the extraction date in `src/template.html` (footer and the `EXTRACT` constant).

To change the interface, edit `src/template.html`, never `docs/index.html`, which is overwritten on every build.

## Method

**Sponsor merging** (`scripts/sponsor_groups.py`)
1. Spelling variants of the same entity are grouped automatically: case, accents, punctuation, legal suffixes (Inc., AG, GmbH, S.A.…).
2. Subsidiaries of the same pharma group are grouped from a hand-made list (Sanofi, Johnson & Johnson / Janssen, Bristol Myers Squibb + Celgene, GSK, Boehringer Ingelheim…). MSD and Merck KGaA are kept separate.
3. A trial filed by several subsidiaries of the same group counts once for that group.

Result on the 4 November 2026 export: 2,264 sponsors, 89 of them merged groups.

**Fit score** (0-100), computed on the trials that match the filters:

| Signal | Points |
|---|---|
| Size: 1 trial in CTIS / 2-3 / 4-6 / 7-10 / more than 10 | 25 / 22 / 16 / 10 / 0 |
| Timing: a trial is authorised and starting recruitment / authorised in the last 12 months / recruiting | 20 / 15 / 10 |
| New sponsor: first trial authorised in the last 18 months | 10 |
| Runs a multi-country trial | 10 |
| Early or mid phase (I, I/II or II) | 5 |
| 100 participants or more in total | 5 |
| Has a trial in France | 25 |

It is a prioritisation heuristic, not an official ranking. The weights are in `fitScore()` in `src/template.html`.

**Participants**: trials reporting more than 100,000 participants are left out of the totals as outliers.

## Known limitations

- The export has exactly 10,000 rows, probably the register's export limit, so the data is likely incomplete.
- The product field is empty for 2,121 trials; they never appear when a product filter is active.
- The product filter also matches trials where the product is a comparator.
- The brand ↔ molecule mapping covers only about 140 common drugs (`scripts/synonyms.py`).

## Data source

Public CTIS register of the European Medicines Agency: [euclinicaltrials.eu](https://euclinicaltrials.eu). The data remains subject to the EMA's terms of use.
