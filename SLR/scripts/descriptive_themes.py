"""
Phase F2.2 — Descriptive Themes Aggregation (Thomas & Harden 2008 Stage 2)
Groups open codes from open_codes_master.csv into descriptive themes.
Each theme: label, contributing papers (N), representative quotes, paper IDs, RQ mapping.

Outputs:
  - SLR/analysis/themes/descriptive_themes.md
  - SLR/analysis/themes/descriptive_themes_matrix.csv
"""

import os
import pandas as pd
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_CSV  = os.path.join(BASE_DIR, "analysis", "themes", "open_codes_master.csv")
CORPUS_CSV  = os.path.join(BASE_DIR, "scripts", "output", "coded_corpus.csv")
OUT_MD      = os.path.join(BASE_DIR, "analysis", "themes", "descriptive_themes.md")
OUT_MATRIX  = os.path.join(BASE_DIR, "analysis", "themes", "descriptive_themes_matrix.csv")

codes_df = pd.read_csv(MASTER_CSV)
corpus_df = pd.read_csv(CORPUS_CSV)
inc = corpus_df[corpus_df["irr_resolution"].isin(["CONSENSUS","DOMAIN_OVERRIDE"])].copy()

# ─────────────────────────────────────────────────────────────────────────────
# DESCRIPTIVE THEME DEFINITIONS
# Each theme: id, label, rq_map, constitutive_codes, description
# constitutive_codes: papers in theme IF they have ANY of these codes
# ─────────────────────────────────────────────────────────────────────────────

