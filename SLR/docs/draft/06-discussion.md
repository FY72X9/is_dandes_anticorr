# 5. Discussion

## 5.1 Answering the Research Questions

### RQ1: What ML methods exist and what are their performance characteristics?

Three unsupervised method families demonstrate applicability to the unlabelled, low-volume
conditions characteristic of village fund data. **Isolation Forest** identifies anomalies
through recursive random partitioning, producing short average path lengths for outlier
instances — a property that proves robust under sparse matrix conditions [12]. **Local
Outlier Factor** compares local density deviations, providing interpretable anomaly scores
relative to neighbourhood context [13]. **Autoencoder-based reconstruction error** detects
anomalies as high-reconstruction-cost instances, with performance advantages when temporal
spending patterns constitute the primary signal [28].

Supervised methods — Random Forest, Gradient Boosting, LSTM — dominate the corpus (22
of 45 papers), but their requirement for labelled training data (AC-LABEL) disqualifies
them from direct application to the Dana Desa context. Graph Neural Networks (20 papers)
offer superior relational anomaly detection but presuppose transaction-graph data structures
absent from village financial records. The ensemble combining IF, LOF, and Autoencoder —
each drawing on different anomaly definitions — provides the best methodological fit for
the primary study's data conditions (RQ1 answered: unsupervised ensemble).

### RQ2: What feature engineering frameworks operationalize corruption signals?

DT1 (16 papers) and DT5 (26 papers) together constitute the evidence base for RQ2. The
procurement fraud literature validates five feature categories: single-bidder frequency
ratios, contract amendment counts and magnitudes, price escalation percentages, timing
concentration metrics (end-of-period clustering), and vendor diversity indices [29, 30].
The village fund governance literature (DT5) adds two context-specific signal dimensions:
budget absorption rate anomalies (deviation from median realization rates across comparable
villages) and disbursement timing irregularities (unusual distribution of Stage 1/2/3
fund releases relative to village development schedule norms) [1, 15].

No paper has integrated these two feature families into a single village fund fraud detection
framework — an integration that the primary study's 12-feature taxonomy performs explicitly.
The taxonomy maps directly from the KPK Dana Desa corruption typology to six absorption
features and six procurement/administrative features (RQ2 answered: transferable feature
categories identified; village-specific integration absent from existing literature).

### RQ3: What structural gaps prevent application to village governance?

Three CRITICAL gaps and two secondary gaps directly respond to RQ3. The primary structural
barrier is the complete absence of ML detection artifacts designed for village-level
governance data (G1) — confirmed by the empty DESIGN×village DSR cell. This absence is
not accidental: it reflects three compounding constraints that the existing literature
has not confronted simultaneously. Label scarcity (G2) eliminates supervised approaches;
the absence of a validated village feature set (G3) means no input pipeline exists;
and the IS theory gap (G4) means that even if an artifact were built, no adoption
evaluation framework has been applied to determine whether auditors would use it.

These gaps are not merely technical limitations — they reflect a deeper conceptual failure.
The ML detection tradition and the IS governance tradition address the same real-world
problem from non-communicating epistemic positions. The primary study's core contribution
is precisely this integration: operationalizing governance knowledge as ML-detectable
features, evaluated against real institutional data, and framed as an IS governance
intervention (RQ3 answered: three CRITICAL structural gaps identified and addressed).

## 5.2 Theoretical Contributions

### 5.2.1 The Operationalization Chasm as a Structural IS Finding

AT1 constitutes a theoretical contribution beyond gap identification. The chasm between
ML detection and IS governance is not a matter of missing papers — it reflects a deeper
epistemological difference in how each tradition defines what corruption _is_. For the
ML tradition, corruption is a statistical pattern: an anomalous vector in feature space.
For the governance tradition, corruption is a social act: a violation of institutional
norms within a principal-agent relationship. Bridging these definitions requires not
just combining methods but constructing a new conceptual bridge — a corruption typology
that is simultaneously sociologically valid (matching known governance failure modes)
and computationally actionable (expressible as numeric features computable from
administrative data). This bridge is the primary theoretical contribution of the
primary study, and its absence in the existing literature is precisely what this SLR
documents.

### 5.2.2 IS Theory as Missing Infrastructure

AT3's finding — 62% IS theory absence — carries a broader implication for the field.
The ML fraud detection literature has optimised for a metric (AUC-ROC on benchmark
datasets) that is entirely orthogonal to the IS success dimensions that determine
whether a detection system can actually serve as a governance instrument. Information
quality (are the anomaly scores interpretable for auditors?), system quality (does the
pipeline run reliably on village-level batch data?), and net benefits (does anomaly
flagging improve audit targeting efficiency?) are the questions that determine field
impact. The field has collectively neglected them.

## 5.3 Practical Implications

For KPK, BPK, and BPKP, the synthesis identifies a specific, actionable design
specification for a Dana Desa anomaly detection tool. The primary study's unsupervised
ensemble approach — requiring no ground truth labels, operating on annual batch
disbursement data, and producing ranked anomaly lists for auditor review — is directly
deployable alongside existing SiKPA/SIMDA monitoring infrastructure. The top-50 anomaly
flagging protocol, validated against KPK/BPK audit records as surrogate ground truth,
provides a practically measurable effectiveness criterion without requiring prosecutorial
confirmation of fraud status.

For international development governance, the study's IS framing — treating detection
as an intervention within institutional processes, not as a standalone technical system
— provides a transferable design template for other fiscal decentralization programmes
facing similar monitoring capacity constraints (Pakistan's PSDP, Bangladesh's LGSP,
Philippines' LGSF).

## 5.4 Sensitivity Analysis Implications

The sensitivity analysis supports the robustness of core findings across quality
thresholds. Two conclusions are particularly important for this discussion:

The village governance findings (DT5) exhibit threshold instability because governance
papers in the corpus are disproportionately published in unranked or Q3 journals. This
scoring disadvantage does not reflect methodological weakness — it reflects the
publication ecosystem of Indonesian public administration research, where domain journals
lack SCImago indexing despite peer review. The domain-override protocol that addressed
this during inclusion was methodologically appropriate; the sensitivity instability
confirms rather than undermines this decision.

The DSR×village gap (empty DESIGN cell) is fully robust: zero DESIGN papers at village
level persists at all three quality thresholds (T1: 0/11 DESIGN papers; T2: 0/8; T3:
0/5). No quality filter reduces this to a sampling artefact.

## 5.5 Comparison with Prior SLRs

This SLR identifies a structural gap that no prior review has characterised. Ahmad et al.
(2022) [3] document method performance without IS theory evaluation; West and Bhattacharya
(2016) [11] address detection heuristics without governance context; Nicholls et al.
(2021) [4] focus on unsupervised methods without public sector framing. The closest prior
SLR, Wahyuni et al. (2023) [21], addresses digital governance of Dana Desa but contains
no ML detection analysis. This review's integration of thematic synthesis with DSR
framework analysis and bibliometric cluster evidence represents a methodological advance
over prior IS-adjacent reviews of this domain.
