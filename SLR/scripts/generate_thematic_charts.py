"""
generate_thematic_charts.py
Phase F2 — Thematic Synthesis Visualization
Produces 6 evidence charts for the IS SLR thematic analysis section.

Method basis:
  Thomas & Harden (2008) BMC Medical Research Methodology 8:45
  Paré et al. (2015) Information & Management 52(2)
  Webster & Watson (2002) MIS Quarterly 26(2)

Outputs (all to SLR/analysis/themes/charts/):
  Fig1  theme_distribution.png       — N papers per descriptive theme
  Fig2  rq_theme_heatmap.png         — Theme × RQ evidence coverage matrix
  Fig3  operationalization_chasm.png — Analytical Theme AT1: method vs IS-theory quadrant map
  Fig4  evidence_density_rq.png      — Evidence density per RQ (shows thin DT7 Silencing gap)
  Fig5  corpus_domain_timeline.png   — ML/technical vs IS-governance papers by year
  Fig6  prisma_flow.png              — PRISMA 2020 screening flow
"""

from __future__ import annotations

import os
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
from matplotlib.patches import FancyArrowPatch
import numpy as np
import pandas as pd
import seaborn as sns

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
CODED_CSV    = ROOT / "SLR/scripts/output/coded_corpus.csv"
DT_MATRIX    = ROOT / "SLR/analysis/themes/descriptive_themes_matrix.csv"
OUT_DIR      = ROOT / "SLR/analysis/themes/charts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Style ──────────────────────────────────────────────────────────────────────
PALETTE_RQ = {"RQ1": "#2196F3", "RQ2": "#FF9800", "RQ3": "#4CAF50",
              "RQ1, RQ3": "#9C27B0", "RQ2, RQ3": "#E91E63",
              "RQ1, RQ2": "#00BCD4", "RQ1 (boundary)": "#90CAF9"}
FONT = {"family": "DejaVu Sans"}
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False,
                      "axes.spines.right": False, "figure.dpi": 150})

# ── Load data ──────────────────────────────────────────────────────────────────
df_coded = pd.read_csv(CODED_CSV)
df_inc   = df_coded[df_coded["coder1_screen"] == "INCLUDE"].copy()
df_dt    = pd.read_csv(DT_MATRIX)

print(f"[INFO] Included papers: {len(df_inc)}")
print(f"[INFO] Descriptive themes: {len(df_dt)}")


# ══════════════════════════════════════════════════════════════════════════════
# Fig 1 — Descriptive Theme Distribution (N papers per theme)
# ══════════════════════════════════════════════════════════════════════════════
def fig1_theme_distribution():
    fig, ax = plt.subplots(figsize=(10, 6))

    df_plot = df_dt.sort_values("n_papers", ascending=True).copy()

    short_labels = {
        "DT1": "DT1 — Operationalizing corruption signals",
        "DT2": "DT2 — Unsupervised ML anomaly detection",
        "DT3": "DT3 — Supervised fraud detection (private)",
        "DT4": "DT4 — Label scarcity / ground-truth barrier",
        "DT5": "DT5 — Village fund governance & corruption",
        "DT6": "DT6 — IS-theoretical framing",
        "DT7": "DT7 — Real-time deployment gap",
        "DT8": "DT8 — Developing-country applicability",
        "DT9": "DT9 — Graph / network-based detection",
        "DT10": "DT10 — Explainability & audit trail",
    }
    labels = [short_labels.get(r, r) for r in df_plot["dt_id"]]
    colors = [PALETTE_RQ.get(r, "#78909C") for r in df_plot["rq_map"]]
    bars   = ax.barh(labels, df_plot["n_papers"], color=colors, edgecolor="white",
                     linewidth=0.5, height=0.65)

    for bar, n in zip(bars, df_plot["n_papers"]):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                str(n), va="center", fontsize=9, color="#333333")

    # Annotation for DT7 thin evidence
    dt7_idx = list(df_plot["dt_id"]).index("DT7")
    ax.annotate("← Silencing gap\n(only 4 papers; real-time\ndeployment unaddressed)",
                xy=(df_plot[df_plot.dt_id == "DT7"]["n_papers"].values[0], dt7_idx),
                xytext=(12, dt7_idx),
                fontsize=8, color="#B71C1C",
                arrowprops=dict(arrowstyle="->", color="#B71C1C", lw=1.2))

    # Legend
    legend_entries = [
        mpatches.Patch(color=PALETTE_RQ["RQ1"], label="RQ1 — Method landscape"),
        mpatches.Patch(color=PALETTE_RQ["RQ2"], label="RQ2 — Corruption operationalization"),
        mpatches.Patch(color=PALETTE_RQ["RQ3"], label="RQ3 — Gaps & applicability"),
        mpatches.Patch(color=PALETTE_RQ["RQ1, RQ3"], label="RQ1 + RQ3"),
        mpatches.Patch(color=PALETTE_RQ["RQ2, RQ3"], label="RQ2 + RQ3"),
        mpatches.Patch(color=PALETTE_RQ["RQ1 (boundary)"], label="RQ1 (boundary)"),
    ]
    ax.legend(handles=legend_entries, loc="lower right", fontsize=8,
              framealpha=0.85, edgecolor="#CCCCCC")

    ax.set_xlabel("Number of contributing papers", fontsize=10)
    ax.set_title("Figure 1 — Descriptive Theme Distribution\n"
                 "(Thomas & Harden, 2008, Stage 2: Descriptive Themes; N=45 included papers)",
                 fontsize=11, pad=12)
    ax.set_xlim(0, 32)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
    ax.grid(axis="x", linestyle="--", linewidth=0.5, alpha=0.6)

    plt.tight_layout()
    out = OUT_DIR / "Fig1_theme_distribution.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Fig1 → {out}")


