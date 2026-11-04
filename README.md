# CTIS Sponsor Prospects

A prospecting dashboard that identifies the most active clinical trial sponsors in Europe, based on the public **CTIS** register (EU Clinical Trials Information System). It is used to prioritise potential clients for a clinical trial management platform.

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

- **KPIs and charts** recomputed from the filters: sponsors, trials, recruiting trials, countries covered; top sponsors, top countries, therapeutic areas, phases.
- **Trial-level filters**: each sponsor is re-ranked on its matching trials only.
  - product or molecule (several terms separated by commas; brand names and molecules are linked);
  - country, therapeutic area, phase, status, sponsor type;
  - year authorised, last update, population, trial size, geographic scope, number of countries, published results;
  - minimum / maximum number of trials, first administration to humans, bioequivalence, and more.
- **Shortcuts**: small active biotechs, oncology in France, anti-PD-1 / PD-L1 immunotherapies, early phases, recruiting academic sponsors.
- **Sponsor detail**: merged entities, countries, areas, phases, products and latest trials.
- **CSV export** of the filtered view (sponsors or trials), comma-separated, UTF-8.

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

**Prospect score**: `(2 × trials + 4 × recruiting trials) × 1.3` for pharmaceutical companies and industry. It is a prioritisation heuristic, not an official ranking.

**Participants**: trials reporting more than 100,000 participants are left out of the totals as outliers.

## Known limitations

- The export has exactly 10,000 rows, probably the register's export limit, so the data is likely incomplete.
- The product field is empty for 2,121 trials; they never appear when a product filter is active.
- The product filter also matches trials where the product is a comparator.
- The brand ↔ molecule mapping covers only about 140 common drugs (`scripts/synonyms.py`).

## Data source

Public CTIS register of the European Medicines Agency: [euclinicaltrials.eu](https://euclinicaltrials.eu). The data remains subject to the EMA's terms of use.
