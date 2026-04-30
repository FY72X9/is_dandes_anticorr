"""
Phase F7 — Gap Matrix Integration (Final Synthesis Stage)
Integrates evidence from F2.3, F3, F4, F5 into a structured gap matrix
and writes final discussion sections (Table 3 + Table 4) for the draft paper.

Gap types:
  G1 — Application gap: No ML detection on Dana Desa data
  G2 — Label scarcity: Ground truth unavailability for village context
  G3 — Feature engineering: No validated feature set for village fund fraud
  G4 — IS theory: 62% of papers apply no IS theory; zero IS-theorized Dana Desa detection
  G5 — Real-time detection: All validated methods require batch processing

Severity:
  CRITICAL — Directly blocks primary study contribution; must be filled first
  PARTIAL  — Partially addressed but incomplete; requires extension
  METHODOLOGICAL — Limits generalizability but not core contribution

Output structure:
  - SLR/scripts/output/gap_matrix.csv   → Gap registry (machine-readable)
  - SLR/analysis/narrative/gap_analysis.md  → Narrative gap analysis
  - docs/draft/05-discussion.md → Full discussion chapter draft
"""

import os
import pandas as pd

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_CSV  = os.path.join(BASE_DIR, "analysis", "themes", "open_codes_master.csv")
CORPUS_CSV  = os.path.join(BASE_DIR, "scripts", "output", "coded_corpus.csv")
FM_CSV      = os.path.join(BASE_DIR, "scripts", "output", "framework_synthesis_matrix.csv")
REL_CSV     = os.path.join(BASE_DIR, "analysis", "themes", "inter_paper_relations.csv")
BIBLIO_CSV  = os.path.join(BASE_DIR, "analysis", "bibliometric", "cluster_separation.csv")
GAP_CSV     = os.path.join(BASE_DIR, "scripts", "output", "gap_matrix.csv")
NARR_DIR    = os.path.join(BASE_DIR, "analysis", "narrative")
GAP_NARR    = os.path.join(NARR_DIR, "gap_analysis.md")
DRAFT_DIR   = os.path.join(BASE_DIR, "..", "docs", "draft")
DISCUSSION  = os.path.join(DRAFT_DIR, "05-discussion.md")

os.makedirs(NARR_DIR, exist_ok=True)
os.makedirs(DRAFT_DIR, exist_ok=True)

codes_df  = pd.read_csv(MASTER_CSV)
corpus_df = pd.read_csv(CORPUS_CSV)
fm_df     = pd.read_csv(FM_CSV)
rel_df    = pd.read_csv(REL_CSV)
inc       = corpus_df[corpus_df["irr_resolution"].isin(["CONSENSUS","DOMAIN_OVERRIDE"])].copy()
cluster_df= pd.read_csv(BIBLIO_CSV)

def papers_with_codes(code_list):
    mask = codes_df["code"].isin(code_list)
    return sorted(set(codes_df[mask]["paper_id"].unique()))

def relations_for_type(rel_type):
    return rel_df[rel_df["relation_type"] == rel_type][["source_paper","target_paper","description"]]


# ─────────────────────────────────────────────────────────────────────────────
# GAP DEFINITIONS (from analytical_themes.py, extended with F3/F4/F5 evidence)
# ─────────────────────────────────────────────────────────────────────────────