# ══════════════════════════════════════════════════════════════════════════════
# Fig 2 — Theme × RQ Evidence Coverage Heatmap
# ══════════════════════════════════════════════════════════════════════════════
def fig2_rq_theme_heatmap():
    # Build matrix manually from the DT data
    # Each DT's rq_map tells us which RQs it contributes to
    dt_order = [f"DT{i}" for i in range(1, 11)]
    dt_labels = {
        "DT1": "DT1 — Corruption signals", "DT2": "DT2 — Unsupervised ML",
        "DT3": "DT3 — Supervised fraud", "DT4": "DT4 — Label scarcity",
        "DT5": "DT5 — Village governance", "DT6": "DT6 — IS theory framing",
        "DT7": "DT7 — Real-time gap", "DT8": "DT8 — Dev-country limits",
        "DT9": "DT9 — Graph methods", "DT10": "DT10 — Explainability",
    }
    rqs = ["RQ1", "RQ2", "RQ3"]
    rq_map_dict = dict(zip(df_dt["dt_id"], df_dt["rq_map"]))
    n_papers_dict = dict(zip(df_dt["dt_id"], df_dt["n_papers"]))

    # Build matrix: cell = n_papers if that DT contributes to that RQ, else 0
    matrix = []
    for dt in dt_order:
        rq_str = str(rq_map_dict.get(dt, ""))
        row = []
        for rq in rqs:
            if rq in rq_str:
                row.append(n_papers_dict.get(dt, 0))
            else:
                row.append(0)
        matrix.append(row)

    mat = np.array(matrix, dtype=float)
    mat_masked = np.where(mat == 0, np.nan, mat)

    fig, ax = plt.subplots(figsize=(7, 7))
    cmap = sns.color_palette("Blues", as_cmap=True)
    cmap.set_bad("white")

    im = ax.imshow(mat_masked, cmap="Blues", aspect="auto", vmin=0, vmax=30)

    # Cell annotations
    for i in range(len(dt_order)):
        for j in range(len(rqs)):
            val = matrix[i][j]
            if val > 0:
                color = "white" if val > 18 else "#333333"
                ax.text(j, i, str(val), ha="center", va="center",
                        fontsize=11, fontweight="bold", color=color)
            else:
                ax.text(j, i, "—", ha="center", va="center",
                        fontsize=10, color="#CCCCCC")

    ax.set_xticks(range(3))
    ax.set_xticklabels(["RQ1\nMethod landscape", "RQ2\nCorruption operationalization",
                         "RQ3\nGaps & applicability"], fontsize=10)
    ax.set_yticks(range(len(dt_order)))
    ax.set_yticklabels([dt_labels[d] for d in dt_order], fontsize=9)
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position("top")

    plt.colorbar(im, ax=ax, label="N contributing papers", shrink=0.6, pad=0.02)
    ax.set_title("Figure 2 — Theme × Research Question Evidence Coverage Matrix\n"
                 "(cell = number of papers in that theme contributing to each RQ;\n"
                 "blank = theme does not address that RQ)",
                 fontsize=10, pad=30)

    # Draw red border around RQ3-DT7 (Silencing)
    rect = plt.Rectangle((2 - 0.5, 6 - 0.5), 1, 1,
                          linewidth=2.5, edgecolor="#B71C1C", facecolor="none")
    ax.add_patch(rect)
    ax.text(2.5, 6, "← Silencing\n(n=4)", fontsize=7.5, color="#B71C1C", va="center")

    plt.tight_layout()
    out = OUT_DIR / "Fig2_rq_theme_heatmap.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Fig2 → {out}")