DESCRIPTIVE_THEMES = [
    {
        "dt_id": "DT1",
        "label": "Operationalizing corruption as detectable computational signals",
        "rq_map": "RQ2",
        "constitutive_codes": ["FE-RFLAG","FE-BID","FE-AMEND","FE-BUDGET","CTX-PROCU","CTX-GOVPUB"],
        "description": (
            "Papers that operationalize corruption or financial irregularity as measurable "
            "computational features — red flags, bid-rigging signals, contract amendment patterns, "
            "or budget absorption anomalies. Includes procurement fraud detection and government "
            "financial fraud studies that produce explicit feature engineering contributions."
        ),
        "anchor_codes": ["FE-RFLAG","FE-BID","FE-BUDGET"],
    },
    {
        "dt_id": "DT2",
        "label": "Unsupervised ML for financial anomaly detection",
        "rq_map": "RQ1",
        "constitutive_codes": ["MC-IF","MC-LOF","MC-AE","MC-UNSUP","MC-GNN"],
        "description": (
            "Papers applying unsupervised or semi-supervised methods (Isolation Forest, LOF, "
            "Autoencoders, graph-based methods) to detect anomalies without requiring labeled "
            "fraud examples. Directly relevant to contexts where ground truth is unavailable."
        ),
        "anchor_codes": ["MC-IF","MC-LOF","MC-AE"],
    },
    {
        "dt_id": "DT3",
        "label": "Supervised fraud detection in private financial contexts",
        "rq_map": "RQ1 (boundary)",
        "constitutive_codes": ["CTX-BANK","DS-PRIVATE","DS-TRANS","CTX-AML"],
        "description": (
            "Papers applying supervised ML (Random Forest, SVM, deep learning) to private-sector "
            "fraud datasets — credit card transactions, banking, AML, payment fraud. Valuable as "
            "method benchmarks and feature engineering inspiration, but their applicability to "
            "public-sector government financial fraud is structurally limited by dataset differences."
        ),
        "anchor_codes": ["CTX-BANK","DS-PRIVATE"],
    },
    {
        "dt_id": "DT4",
        "label": "Label scarcity and ground truth unavailability as structural barrier",
        "rq_map": "RQ3",
        "constitutive_codes": ["LIM-NOLABEL","AC-LABEL","DS-SYNTH"],
        "description": (
            "Papers acknowledging the absence of labeled fraud data as a critical limitation, "
            "using synthetic datasets as workarounds, or explicitly calling for unsupervised "
            "approaches due to ground truth scarcity. This theme provides the theoretical "
            "justification for unsupervised methods in the Dana Desa context."
        ),
        "anchor_codes": ["LIM-NOLABEL","DS-SYNTH"],
    },
    {
        "dt_id": "DT5",
        "label": "Village fund governance, institutional controls, and corruption patterns",
        "rq_map": "RQ2, RQ3",
        "constitutive_codes": ["CTX-VILLAGE","DS-DANDES","CTX-INDO","DS-GOVERN"],
        "description": (
            "Papers directly addressing Dana Desa (village fund) governance, Indonesian "
            "sub-national public financial management, institutional control mechanisms, "
            "and corruption patterns at the village government level. These papers provide "
            "domain knowledge and contextual grounding for the primary study design."
        ),
        "anchor_codes": ["CTX-VILLAGE","DS-DANDES"],
    },
    {
        "dt_id": "DT6",
        "label": "IS-theoretical framing of detection artifacts and governance systems",
        "rq_map": "RQ1, RQ3",
        "constitutive_codes": ["IST-TAM","IST-TTF","IST-DM","IST-IT","IST-AT","IST-DSR","IST-GRC","IST-UTAUT","IST-FRAUD"],
        "description": (
            "Papers that apply IS theories (Agency Theory, Institutional Theory, TAM, DeLone & McLean "
            "IS Success Model, Design Science Research, GRC frameworks) to frame detection systems "
            "within organizational and governance contexts. Notable for their minority status in "
            "the corpus — most papers are purely technical."
        ),
        "anchor_codes": ["IST-AT","IST-IT","IST-DM"],
    },
    {
        "dt_id": "DT7",
        "label": "Real-time detection and deployment gap in operational governance",
        "rq_map": "RQ3",
        "constitutive_codes": ["GAP-RT","LIM-STATIC","GAP-EXPLAIN"],
        "description": (
            "Papers identifying the gap between research-prototype ML systems and operational "
            "deployment: real-time processing not addressed, static historical datasets used for "
            "validation only, or explainability insufficient for auditor adoption. Critical for "
            "establishing what the primary study's system architecture must address."
        ),
        "anchor_codes": ["GAP-RT","LIM-STATIC"],
    },
    {
        "dt_id": "DT8",
        "label": "Developing-country and sub-national applicability constraints",
        "rq_map": "RQ3",
        "constitutive_codes": ["CTX-DEV","GAP-DC","GAP-VILLAGE","AC-ENGLISH","LIM-SINGLE","LIM-CONTEXT"],
        "description": (
            "Papers explicitly noting inapplicability or untested nature of their approaches "
            "for developing-country or sub-national government contexts — English-language "
            "assumptions, single-country data, Western regulatory contexts, or explicit statements "
            "that village/local government application remains a future work direction."
        ),
        "anchor_codes": ["GAP-DC","GAP-VILLAGE","LIM-SINGLE"],
    },
    {
        "dt_id": "DT9",
        "label": "Graph and network-based fraud detection methods",
        "rq_map": "RQ1",
        "constitutive_codes": ["MC-GNN","FE-NETW","CTX-SHELL"],
        "description": (
            "Papers applying graph-based machine learning (GNNs, GCNs, GATs) or network "
            "analysis to detect fraud through relationship patterns — vendor networks, "
            "shell company structures, beneficial ownership, and inter-entity relationships. "
            "Particularly relevant to procurement collusion detection."
        ),
        "anchor_codes": ["MC-GNN","FE-NETW"],
    },
    {
        "dt_id": "DT10",
        "label": "Explainability, transparency, and audit trail requirements",
        "rq_map": "RQ1, RQ3",
        "constitutive_codes": ["GAP-EXPLAIN","LIM-INTERP","IST-GRC"],
        "description": (
            "Papers addressing or noting the absence of explainability in ML-based fraud "
            "detection — black-box limitations, audit trail requirements for regulatory "
            "compliance, and the tension between predictive performance and interpretability "
            "for human decision-makers."
        ),
        "anchor_codes": ["GAP-EXPLAIN","LIM-INTERP"],
    },
]


def get_papers_for_theme(theme, codes_df):
    """Return set of paper_ids contributing to this theme."""
    mask = codes_df["code"].isin(theme["constitutive_codes"])
    return set(codes_df[mask]["paper_id"].unique())


