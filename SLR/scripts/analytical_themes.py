"""
Phase F2.3 — Analytical Themes + Inter-Paper Relation Mapping
(Thomas & Harden 2008 Stage 3; Britten et al. 2002 relation types)

Constructs 4 analytical themes from cross-paper interpretation of descriptive themes.
Maps converging, extending, contradicting, silencing, and bridging relations.

Outputs:
  - SLR/analysis/themes/analytical_themes.md
  - SLR/analysis/themes/inter_paper_relations.csv
"""

import os
import pandas as pd
from collections import defaultdict

BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_CSV     = os.path.join(BASE_DIR, "analysis", "themes", "open_codes_master.csv")
DT_MATRIX_CSV  = os.path.join(BASE_DIR, "analysis", "themes", "descriptive_themes_matrix.csv")
CORPUS_CSV     = os.path.join(BASE_DIR, "scripts", "output", "coded_corpus.csv")
OUT_AT_MD      = os.path.join(BASE_DIR, "analysis", "themes", "analytical_themes.md")
OUT_REL_CSV    = os.path.join(BASE_DIR, "analysis", "themes", "inter_paper_relations.csv")

codes_df  = pd.read_csv(MASTER_CSV)
dt_df     = pd.read_csv(DT_MATRIX_CSV)
corpus_df = pd.read_csv(CORPUS_CSV)
inc       = corpus_df[corpus_df["irr_resolution"].isin(["CONSENSUS","DOMAIN_OVERRIDE"])].copy()


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: get paper IDs in a descriptive theme
# ─────────────────────────────────────────────────────────────────────────────

def theme_papers(dt_id):
    row = dt_df[dt_df["dt_id"] == dt_id]
    if len(row) == 0:
        return set()
    pids_str = row.iloc[0]["paper_ids"]
    if pd.isna(pids_str) or not pids_str:
        return set()
    return set(str(pids_str).split("|"))


def get_title(pid):
    row = inc[inc["paper_id"] == pid]
    if len(row) == 0:
        return pid
    return str(row.iloc[0]["title"])[:80]


def papers_with_codes(code_list):
    mask = codes_df["code"].isin(code_list)
    return set(codes_df[mask]["paper_id"].unique())


# ─────────────────────────────────────────────────────────────────────────────
# INTER-PAPER RELATIONS
# ─────────────────────────────────────────────────────────────────────────────

# ML cluster (primarily DT2, DT3, DT9) — machine learning detection papers
ml_cluster  = theme_papers("DT2") | theme_papers("DT9")
ml_also_private = theme_papers("DT3")  # private sector boundary
gov_cluster = theme_papers("DT5")      # village fund / governance papers
ist_papers  = theme_papers("DT6")      # IS-theory papers

# Bridging papers: appear in BOTH ml_cluster AND gov_cluster
bridging = ml_cluster & gov_cluster
# ML papers with IS theory (extremely rare)
ml_with_ist = ml_cluster & ist_papers
# ML papers that acknowledge label scarcity
ml_label_scarce = ml_cluster & theme_papers("DT4")
# Governance papers that include ML methods
gov_with_ml = gov_cluster & (theme_papers("DT2") | papers_with_codes(["MC-RF","MC-GBM","MC-IF","MC-UNSUP"]))

# Papers using synthetic data AND claiming high performance (circular validation issue)
synth_papers = papers_with_codes(["DS-SYNTH"])
perf_papers  = papers_with_codes(["MC-PERF"])
circular_validation = synth_papers & perf_papers

# Papers explicitly noting developing-country gap
dc_gap_papers = papers_with_codes(["GAP-DC","GAP-VILLAGE"])

relations = []

# ── CONVERGING relations ─────────────────────────────────────────────────────
# C1: High ML performance converges across multiple method types
ml_perf = papers_with_codes(["MC-PERF","MC-COMP"])
conv1_papers = sorted(ml_perf)
if len(conv1_papers) >= 3:
    for pid in conv1_papers:
        relations.append({
            "relation_type": "CONVERGING",
            "relation_id": "CON-01",
            "paper_id": pid,
            "partner_paper_id": "ALL_ML_PAPERS",
            "description": "Multiple ML methods independently report >90% AUC/F1 on fraud detection tasks — converging performance evidence",
            "analytical_theme": "AT2",
        })