# ══════════════════════════════════════════════════════════════════════════════
# Fig 3 — "The Operationalization Chasm" — Analytical Theme AT1 Quadrant Map
# ══════════════════════════════════════════════════════════════════════════════
def fig3_operationalization_chasm():
    """
    2×2 quadrant: X = Has computational method (0/1), Y = Has IS theory (0/1)
    Maps 45 included papers to quadrants based on theme_tags content.
    """
    def has_comp(tags: str) -> bool:
        comp_tags = {"anomaly_detection", "deep_learning", "random_forest", "ensemble",
                     "isolation_forest", "svm", "cnn", "lstm", "gnn", "aml",
                     "transformer_bert", "federated_learning", "quantum_ml",
                     "fraud_detection", "financial_fraud"}
        t = set(str(tags).lower().split("|"))
        return bool(t & comp_tags)

    def has_is_theory(tags: str) -> bool:
        is_tags = {"internal_control", "whistleblowing", "dana_desa", "corruption",
                   "government_finance", "public_procurement", "accounting_audit",
                   "tax_revenue", "scalability_gap"}
        t = set(str(tags).lower().split("|"))
        return bool(t & is_tags)

    df_q = df_inc.copy()
    df_q["comp"] = df_q["theme_tags"].apply(has_comp)
    df_q["is_t"] = df_q["theme_tags"].apply(has_is_theory)

    q = {
        "Q1": df_q[df_q.comp & ~df_q.is_t],     # ML only — no governance
        "Q2": df_q[df_q.comp & df_q.is_t],       # Bridging — both
        "Q3": df_q[~df_q.comp & ~df_q.is_t],     # Neither
        "Q4": df_q[~df_q.comp & df_q.is_t],      # IS/governance only — no ML
    }

    fig, ax = plt.subplots(figsize=(9, 8))

    # Quadrant backgrounds
    ax.axvspan(0.5, 2.0, ymin=0.5, ymax=1.0, color="#E3F2FD", alpha=0.7, zorder=0)  # Q1
    ax.axvspan(0.5, 2.0, ymin=0.0, ymax=0.5, color="#FFF3E0", alpha=0.7, zorder=0)  # Q2
    ax.axvspan(-1.0, 0.5, ymin=0.5, ymax=1.0, color="#F5F5F5", alpha=0.7, zorder=0) # Q3
    ax.axvspan(-1.0, 0.5, ymin=0.0, ymax=0.5, color="#E8F5E9", alpha=0.7, zorder=0) # Q4

    # Jitter to separate overlapping points
    rng = np.random.default_rng(42)

    def jitter(n, center, spread=0.25):
        return rng.uniform(center - spread, center + spread, n)

    # Q1: comp=True, is_t=False  → x~1.2, y~0.75
    ax.scatter(jitter(len(q["Q1"]), 1.2), jitter(len(q["Q1"]), 0.75),
               s=90, color="#1565C0", alpha=0.75, zorder=3, label=f"ML-only (no IS theory) — n={len(q['Q1'])}")
    # Q2: both → x~1.2, y~0.25
    ax.scatter(jitter(len(q["Q2"]), 1.2), jitter(len(q["Q2"]), 0.25),
               s=120, color="#2E7D32", marker="D", alpha=0.85, zorder=4,
               label=f"Bridging (ML + IS theory) — n={len(q['Q2'])}")
    # Q3: neither → x~-0.2, y~0.75
    ax.scatter(jitter(len(q["Q3"]), -0.2), jitter(len(q["Q3"]), 0.75),
               s=70, color="#9E9E9E", alpha=0.65, zorder=3,
               label=f"Peripheral (neither) — n={len(q['Q3'])}")
    # Q4: is_t only → x~-0.2, y~0.25
    ax.scatter(jitter(len(q["Q4"]), -0.2), jitter(len(q["Q4"]), 0.25),
               s=90, color="#E65100", marker="s", alpha=0.75, zorder=3,
               label=f"Governance-only (no ML method) — n={len(q['Q4'])}")

    # Quadrant labels
    quad_kw = dict(ha="center", fontsize=12, fontweight="bold", alpha=0.55, zorder=2)
    ax.text(1.2, 0.92, f"ML-Only\nn={len(q['Q1'])}", color="#1565C0", **quad_kw)
    ax.text(1.2, 0.08, f"Bridging\nn={len(q['Q2'])}", color="#2E7D32", **quad_kw)
    ax.text(-0.2, 0.92, f"Peripheral\nn={len(q['Q3'])}", color="#757575", **quad_kw)
    ax.text(-0.2, 0.08, f"Governance-Only\nn={len(q['Q4'])}", color="#E65100", **quad_kw)

    # Dividers
    ax.axhline(0.5, color="#BDBDBD", linestyle="--", linewidth=1.5, zorder=1)
    ax.axvline(0.5, color="#BDBDBD", linestyle="--", linewidth=1.5, zorder=1)

    # THE CHASM ARROW
    ax.annotate("", xy=(-0.1, 0.5), xytext=(0.9, 0.5),
                arrowprops=dict(arrowstyle="<->", color="#B71C1C", lw=2.5))
    ax.text(0.4, 0.54, "THE OPERATIONALIZATION CHASM", ha="center", fontsize=9.5,
            color="#B71C1C", fontweight="bold", style="italic", zorder=5)
    ax.text(0.4, 0.45,
            "No paper bridges computational\nML and village-level IS governance\nin a single study design",
            ha="center", fontsize=8, color="#B71C1C", zorder=5)

    ax.set_xlim(-1.0, 2.0)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks([0.5])
    ax.set_xticklabels([])
    ax.set_yticks([0.5])
    ax.set_yticklabels([])
    ax.set_xlabel("← No computational method         Has computational ML method →",
                  fontsize=10)
    ax.set_ylabel("← No IS-theoretical framing         Has IS-theoretical grounding →",
                  fontsize=10)
    ax.legend(loc="upper left", fontsize=8.5, framealpha=0.9, edgecolor="#CCCCCC")
    ax.set_title("Figure 3 — Analytical Theme AT1: The Operationalization Chasm\n"
                 "(Quadrant distribution of 45 included papers: computational method presence vs IS-theoretical grounding)",
                 fontsize=10, pad=12)

    plt.tight_layout()
    out = OUT_DIR / "Fig3_operationalization_chasm.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Fig3 → {out}")
    print(f"      Q1 ML-only={len(q['Q1'])}, Q2 Bridge={len(q['Q2'])}, "
          f"Q3 Neither={len(q['Q3'])}, Q4 Gov-only={len(q['Q4'])}")