def get_evidence_for_theme(theme, codes_df, max_quotes=3):
    """Get evidence quotes from anchor codes."""
    anchor_codes = theme.get("anchor_codes", theme["constitutive_codes"][:3])
    mask = codes_df["code"].isin(anchor_codes)
    rows = codes_df[mask].dropna(subset=["evidence_1"])
    rows = rows[rows["evidence_1"].str.len() > 20]
    quotes = []
    for _, row in rows.iterrows():
        q = str(row["evidence_1"]).strip()
        if q and len(quotes) < max_quotes:
            quotes.append((row["paper_id"], row["code"], q))
    return quotes


# ─────────────────────────────────────────────────────────────────────────────
# BUILD THEME TABLE
# ─────────────────────────────────────────────────────────────────────────────

theme_rows = []
for theme in DESCRIPTIVE_THEMES:
    papers = get_papers_for_theme(theme, codes_df)
    evidence = get_evidence_for_theme(theme, codes_df)
    theme_rows.append({
        "dt_id": theme["dt_id"],
        "label": theme["label"],
        "rq_map": theme["rq_map"],
        "n_papers": len(papers),
        "paper_ids": "|".join(sorted(papers)),
        "constitutive_codes": "|".join(theme["constitutive_codes"]),
        "description": theme["description"],
        "evidence_1": f"{evidence[0][0]}: {evidence[0][2]}" if len(evidence) > 0 else "",
        "evidence_2": f"{evidence[1][0]}: {evidence[1][2]}" if len(evidence) > 1 else "",
        "evidence_3": f"{evidence[2][0]}: {evidence[2][2]}" if len(evidence) > 2 else "",
    })

theme_df = pd.DataFrame(theme_rows)
theme_df = theme_df.sort_values("n_papers", ascending=False).reset_index(drop=True)
theme_df.to_csv(OUT_MATRIX, index=False)

# Also compute: IST-NONE coverage (critical finding)
ist_none_papers = set(codes_df[codes_df["code"]=="IST-NONE"]["paper_id"].unique())
total_inc = 45

# ─────────────────────────────────────────────────────────────────────────────
# WRITE MARKDOWN REPORT
# ─────────────────────────────────────────────────────────────────────────────

lines = [
    "# Phase F2.2 — Descriptive Themes",
    "",
    "> **Method**: Thomas & Harden (2008) Stage 2 — Descriptive Theme Construction",
    "> **Basis**: 613 code instances from 45 INCLUDE papers (F2.1 open coding)",
    "> **Date**: April 30, 2026",
    "",
    "---",
    "",
    "## Overview",
    "",
    f"The open coding phase (F2.1) produced **613 code instances** across **45 papers**, distributed across",
    f"8 code categories (MC=167, CTX=119, DS=70, FE=67, AC=58, IST=51, LIM=42, GAP=39).",
    "",
    f"**Critical cross-cutting finding**: **{len(ist_none_papers)}/{total_inc} papers ({len(ist_none_papers)/total_inc*100:.0f}%)**",
    f"contain no detectable IS theory (`IST-NONE`). This is the most structurally significant",
    f"finding of F2.1 and directly supports Analytical Theme AT3 (absence of IS-theoretical grounding).",
    "",
    "---",
    "",
    "## Descriptive Theme Summary Table",
    "",
    "| ID | Theme Label | N Papers | RQ |",
    "|---|---|---|---|",
]

for _, row in theme_df.iterrows():
    lines.append(f"| {row['dt_id']} | {row['label'][:75]} | {row['n_papers']} | {row['rq_map']} |")

lines += [
    "",
    "---",
    "",
    "## Detailed Theme Descriptions",
    "",
]

for theme in DESCRIPTIVE_THEMES:
    # Find theme row
    trow = theme_df[theme_df["dt_id"] == theme["dt_id"]].iloc[0]
    papers = sorted(trow["paper_ids"].split("|")) if trow["paper_ids"] else []
    n = trow["n_papers"]

    lines += [
        f"### {theme['dt_id']}: {theme['label']}",
        "",
        f"**RQ Mapping**: {theme['rq_map']}  ",
        f"**Contributing papers**: {n} / 45  ",
        f"**Constitutive codes**: `{'`, `'.join(theme['constitutive_codes'])}`",
        "",
        f"**Description**:",
        f"{theme['description']}",
        "",
        f"**Contributing paper IDs**: {', '.join(papers[:20])}{'...' if len(papers)>20 else ''}",
        "",
    ]

    # Evidence quotes
    evidence = get_evidence_for_theme(theme, codes_df)
    if evidence:
        lines.append("**Representative evidence**:")
        lines.append("")
        for pid, code, quote in evidence:
            lines.append(f"> [{pid}] `{code}`: \"{quote[:180]}\"")
        lines.append("")
    lines.append("---")
    lines.append("")