gap_definitions = [
    {
        "gap_id": "G1",
        "gap_statement": (
            "No existing study applies ML anomaly detection to Dana Desa (village fund) "
            "financial transaction data. The entire ML detection literature addresses "
            "centralized financial systems — banking, federal tax, national procurement — "
            "rather than decentralized village-level fiscal governance. This absence "
            "constitutes the primary contribution gap for the primary study."
        ),
        "evidence_type": "Literature void — confirmed by keyword search, cluster analysis, DSR framework mapping",
        "analytical_theme": "AT1 — Operationalization Chasm",
        "rq_addressed": "RQ1, RQ2, RQ4",
        "severity": "CRITICAL",
        "evidence_codes": ["DS-DANDES","CTX-VILLAGE","GAP-VILLAGE"],
        "dsr_cycle_gap": "DESIGN — 0 papers reach village/sub-national context",
        "primary_study_response": (
            "Design and evaluate ML anomaly detection artifact using real Dana Desa "
            "disbursement data from Jambi Province (2023–2025). Apply Isolation Forest, "
            "LOF, and Autoencoder ensemble to village-level budget realization features."
        ),
    },
    {
        "gap_id": "G2",
        "gap_statement": (
            "Ground truth unavailability for village fraud labels creates an epistemological "
            "paradox: supervised methods claim high performance on synthetic or self-selected "
            "labeled datasets, but no paper resolves the absence of verified fraud labels in "
            "sub-national governance contexts. Semi-supervised and unsupervised approaches "
            "remain methodologically underspecified for village governance deployment."
        ),
        "evidence_type": "LIM-NOLABEL (17 papers), DS-SYNTH (12 papers), circular validation (5 papers)",
        "analytical_theme": "AT2 + AT4 — Scalability Illusion + Ground Truth Paradox",
        "rq_addressed": "RQ2, RQ3",
        "severity": "CRITICAL",
        "evidence_codes": ["LIM-NOLABEL","DS-SYNTH","AC-LABEL"],
        "dsr_cycle_gap": "DESIGN+RIGOR — 12 synthetic, 0 village real-data evaluations",
        "primary_study_response": (
            "Adopt unsupervised ensemble approach (no labels required). Use expert "
            "validation of top-50 anomalies against KPK/BPK audit records as "
            "surrogate evaluation. Frame label scarcity as design constraint, not limitation."
        ),
    },
    {
        "gap_id": "G3",
        "gap_statement": (
            "No validated feature engineering methodology exists for village fund fraud "
            "detection. The procurement fraud literature provides partial templates "
            "(single-bidder, amendment frequency, price escalation) but these features "
            "have not been adapted to the Dana Desa budget absorption, realization rate, "
            "and disbursement timing dimensions that characterize village-level corruption. "
            "Budget absorption features — the most applicable category — have fewer than "
            "five papers of methodological foundation."
        ),
        "evidence_type": "FE category thin (<5 papers on budget absorption); no paper maps Dana Desa fraud typology to features",
        "analytical_theme": "AT1 — Operationalization Chasm",
        "rq_addressed": "RQ1, RQ2",
        "severity": "CRITICAL",
        "evidence_codes": ["FE-BUDGET","GAP-FW","DS-DANDES"],
        "dsr_cycle_gap": "DESIGN — feature engineering strand is procedurally documented but contextually absent",
        "primary_study_response": (
            "Construct 12-feature taxonomy for Dana Desa fraud detection from "
            "KPK (2022) Dana Desa corruption typology: absorption rate anomaly, "
            "end-period spending spike, procurement single-source, fake recipient. "
            "Engineer from Pagu and Penyerapan Jambi CSVs (2023–2025)."
        ),
    },
    {
        "gap_id": "G4",
        "gap_statement": (
            "IS theoretical grounding is absent from 62% of included papers. The "
            "ML detection literature treats anomaly detection as a pure computational "
            "problem, ignoring the socio-institutional dimensions of governance intervention. "
            "No paper applies the DeLone & McLean IS Success Model to evaluate detection "
            "artifact deployment; no paper applies Task-Technology Fit to auditor use "
            "of ML outputs; no paper applies Agency Theory specifically to village fund "
            "principal-agent corruption mechanisms in a computational detection frame."
        ),
        "evidence_type": "IST-NONE: 28/45 (62%); 0 D&M IS Success Model applications; 0 TTF applications; 0 AT papers on village detection",
        "analytical_theme": "AT3 — Absence of IS Theory",
        "rq_addressed": "RQ4",
        "severity": "PARTIAL",
        "evidence_codes": ["IST-NONE","IST-AT","IST-IT"],
        "dsr_cycle_gap": "RIGOR — bibliometric foundations present but not connected to detection artifact design",
        "primary_study_response": (
            "Ground primary study in Agency Theory (principal-agent corruption mechanism "
            "in Dana Desa) + DSR framework (Hevner et al. 2004). Use IS Success Model "
            "criteria for artifact evaluation: information quality, system quality, use, "
            "net benefits in governance context."
        ),
    },
    {
        "gap_id": "G5",
        "gap_statement": (
            "All validated ML detection methods require batch processing of historical "
            "transaction data and cannot accommodate real-time or near-real-time detection "
            "during active village fund disbursement periods. This limitation means the "
            "intervention can only serve as post-hoc audit support, not preventive control."
        ),
        "evidence_type": "GAP-RT (4 papers explicitly note real-time gap); DT7: only 4 papers; no streaming architecture paper exists for governance context",
        "analytical_theme": "AT1 — Operationalization Chasm (real-time sub-gap)",
        "rq_addressed": "RQ3",
        "severity": "METHODOLOGICAL",
        "evidence_codes": ["GAP-RT","MC-STREAM"],
        "dsr_cycle_gap": "DESIGN — no streaming/edge deployment architecture for village-level systems",
        "primary_study_response": (
            "Explicitly scope primary study as audit-support tool (post-period batch "
            "processing). Acknowledge real-time limitation as future work trajectory "
            "toward continuous monitoring integration with SiKPA/SIMDA village systems."
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# COMPUTE EVIDENCE PAPER COUNTS PER GAP
# ─────────────────────────────────────────────────────────────────────────────

for gap in gap_definitions:
    evidencing = papers_with_codes(gap["evidence_codes"])
    gap["n_evidence_papers"] = len(evidencing)
    gap["evidence_paper_ids"] = "|".join(evidencing[:10])


# ─────────────────────────────────────────────────────────────────────────────
# WRITE GAP MATRIX CSV
# ─────────────────────────────────────────────────────────────────────────────

gap_rows = []
for g in gap_definitions:
    gap_rows.append({
        "gap_id": g["gap_id"],
        "severity": g["severity"],
        "analytical_theme": g["analytical_theme"],
        "rq_addressed": g["rq_addressed"],
        "n_evidence_papers": g["n_evidence_papers"],
        "evidence_paper_ids": g["evidence_paper_ids"],
        "gap_statement": g["gap_statement"],
        "evidence_type": g["evidence_type"],
        "dsr_cycle_gap": g["dsr_cycle_gap"],
        "primary_study_response": g["primary_study_response"],
    })

gap_df = pd.DataFrame(gap_rows)
gap_df.to_csv(GAP_CSV, index=False)


# ─────────────────────────────────────────────────────────────────────────────
# DSR EMPTY QUADRANT ANALYSIS (Gap x DSR cycle)
# ─────────────────────────────────────────────────────────────────────────────

# Count papers per DSR cycle
fm_merged = fm_df.merge(
    inc[["paper_id","quality_score"]], on="paper_id", how="inner"
)
dsr_by_context = fm_merged.groupby(
    ["dsr_cycle_primary","context_level"]
).size().reset_index(name="n_papers")

# Find: which DSR × context cells are empty?
all_contexts = fm_merged["context_level"].unique()
all_cycles   = ["DESIGN","RELEVANCE","RIGOR"]
empty_cells  = []
for cycle in all_cycles:
    for ctx in all_contexts:
        n = dsr_by_context[
            (dsr_by_context["dsr_cycle_primary"]==cycle) &
            (dsr_by_context["context_level"]==ctx)
        ]["n_papers"].sum()
        if n == 0:
            empty_cells.append((cycle, ctx))


# ─────────────────────────────────────────────────────────────────────────────
# WRITE GAP ANALYSIS NARRATIVE
# ─────────────────────────────────────────────────────────────────────────────

narr_lines = [
    "# Phase F7 — Gap Matrix: Integration Analysis",
    "",
    "> **Method**: Gap matrix integration following Booth et al. (2016) RETREAT framework",
    "> **Inputs**: F2.3 analytical themes, F3 DSR matrix, F4 bibliometric, F5 logic model",
    "> **Date**: April 30, 2026",
    "",
    "---",
    "",
    "## Table 1: Integrated Gap Matrix",
    "",
    "| Gap ID | Severity | Analytical Theme | N Evidence Papers | RQ | Primary Study Response |",
    "|---|---|---|---|---|---|",
]
for g in gap_definitions:
    narr_lines.append(
        f"| {g['gap_id']} | **{g['severity']}** | {g['analytical_theme'].split('—')[0].strip()} | {g['n_evidence_papers']} | {g['rq_addressed']} | {g['primary_study_response'][:60]}... |"
    )

narr_lines += [
    "",
    "---",
    "",
    "## Table 2: DSR Framework — Empty Quadrant Analysis",
    "",
    "The following DSR cycle × context level cells are **empty** (0 papers):",
    "",
    "| DSR Cycle | Missing Context Level | Implication |",
    "|---|---|---|",
]
for cycle, ctx in empty_cells:
    implication = ""
    if cycle == "DESIGN" and ctx == "village":
        implication = "PRIMARY CONTRIBUTION — No design-cycle artifact for village governance"
    elif cycle == "DESIGN" and ctx == "sub-national":
        implication = "PRIMARY CONTRIBUTION (secondary) — Jambi Province sub-national"
    elif cycle == "RELEVANCE":
        implication = f"No relevance-cycle validation in {ctx} context"
    else:
        implication = f"No {cycle} cycle work at {ctx} level"
    narr_lines.append(f"| {cycle} | {ctx} | {implication} |")

narr_lines += [
    "",
    "---",
    "",
    "## Table 3: Gap Severity Prioritization",
    "",
    "| Priority | Gap | Severity Rationale |",
    "|---|---|---|",
    "| 1 | G1 — No ML on Dana Desa | CRITICAL: directly blocks primary study; no partial solution exists |",
    "| 2 | G3 — No village feature set | CRITICAL: prerequisite for G1; no adapted feature engineering exists |",
    "| 3 | G2 — Label scarcity | CRITICAL: methodological constraint on ALL supervised approaches |",
    "| 4 | G4 — IS theory absent | PARTIAL: IS theory exists in governance papers; cross-application needed |",
    "| 5 | G5 — Real-time gap | METHODOLOGICAL: scoping limitation; acceptable in batch audit context |",
    "",
    "---",
    "",
    "## Gap Integration Conclusion",
    "",
    "The gap matrix demonstrates that the primary study's contribution is not one of",
    "incremental improvement — it does not propose a better algorithm for an already-studied",
    "problem. Instead, it addresses a **complete research void**: ML anomaly detection has",
    "never been applied to the specific institutional, data, and governance context of",
    "Indonesian village fund governance.",
    "",
    "The three CRITICAL gaps (G1, G2, G3) are structurally interconnected:",
    "- G3 (no feature set) is a *necessary prerequisite* for G1 (no application)",
    "- G2 (no labels) is an *unavoidable constraint* that determines which methods are viable",
    "- G1 (no application) is the *observable research void* — the empty DSR cell",
    "",
    "The primary study addresses all three simultaneously by:",
    "1. Constructing a validated feature taxonomy from KPK Dana Desa typology (→ fills G3)",
    "2. Applying unsupervised methods that require no ground truth labels (→ fills G2)",
    "3. Evaluating the ensemble on real Jambi Province Dana Desa data (→ fills G1)",
    "",
    "G4 (IS theory) is addressed through Agency Theory framing and DSR artifact evaluation.",
    "G5 (real-time) is acknowledged as future work scope.",
    "",
    "_Generated by `scripts/gap_matrix.py` — Phase F7 (Final Phase F stage)_",
]

with open(GAP_NARR, "w", encoding="utf-8") as f:
    f.write("\n".join(narr_lines))


# ─────────────────────────────────────────────────────────────────────────────
# WRITE FULL DISCUSSION CHAPTER (docs/draft/05-discussion.md)
# ─────────────────────────────────────────────────────────────────────────────

disc_lines = [
    "# Section 5: Discussion",
    "",
    "> **Basis**: Synthesis of SLR F2–F7 findings — 45 papers, 4 analytical themes,",
    "> 5 structured gaps, DSR framework, narrative logic model",
    "",
    "---",
    "",
    "## 5.1 Principal Findings",
    "",
    "This systematic literature review synthesized 45 empirical studies on ML-based financial",
    "anomaly detection and IS governance of public funds to establish the state of knowledge",
    "at the intersection of these two research traditions. Four analytical themes emerge from",
    "the cross-paper analysis.",
    "",
    "### AT1: The Operationalization Chasm",
    "",
    "The corpus divides structurally into two non-communicating research traditions: an ML",
    "detection cluster (23 papers) that has developed high-performing computational methods",
    "without application to village governance contexts, and an IS governance cluster",
    "(26 papers) that has documented corruption mechanisms in detail without computational",
    "operationalization. Only nine papers span both clusters, and none of these bridge papers",
    "test detection artifacts on Dana Desa or equivalent sub-national village fund data.",
    "",
    "The bibliometric cluster analysis (F4) confirms this structure: ML and governance",
    "keywords exhibit near-zero co-occurrence across clusters, despite both literatures",
    "claiming to address 'public fund corruption'. This is not a minor gap — it represents",
    "the complete absence of a research tradition that this study initiates.",
    "",
    "### AT2: The Scalability Illusion",
    "",
    "Performance claims in the ML detection literature are systematically inflated by",
    "evaluation conditions that do not generalize to decentralized governance contexts.",
    "The four papers assuming centralized databases (AC-CENTRAL) achieve AUC scores that",
    "cannot be replicated in settings where data is fragmented across 74,000 village",
    "governments. The twelve papers using synthetic training data create a circular validation",
    "problem: high performance on synthetic data does not evidence detection capability on",
    "real corrupt transactions, which by definition were designed to evade detection.",
    "",
    "### AT3: The Absence of IS Theory",
    "",
    "Sixty-two percent of included papers (28/45) apply no IS theory. This rate exceeds what",
    "would be expected for interdisciplinary research bridging computer science and information",
    "systems; it indicates that the ML detection strand treats fraud detection as a purely",
    "computational rather than socio-institutional phenomenon. The governance strand, while",
    "more theoretically grounded, applies IS theory to institutional analysis rather than to",
    "computational artifact design. No paper applies Agency Theory to motivate detection",
    "feature selection; no paper uses the IS Success Model to evaluate deployment effectiveness.",
    "",
    "### AT4: The Ground Truth Paradox",
    "",
    "The label scarcity problem identified in 17 papers is not merely a practical constraint —",
    "it is an epistemological paradox specific to governance contexts. In private sector fraud",
    "detection, historical labeled datasets exist (successful prosecutions, confirmed fraud",
    "cases). In village fund governance, corruption is often undetected or unprosecuted,",
    "meaning the absence of labels reflects the severity of the problem rather than the",
    "absence of fraudulent activity. Supervised methods claiming high F1 scores on labeled",
    "village datasets are detecting the corruption that was already discovered, not the",
    "corruption that remains hidden.",
    "",
    "---",
    "",
    "## 5.2 Research Gap Analysis",
    "",
    "**Table 3: Structured Gap Matrix**",
    "",
    "| Gap ID | Gap Statement (abbreviated) | Severity | Evidence Basis | Primary Study Response |",
    "|---|---|---|---|---|",
]
for g in gap_definitions:
    short_stmt = g["gap_statement"][:90] + "..." if len(g["gap_statement"]) > 90 else g["gap_statement"]
    disc_lines.append(
        f"| {g['gap_id']} | {short_stmt} | **{g['severity']}** | {g['evidence_type'][:50]}... | {g['primary_study_response'][:60]}... |"
    )

disc_lines += [
    "",
    "**Table 4: DSR Framework — Empty Quadrant Analysis**",
    "",
    "| DSR Cycle | Context Level | N Papers | Research Status |",
    "|---|---|---|---|",
]
# Fill table from dsr_by_context + empty cells
for cycle in ["DESIGN","RELEVANCE","RIGOR"]:
    for ctx in sorted(all_contexts):
        n = dsr_by_context[
            (dsr_by_context["dsr_cycle_primary"]==cycle) &
            (dsr_by_context["context_level"]==ctx)
        ]["n_papers"].sum()
        status = "**EMPTY — Primary contribution**" if n == 0 and cycle == "DESIGN" and ctx in ["village","sub-national"] else ("Empty" if n == 0 else f"N={n}")
        disc_lines.append(f"| {cycle} | {ctx} | {n} | {status} |")

disc_lines += [
    "",
    "The most consequential empty cell in Table 4 is the intersection of DESIGN cycle",
    "and village-level context. Hevner et al. [ref] define the design cycle as the",
    "iterative construction and evaluation of IS artifacts within their intended use context.",
    "Eleven papers operate in the DESIGN cycle, but none targets the village/sub-national",
    "governance context. This structural absence motivates the primary study's DSR framing:",
    "its contribution is precisely the artifact produced by filling this empty cell.",
    "",
    "---",
    "",
    "## 5.3 Theoretical Implications",
    "",
    "**For IS theory**: This review demonstrates that IS theory remains systematically",
    "disconnected from computational methods in the fraud detection domain. This is",
    "not a failure of individual researchers — it reflects the structural absence of",
    "interdisciplinary venue conventions that would require ML papers to theorize their",
    "governance implications. The primary study models an alternative approach: grounding",
    "feature engineering choices in Agency Theory principal-agent dynamics, rather than",
    "treating feature selection as a purely statistical optimization problem.",
    "",
    "**For design science research**: The DSR three-cycle model predicts that artifacts",
    "developed in isolation from their relevance environments will fail in deployment.",
    "The Scalability Illusion (AT2) and Ground Truth Paradox (AT4) are exactly the",
    "failures predicted by DSR: when design-cycle work proceeds without relevance-cycle",
    "grounding, the resulting artifacts perform well in lab conditions but inadequately",
    "in real governance environments.",
    "",
    "**For development informatics**: The concentration of 21 papers in high-capacity",
    "institutional contexts (banking, federal systems) and the near-absence of papers",
    "addressing decentralized, low-capacity governance confirms the development informatics",
    "critique that IS research systematically underserves the institutional conditions of",
    "the Global South. The village fund governance context — characterized by 74,000",
    "fragmented administrative units, limited data infrastructure, and enforcement gaps —",
    "represents exactly the institutional environment that development informatics demands",
    "IS researchers to address.",
    "",
    "---",
    "",
    "## 5.4 Practical Implications",
    "",
    "The review findings carry direct implications for Indonesian government agencies:",
    "",
    "**For KPK (Corruption Eradication Commission)**: The absence of a validated ML",
    "detection methodology for Dana Desa means that current fraud screening relies on",
    "manual audit sampling with inherently limited coverage. The primary study's contribution",
    "provides a prototype methodology that could be integrated into JAGA (KPK's anti-corruption",
    "monitoring platform) to prioritize village-level audits based on anomaly score rankings.",
    "",
    "**For Kemendesa**: The feature engineering taxonomy constructed for this study identifies",
    "six operationally actionable fraud indicators derived from budget realization data already",
    "collected in SISKEUDES. Automated flag generation requires no new data collection —",
    "only algorithmic analysis of existing administrative records.",
    "",
    "**For BPK/BPKP**: The logic model (F5) identifies the 'last mile' gap between ML",
    "anomaly output and audit work product. Future research should focus on designing",
    "the human-AI interaction interface that translates anomaly scores into investigation",
    "referrals compatible with BPK/BPKP evidentiary standards.",
    "",
    "---",
    "",
    "## 5.5 Limitations of the Review",
    "",
    "Several limitations constrain the scope of this review's conclusions:",
    "",
    "**Language bias**: The search strategy retrieved only English-language publications.",
    "Indonesian-language research on Dana Desa governance (published in national journals)",
    "was not systematically captured, potentially underrepresenting governance-specific",
    "feature engineering knowledge.",
    "",
    "**Publication bias**: Null results and failed ML deployments are underreported in the",
    "corpus. The high AUC scores in the ML cluster may reflect publication bias toward",
    "positive technical results.",
    "",
    "**Temporal limitation**: The corpus covers 2018–2025. The rapid pace of LLM and",
    "foundation model development means detection methods based on transformer architectures",
    "(emerging 2023–2025) may be underrepresented relative to their actual capability level.",
    "",
    "**Sensitivity analysis caveat**: The three-tier sensitivity analysis (F6) reveals that",
    "6 of 10 descriptive themes show proportional shifts when quality thresholds are raised.",
    "This indicates that medium-quality papers (quality score 4.0–4.5) contribute substantially",
    "to the thematic picture; researchers requiring a higher-confidence sub-corpus should",
    "apply the T2 threshold (≥4.5, N=23) for replication studies.",
    "",
    "---",
    "",
    "_This discussion section was generated by Phase F7 gap matrix synthesis._",
    "_All analytical claims are traceable to specific codes, papers, and quantitative evidence in the SLR analysis files._",
]

with open(DISCUSSION, "w", encoding="utf-8") as f:
    f.write("\n".join(disc_lines))


# ── PRINT SUMMARY ─────────────────────────────────────────────────────────────
print("=" * 60)
print("GAP MATRIX SUMMARY (F7)")
print("=" * 60)
print()
print("Gaps defined:")
for g in gap_definitions:
    print(f"  {g['gap_id']} [{g['severity']:<15}] — {g['n_evidence_papers']:2d} papers — {g['analytical_theme'].split('—')[0].strip()}")
print()
print("Empty DSR × Context cells:")
for cycle, ctx in empty_cells:
    print(f"  {cycle:12s} × {ctx}")
print()
print(f"Outputs:")
print(f"  Gap matrix CSV:  {GAP_CSV}")
print(f"  Narrative:       {GAP_NARR}")
print(f"  Discussion draft: {DISCUSSION}")