# ══════════════════════════════════════════════════════════════════════════════
# Fig 4 — Evidence Density per RQ (shows Silencing gaps)
# ══════════════════════════════════════════════════════════════════════════════
def fig4_evidence_density_rq():
    # Per-RQ: total evidence (papers addressing that RQ)
    # and thin vs rich themes
    rq_themes = {
        "RQ1": [("DT2", 18), ("DT3", 22), ("DT9", 20), ("DT6", 17),
                ("DT10", 7), ("DT1", 16)],
        "RQ2": [("DT1", 16), ("DT5", 26)],
        "RQ3": [("DT4", 19), ("DT8", 18), ("DT6", 17), ("DT10", 7),
                ("DT5", 26), ("DT7", 4)],
    }

    thin_threshold = 6   # below this = evidence-thin

    fig, axes = plt.subplots(1, 3, figsize=(13, 5.5), sharey=False)
    rq_colors = {"RQ1": "#2196F3", "RQ2": "#FF9800", "RQ3": "#4CAF50"}
    rq_titles = {
        "RQ1": "RQ1\nMethod Landscape",
        "RQ2": "RQ2\nCorruption\nOperationalization",
        "RQ3": "RQ3\nGaps & Applicability",
    }

    for ax, (rq, themes) in zip(axes, rq_themes.items()):
        labels = [t[0] for t in themes]
        vals   = [t[1] for t in themes]
        colors = ["#EF9A9A" if v <= thin_threshold else rq_colors[rq] for v in vals]

        bars = ax.bar(labels, vals, color=colors, edgecolor="white", linewidth=0.8)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                    str(v), ha="center", va="bottom", fontsize=10, fontweight="bold")

        ax.axhline(thin_threshold, color="#B71C1C", linestyle=":", linewidth=1.5,
                   label=f"Thin evidence (≤{thin_threshold})")
        ax.set_title(rq_titles[rq], fontsize=11, fontweight="bold",
                     color=rq_colors[rq])
        ax.set_ylabel("N papers" if rq == "RQ1" else "", fontsize=9)
        ax.set_ylim(0, 35)
        ax.yaxis.set_major_locator(mticker.MultipleLocator(5))
        ax.grid(axis="y", linestyle="--", linewidth=0.4, alpha=0.6)

        # Silencing annotation for DT7 in RQ3
        if rq == "RQ3":
            dt7_pos = labels.index("DT7")
            ax.text(dt7_pos, vals[dt7_pos] + 1.5,
                    "Silencing\ngap ↑", ha="center", fontsize=7.5,
                    color="#B71C1C", fontweight="bold")
            ax.legend(fontsize=8, loc="upper right")

    fig.suptitle(
        "Figure 4 — Evidence Density per Research Question\n"
        "(red bars = thin evidence ≤6 papers; dashed line = thin-evidence threshold;\n"
        " DT7 in RQ3 = Silencing gap: real-time deployment addressed by only 4 papers)",
        fontsize=10, y=1.02,
    )
    plt.tight_layout()
    out = OUT_DIR / "Fig4_evidence_density_rq.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Fig4 → {out}")


