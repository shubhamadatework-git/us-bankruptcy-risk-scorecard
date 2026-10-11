// Power Query (M) code extracted from excel/US_Bankruptcy_Risk_Scorecard.xlsx
// Edit the "Source" path below to your local copy of data/raw/american_bankruptcy.csv before refreshing.

section Section1;

shared american_bankruptcy = let
    Source = Csv.Document(File.Contents("C:\path\to\american_bankruptcy.csv"), [Delimiter=",", Columns=21, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Promoted, {{"company_name", type text}, {"status_label", type text}, {"year", Int64.Type}, {"X1", type number}, {"X2", type number}, {"X3", type number}, {"X4", type number}, {"X5", type number}, {"X6", type number}, {"X7", type number}, {"X8", type number}, {"X9", type number}, {"X10", type number}, {"X11", type number}, {"X12", type number}, {"X13", type number}, {"X14", type number}, {"X15", type number}, {"X16", type number}, {"X17", type number}, {"X18", type number}}),
    Renamed = Table.RenameColumns(Typed, {{"X1", "Current_Assets"}, {"X2", "COGS"}, {"X3", "Depreciation_Amort"}, {"X4", "EBITDA"}, {"X5", "Inventory"}, {"X6", "Net_Income"}, {"X7", "Receivables"}, {"X8", "Market_Value"}, {"X9", "Net_Sales"}, {"X10", "Total_Assets"}, {"X11", "LT_Debt"}, {"X12", "EBIT"}, {"X13", "Gross_Profit"}, {"X14", "Current_Liabilities"}, {"X15", "Retained_Earnings"}, {"X16", "Total_Revenue"}, {"X17", "Total_Liabilities"}, {"X18", "Operating_Expenses"}}),
    Failed = Table.AddColumn(Renamed, "Failed_Flag", each if [status_label] = "failed" then 1 else 0, Int64.Type),
    LastYears = Table.Group(Failed, {"company_name"}, {{"Last_Year", each List.Max([year]), Int64.Type}}),
    Joined = Table.NestedJoin(Failed, {"company_name"}, LastYears, {"company_name"}, "LY", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Joined, "LY", {"Last_Year"}),
    LastFlag = Table.AddColumn(Expanded, "Is_Last_Year", each if [year] = [Last_Year] then 1 else 0, Int64.Type),
    ValidZ = Table.AddColumn(LastFlag, "Z_Valid", each if [Total_Assets] >= 1 and [Total_Liabilities] >= 1 then 1 else 0, Int64.Type),
    AddWC = Table.AddColumn(ValidZ, "WC_TA", each if [Z_Valid] = 1 then ([Current_Assets] - [Current_Liabilities]) / [Total_Assets] else null, type number),
    AddRE = Table.AddColumn(AddWC, "RE_TA", each if [Z_Valid] = 1 then [Retained_Earnings] / [Total_Assets] else null, type number),
    AddEBIT = Table.AddColumn(AddRE, "EBIT_TA", each if [Z_Valid] = 1 then [EBIT] / [Total_Assets] else null, type number),
    AddMVE = Table.AddColumn(AddEBIT, "MVE_TL", each if [Z_Valid] = 1 then [Market_Value] / [Total_Liabilities] else null, type number),
    AddSales = Table.AddColumn(AddMVE, "Sales_TA", each if [Z_Valid] = 1 then [Net_Sales] / [Total_Assets] else null, type number),
    AddZ = Table.AddColumn(AddSales, "Altman_Z", each if [Z_Valid] = 1 then 1.2 * [WC_TA] + 1.4 * [RE_TA] + 3.3 * [EBIT_TA] + 0.6 * [MVE_TL] + 1.0 * [Sales_TA] else null, type number),
    AddZone = Table.AddColumn(AddZ, "Zone", each if [Z_Valid] = 0 then "Excluded" else if [Altman_Z] > 2.99 then "Safe" else if [Altman_Z] >= 1.81 then "Grey" else "Distress", type text)
in
    AddZone;

shared Company_Scores = let
    Source = american_bankruptcy,
    Latest = Table.SelectRows(Source, each [Is_Last_Year] = 1 and [Z_Valid] = 1),
    Sorted = Table.Sort(Latest, {{"Altman_Z", Order.Ascending}}),
    Indexed = Table.AddIndexColumn(Sorted, "Risk_Rank", 1, 1, Int64.Type),
    TotalRows = Table.RowCount(Indexed),
    Decile = Table.AddColumn(Indexed, "Risk_Decile", each Number.RoundUp([Risk_Rank] * 10 / TotalRows), Int64.Type),
    Keep = Table.SelectColumns(Decile, {"company_name", "status_label", "year", "Failed_Flag", "Total_Assets", "Total_Liabilities", "Net_Sales", "Net_Income", "WC_TA", "RE_TA", "EBIT_TA", "MVE_TL", "Sales_TA", "Altman_Z", "Zone", "Risk_Rank", "Risk_Decile"})
in
    Keep;