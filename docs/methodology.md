# Methodology

## Data
Kaggle *US Company Bankruptcy Prediction Dataset* (CC0), based on Lombardo et al. (2022), *Future Internet* 14(8):244 — 78,682 firm-year rows, 18 accounting variables (`X1`–`X18`), 1999–2018, 8,971 companies.

## Power Query steps (`powerquery/scorecard_queries.m`)
| Step | Logic |
|---|---|
| Rename | `X1…X18` → readable names (e.g. `X10` → `Total_Assets`) |
| `Failed_Flag` | 1 if `status_label = "failed"` |
| `Last_Year` / `Is_Last_Year` | max year per company; flag the row for that year |
| `Z_Valid` | 1 if `Total_Assets ≥ 1` and `Total_Liabilities ≥ 1` (assumed USD mm) |
| Ratios | WC/TA, RE/TA, EBIT/TA, MVE/TL, Sales/TA (only when `Z_Valid`) |
| `Altman_Z`, `Zone` | 1968 coefficients; Safe > 2.99, Grey 1.81–2.99, Distress < 1.81 |
| `Company_Scores` | last-year valid rows, sorted by Z ascending, `Risk_Rank`, `Risk_Decile = ceil(rank·10/N)` |

## Why one row per company
In this dataset *every* year of a failed company is labelled failed — including healthy early years — so firm-year analysis would mislabel observations. Scoring each company at its **final reported year** compares like with like, and that year doubles as the bankruptcy-year proxy.

## Exclusions
629 companies (22 failed) whose final-year total assets or liabilities are below 1 are excluded because ratios explode. Scored: 8,342 companies, 587 failed.

## Evaluation
* **Zone validation** — bankruptcy rate and share of bankruptcies per zone.
* **Decile lift** — rate per decile, cumulative capture of bankruptcies.
* **Median ratios** — failed vs healthy.
All results are re-computed independently in pandas by `src/validate_scorecard.py`.

## Limitations
See the README. The model is descriptive: ~46 % of healthy companies sit in the Distress zone.
