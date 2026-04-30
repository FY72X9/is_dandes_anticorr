# 4. Results

## 4.1 Bibliometric Characteristics

### 4.1.1 Temporal Distribution

The 45 included papers span 2018–2026, with 98% published in 2022–2026. This concentration
reflects the field's response to two converging trends: the proliferation of deep learning
architectures accessible through open-source frameworks, and increased Indonesian government
and KPK attention to Dana Desa misuse following the 2019–2022 audit escalation. Publication
volume increases year-on-year: 6 papers (2022), 9 (2023), 12 (2024), 15 (2025), and 2 in
early 2026. **2025 is the peak publication year** (33% of the total corpus).

### 4.1.2 Journal Distribution

The corpus spans 30 distinct publication venues. IEEE Access (Q1, 9 papers) and Applied
Sciences (Q2, 3 papers) dominate the ML detection strand; Integritas Jurnal Antikorupsi and
Indonesian law and management journals host the governance strand. Approximately 30% of
included papers lack a SCImago quartile (unranked venues), disproportionately concentrated
in the village governance cluster — a structural feature that influenced quality score
distribution and motivated the domain-override protocol.

### 4.1.3 Two-Cluster Structure

Bibliometric cluster analysis (keyword-fraction method, threshold >0.6) reveals a
structurally disconnected two-cluster corpus:

| Cluster | N Papers | Dominant Keywords |
|---|---|---|
| ML_DETECTION | 21 | deep learning, isolation forest, LOF, AML, banking |
| IS_GOVERNANCE | 21 | dana desa, village governance, agency theory, fraud triangle |
| BRIDGING | 3 | procurement fraud, ML, public sector |

The three bridging papers (P067, P089, P094) represent the only structural links between
the clusters. Keyword co-occurrence analysis confirms that no pair of keywords from the
ML_DETECTION cluster co-occurs with any keyword from the IS_GOVERNANCE cluster at count >2,
providing structural bibliometric evidence for the Operationalization Chasm (AT1, Section 4.3).

## 4.2 Descriptive Themes

Thematic synthesis of 613 code instances across 45 papers produced 10 descriptive themes
(DT1–DT10). Table 1 summarises the themes by paper count and primary RQ alignment.

**Table 1: Descriptive Theme Summary**

| DT | Theme | N Papers | Primary RQ |
|---|---|---|---|
| DT1 | Operationalizing corruption as computational signals | 16 | RQ2 |
| DT2 | Unsupervised ML for financial anomaly detection | 18 | RQ1 |
| DT3 | Supervised fraud detection in private financial contexts | 22 | RQ1 (boundary) |
| DT4 | Label scarcity and ground truth unavailability | 19 | RQ3 |
| DT5 | Village fund governance and corruption patterns | 26 | RQ2, RQ3 |
| DT6 | IS-theoretical framing of detection artifacts | 17 | RQ1, RQ3 |
| DT7 | Real-time detection and deployment gap | 4 | RQ3 |
| DT8 | Developing-country and sub-national constraints | 18 | RQ3 |
| DT9 | Graph and network-based fraud detection | 20 | RQ1 |
| DT10 | Explainability and audit trail requirements | 7 | RQ1, RQ3 |

**Critical cross-cutting finding**: 28 of 45 papers (62%) contain no IS-theoretical
framing (`IST-NONE`). This absence is uniform across the ML detection cluster (DT2, DT3,
DT9) and concentrated in technical method papers — a finding with direct implications
for IS theory contribution (AT3).

### 4.2.1 DT2 — Unsupervised ML Methods (RQ1)

Eighteen papers contribute to DT2, establishing that the unsupervised methods most
applicable to unlabelled governance data are Isolation Forest (IF) [12], Local Outlier
Factor (LOF) [13], and reconstruction-based Autoencoders. Of these, IF demonstrates
the most consistent performance across sparse, low-volume datasets — a property directly
relevant to village-level financial data with 12–24 annual transactions per unit. Graph
Neural Networks (GNNs) offer superior performance when relational transaction data is
available (DT9, 20 papers), but require a connected transaction graph that does not
exist in current village fund record systems.

### 4.2.2 DT4 — Label Scarcity (RQ3)

Nineteen papers explicitly document ground truth unavailability as a structural research
limitation. Five papers report high performance on synthetic data and then acknowledge
that these results cannot generalise to contexts where labelled real-world fraud examples
are absent. This circular validation pattern — which we term the Ground Truth Paradox
(AT4) — directly constrains method selection for the primary study: only unsupervised
methods that require no labelled training data are viable for village fund application.

### 4.2.3 DT5 — Village Fund Governance (RQ2, RQ3)

The 26 governance papers collectively document a well-defined corruption typology:
budget absorption manipulation (inflating year-end expenditure to meet targets while
concealing fictitious activities), single-bidder procurement (directing contracts to
related parties), phantom projects (reporting physical outputs that do not exist), and
administrative fraud (falsifying attendance records, receipts, and accountability reports).
This typology — confirmed across multiple KPK case analyses and BPK audit reports — is
the primary input for the feature engineering framework in the primary study.