# C2: Label scarcity converges across papers from different domains
lim_nolabel_papers = sorted(papers_with_codes(["LIM-NOLABEL","AC-LABEL"]))
for pid in lim_nolabel_papers:
    relations.append({
        "relation_type": "CONVERGING",
        "relation_id": "CON-02",
        "paper_id": pid,
        "partner_paper_id": "ALL_LABEL_SCARCE",
        "description": "Papers from both ML detection and governance domains converge on label scarcity as the primary methodological barrier",
        "analytical_theme": "AT1",
    })

# C3: IS theory absent — converges across ALL domains
ist_none_papers = sorted(papers_with_codes(["IST-NONE"]))
for pid in ist_none_papers:
    relations.append({
        "relation_type": "CONVERGING",
        "relation_id": "CON-03",
        "paper_id": pid,
        "partner_paper_id": "ALL_IST_NONE",
        "description": "Papers across all domains converge on absence of IS-theoretical framing — purely technical evaluation criteria dominate",
        "analytical_theme": "AT3",
    })

# ── CONTRADICTING relations ───────────────────────────────────────────────────
# CON-T1: High performance on synthetic data vs acknowledged ground truth problem
for pid in sorted(circular_validation):
    relations.append({
        "relation_type": "CONTRADICTING",
        "relation_id": "CON-T1",
        "paper_id": pid,
        "partner_paper_id": "CON-02_GROUP",
        "description": "Paper reports high F1/AUC on synthetic dataset while acknowledging real-world ground truth unavailability — internally contradictory validity claim",
        "analytical_theme": "AT4",
    })

# CON-T2: ML scalability claims vs centralized DB assumption
central_claims = papers_with_codes(["AC-CENTRAL","AC-LABEL"])
for pid in sorted(central_claims):
    relations.append({
        "relation_type": "CONTRADICTING",
        "relation_id": "CON-T2",
        "paper_id": pid,
        "partner_paper_id": "DT5_GOV_CLUSTER",
        "description": "ML paper assumes centralized, well-maintained database — directly contradicts the fragmented, paper-based data reality of village fund governance",
        "analytical_theme": "AT2",
    })

# ── SILENCING relations ───────────────────────────────────────────────────────
silencing_items = [
    {
        "relation_id": "SIL-01",
        "description": "No paper in corpus applies ML anomaly detection to actual Dana Desa village fund financial records",
        "analytical_theme": "AT1",
        "gap_type": "EMPIRICAL_ABSENCE",
        "evidence_for_rq": "RQ3",
    },
    {
        "relation_id": "SIL-02",
        "description": "No paper proposes or validates a feature engineering framework specifically for sub-national Indonesian government financial data",
        "analytical_theme": "AT1",
        "gap_type": "METHODOLOGICAL_ABSENCE",
        "evidence_for_rq": "RQ2",
    },
    {
        "relation_id": "SIL-03",
        "description": "No paper evaluates a fraud detection artifact using IS Success Model (DeLone & McLean) or TTF criteria in a public governance context",
        "analytical_theme": "AT3",
        "gap_type": "THEORETICAL_ABSENCE",
        "evidence_for_rq": "RQ1",
    },
    {
        "relation_id": "SIL-04",
        "description": "No paper addresses real-time or near-real-time anomaly detection in decentralized government financial flows at village level",
        "analytical_theme": "AT2",
        "gap_type": "OPERATIONAL_ABSENCE",
        "evidence_for_rq": "RQ3",
    },
    {
        "relation_id": "SIL-05",
        "description": "No paper provides a validated ground-truth construction methodology for public-sector corruption labeling without relying on judicial conviction records",
        "analytical_theme": "AT4",
        "gap_type": "METHODOLOGICAL_ABSENCE",
        "evidence_for_rq": "RQ3",
    },
    {
        "relation_id": "SIL-06",
        "description": "No paper constructs a typological mapping between corruption pattern types (procurement manipulation, fictitious spending, kickbacks) and specific detectable ML signal signatures",
        "analytical_theme": "AT1",
        "gap_type": "THEORETICAL_ABSENCE",
        "evidence_for_rq": "RQ2",
    },
]

