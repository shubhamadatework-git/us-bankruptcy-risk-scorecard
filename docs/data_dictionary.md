# Data Dictionary

## Source CSV (`data/raw/american_bankruptcy.csv`)
| CSV column | Workbook name | Meaning |
|---|---|---|
| `company_name` | company_name | Anonymised ID (`C_1`…`C_8971`) |
| `status_label` | status_label | `alive` / `failed` (company-level label) |
| `year` | year | Fiscal year 1999–2018 |
| `X1` | Current_Assets | Current assets |
| `X2` | COGS | Cost of goods sold |
| `X3` | Depreciation_Amort | Depreciation & amortization |
| `X4` | EBITDA | Earnings before interest, tax, D&A |
| `X5` | Inventory | Inventory |
| `X6` | Net_Income | Net income |
| `X7` | Receivables | Total receivables |
| `X8` | Market_Value | Market value (capitalisation) |
| `X9` | Net_Sales | Net sales |
| `X10` | Total_Assets | Total assets |
| `X11` | LT_Debt | Total long-term debt |
| `X12` | EBIT | Earnings before interest and tax |
| `X13` | Gross_Profit | Gross profit |
| `X14` | Current_Liabilities | Total current liabilities |
| `X15` | Retained_Earnings | Retained earnings |
| `X16` | Total_Revenue | Total revenue (identical to `X9`) |
| `X17` | Total_Liabilities | Total liabilities |
| `X18` | Operating_Expenses | Total operating expenses |

## Columns added by Power Query
| Column | Meaning |
|---|---|
| `Failed_Flag` | 1 = failed company |
| `Last_Year` | Company's last reported year |
| `Is_Last_Year` | 1 on that row |
| `Z_Valid` | 1 if assets ≥ 1 and liabilities ≥ 1 |
| `WC_TA`, `RE_TA`, `EBIT_TA`, `MVE_TL`, `Sales_TA` | Altman ratios |
| `Altman_Z`, `Zone` | Score and zone (`Safe` / `Grey` / `Distress` / `Excluded`) |
| `Risk_Rank`, `Risk_Decile` | (Company Scores) rank by Z, decile 1 = riskiest |