## 4.3 Analytical Themes

Cross-paper relationship analysis (121 inter-paper relations: 61 converging, 20
contradicting, 6 silencing, 9 bridging, 25 extending) produced four analytical themes.

### 4.3.1 AT1 — The Operationalization Chasm

The corpus reveals a fundamental epistemic divide. **23 papers** (DT2, DT3, DT9 cluster)
develop and evaluate detection algorithms without engaging with the governance contexts in
which those algorithms must function. **26 papers** (DT5 cluster) document village fund
corruption patterns without developing computational detection approaches. **9 bridging
papers** exist but none unites both traditions in a single study design.

Six SILENCING relations confirm the absence of the bridge: (1) no paper applies ML to
Dana Desa financial data; (2) no paper proposes a village fund feature engineering
framework; (3) no paper maps Dana Desa corruption typology to ML-detectable signals;
(4) no paper evaluates a detection artifact against Indonesian government data; (5) no
paper addresses IS adoption requirements for auditor use of ML outputs; (6) no paper
tests detection in a decentralised, low-volume public governance data context.

This is the primary justification for the primary study.

### 4.3.2 AT2 — The Scalability Illusion

The technical literature reports AUC-ROC >0.95 and F1-scores >0.92 across multiple
method papers. These figures are uniformly conditioned on assumptions that do not hold
in village governance: centralised databases, labeled training data, and transaction
volumes in the thousands. Four papers explicitly acknowledge centralisation assumptions
(AC-CENTRAL); 12 papers require labeled data (AC-LABEL); 5 papers use synthetic data
validation (DS-SYNTH). The performance claims are real within their stated boundary
conditions — but those conditions exclude the Dana Desa context entirely.

### 4.3.3 AT3 — The Absence of IS Theory

28 of 45 papers (62%) contain no IS-theoretical framework. The IS theory that does appear
(Agency Theory, Fraud Triangle, Institutional Theory) resides exclusively in the governance
cluster and never co-occurs with technical detection methods in a single paper. No paper
evaluates a detection artifact using the DeLone and McLean IS Success Model, Task-Technology
Fit, or any adoption-readiness framework. The detection field has optimised for performance
benchmarks while systematically ignoring the question of whether practitioners will actually
use the systems it produces.

### 4.3.4 AT4 — The Ground Truth Paradox

Five papers report superior performance on synthetic or self-labeled datasets while
simultaneously acknowledging that real-world ground truth labels do not exist in their
target domain. This contradictory pattern (CONTRADICTING relations: C-01 through C-05)
creates a literature that cannot be used as direct evidence of operational viability.
The paradox is particularly acute for public sector applications: audit findings are not
equivalent to fraud labels, and the absence of prosecution does not confirm non-fraud.

## 4.4 DSR Framework Matrix

Mapping 45 papers to Hevner et al.'s (2004) three cycles × four context levels reveals
critical empty cells:

**Table 2: DSR × Context Level Matrix (N papers per cell)**

| DSR Cycle | Village | Sub-national | National | Cross-national |
|---|---|---|---|---|
| DESIGN | **0** | **0** | 4 | 7 |
| RELEVANCE | 15 | 0 | 8 | 5 |
| RIGOR | 11 | 1 | 7 | 12 |

The DESIGN × village cell contains **zero papers** — the most structurally significant
finding in the entire synthesis. No study in this corpus has ever designed and evaluated
an ML artifact using real village-level government financial data. This empty cell,
confirmed robust across all three quality thresholds in the sensitivity analysis, is
the most direct empirical justification for the primary study.

## 4.5 Gap Matrix

Integrating the thematic synthesis, bibliometric evidence, and DSR framework analysis
yields five structured research gaps (Table 3).

**Table 3: Integrated Research Gap Matrix**

| Gap | Severity | Theme | N Evidence Papers | Primary Study Response |
|---|---|---|---|---|
| G1: No ML on Dana Desa data | CRITICAL | AT1 | 14 | Design and evaluate on real Jambi Province data (2023–2025) |
| G2: Label scarcity | CRITICAL | AT2 + AT4 | 19 | Adopt unsupervised ensemble; use expert validation as surrogate |
| G3: No village feature set | CRITICAL | AT1 | 40 | Construct 12-feature taxonomy from KPK Dana Desa typology |
| G4: IS theory absent | PARTIAL | AT3 | 37 | Ground design in Agency Theory + DSR artifact evaluation |
| G5: Deployment gap | METHODOLOGICAL | AT1 | 7 | Scope as audit-support batch tool; frame real-time as future work |

Gaps G1, G2, and G3 are structurally interconnected: G3 (no feature set) is a necessary
prerequisite for G1 (no application), and G2 (no labels) determines method viability for
both. The primary study addresses all three simultaneously — an integrated contribution
not achievable through incremental extension of any single prior work.