# ══════════════════════════════════════════════════════════════════════════════
# Fig 5 — Corpus Domain Timeline (ML/technical vs IS-governance by year)
# ══════════════════════════════════════════════════════════════════════════════
def fig5_domain_timeline():
    def classify_domain(row):
        tags = str(row.get("theme_tags", "")).lower()
        dana  = any(k in tags for k in ["dana_desa", "corruption", "internal_control",
                                          "whistleblowing", "government_finance",
                                          "public_procurement", "accounting_audit"])
        ml    = any(k in tags for k in ["deep_learning", "anomaly_detection", "cnn",
                                          "lstm", "gnn", "ensemble", "random_forest",
                                          "isolation_forest", "federated_learning",
                                          "aml", "transformer_bert"])
        if dana and ml:
            return "Bridging"
        elif dana:
            return "IS Governance"
        elif ml:
            return "ML / Technical"
        else:
            return "Other"

    df_q = df_inc.copy()
    df_q["domain"] = df_q.apply(classify_domain, axis=1)
    df_q["year_int"] = df_q["year"].astype(float).astype(int)

    domain_order  = ["ML / Technical", "Bridging", "IS Governance", "Other"]
    domain_colors = {"ML / Technical": "#1565C0", "Bridging": "#2E7D32",
                     "IS Governance": "#E65100", "Other": "#9E9E9E"}

    years = sorted(df_q["year_int"].unique())
    pivot = df_q.groupby(["year_int", "domain"]).size().unstack(fill_value=0)
    for col in domain_order:
        if col not in pivot.columns:
            pivot[col] = 0
    pivot = pivot[domain_order]

    fig, ax = plt.subplots(figsize=(11, 5.5))
    bottom = np.zeros(len(pivot))
    for domain in domain_order:
        vals = pivot[domain].values
        ax.bar(pivot.index, vals, bottom=bottom,
               color=domain_colors[domain], label=domain,
               edgecolor="white", linewidth=0.6, alpha=0.88)
        bottom += vals

    # Annotate the gap — no bridging papers before 2023
    ax.annotate("Village fund governance\nliterature emerges 2022+",
                xy=(2022, 3.5), xytext=(2018.5, 10),
                fontsize=8.5, color="#E65100",
                arrowprops=dict(arrowstyle="->", color="#E65100", lw=1.2))

    ax.set_xlabel("Publication Year", fontsize=10)
    ax.set_ylabel("Number of included papers", fontsize=10)
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45, ha="right")
    ax.yaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.legend(title="Domain cluster", fontsize=9, title_fontsize=9,
              loc="upper left", framealpha=0.9)
    ax.grid(axis="y", linestyle="--", linewidth=0.4, alpha=0.6)
    ax.set_title("Figure 5 — Corpus Domain Cluster Distribution by Year\n"
                 "(ML/Technical vs IS-Governance/Dana Desa — N=45 included papers;\n"
                 " illustrates temporal gap in bridging literature)",
                 fontsize=10, pad=12)

    plt.tight_layout()
    out = OUT_DIR / "Fig5_corpus_domain_timeline.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    print(f"[OK] Fig5 → {out}")