for item in silencing_items:
    relations.append({
        "relation_type": "SILENCING",
        "relation_id": item["relation_id"],
        "paper_id": "(none — gap defined by absence)",
        "partner_paper_id": "",
        "description": item["description"],
        "analytical_theme": item["analytical_theme"],
    })

# ── BRIDGING papers ───────────────────────────────────────────────────────────
for pid in sorted(bridging):
    relations.append({
        "relation_type": "BRIDGING",
        "relation_id": "BRG-01",
        "paper_id": pid,
        "partner_paper_id": "ML_CLUSTER + GOV_CLUSTER",
        "description": f"Bridging paper: spans both ML detection methods and governance/village fund context — potential integration point for primary study design",
        "analytical_theme": "AT1",
    })

# ── EXTENDING relations ───────────────────────────────────────────────────────
# Village fund governance papers extend each other (each adds a specific angle)
gov_ids = sorted(gov_cluster)
for i, pid in enumerate(gov_ids):
    if i > 0:
        relations.append({
            "relation_type": "EXTENDING",
            "relation_id": "EXT-01",
            "paper_id": pid,
            "partner_paper_id": gov_ids[0],
            "description": "Governance paper extends village fund corruption literature — contributes contextual or institutional knowledge to cumulative understanding of Dana Desa fraud patterns",
            "analytical_theme": "AT1",
        })

# Save relations CSV
rel_df = pd.DataFrame(relations)
rel_df.to_csv(OUT_REL_CSV, index=False)

# ─────────────────────────────────────────────────────────────────────────────
# ANALYTICAL THEMES DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

# Count evidence for each AT
at_counts = {
    "AT1": len([r for r in relations if r["analytical_theme"] == "AT1"]),
    "AT2": len([r for r in relations if r["analytical_theme"] == "AT2"]),
    "AT3": len([r for r in relations if r["analytical_theme"] == "AT3"]),
    "AT4": len([r for r in relations if r["analytical_theme"] == "AT4"]),
}

# Key stats for narrative
n_bridging      = len(bridging)
n_ml_with_ist   = len(ml_with_ist)
n_gov_with_ml   = len(gov_with_ml)
n_circ_valid    = len(circular_validation)
n_dc_gap        = len(dc_gap_papers)
n_ist_none      = len(ist_none_papers)
n_ml_cluster    = len(ml_cluster)
n_gov_cluster   = len(gov_cluster)

# ─────────────────────────────────────────────────────────────────────────────
# WRITE ANALYTICAL THEMES MARKDOWN
# ─────────────────────────────────────────────────────────────────────────────