# ── CROSS-THEME ANALYSIS ──────────────────────────────────────────────────────
lines += [
    "## Cross-Theme Analysis",
    "",
    "### Theme Overlap: Papers Contributing to Multiple Themes",
    "",
    "| Paper ID | Themes | Interpretation |",
    "|---|---|---|",
]

# Find multi-theme papers
paper_to_themes = defaultdict(list)
for theme in DESCRIPTIVE_THEMES:
    trow = theme_df[theme_df["dt_id"] == theme["dt_id"]].iloc[0]
    papers = trow["paper_ids"].split("|") if trow["paper_ids"] else []
    for pid in papers:
        paper_to_themes[pid].append(theme["dt_id"])

multi_theme = {pid: themes for pid, themes in paper_to_themes.items() if len(themes) >= 3}
# Add paper title for context
for pid, themes in sorted(multi_theme.items()):
    title_row = inc[inc["paper_id"] == pid]
    title = title_row["title"].values[0][:60] + "..." if len(title_row) > 0 else pid
    lines.append(f"| {pid} | {', '.join(themes)} | Bridging paper: spans {len(themes)} themes |")

lines += [
    "",
    "### Theme Coverage of RQ Space",
    "",
    "| RQ | Themes | N Papers Addressing | Evidence Strength |",
    "|---|---|---|---|",
]

# RQ coverage
rq_coverage = {
    "RQ1": ["DT1","DT2","DT3","DT6","DT9","DT10"],
    "RQ2": ["DT1","DT5"],
    "RQ3": ["DT4","DT5","DT6","DT7","DT8","DT10"],
}
for rq, dts in rq_coverage.items():
    papers_in_rq = set()
    for dt in dts:
        trow = theme_df[theme_df["dt_id"] == dt]
        if len(trow) > 0:
            pids = trow.iloc[0]["paper_ids"].split("|") if trow.iloc[0]["paper_ids"] else []
            papers_in_rq.update(pids)
    n = len(papers_in_rq)
    strength = "Strong (>20)" if n > 20 else "Moderate (10–20)" if n >= 10 else "Thin (<10)"
    lines.append(f"| {rq} | {', '.join(dts)} | {n} | {strength} |")

lines += [
    "",
    "### Structural Gap: IST-NONE Dominance",
    "",
    f"**{len(ist_none_papers)} of 45 papers ({len(ist_none_papers)/total_inc*100:.0f}%) apply no IS theory.**",
    "",
    "This is not merely a minor gap — it represents a systemic epistemic failure in the field:",
    "detection-focused papers adopt exclusively technical evaluation criteria (F1-score, AUC-ROC)",
    "without considering adoption feasibility, institutional fit, or governance implications.",
    "Papers applying IS theory (DT6, N=17) cluster in the governance / village-fund strand",
    "and virtually never cross-pollinate with the ML detection strand.",
    "",
    "This structural divide is the primary evidence for Analytical Theme AT3.",
    "",
    "---",
    "",
    "_Generated by `scripts/descriptive_themes.py` — Phase F2.2_",
    "_Next step: Phase F2.3 — Analytical themes + inter-paper relations_",
]

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ── PRINT SUMMARY ─────────────────────────────────────────────────────────────
print("=" * 60)
print("DESCRIPTIVE THEMES SUMMARY (F2.2)")
print("=" * 60)
print()
for _, row in theme_df.iterrows():
    print(f"  {row['dt_id']}: {row['label'][:65]}")
    print(f"      N={row['n_papers']:2d} papers | RQ: {row['rq_map']}")
    print()
print(f"IST-NONE (no IS theory): {len(ist_none_papers)}/45 papers ({len(ist_none_papers)/total_inc*100:.0f}%)")
print()
print(f"Outputs:")
print(f"  {OUT_MD}")
print(f"  {OUT_MATRIX}")