# ══════════════════════════════════════════════════════════════════════════════
# Fig 6 — PRISMA 2020 Screening Flow Diagram
# ══════════════════════════════════════════════════════════════════════════════
def fig6_prisma_flow():
    # ── Canvas & coordinate system ────────────────────────────────────────────
    # xlim 0-15: main boxes at x=7.2 (w=9.0) span 2.7-11.7;
    #            side boxes at x=13.5 (w=2.8) span 12.1-14.9 — no clipping needed
    # ylim 0-26: stages at uniform 2.6-unit spacing, BH=1.0 → 1.6-unit arrow gaps
    fig, ax = plt.subplots(figsize=(13, 18))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 26.5)
    ax.axis("off")

    MX  = 7.2    # main box center x
    MW  = 9.0    # main box width
    EX  = 13.5   # exclusion / side-note box center x
    EW  = 2.8    # exclusion box width
    LX  = 0.85   # phase label center x (rotated 90°)
    BH  = 1.0    # uniform box height

    # Stage y-centers (uniform 2.6-unit spacing)
    Y_TITLE  = 25.5
    Y_IDENT  = 23.5
    Y_SCREEN = 20.9
    Y_QUAL   = 18.3
    Y_OVER   = 15.7
    Y_INCL   = 13.1
    Y_PDF    = 10.5
    Y_SYNTH  =  7.9
    Y_SPLIT  =  5.3   # center y of the two side-by-side threshold boxes
    Y_OUT    =  2.7

    # ── Style dict ────────────────────────────────────────────────────────────
    S = {
        "main":  dict(boxstyle="round,pad=0.45", facecolor="white",
                      edgecolor="#455A64", linewidth=1.6),
        "exc":   dict(boxstyle="round,pad=0.38", facecolor="#FFEBEE",
                      edgecolor="#C62828", linewidth=1.2),
        "pend":  dict(boxstyle="round,pad=0.38", facecolor="#FFF8E1",
                      edgecolor="#F9A825", linewidth=1.2),
        "incl":  dict(boxstyle="round,pad=0.45", facecolor="#E8F5E9",
                      edgecolor="#2E7D32", linewidth=1.6),
        "final": dict(boxstyle="round,pad=0.45", facecolor="#E8EAF6",
                      edgecolor="#3F51B5", linewidth=2.2),
    }

    # ── Helper functions ──────────────────────────────────────────────────────
    def draw_box(x, y, w, h, text, style="main", fsize=9):
        patch = mpatches.FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            **S[style], transform=ax.transData, clip_on=False)
        ax.add_patch(patch)
        ax.text(x, y, text, ha="center", va="center", fontsize=fsize,
                multialignment="center", color="#212121", clip_on=False)

    def darrow(x1, y1, x2, y2, color="#455A64"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=color,
                                    lw=1.6, mutation_scale=15),
                    annotation_clip=False)

    def seg(x1, y1, x2, y2, color="#455A64", lw=1.6):
        ax.plot([x1, x2], [y1, y2], color=color, lw=lw, clip_on=False)

    def phase_lbl(y, text, color="#455A64"):
        ax.text(LX, y, text, fontsize=8, fontweight="bold", color=color,
                rotation=90, va="center", ha="center", clip_on=False)

    def exc_side(main_y, text, fsize=8):
        """Arrow right from main box edge → exclusion box."""
        darrow(MX + MW / 2, main_y, EX - EW / 2, main_y, color="#C62828")
        draw_box(EX, main_y, EW, BH, text, style="exc", fsize=fsize)

    # ── TITLE ─────────────────────────────────────────────────────────────────
    ax.text(MX, Y_TITLE, "PRISMA 2020 Screening Flow Diagram",
            ha="center", va="center", fontsize=14, fontweight="bold",
            color="#1A237E")

    # ── IDENTIFICATION ────────────────────────────────────────────────────────
    phase_lbl(Y_IDENT, "IDENTIFICATION")
    draw_box(MX, Y_IDENT, MW, BH,
             "Database search: OpenAlex API — 5 query strings\n"
             "Initial records: 1,001  →  945 unique after deduplication")
    # Pending manual search: side note (orange/warning), not in main flow
    darrow(MX + MW / 2, Y_IDENT, EX - EW / 2, Y_IDENT, color="#F9A825")
    draw_box(EX, Y_IDENT, EW, BH,
             "⚠ Manual export\n(Scopus / IEEE / WoS)\nPENDING",
             style="pend", fsize=8)

    # ── SCREENING ─────────────────────────────────────────────────────────────
    phase_lbl(Y_SCREEN, "SCREENING\nStage 1")
    darrow(MX, Y_IDENT - BH / 2, MX, Y_SCREEN + BH / 2)
    draw_box(MX, Y_SCREEN, MW, BH,
             "Title + Abstract screening against inclusion / exclusion criteria\n"
             "N = 945 records evaluated by automated pipeline")
    exc_side(Y_SCREEN, "Excluded: 21\nEC-07 IoT/cyber: 14\nEC-02 domain mismatch: 7")

    # ── QUALITY FILTER ────────────────────────────────────────────────────────
    phase_lbl(Y_QUAL, "QUALITY\nFILTER")
    darrow(MX, Y_SCREEN - BH / 2, MX, Y_QUAL + BH / 2)
    draw_box(MX, Y_QUAL, MW, BH,
             "Composite quality scoring — quality_filter_slr.py  (score 0–10)\n"
             "Inclusion threshold: ≥ 5.0  |  Pipeline version 3")
    exc_side(Y_QUAL, "Below threshold: 900\n(score < 5.0)\n→ slr_excluded_log.csv")

    # ── DOMAIN OVERRIDE ───────────────────────────────────────────────────────
    phase_lbl(Y_OVER, "DOMAIN\nOVERRIDE")
    darrow(MX, Y_QUAL - BH / 2, MX, Y_OVER + BH / 2)
    draw_box(MX, Y_OVER, MW, BH,
             "Domain relevance adjudication — village fund / Dana Desa literature\n"
             "12 high-relevance papers: quality score overridden to 6.0")
    exc_side(Y_OVER, "Not overridden: 15\n(MEDIUM relevance;\ncriteria not met)")

    # ── INCLUDED CORPUS ───────────────────────────────────────────────────────
    phase_lbl(Y_INCL, "INCLUDED\nCORPUS", color="#1B5E20")
    darrow(MX, Y_OVER - BH / 2, MX, Y_INCL + BH / 2)
    draw_box(MX, Y_INCL, MW, BH,
             "N = 56 papers in coded corpus\n"
             "(45 pipeline-passed  +  12 domain-overridden  −  1 permanently inaccessible)",
             style="incl")

    # ── PDF ACQUISITION ───────────────────────────────────────────────────────
    phase_lbl(Y_PDF, "PDF\nACQUISITION")
    darrow(MX, Y_INCL - BH / 2, MX, Y_PDF + BH / 2)
    draw_box(MX, Y_PDF, MW, BH,
             "44 / 56 full-text PDFs confirmed on disk\n"
             "1 permanently blocked (publisher paywall);  11 proceeding on abstract only")
    exc_side(Y_PDF, "PDF unavailable: 1\nPublisher paywall\n(restricted access)")

    # ── SYNTHESIS ─────────────────────────────────────────────────────────────
    phase_lbl(Y_SYNTH, "SYNTHESIS\nPhase F", color="#1A237E")
    darrow(MX, Y_PDF - BH / 2, MX, Y_SYNTH + BH / 2)
    draw_box(MX, Y_SYNTH, MW, BH,
             "Thematic Synthesis — Thomas & Harden (2008)\n"
             "Stage 1: Open coding  →  Stage 2: Descriptive themes  →  Stage 3: Analytical themes")

    # ── THRESHOLD SPLIT ───────────────────────────────────────────────────────
    # Vertical stem from synthesis bottom to the horizontal branch
    stem_y  = (Y_SYNTH - BH / 2 + Y_SPLIT + BH / 2) / 2   # midpoint
    LBX, RBX, SBW = 4.6, 9.8, 4.2   # left/right box centers and width
    # left: 2.5–6.7  right: 7.7–11.9  gap = 1.0  — no overlap

    seg(MX, Y_SYNTH - BH / 2, MX, stem_y)        # vertical stem
    seg(LBX, stem_y, RBX, stem_y)                 # horizontal branch
    darrow(LBX, stem_y, LBX, Y_SPLIT + BH / 2)   # left drop arrow
    darrow(RBX, stem_y, RBX, Y_SPLIT + BH / 2)   # right drop arrow

    draw_box(LBX, Y_SPLIT, SBW, BH,
             "Primary analysis\nThreshold ≥ 5.5\nN = 31 papers")
    draw_box(RBX, Y_SPLIT, SBW, BH,
             "Sensitivity bounds\n≥ 5.0 (N=56)  |  ≥ 6.0 (N=23)\nPhase F6 robustness check")

    # Convergence from both boxes to final output
    conv_y = (Y_SPLIT - BH / 2 + Y_OUT + BH / 2) / 2
    seg(LBX, Y_SPLIT - BH / 2, LBX, conv_y)
    seg(RBX, Y_SPLIT - BH / 2, RBX, conv_y)
    seg(LBX, conv_y, RBX, conv_y)                 # horizontal convergence bar
    darrow(MX, conv_y, MX, Y_OUT + BH / 2)        # final arrow down

    # ── FINAL OUTPUT ──────────────────────────────────────────────────────────
    phase_lbl(Y_OUT, "OUTPUT", color="#1A237E")
    draw_box(MX, Y_OUT, MW, BH,
             "SLR Synthesis Output — Peer-reviewed Research Paper\n"
             "RQ1: ML method landscape  ·  RQ2: Corruption operationalization  ·  RQ3: Research gaps",
             style="final", fsize=9)

    plt.tight_layout(pad=0.8)
    out = OUT_DIR / "Fig6_prisma_flow.png"
    fig.savefig(out, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"[OK] Fig6 → {out}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  Phase F2 — Thematic Synthesis Charts")
    print(f"  Output: {OUT_DIR}")
    print("=" * 60)
    fig1_theme_distribution()
    fig2_rq_theme_heatmap()
    fig3_operationalization_chasm()
    fig4_evidence_density_rq()
    fig5_domain_timeline()
    fig6_prisma_flow()
    print("=" * 60)
    print("  All 6 charts generated successfully.")
    print("=" * 60)