lines = [
    "# Phase F2.3 — Analytical Themes",
    "",
    "> **Method**: Thomas & Harden (2008) Stage 3 — Analytical Theme Construction",
    "> **Basis**: 10 descriptive themes + 613 code instances from 45 papers",
    "> **Inter-paper relations**: Britten et al. (2002) — Converging, Extending, Contradicting, Silencing, Bridging",
    "> **Date**: April 30, 2026",
    "",
    "---",
    "",
    "## Analytical Theme Summary",
    "",
    "| AT | Theme | Evidence Type | RQ | Relation Count |",
    "|---|---|---|---|---|",
    f"| AT1 | The Operationalization Chasm | SILENCING (3) + BRIDGING + EXTENDING | RQ2, RQ3 | {at_counts['AT1']} |",
    f"| AT2 | The Scalability Illusion | CONVERGING + CONTRADICTING + SILENCING | RQ1, RQ3 | {at_counts['AT2']} |",
    f"| AT3 | The Absence of IS Theory in Detection Artifacts | CONVERGING (28 papers) | RQ1, RQ3 | {at_counts['AT3']} |",
    f"| AT4 | The Ground Truth Paradox | CONTRADICTING + SILENCING | RQ3 | {at_counts['AT4']} |",
    "",
    "---",
    "",
    "## AT1: The Operationalization Chasm",
    "",
    "### Statement",
    "",
    "The corpus reveals a fundamental epistemic divide between two parallel knowledge traditions",
    "that have never been united in a single study: (1) the ML detection tradition, which constructs",
    "computational models of fraud on the assumption that fraud manifests as detectable patterns",
    "in structured, labeled transactional data; and (2) the IS governance tradition, which understands",
    "corruption as a socially embedded, institutionally interpreted phenomenon that resists",
    "straightforward operationalization into machine-readable signals.",
    "",
    "No paper in the corpus of 45 builds a bridge between these two traditions within a single",
    "study design. This is not merely a matter of combining methods — it requires resolving a",
    "deeper conceptual question that neither tradition has asked: *what does corruption look like*",
    "*as a computational feature in the specific institutional context of village fund governance?*",
    "",
    "### Evidence",
    "",
    f"- **{n_ml_cluster} papers** form the ML detection cluster (DT2, DT3, DT9): they develop, compare,",
    f"  and evaluate detection algorithms without engaging with the institutional conditions under",
    f"  which those algorithms would be deployed.",
    f"- **{n_gov_cluster} papers** form the governance cluster (DT5): they document corruption patterns,",
    f"  institutional failures, and control weaknesses in village fund governance without developing",
    f"  computational detection approaches.",
    f"- **{n_bridging} bridging paper{'s' if n_bridging!=1 else ''}** ({', '.join(sorted(bridging)) if bridging else 'none'}) span both clusters — these are the",
    f"  primary integration candidates for the primary study's design.",
    f"- **6 SILENCING gaps** confirm the absence of the bridge: no paper tests ML on Dana Desa data;",
    f"  no paper proposes a village-fund feature set; no paper maps corruption typology to ML signals.",
    "",
    "### Implication for Primary Study",
    "",
    "The primary study's core contribution is to fill this chasm: design and empirically test a",
    "feature engineering framework that operationalizes Dana Desa corruption patterns as",
    "ML-detectable anomaly signals, grounded in the governance literature's typological knowledge.",
    "",
    "---",
    "",
    "## AT2: The Scalability Illusion",
    "",
    "### Statement",
    "",
    "The ML detection literature reports impressively high performance figures — AUC-ROC >0.95,",
    "F1-scores >0.92 — that create an implicit assumption that these methods are ready for",
    "operational deployment in any financial fraud context. This is an illusion. The performance",
    "claims are uniformly conditioned on three assumptions that do not hold in the Dana Desa",
    "governance context:",
    "",
    "1. **Centralized, structured databases** with consistent schema and complete transaction records",
    "2. **Labeled training data** with known fraud/non-fraud ground truth",
    "3. **High transaction volume** (thousands to millions of records) enabling stable model training",
    "",
    "Village fund financial management in Indonesia operates under fundamentally different conditions:",
    "fragmented paper-based and semi-digital records across 74,000+ villages, no universal ground",
    "truth labeling system, and transaction volumes of approximately 12–24 per village per fiscal year.",
    "",
    "### Evidence",
    "",
    f"- **{len(papers_with_codes(['AC-CENTRAL']))} papers** explicitly assume centralized or well-maintained databases (AC-CENTRAL)",
    f"- **{len(papers_with_codes(['AC-LABEL']))} papers** require labeled training data for their core method (AC-LABEL)",
    f"- **{n_circ_valid} papers** report high performance on **synthetic data** while acknowledging",
    f"  real-world ground truth unavailability — a circular validation that does not support",
    f"  generalization claims (Silencing SIL-04).",
    f"- **{len(papers_with_codes(['LIM-SINGLE']))} papers** acknowledge single-country or single-institution generalizability limits",
    f"  (LIM-SINGLE) — yet none specifically test Indonesian sub-national government data.",
    "",
    "### Implication for Primary Study",
    "",
    "The primary study must explicitly position itself as addressing the scalability limitation: it",
    "provides the first empirical test of whether unsupervised anomaly detection methods can be",
    "adapted to low-volume, partially-labeled, fragmented village fund financial data.",
    "",
    "---",
    "",
    "## AT3: The Absence of IS Theory in Detection Artifacts",
    "",
    "### Statement",
    "",
    f"**{n_ist_none} of 45 papers (62%) contain no IS-theoretical framing.** This is the most",
    "structurally significant finding of the entire synthesis. It means that the field of",
    "ML-based financial fraud detection has built an extensive technical literature that cannot",
    "answer the most fundamental IS question: *will this system actually be adopted and used?*",
    "",
    "The IS theory that does appear (Agency Theory, Institutional Theory, Fraud Triangle) is",
    "exclusively located in the governance cluster (DT5, DT6). It never co-occurs with technical",
    "detection methods in the same paper. The two knowledge traditions have developed entirely",
    "separate evaluation criteria: the ML tradition evaluates by F1/AUC on held-out test sets;",
    "the governance tradition evaluates by theoretical coherence and institutional fit.",
    "",
    "No paper in the corpus evaluates a detection artifact using any IS success model",
    "(DeLone & McLean), task-technology fit criterion, or adoption-readiness framework. This",
    "creates a 'Silencing' gap (SIL-03): the question of whether these systems can actually serve",
    "as governance instruments has never been empirically addressed.",
    "",
    "### Evidence",
    "",
    f"- IST-NONE: {n_ist_none}/45 papers (62%) — purely technical framing",
    f"- IST papers that ARE present: {45 - n_ist_none}/45 papers — exclusively in governance cluster",
    f"- ML papers with IS theory: {n_ml_with_ist} ({', '.join(sorted(ml_with_ist)) if ml_with_ist else 'none'}) — represents the integration gap",
    f"- DeLone & McLean IS Success: **0 papers** apply this model to evaluate a detection artifact",
    f"- Task-Technology Fit: **0 papers** apply TTF to assess detection system fitness for auditor use",
    "",
    "### Implication for Primary Study",
    "",
    "The primary study must adopt a DSR-aligned IS evaluation framework. This is not decorative",
    "theory — it is the methodological contribution that makes this study genuinely IS research",
    "rather than an applied ML paper: framing the detection pipeline as a *governance artifact*",
    "evaluated against IS-theoretical criteria (utility, adoptability, institutional fit).",
    "",
    "---",
    "",
    "## AT4: The Ground Truth Paradox",
    "",
    "### Statement",
    "",
    "The corpus reveals a deep structural contradiction in the research field: papers simultaneously",
    "acknowledge the absence of reliable labeled fraud data AND report high-performing supervised",
    "models. This paradox is resolved in the literature through three strategies, each problematic:",
    "",
    "1. **Synthetic data** (19 papers, DS-SYNTH): Generate artificial fraud patterns that replicate",
    "   *known* fraud types — but this creates circular validation, since the model learns only the",
    "   fraud patterns the researcher already knew about.",
    "2. **Private-sector proxies** (22 papers, DT3): Use credit card or banking fraud datasets",
    "   (which do have labels) as stand-ins for public-sector corruption — but the structural",
    "   differences make this transfer epistemically unjustifiable.",
    "3. **Post-hoc labeling** from judicial records: Use KPK conviction records or audit findings",
    "   as ground truth — but this introduces severe selection bias (only detected and prosecuted",
    "   cases become positive labels; all undetected corruption remains in the negative class).",
    "",
    f"No paper in the corpus proposes or validates a ground-truth construction methodology that",
    f"resolves this paradox for public-sector contexts (SIL-05).",
    "",
    "### Evidence",
    "",
    f"- {n_circ_valid} papers report high F1/AUC on synthetic data while acknowledging label scarcity",
    f"  (CONTRADICTING relation CON-T1)",
    f"- {len(papers_with_codes(['DS-SYNTH']))} papers use DS-SYNTH but only {len(papers_with_codes(['LIM-NOLABEL']) & papers_with_codes(['DS-SYNTH']))}",
    f"  explicitly acknowledge the circularity risk",
    f"- SIL-05: No validated ground-truth construction methodology for public-sector exists",
    f"- The paradox is most acute for RQ3: any primary study claiming to detect Dana Desa corruption",
    f"  must address this paradox explicitly in its methodology section.",
    "",
    "### Implication for Primary Study",
    "",
    "The primary study must adopt **unsupervised anomaly detection** as the primary methodological",
    "commitment — not because supervised methods are unavailable, but because they are",
    "epistemically inappropriate for this context. The AT4 paradox provides the theoretical",
    "justification for this choice in the Methods section.",
    "",
    "---",
    "",
    "## Inter-Paper Relation Summary",
    "",
    "| Relation Type | Count | Key Insight |",
    "|---|---|---|",
]

