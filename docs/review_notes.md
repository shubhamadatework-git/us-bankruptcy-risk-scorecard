# Review notes

## Verified
* All 73 compared values (KPIs, zones, deciles, trend, median ratios) match an independent pandas re-implementation.
* Text claims on `Methodology` agree with the data (11.6 / 4.4 / 2.0 %, 79.6 %, 60 %, 629 excluded / 22 failed, ~46 % healthy in Distress).

## Changes applied to the workbook
| Area | Change |
|---|---|
| Typo | "Bankrupticies " → "Bankruptcies" (Bankruptcy Trend header and its pivot data-field name) |
| Opening view | Workbook now opens on **Dashboard** (was Methodology); Dashboard gets a one-page landscape print setup |
| Methodology | Text wraps (column 192 → 120 wide); states that bankruptcy year = last reported year; refresh instructions and Excel-version note |
| Company Lookup | `B13` no longer returns #N/A for unknown IDs; "Risk Rank (of N)" label is formula-driven; input cell highlighted; Z-score shown to 2 decimals; validation warns on unknown IDs |
| Privacy | Removed the local `C:\Users\…` path stored in the workbook properties |
| Housekeeping | Stale calc chain removed (Excel rebuilds it); full recalculation on open |
Clean Data, Company Scores, pivot caches, charts and the Power Query definition are unchanged (byte-identical).

## Observations (not changed)
1. **Power Query still points to a local path** (`C:\Users\…\american_bankruptcy.csv`). Anyone cloning the repo must edit the `Source` step before refreshing.
2. **Top deciles are flat:** deciles 1–3 fail at 13.4 %, 13.9 % and 14.9 %. Winsorising the ratios does not change this, so it is a genuine plateau, not an outlier bug. The riskiest decile is 58 % firms with < $10M assets (9.5 % overall) where ratios are noisy. Excluding firms with assets or liabilities < 10 raises the top-30 % capture from 60 % to ~65 % but drops 98 bankrupt companies from scoring — a trade-off worth a sensitivity note.
3. **Ranking quality is not summarised in one number.** The scorecard's AUC is about 0.71 — worth adding to the Dashboard.
4. `X9` and `X16` are identical (redundant).
5. The Methodology result percentages are typed text; they will not update after a data refresh.
6. The file is ~35 MB (78,682 × 32 values stored). It is within GitHub's limit, but Git LFS is an option if the repo grows.
7. Excel screenshots of the Dashboard and pivot charts (`images/`) confirm they render as intended. Minor: the "Grey" label on the zone doughnut is truncated ("1…"); widening the chart or moving labels outside fixes it. The Company Lookup screenshot predates the formatting changes — retake it from the updated file.
