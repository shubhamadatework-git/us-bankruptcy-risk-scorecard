#!/usr/bin/env python3
"""
make_charts.py
==============
Re-creates the scorecard's headline charts as PNGs (for the README) from the raw CSV.
The numbers are produced by the same logic as the workbook's Power Query and are
verified against it by `validate_scorecard.py`.

    python src/make_charts.py --csv data/raw/american_bankruptcy.csv --out images/generated
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from validate_scorecard import score  # noqa: E402

BG, PANEL, FG, GRID = "#1F2937", "#374151", "#F9FAFB", "#6B7280"
RED, GREEN, AMBER, BLUE = "#DC2626", "#16A34A", "#F59E0B", "#60A5FA"


def style(ax, title):
    ax.set_facecolor(PANEL)
    ax.figure.set_facecolor(BG)
    ax.set_title(title, color=FG, fontsize=13, pad=12, fontweight="bold")
    ax.tick_params(colors=FG)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.grid(axis="y", color=GRID, alpha=0.4, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.xaxis.label.set_color(FG)
    ax.yaxis.label.set_color(FG)


def save(fig, out: Path, name: str):
    fig.tight_layout()
    fig.savefig(out / name, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print("wrote", out / name)


def main(csv: str, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    _, c = score(csv)
    n, f = len(c), int(c.Failed_Flag.sum())

    # 1 - bankruptcy rate by decile
    t = c.groupby("Risk_Decile").Failed_Flag.agg(["size", "sum"])
    rate = t["sum"] / t["size"]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    bars = ax.bar(rate.index.astype(str), rate.values * 100, color=BLUE, width=0.7)
    ax.axhline(f / n * 100, color=AMBER, linestyle="--", linewidth=1.5, label=f"Overall rate {f / n:.1%}")
    for b, v in zip(bars, rate.values):
        ax.text(b.get_x() + b.get_width() / 2, v * 100 + 0.3, f"{v:.1%}", ha="center", color=FG, fontsize=8)
    style(ax, "Bankruptcy rate by risk decile (1 = riskiest)")
    ax.set_xlabel("Risk decile (by Altman Z, ascending)")
    ax.set_ylabel("% of companies bankrupt")
    ax.legend(facecolor=PANEL, edgecolor="none", labelcolor=FG)
    save(fig, out, "chart_decile_rate.png")

    # 2 - cumulative gains
    cap = t["sum"].cumsum() / f
    rev = (t["size"].cumsum() / n)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot([0] + list(rev.values * 100), [0] + list(cap.values * 100), color=GREEN, marker="o", linewidth=2.2, label="Scorecard")
    ax.plot([0, 100], [0, 100], color=GRID, linestyle="--", label="Random")
    ax.annotate(f"{cap.loc[3]:.0%} of bankruptcies\nin riskiest 30%", xy=(rev.loc[3] * 100, cap.loc[3] * 100),
                xytext=(38, 38), color=FG, arrowprops=dict(arrowstyle="->", color=FG))
    style(ax, "Cumulative gains: bankruptcies captured")
    ax.set_xlabel("% of companies reviewed (riskiest first)")
    ax.set_ylabel("% of bankruptcies captured")
    ax.legend(facecolor=PANEL, edgecolor="none", labelcolor=FG, loc="lower right")
    save(fig, out, "chart_cumulative_gains.png")

    # 3 - bankruptcies by year
    by = c[c.Failed_Flag == 1].groupby("year").size().reindex(range(1999, 2019), fill_value=0)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(by.index, by.values, color=RED, marker="o", linewidth=2.2)
    ax.fill_between(by.index, by.values, color=RED, alpha=0.18)
    pk = by.idxmax()
    ax.annotate(f"peak {int(by.max())} ({pk})", xy=(pk, by.max()), xytext=(pk + 1.2, by.max() - 4), color=FG)
    style(ax, "Bankruptcies by final reported year")
    ax.set_xticks(range(1999, 2019, 3))
    save(fig, out, "chart_bankruptcies_by_year.png")

    # 4 - zone validation
    z = c.groupby("Zone").Failed_Flag.agg(["size", "sum"]).reindex(["Distress", "Grey", "Safe"])
    zr = z["sum"] / z["size"]
    fig, ax = plt.subplots(figsize=(7, 4.2))
    bars = ax.bar(zr.index, zr.values * 100, color=[RED, AMBER, GREEN], width=0.55)
    for b, v, (cnt, bk) in zip(bars, zr.values, z.itertuples(index=False)):
        ax.text(b.get_x() + b.get_width() / 2, v * 100 + 0.25, f"{v:.1%}\n({bk}/{cnt:,})", ha="center", color=FG, fontsize=9)
    style(ax, "Bankruptcy rate by Altman zone")
    ax.set_ylabel("% of companies bankrupt")
    ax.set_ylim(0, zr.max() * 100 * 1.25)
    save(fig, out, "chart_zone_validation.png")

    # 5 - median ratios
    cols = [("WC_TA", "Working capital\n/ assets"), ("RE_TA", "Retained earn.\n/ assets"), ("EBIT_TA", "EBIT\n/ assets"),
            ("MVE_TL", "Market value\n/ liabilities"), ("Sales_TA", "Sales\n/ assets")]
    h = [c[c.status_label == "alive"][k].median() for k, _ in cols]
    fl = [c[c.status_label == "failed"][k].median() for k, _ in cols]
    x = np.arange(len(cols))
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.bar(x - 0.19, h, 0.38, color=GREEN, label="Healthy")
    ax.bar(x + 0.19, fl, 0.38, color=RED, label="Failed")
    ax.axhline(0, color=FG, linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels([l for _, l in cols], fontsize=8)
    style(ax, "Median ratios: failed vs healthy companies")
    ax.legend(facecolor=PANEL, edgecolor="none", labelcolor=FG)
    save(fig, out, "chart_median_ratios.png")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="data/raw/american_bankruptcy.csv")
    ap.add_argument("--out", default="images/generated")
    a = ap.parse_args()
    main(a.csv, Path(a.out))