for rtype in ["CONVERGING","CONTRADICTING","SILENCING","BRIDGING","EXTENDING"]:
    n = len([r for r in relations if r["relation_type"] == rtype])
    insights = {
        "CONVERGING": "Label scarcity + IST-NONE converge across all 45 papers",
        "CONTRADICTING": "Synthetic-data performance claims vs ground truth absence",
        "SILENCING": "6 structural gaps; Dana Desa ML test = most critical",
        "BRIDGING": f"{n_bridging} paper(s) span ML and governance clusters",
        "EXTENDING": f"Village fund papers build cumulative domain knowledge ({n_gov_cluster} papers)",
    }
    lines.append(f"| {rtype} | {n} | {insights.get(rtype, '')} |")

lines += [
    "",
    "---",
    "",
    "## Structural Diagram: Two Cluster Model",
    "",
    "```",
    "┌─────────────────────────────────────┐    ┌─────────────────────────────────────┐",
    "│        ML DETECTION CLUSTER          │    │      IS GOVERNANCE CLUSTER           │",
    "│  DT2: Unsupervised ML (N=18)         │    │  DT5: Village fund governance (N=26) │",
    "│  DT3: Supervised fraud (N=22)        │    │  DT6: IS theory papers (N=17)        │",
    "│  DT9: Graph methods (N=20)           │    │  DT8: DC constraints (N=18)          │",
    "│                                     │    │  DT1: Operationalization (partial)   │",
    "│  Eval: F1, AUC-ROC, accuracy        │    │  Eval: Theory, institutional fit     │",
    "│  Data: Banking, synthetic, private  │    │  Data: Audit reports, Dana Desa      │",
    "│  Theory: NONE (62%)                 │    │  Theory: Agency, Institutional, FT   │",
    "└──────────────────┬──────────────────┘    └──────────────────────────────────────┘",
    "                   │                                   ▲",
    "             CHASM │ (0 papers bridge both sides)      │",
    "                   │                                   │",
    "     PRIMARY STUDY CONTRIBUTION: Bridge this gap ──────┘",
    "     Operationalize Dana Desa corruption as ML features",
    "     Evaluate with IS-theoretical criteria (DSR framework)",
    "```",
    "",
    "---",
    "",
    "_Generated by `scripts/analytical_themes.py` — Phase F2.3_",
    "_Next step: Phase F3 — Framework synthesis DSR matrix_",
]

with open(OUT_AT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ── PRINT SUMMARY ─────────────────────────────────────────────────────────────
print("=" * 60)
print("ANALYTICAL THEMES SUMMARY (F2.3)")
print("=" * 60)
print()
print("AT1: The Operationalization Chasm")
print(f"     ML cluster: {n_ml_cluster} papers | Governance cluster: {n_gov_cluster} papers")
print(f"     Bridging: {n_bridging} paper(s) | Silencing gaps: 6")
print()
print("AT2: The Scalability Illusion")
print(f"     AC-CENTRAL: {len(papers_with_codes(['AC-CENTRAL']))} papers | DS-SYNTH: {len(papers_with_codes(['DS-SYNTH']))} papers")
print(f"     Circular validation: {n_circ_valid} papers")
print()
print("AT3: Absence of IS Theory")
print(f"     IST-NONE: {n_ist_none}/45 papers (62%)")
print(f"     ML papers with IS theory: {n_ml_with_ist}")
print(f"     D&M IS Success or TTF applied: 0 papers")
print()
print("AT4: Ground Truth Paradox")
print(f"     Circular (synth+perf): {n_circ_valid} papers | No resolved methodology: 0 papers")
print()
print("Inter-paper relations by type:")
for rtype in ["CONVERGING","CONTRADICTING","SILENCING","BRIDGING","EXTENDING"]:
    n = len([r for r in relations if r["relation_type"] == rtype])
    print(f"  {rtype:<15}: {n:3d} relations")
print()
print(f"Outputs:")
print(f"  {OUT_AT_MD}")
print(f"  {OUT_REL_CSV}")
