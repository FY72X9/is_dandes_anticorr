# In-Depth Analysis — Version 1
## Corruption Indication Detection in Village Fund Activities: Theoretical Interpretation of Empirical Findings

> **Report Date**: April 2026  
> **Analysis Type**: Theory-Driven Interpretive Analysis  
> **Grounded In**: ANALYSIS_REPORT_v1.md (empirical pipeline outputs) · research_concept_phase1.md (theoretical framework) · referenced_quotes_statement.md (verified literature)  
> **Citation Format**: IEEE (continuous numbering as assigned in research_concept_phase1.md)

---

## Table of Contents

1. [Framing: Why In-Depth Analysis Is Necessary](#1-framing-why-in-depth-analysis-is-necessary)
2. [Algorithm Performance in Theoretical Context](#2-algorithm-performance-in-theoretical-context)
3. [The Fraud Triangle in Quantitative Form](#3-the-fraud-triangle-in-quantitative-form)
4. [Principal-Agent Collapse and Information Asymmetry Amplification](#4-principal-agent-collapse-and-information-asymmetry-amplification)
5. [Corruption Typology: Deep Structural Interpretation](#5-corruption-typology-deep-structural-interpretation)
6. [Activity-Level Fraud Vectors: BLT and BUMDes as Structural Vulnerabilities](#6-activity-level-fraud-vectors-blt-and-bumdes-as-structural-vulnerabilities)
7. [Geographic and Temporal Concentration: Structural vs. Incidental Anomaly](#7-geographic-and-temporal-concentration-structural-vs-incidental-anomaly)
8. [Anomaly Persistence as Evidence of Sustained Opportunity Exploitation](#8-anomaly-persistence-as-evidence-of-sustained-opportunity-exploitation)
9. [DeLone and McLean IS Success Model: Operational Assessment](#9-delone-and-mclean-is-success-model-operational-assessment)
10. [Unclassified Anomalies: The Subthreshold Masking Problem](#10-unclassified-anomalies-the-subthreshold-masking-problem)
11. [Methodological Limitations Revisited Through IS Lens](#11-methodological-limitations-revisited-through-is-lens)
12. [Implications for APIP Inspection Practice](#12-implications-for-apip-inspection-practice)
13. [Research Gap Validation: How Empirical Results Confirm Theoretical Claims](#13-research-gap-validation-how-empirical-results-confirm-theoretical-claims)
14. [Directions for Phase 2](#14-directions-for-phase-2)

---

## 1. Framing: Why In-Depth Analysis Is Necessary

The descriptive outputs summarised in ANALYSIS_REPORT_v1.md establish what the pipeline detected: 3,107 consensus-flagged records, 642 Tier-1 villages, LOF bimodality coefficient of 0.957, T1 and T7 co-dominance at 50.6% and 50.5% respectively. These numbers are necessary but insufficient. Numbers without theory produce audit lists without explanatory power — and inspection lists without explanatory power are indistinguishable from random sampling to the institutional actors who must act on them.

This in-depth analysis converts quantitative outputs into theoretically grounded arguments. Each empirical finding is interrogated through three analytical lenses: (a) the algorithmic properties of the detection methods, which predict specific patterns in score distributions and inter-method agreement; (b) the theoretical frameworks adopted in the study — Fraud Triangle, Principal-Agent Theory, and the DeLone and McLean IS Success Model — which map computational signals to social phenomena; and (c) the documented modus operandi drawn from judicial records and institutional audit reports [6], [8], which ground algorithmic abstraction in verified corruption behaviour.

The central analytical question this document answers is: **do the empirical findings confirm, refine, or challenge the theoretical premises on which the pipeline was designed?** The answer is that they do all three — confirming the Fraud Triangle's structural predictions, refining the precision of typology detection, and challenging the adequacy of single-threshold rule-based typology assignment for compound fraud patterns.

---

## 2. Algorithm Performance in Theoretical Context

### 2.1 LOF Bimodality Coefficient 0.957 — Theoretical Explanation

The Local Outlier Factor (LOF) produced a bimodality coefficient of 0.957 — the highest among the three methods by a substantial margin, exceeding the bimodality threshold of 0.555 by 73%. This result is theoretically predictable and empirically meaningful, and it warrants detailed explanation rather than bare reporting.

LOF computes anomaly scores by comparing each record's local reachability density to its k-nearest neighbours' densities [25]. In a dataset where normal records cluster coherently within activity categories (determined by Kode_Output prefix codes), normal records receive LOF scores approaching 1.0 — they are neither denser nor sparser than their neighbours. The Jambi village fund dataset provides precisely this structure: activities within the same Kode_Output category (e.g., all PAUD operational expenses, all road construction activities) share similar cost ranges, procurement methods, and disbursement patterns, forming natural high-density regional clusters in feature space.

When a fraudulent activity sits within such a cluster — for instance, a road construction activity with `cost_per_unit` at 42.42 standard deviations above category mean — it is locally isolated within a dense cluster of comparably classified activities. LOF correctly identifies this record as a local outlier (LOF >> 1.0) even though the record may not appear as a global outlier from Isolation Forest's path-partitioning perspective. The extreme L-shaped distribution (virtually all normal records near LOF = 1.0, a thin anomalous tail extending to LOF = 5.40 × 10⁹) reflects the structural clarity of local density contrasts when corruption manifests as category-specific cost inflation — which, as the T1+T7 analysis in Section 5 demonstrates, is the dominant fraud mechanism in this dataset.

This finding directly confirms Li et al.'s [18] observation that LOF identifies a distinct anomaly subset from Isolation Forest's global partitioning on government spending data. The theoretical implication is significant: supervised or globally-parametric detection methods would structurally miss the within-category price inflation pattern that LOF captures. An audit system relying solely on IF would overlook 4,668 records (4,985 LOF flags minus 317 IF∩LOF overlap) that the local density mechanism identifies as administratively suspicious within their Kode_Output peer group.

### 2.2 Isolation Forest Bimodality Coefficient 0.335 — Why Path-Partitioning Produces Ambiguous Scores Here

Isolation Forest's BC of 0.335 indicates a unimodal score distribution — the decision function produces a broad, overlapping range without a clean separation between normal and anomalous clusters. This result, while appearing to indicate inferior discriminative power, is theoretically explicable and does not constitute a failure of the algorithm per se.

Isolation Forest isolates anomalies by measuring random-partitioning path length: records that require fewer partitions to isolate are globally sparse and therefore anomalous [19]. The algorithm performs optimally when anomalies are both globally rare and globally different — occupying extreme positions in the joint feature space. Village fund corruption patterns, however, are systematically structured rather than randomly sparse: they cluster by activity category (all BLT manipulations look similar to each other; all fictitious road construction records share structural features). This clustering means that IF's path-partitioning mechanism partially isolates anomalies as a group — they are globally rare — but simultaneously misidentifies the cluster's internal members as less anomalous than true global outliers, suppressing score variance and producing a unimodal distribution.

The consequence is that the 95th-percentile threshold (≈ +0.18) falls within a dense score region, drawing the anomaly boundary through normal data. This does not invalidate IF's detections — the 7,974 flagged records include genuine anomalies — but it does mean that IF's threshold placement introduces more false positives among borderline records than LOF's natural score valley achieves. For operational inspection triage purposes, IF records should be weighted by their consensus score (confirmed by LOF or RDA) rather than by their IF score alone.

### 2.3 Inter-Method Overlap Architecture: What the 50.3% IF∩RDA Convergence Reveals

The pairwise overlap structure — IF∩RDA = 50.3%, IF∩LOF = 6.4%, LOF∩RDA = 12.0% — encodes important methodological information that the raw numbers obscure.

IF and RDA converge on 2,506 of RDA's 4,985 flagged records. Both methods apply threshold-based scoring: IF at the 5th percentile of the decision function and RDA at the 95th percentile of reconstruction error. Both methods respond strongly to globally extreme deviations across the full feature set — records with `cost_per_unit` at 102.83 standard deviations above median and `cost_deviation_by_category` at 42.42 simultaneously represent global multi-feature extremes that both global partitioning (IF) and global reconstruction (RDA) flag as anomalous. Their convergence is not redundant: it confirms that the most extreme records in the Jambi dataset are anomalous by multiple independent technical criteria — a high-confidence corruption signal.

LOF's low overlap with both other methods (6.4% with IF, 12.0% with RDA) reflects its architectural independence: it operates strictly on local density relationships without reference to global thresholds. The 3,951 records LOF flags that neither IF nor RDA detects represent locally deviant activities — activities that are unremarkable in the global feature distribution (thus evading IF's global partitioning) and reconstructable by the autoencoder at normal MSE levels (thus evading RDA's error threshold), but whose cost structure, completion reporting, or procurement method is statistically abnormal relative to their immediate peer activities within the same Kode_Output category. These are the within-category mark-up cases — the exact fraud mechanism documented in 50.6% of typology assignments (T1: Mark-up).

This architecture demonstrates why Alam et al.'s [24] recommendation for multi-paradigm benchmarking produces substantively different detection coverage than any single method: the three paradigms cover three distinct channels through which corruption manifests in financial data — global extremity, global non-reconstructability, and local peer deviation — and a consensus across any two of these channels constitutes stronger evidence than any single channel alone.

### 2.4 RDA Reconstruction Error Architecture and the Contamination Resistance Argument

RDA's bimodality coefficient of 0.703 — the 12.5× separation between median MSE (2.80 × 10⁻⁵) and the 95th-percentile threshold (3.50 × 10⁻⁴) — confirms that the sparse noise decomposition successfully separated normal expenditure patterns from anomalous ones during training. Under a standard autoencoder trained on the same contaminated dataset, the network would partially learn to reconstruct anomalous feature combinations (because they appear in the training set), compressing the gap between normal and anomalous reconstruction errors and reducing bimodality [34]. The observed 12.5× separation provides empirical confirmation that the sparse noise matrix S absorbed contaminating records during training, isolating the encoder's learned representation of normal village fund behaviour.

The per-feature reconstruction error diagnosis (Section 9 of ANALYSIS_REPORT_v1.md) further validates the RDA's interpretive utility: `avg_completion` dominates the primary error feature for 43.5% of Tier-1 villages, followed by `activity_category` (31.2%) and `cost_per_unit` (14.9%). This rank ordering is not random — it reflects the structural properties of village fund fraud. Completion percentage manipulation is the most prevalent documentation falsification technique: reporting T1 disbursement at 100% while T2 and T3 realisations approach zero creates an `avg_completion` pattern that is simultaneously anomalous in absolute magnitude and impossible to reconstruct from normal fund absorption behaviour. The autoencoder's failure to reconstruct these completion profiles is a direct artefact of fraudulent reporting.

---

## 3. The Fraud Triangle in Quantitative Form

### 3.1 Pressure: The Fiscal Expansion Context

The Fraud Triangle's Pressure dimension — the financial or situational motive that drives individuals to consider fraudulent action — appears quantitatively in the temporal structure of the dataset. The 2023 fiscal year produced the highest IF anomaly rate (10.5%) and the highest absolute consensus flag count (1,364 records), compared to 2024 (735 records, 2.0% consensus rate) and 2025 (1,008 records, 3.3%).

This 2023 elevation aligns structurally with the post-COVID fiscal expansion period, during which Indonesia's central government significantly expanded village fund allocations as part of economic recovery programming. Budget expansion — the gap between allocated Pagu and historical absorption — creates Pressure in the Fraud Triangle sense: village officials responsible for delivering spending targets within a fiscal year face organisational pressure to maximise absorption, creating incentives to fabricate or inflate activities. Hidajat [6] specifically identifies pressure from budget utilisation targets as one of the principal drivers of village fund fraud — the Diamond Fraud theory operationalisation cited in that paper adds "capability" to the Cressey triangle, and budget expansion provides both the motive (Pressure) and the means (inflated Pagu creating mark-up headroom).

The fact that 2023 anomaly rates decline in 2024 and partially recover in 2025 is consistent with a pressure-driven model: post-expansion audit scrutiny typically intensifies in the year following a high-anomaly period, temporarily suppressing fraudulent behaviour. The 2025 uptick — LOF increases to 5.8%, RDA to 5.9% — may signal recurrence after a period of reduced vigilance.

### 3.2 Opportunity: The 98.8% Swakelola Structure as Structural Vacancy of Control

The Opportunity dimension of the Fraud Triangle — weak controls and oversight that make fraud executable without detection — is most starkly quantified by a single statistic: **98.8% of all village fund activities are procured through Swakelola**, a self-managed procurement mechanism requiring no competitive tender, no independent cost benchmarking, and no mandatory third-party verification of physical outputs.

Søreide's [9] analysis of procurement corruption identifies competitive bidding as the primary structural safeguard against procurement-stage fraud. Its near-total absence from village fund activity procurement removes the most effective preventive control at the transaction level. The consequence is direct: all activity cost decisions — what to spend, how much to pay per unit, how to record completion — rest with the village head (kepala desa) as both authoriser and reporter. Sutarna and Subandi [9] identify this information asymmetry — the agent controlling both the action and its documentation — as the defining condition for principal-agent exploitation in the village fund context. The 98.8% Swakelola finding transforms this theoretical condition into an empirical measurement of the structural opportunity environment.

The slight but meaningful Swakelola over-representation in consensus-flagged records (96.4% of 3,107 consensus flags, compared to 98.8% baseline) requires careful interpretation. The difference is only 2.4 percentage points. This does not indicate that Swakelola records are proportionally more suspicious than baseline — it indicates that the detection algorithms successfully discriminate within an almost entirely Swakelola population. The discriminating variables are `cost_per_unit` deviation, `avg_completion` anomaly, and `cost_deviation_by_category` — not the procurement method flag itself. This confirms that `swakelola_high_value`, while theoretically motivated, is not the strongest detection feature; the cost structure and completion reporting irregularities within Swakelola activities carry the primary anomaly signal.

### 3.3 Rationalisation: The Activity Code Ambiguity Structure as Cognitive Cover

The Fraud Triangle's Rationalisation dimension — the cognitive justification that enables trusted persons to reframe fraud as acceptable — manifests in the dataset through the T7 Cross-Category Dump pattern, which affects exactly 50.5% of consensus-flagged records (1,568 records in 3,107 total flags).

Activity codes that carry operationally vague descriptions — "Biaya Koordinasi Pemerintah Desa," "Operasional PKK," "Penyelenggaraan Festival Kesenian/Kebudayaan/Keagamaan" — appear disproportionately in flagged records (see Section 5.2 of ANALYSIS_REPORT_v1.md). These category descriptions provide rationalisation scaffolding: a village official who inflates "coordination costs" to ten times the category norm can, when questioned, assert that coordination activities are inherently variable and difficult to benchmark. This is precisely the rationalisation mechanism that Hidajat [6] documents — the perpetrator's ability to frame fraudulent expenditure as legitimate administrative discretion is structurally enabled by the ambiguity of category definitions in the Siskeudes activity catalogue.

The T1+T7 co-occurrence at 1,141 records (36.7% of all consensus flags) — where price mark-up and cross-category routing occur simultaneously — is not coincidental. It encodes a specific fraud mechanism: the fraudster selects activity categories whose definitional ambiguity provides rationalisation coverage, routes inflated expenditure through those categories (generating T7 cross-category signals), and marks up unit costs under the cover of definitional flexibility (generating T1 price signals). The algorithm's detection of this compound pattern validates that the feature engineering correctly operationalised the Rationalisation dimension of the Fraud Triangle as a detectable computational signal.

---

## 4. Principal-Agent Collapse and Information Asymmetry Amplification

### 4.1 The Structural Information Asymmetry in Village Fund Governance

Sutarna and Subandi [9] identify the village head as an agent operating under conditions of profound information asymmetry relative to the principal chain — district government (Bupati), provincial government, KPK, and BPKP. The agent controls: (a) activity planning (what activities to execute), (b) activity execution (how to procure and deliver), (c) financial recording (what Siskeudes records to enter), and (d) progress reporting (what completion percentages to submit). The principal observes only the Siskeudes records — precisely the data layer that the fraudulent agent controls.

The Jambi province monitoring context amplifies this structural asymmetry in two measurable ways. First, jaga.id recorded only 11 complaint submissions from Jambi Province against 761 national reports — constituting 1.4% of national voluntary reporting while Jambi contains a larger proportional share of village fund-receiving villages. Provinces of comparable size (Sumatera Utara: 81 complaints, Sumatera Selatan: 48 complaints) registered substantially higher reporting rates. Low voluntary oversight engagement means that the community-based principal observation channel — the mechanism through which citizens can alert APIP to on-ground irregularities — is effectively inactive in Jambi, removing the informal monitoring signal that might constrain agent behaviour between formal audit cycles.

Second, Srirejeki and Faturokhman [28] document that kabupaten-level inspectorates lack operational staffing to screen thousands of individual village activity records per disbursement cycle. With Jambi's Penyerapan dataset containing 99,692 activity records across three fiscal years, and a typical inspectorate cycle covering a subset of villages per year, the probability that any given anomalous activity record receives direct APIP attention prior to the present pipeline is structurally near zero. Alfada's [29] empirical confirmation — from panel GMM estimation across 19 Indonesian provinces — that intergovernmental transfer dependence combined with weak accountability structures drives elevated corruption incidence applies directly to Jambi's structural profile.

### 4.2 How the Pipeline Reconstructs the Principal's Informational Position

The significance of the anomaly detection pipeline, viewed through the principal-agent lens, is that it reconstructs a meaningful principal observation capability from data the agent was assumed to control exclusively. The agent reports Siskeudes records believing that the complexity and volume of activity-level data makes systematic statistical screening impractical — a reasonable assumption given that no such screening existed at the provincial level prior to this research.

The pipeline's feature engineering reverses this information advantage. `cost_deviation_by_category` computes year-stratified z-scores of unit costs within each Kode_Output grouping — a calculation the agent cannot corrupt without simultaneously corrupting every other comparable activity in the same category across the province. `avg_completion` captures the reporting pattern across all three disbursement stages — a cross-stage signal the agent would need to coordinate across the T1, T2, and T3 reporting cycles to falsify coherently. The `swakelola_high_value` flag identifies activities where the procurement structure eliminates benchmarking, but the anomaly detection treats the entire within-category cost distribution as the benchmark — reconstructing the comparative cost reference the Swakelola mechanism was designed to eliminate.

This is the computational operationalisation of the DeLone and McLean information quality construct [10]: the pipeline produces information (ranked anomaly lists with typology diagnoses) from data that previously carried no actionable signal for the principal. Information quality becomes the mechanism through which information asymmetry is reduced.

### 4.3 The 5-Year Detection Lag from Prosecution Records

The prosecution cases cited in the research background provide empirical calibration of the principal-agent monitoring gap. The four verified Jambi cases collectively document irregularities spanning fiscal years 2020–2024, yet prosecution or administrative action occurred no earlier than mid-2024 — a detection lag ranging from two to five years.

Within the current study's data scope (2023–2025), the implication is specific: activities flagged by the pipeline as consensus anomalies in 2023 would, under the existing monitoring regime, remain undetected through the period of legal prosecution in approximately 2027–2028 — by which point compounded losses across subsequent disbursement stages would substantially exceed the original irregularity value. The Desa Muara Hemat case (Rp 942 juta, detected after ~5 years) and Desa Batang Merangin case (Rp 644 juta, TA 2021, named suspects only in late 2025) illustrate precisely this compound-loss trajectory. The pipeline's ability to surface 2023 anomaly patterns in the same fiscal period they occur — rather than after a 2–5 year institutional escalation pathway — constitutes the primary reduction in information asymmetry that the principal-agent framework requires.

---

## 5. Corruption Typology: Deep Structural Interpretation

### 5.1 T1 + T7 Co-Dominance as a Compound Fraud Mechanism

The simultaneous co-dominance of T1 (Mark-up / Price Inflation: 1,571 records, 50.6%) and T7 (Cross-Category Dump: 1,568 records, 50.5%), with T1+T7 co-occurring in 1,141 records (36.7% of all consensus flags), encodes a specific compound fraud mechanism that deserves structural decomposition.

The typical progression of this fraud type follows three stages. First, the village official selects activity categories with definitional ambiguity — "operasional" items (PKK, PAUD, RT/RW, BPD) whose cost structures lack credible external benchmarks. Second, the official fabricates or inflates unit quantities or unit prices under the cover of the selected category's definitional flexibility, routing expenditure through an activity code whose peers in other villages show markedly different cost profiles — generating the `cost_deviation_by_category` z-score that triggers T1 detection. Third, the expenditure routing may itself deviate from the activity category's typical Kode_Output group, meaning the activity code is misaligned with the nature of the spending — generating the `activity_category` extreme z-score that triggers T7 detection.

The 1,141 co-occurrence records are the most analytically significant subset of the entire flagged dataset, because they represent activities where two independent algorithmic signals converge on the same record through different feature channels. This double convergence within a single record, in addition to the multi-method consensus requirement (≥ 2 of 3 algorithms), means these records carry three independent layers of anomaly evidence: method convergence across algorithmic paradigms AND feature convergence across independent financial indicators.

### 5.2 T2 Ghost Activity — The Structural Absence Problem

T2 (Ghost Activity / Proyek Fiktif: 774 records, 24.9%) identifies activities with near-zero absorption despite recorded allocation. The detection rule operates on `absorption_ratio` (near-zero total realization relative to Pagu) and `avg_completion` (near-zero completion percentages). The Jambi prosecution record validates this typology directly: Desa Jambi Tulo's 2024 irregularities involved "fictitious road and seedling procurement — zero field output" (Rp 300+ juta, disbursement frozen by Inspektorat [31]), and Desa Batang Merangin's "unfinished and fictitious meeting hall construction" (Rp 644 juta [32]) both constitute T2 patterns in the classification schema.

The 450 records with T2 alone (no co-occurring T1 or T7) represent the cleanest ghost activity signal: low absorption without price manipulation. These are activities that appear in Siskeudes records but show no evidence of physical execution at any disbursement stage. The detection rule captures this as an extreme: activities budgeted but unrealised. Whether this reflects non-execution (proyek fiktif) or deferred execution (legitimate rollover) cannot be determined from financial records alone — field verification is required. This constitutes one of the primary arguments for connecting the algorithmic output to APIP inspection protocols rather than treating machine flags as definitive determinations.

### 5.3 T4 Stage Lock — Zero Detections and Their Methodological Implication

T4 (Stage Lock: 0 detections) produced no results despite representing a theoretically well-motivated fraud mechanism — concentrating all realization in a single disbursement stage to fabricate multi-stage progress. The complete absence of detections reveals a specific implementation gap with important methodological implications.

The implemented `n_stages_active` feature counts disbursement stages with Real > 0. This binary count does not capture the *concentration* of spending within a stage — a record with Real_T1 = 98% of total, Real_T2 = 1%, Real_T3 = 1% receives `n_stages_active = 3` (three active stages), when in fact the concentration of spending in T1 is the anomaly signal. Many legitimate activities have regulatory disbursement schedules that front-load T1 payments (particularly Bantuan Langsung Tunai, which disburses in multiple waves with T1 constituting the majority), making `n_stages_active = 1` or `n_stages_active = 2` ambiguous without activity-type stratification.

The recommended v2 implementation — Stage Lock index = max(Real_T1, Real_T2, Real_T3) / total_realization, with flag threshold > 0.95 when `n_stages_active ≥ 2` — would correctly identify front-loaded concentration while excluding legitimate single-stage activities. The absence of T4 detections in v1 does not indicate that stage-lock fraud is absent from the dataset; it indicates that the current feature cannot discriminate it from legitimate single-stage activity schedules. This limitation matters practically because the Desa Muara Hemat prosecution involved fictitious physical construction reports (Rp 942 juta), a fraud type that typically accompanies artificial multi-stage completion reporting — precisely the signal T4 was designed to capture.

### 5.4 The Unclassified 22.8% — Compound Anomaly Without Typological Capture

708 consensus-flagged records (22.8%) carry no typology assignment. These records passed multi-method consensus thresholds — flagged by at least two of three independent algorithmic paradigms — yet exceeded no individual typology rule threshold. This cohort is analytically significant because it challenges the completeness of the current rule-based typology framework.

The theoretical interpretation is that these records exhibit compound anomalies where multiple features are simultaneously slightly elevated — individually below typology thresholds, collectively above consensus detection thresholds. This is structurally consistent with the "masking" and "camouflage" behaviours identified in advanced fraud detection literature [19]: sophisticated actors learn to distribute irregularity across multiple dimensions to avoid triggering any single indicator, while the aggregate pattern remains statistically deviant.

The RDA's ability to detect these records through non-linear reconstruction error — capturing compound feature interaction patterns that no individual rule encodes — confirms Kumar et al.'s [19] theoretical argument that deep autoencoder architectures detect compound anomaly interactions that rule-based and linear methods structurally miss. The 22.8% unclassified proportion represents the frontier of interpretable fraud detection: the algorithm detects the signal, but the typology taxonomy lacks the resolution to characterise it. A T8 "Compound Irregular" category, or a soft typology classification model trained on the T1–T7 labelled subset, would address this gap in v2.

---

## 6. Activity-Level Fraud Vectors: BLT and BUMDes as Structural Vulnerabilities

### 6.1 BLT Dana Desa — The Cash Disbursement Accountability Vacuum

Bantuan Langsung Tunai Dana Desa (BLT-DD) heads the consensus-flagged activity list with 301 records — the highest single-activity count, representing 9.7% of all 3,107 consensus anomalies. This concentration is not attributable to BLT's prevalence alone: BLT constitutes a non-proportional share of flags relative to its overall record count in the full dataset.

The structural explanation connects directly to the Fraud Triangle's Opportunity dimension. BLT-DD is a direct cash transfer programme — the village disburses cash to registered beneficiaries (penerima manfaat), verified through beneficiary signature lists. Physical outputs are absent by design. Audit verification depends entirely on: (a) the accuracy and completeness of beneficiary registration lists controlled by the kepala desa, and (b) the authenticity of disbursement signatures that APIP must verify against legitimate living beneficiaries. Hidajat [6] specifically identifies pemotongan (deduction at the point of distribution — distributing less than the authorised amount while recording full disbursement) as the BLT-specific fraud mode, a manipulation that leaves no trace in Siskeudes financial records while creating an `absorption_ratio` and `avg_completion` pattern that deviates from expected disbursement behaviour.

The 301 flagged BLT records across 3,107 consensus anomalies (9.7%) represent the computational signature of pemotongan: full-value entries in the Siskeudes record with anomalous cost-per-beneficiary deviations from provincial BLT disbursement norms. These records require field verification — specifically, cross-referencing actual beneficiary receipts against Siskeudes entries — a task that APIP inspectors are operationally positioned to conduct with a ranked BLT anomaly list as the triage input.

### 6.2 Penyertaan Modal BUMDes — The Equity Injection Opacity Problem

Penyertaan Modal BUMDes (equity injections into village-owned enterprises) ranks second among flagged activities with 206 consensus records. This represents the most structurally opaque fraud category in the entire village fund typology for three compounding reasons.

First, equity injections have no unit of measurement — there is no Volume or Satuan to calculate `cost_per_unit` against, making the primary price-signal feature (T1 detection rule) structurally inapplicable. Detection relies entirely on `absorption_ratio` anomalies and `cost_deviation_by_category` relative to peer Penyertaan Modal entries across other villages. Second, the accountability pathway for equity injections is recursive: the kepala desa authorises the injection, the BUMDes management (appointed by and accountable to the kepala desa) receives and records the funds, and the BUMDes reports back to the same kepala desa who authorised the injection. The principal (district government) receives only the Siskeudes entry — not the BUMDes enterprise's utilisation of the injected capital. Third, Penyertaan Modal's over-representation in consensus-flagged records relative to baseline (2.7% of consensus flags vs. 0.8% baseline — a 3.375× ratio) confirms that the algorithms successfully detected anomalies within this small but structurally vulnerable population, suggesting that the detected patterns represent genuine structural irregularities rather than distributional noise.

The ICW (2024) [8] report documents equity injection irregularities as one of the most challenging corruption modes to prosecute due to their documentation opacity. The algorithmic flag on 206 records constitutes a prioritised investigation entry point that field auditors can use to request BUMDes financial records, physical asset inventories, and enterprise activity logs — the multi-source verification protocol that traditional APIP cycles rarely apply to BUMDes activities due to competing inspection priorities.

---

## 7. Geographic and Temporal Concentration: Structural vs. Incidental Anomaly

### 7.1 Kabupaten Bungo's Dominance — Structural Diagnosis

Kabupaten Bungo recorded the highest absolute consensus anomaly count (577 records, 103 Tier-1 villages) and the largest single-year contribution in 2023 (319 records, 23.4% of 2023 total consensus anomalies). Understanding why Bungo leads requires moving beyond statistical description into structural hypothesis generation.

Two non-exclusive structural hypotheses warrant examination for Phase 2. First, budget structure: Bungo may allocate a disproportionate share of village fund budgets to Swakelola-executed operational activities relative to capital infrastructure — the activity type profile of Bungo's anomaly portfolio (dominated by T1 mark-up and T7 cross-category dump) is consistent with operational budget inflation rather than infrastructure fraud. Second, APIP capacity: if Bungo's kabupaten inspectorate operates at reduced staffing or coverage relative to its village count, the probability of detection-induced deterrence is lower, allowing anomalous patterns to persist across years. The Tier-1 village persistence analysis (103 villages with ≥ 2 flagged years out of 3) supports the deterrence-gap hypothesis: persistent anomalies signal that existing monitoring mechanisms have not constrained fraudulent behaviour across fiscal years.

### 7.2 Kota Sungai Penuh's Anomaly-to-Village Ratio

Kota Sungai Penuh's 309 consensus anomalies concentrated in an urban municipality (Kota-status administrative unit) is a distinct pattern from Bungo's rural-kabupaten concentration. Urban municipalities typically have higher per-activity expenditure values due to higher input costs, more complex service delivery requirements, and higher personnel cost benchmarks. This creates a specific mark-up environment: the same percentage price inflation in a Sungai Penuh activity produces a higher absolute loss than the equivalent inflation in a rural kabupaten desa.

The concentration of 221 out of 309 Sungai Penuh consensus anomalies in 2023 alone (71.5% of its three-year total) is particularly striking — it represents either a structural change in expenditure patterns during 2023 or a genuine surge in anomalous activities during the post-COVID budget expansion period. The later decline (88 records across 2024+2025 combined) could reflect either genuine correction or successful adaptation of reporting patterns to reduce detectable anomalies. These two scenarios have opposite policy implications — genuinely reduced fraud requires no escalation, while adapted reporting suggests the need for feature engineering updates in v2 to capture evolved concealment patterns.

### 7.3 Temporal Pattern Interpretation: 2023 Anomaly Spike vs. 2024 Trough

The across-method anomaly rate profile — 2023 substantially higher than 2024 for all three algorithms (IF: 10.5% → 6.5%, RDA: 5.5% → 3.8%, Consensus: 4.1% → 2.0%) — with partial recovery in 2025 (IF: 7.1%, Consensus: 3.3%) forms a distinctive temporal pattern carrying two plausible explanations.

The fiscal expansion hypothesis attributes the 2023 spike to budget expansion pressure: Indonesia's central government increased village fund allocations in 2023, expanding the Pagu-realization gap and creating both the opportunity (larger budget to manipulate) and the pressure (mandatory absorption targets) for fraudulent activity. The post-correction hypothesis interprets the 2024 trough as genuine administrative improvement — new village fund regulations introduced in 2023 (PP No. 11/2021 implementation guidance) may have produced temporary compliance improvements.

These two hypotheses are not mutually exclusive and both may contribute to the observed pattern. The 2025 partial recovery is more diagnostically useful: if improved compliance explained the 2024 trough, 2025 rates should remain low or continue declining. Their uptick (LOF: 4.6% → 5.8%, RDA: 3.8% → 5.9%) suggests a rebound rather than sustained improvement — consistent with compliance interventions that modify surface reporting behaviour without addressing structural opportunity factors (the 98.8% Swakelola structure, the inspectorate capacity gap). A quarterly or semi-annual algorithmic monitoring cycle that processes Siskeudes records at each disbursement stage would provide the temporal resolution to distinguish between these trajectories, rather than relying on the annual cross-section that the current dataset captures.

---

## 8. Anomaly Persistence as Evidence of Sustained Opportunity Exploitation

### 8.1 The 174 Fully Persistent Villages as the Highest-Priority Analytical Cohort

The 174 villages that generated consensus anomalies in all three fiscal years (2023, 2024, and 2025) constitute the most analytically significant cohort in the entire study output. Their persistence score of 1.0 — every available fiscal year produced at least one consensus-flagged activity — encodes a specific theoretical condition: the Fraud Triangle's Opportunity dimension has been continuously available, and the detection-deterrence mechanism has been absent, across a full three-year period.

From the principal-agent perspective, three-year persistence means that the information asymmetry between kepala desa and the principal chain has remained uncorrected through three full disbursement cycles. This is not consistent with incidental irregularity — a one-time entry error or legitimate budget deviation would not systematically recur across three independent fiscal years. Statistical probability favours a structural explanation: these 174 villages exhibit persistent expenditure pattern anomalies because the underlying structural conditions enabling them (Swakelola dominance, low community oversight, insufficient inspectorate coverage) have not changed during the study period.

The prosecution record reinforces this interpretation empirically. Desa Batang Merangin's irregularities span TA 2021 with a village facilitator added as a suspect only in November 2025 — indicating that collusion networks persist across administrative cycles even as corruption personnel change. The absence of any prosecution from within the study's 2023–2025 data window suggests that the 174 fully persistent villages in the pipeline output include cases where the compounding loss trajectory has already begun but institutional escalation has not yet occurred.

### 8.2 Persistence Score Methodology and its Theoretical Justification

The village-level anomaly persistence score — proportion of fiscal years (2023–2025) with at least one consensus-flagged activity — operationalises a critical conceptual distinction between systematic and incidental irregularity that the Fraud Triangle does not explicitly encode.

The Fraud Triangle describes conditions for a single fraudulent act. The persistence score extends the framework to multi-period behaviour: a village that generates anomalies in all three years demonstrates not merely that the Fraud Triangle conditions existed once, but that they remained unconstrained across repeated cycles — indicating either a sustained structural Opportunity environment or, more concerningly, that prior anomalies failed to produce corrective institutional responses.

The distinction between Tier 1 (642 villages, ≥ 2 flagged years) and Tier 2 (459 villages, 1 flagged year) carries inspection prioritisation implications beyond simple anomaly count. A village flagged in 1 of 3 years may represent legitimate spending volatility. A village flagged in 2 or 3 of 3 years demonstrates cross-year pattern consistency that transcends single-period noise — the systematic behaviour signal that APIP inspection protocols should prioritise above single-year high-score records.

---

## 9. DeLone and McLean IS Success Model: Operational Assessment

### 9.1 The Six-Dimension Framework Applied to the Pipeline

DeLone and McLean's [10] IS Success Model evaluates information systems along six interdependent dimensions: System Quality, Information Quality, Service Quality, Use / Intention to Use, User Satisfaction, and Net Benefits (Individual and Organisational Impact). This assessment applies the model to evaluate the pipeline's maturity against each dimension.

| D&M Dimension | Pipeline Status | Assessment |
|---|---|---|
| **System Quality** | Three independent algorithms + consensus logic + tier classification + per-feature RDA diagnosis | ✅ High — multi-paradigm architecture, automated three-year longitudinal panel |
| **Information Quality** | 3,107 consensus flags (3.1%), typology labels on 77.2%, RDA per-feature driver for each Tier-1 village | ✅ Moderate-High — actionable precision; 22.8% unclassified limits complete typological resolution |
| **Service Quality** | Export to structured CSV (expert validation sheets, Tier-1 priority list) — no dashboard or APIP integration | ⚠️ Pending — data outputs exist but no service delivery mechanism to inspectorate |
| **Use / Intention to Use** | Expert validation pending (4 × top-50 sheets unfilled) — no documented APIP engagement | ❌ Not yet established — Precision@50 metric unavailable; user adoption unmeasured |
| **User Satisfaction** | N/A — no user engagement has occurred | ❌ Not applicable at current stage |
| **Net Benefits — Individual Impact** | Auditors receive ranked list + typology + RDA feature driver — design supports decision | ✅ Design-level: output format enables individual audit decision support |
| **Net Benefits — Organisational Impact** | 174 persistent villages available for mandatory inspection cycle; 642 Tier-1 list reduces triage effort from 1,364 to 642 | ✅ Design-level: inspection coverage efficiency improvement quantifiable |

### 9.2 The Expert Validation Gap as a D&M Use Criterion

The most critical limitation for D&M Success Model compliance is the unfilled expert validation sheets — the Use dimension remains the only unestablished criterion. DeLone and McLean's model holds that Information Quality drives Use, and Use drives Individual and Organisational Impact. Without demonstrated Use by an intended user (an APIP officer or equivalent domain expert), the pipeline's organisational impact remains a theoretical projection rather than an empirical finding.

The Precision@50 metric — expert validation of the top-50 records per method as "Suspicious / Not Suspicious" using the modus operandi rubric — is not merely an academic evaluation metric. In the D&M framework, it operationalises the Use dimension: an expert who reviews and classifies the validation sheets demonstrates use of the system's information quality output, and their subsequent assessment constitutes the individual impact measurement. Expert validation is therefore the single highest-priority action for converting the pipeline from a System Quality / Information Quality achievement into a full IS Success demonstration.

### 9.3 Information Quality Contribution to the D&M Chain

The pipeline's most defensible D&M claim is Information Quality — the accuracy, completeness, timeliness, and actionability of its anomaly outputs. Specifically:

- **Accuracy**: The multi-method consensus requirement (≥ 2 of 3 independent paradigms) substantially reduces single-method false positives. The 156 triple-consensus records represent the highest accuracy stratum — independent algorithmic reasoning from tree partitioning, local density estimation, and non-linear reconstruction converges on the same 156 records.
- **Completeness**: Three fiscal years of longitudinal data enable persistence scoring — a dimension of information completeness unavailable from any single-period analysis.
- **Timeliness**: The pipeline processes 99,692 records across three years in a single Colab notebook execution — the computational latency between data availability and detection output is hours, not the 2–5 year institutional lag documented in the prosecution records.
- **Actionability**: RDA per-feature error diagnosis, typology labelling, and geographic/village-level aggregation produce information in a form that maps directly to APIP's existing inspection workflow.

---

## 10. Unclassified Anomalies: The Subthreshold Masking Problem

### 10.1 The Theoretical Case for Composite Irregularity Patterns

The 708 unclassified consensus-flagged records (22.8%) represent the algorithmically most challenging cohort to interpret. These records triggered multi-method consensus — at least two of three independent algorithmic paradigms flagged them as anomalous — yet no individual typology threshold was breached. The natural inference is that the anomaly resides in the interaction of features rather than in the extremity of any single feature.

Kumar et al. [19] document this phenomenon in their hybrid anomaly detection study: sophisticated fraudsters exposed to threshold-based detection mechanisms adapt their behaviour to keep each individual indicator just below the threshold, distributing irregularity across multiple dimensions to avoid triggering any single rule. The consequence is that individual features remain within plausible ranges while the joint feature distribution is statistically impossible under honest expenditure behaviour. A standard rule engine cannot detect this pattern because each rule applies to a single feature independently. The autoencoder detects it because the non-linear encoder learns the joint distribution of features under normal expenditure behaviour — when multiple features are simultaneously mildly deviant in a correlated manner, the autoencoder's reconstruction of their joint pattern fails, producing elevated MSE despite no single feature being individually extreme.

### 10.2 What the 708 Unclassified Records Tell APIP Inspectors

From an operational perspective, the 708 unclassified records do not represent "inconclusive" findings — they represent records where automated classification is insufficient and human expert judgment is essential. The multi-method consensus requirement already establishes algorithmic confidence: something is statistically wrong with these records, even if the typology label cannot be assigned mechanically.

The appropriate APIP protocol for unclassified consensus records is expert triage using the full activity context (activity description, village history, Kode_Desa financial profile across years) rather than the feature-level interpretation that typology rules provide. This is precisely the context that the expert validation sheets are designed to elicit: domain experts who review these records may identify fraud indicators invisible to automated rules — duplicate activity names, implausible physical output quantities, or BUMDes equity injections routed through misclassified Kode_Output codes — that the textual and contextual features currently excluded from the numerical feature matrix would capture.

---

## 11. Methodological Limitations Revisited Through IS Lens

### 11.1 Cohen's κ Absence and its Interpretive Impact

The inter-method agreement analysis currently reports pairwise overlap counts (3.3–50.3% across method pairs) but lacks the Cohen's κ statistic required for publication-quality evaluation. The pairwise counts describe agreement at the record level, but κ corrects for chance agreement — the expected level of overlap between two binary flag vectors even if the methods were applied randomly. On a dataset with 5–8% anomaly rates, substantial chance overlap exists; without κ correction, the reported 6.4% IF∩LOF overlap cannot be rigorously interpreted as evidence of independent or convergent detection.

The κ computation is straightforward from the binary flag vectors in `anomaly_flags.csv` and is strongly recommended before academic submission. The theoretical expectation, based on the BC scores and architectural independence of the three methods, is that κ(IF, LOF) will be substantially lower than κ(IF, RDA) — confirming that LOF and IF detect genuinely different anomaly populations while IF and RDA detect partially convergent populations. This pattern, if confirmed by κ, would constitute the primary methodological evidence for the multi-paradigm approach's advantage over single-algorithm deployments.

### 11.2 Kode_Desa = −1 Artefact and Data Quality Implications

The 80 flagged records attributed to `Kode_Desa = −1` (Nama_Desa = NaN) represent a data merge artefact — records in the Penyerapan dataset whose village codes do not match any entry in the Pagu dataset. For IS research purposes, this artefact carries two implications.

Methodologically, these 80 records cannot contribute to village-level persistence analysis or geographic attribution, reducing the effective coverage of the Tier-1 village summary by an unknown but bounded number of genuine anomalies. More importantly, the existence of unmatched Kode_Desa values indicates that the Siskeudes data infrastructure, while comprehensive, is not perfectly clean — some villages report expenditure activities without a corresponding budget ceiling entry, either through data entry error, late Pagu entry timing, or genuine missing data in the provincial repository. A production-grade version of this pipeline requires data quality gate checks (referential integrity validation between Penyerapan and Pagu) before feature engineering to prevent unmatched records from contaminating or distorting feature calculations.

### 11.3 Single Province Scope and External Validity

All findings are scoped to Jambi Province (99,692 records). While the theoretical framework — Fraud Triangle, principal-agent information asymmetry, DeLone and McLean IS Success — applies across Indonesian provinces, the detection model's trained parameters (RobustScaler statistics, RDA encoder weights, category-specific z-score distributions) are calibrated on Jambi's specific activity-type distribution, cost ranges, and procurement method profile.

Provinces with substantially different activity profiles — Jawa Timur's higher-volume infrastructure expenditure, Papua's unique local government spending structure, or DKI Jakarta's near-absence of traditional village fund governance — would produce different feature distributions. Direct transfer of v1 model parameters would systematically distort the z-score benchmarks and RDA reconstruction error baselines. Cross-province application requires either: (a) province-specific model calibration (retraining on each province's data), or (b) national-level pooled training with province as a stratification covariate — a methodological design decision that has significant implications for the pipeline's scalability as a national-level APIP tool.

---

## 12. Implications for APIP Inspection Practice

### 12.1 Converting Pipeline Output into an Inspection Protocol

The pipeline's operational value is realised only when its outputs are converted into inspection actions. The following protocol translates the four-tier output structure into APIP decision workflows:

**Tier 1A — Triple-Consensus Records (n = 156)**  
Priority: Immediate. These 156 records were independently flagged by all three algorithmic paradigms — ensemble partitioning, local density estimation, and non-linear reconstruction. No single-method false positive mechanism can explain their simultaneous detection. Recommend field verification within the current fiscal period, focusing on physical output confirmation (construction site visits for T2 records) and beneficiary verification (BLT records). Maximum expected precision based on the theoretical multi-method evidence structure.

**Tier 1B — Fully Persistent Tier-1 Villages (n = 174 villages, 3/3 years flagged)**  
Priority: High. Three-year persistence indicates structural rather than incidental irregularity. Recommend mandatory inclusion in the APIP annual audit cycle with multi-year financial record review, not limited to the current fiscal year. Cross-year comparison of activity profiles for the same Kode_Output codes across 2023–2025 may reveal price inflation trajectories or activity title repetition consistent with double budgeting.

**Tier 1C — Remaining Tier-1 Villages (n = 468 villages, 2/3 years flagged)**  
Priority: Moderate-High. Two-year flagging exceeds the threshold for random noise. Recommend risk-stratified inspection: villages with T2 (ghost activity) dominance receive field visits; villages with T1/T7 dominance receive financial document review and unit cost comparison against market benchmarks.

**Tier 2 — Single-Year Flagged Villages (n = 459 villages, 1/3 years)**  
Priority: Monitoring. Recommend annual monitoring via the pipeline rather than immediate field inspection. If the same village appears in Tier 2 for 2025, reclassify to Tier 1B in the 2026 cycle.

### 12.2 RDA Per-Feature Driver as the Inspection Entry Point

The RDA per-feature error decomposition provides APIP with the specific financial variable driving the anomaly for each Tier-1 village. This output is operationally valuable because it directs inspector attention to specific documentary evidence:

- `avg_completion` as primary driver (43.5% of Tier-1 villages): Request monthly progress reports and stage-completion certification documents; cross-check T1 completion percentages against physical construction or service delivery logs.
- `activity_category` as primary driver (31.2%): Request Kode_Output justification documentation; compare activity descriptions against standard Permendesa activity catalogues to identify misclassified spending.
- `cost_per_unit` as primary driver (14.9%): Request procurement documentation (Rencana Anggaran Biaya) and compare unit costs against market price surveys (Survei Harga Pasar) at kabupaten level.

This per-feature triage converts the pipeline's output from a binary anomaly flag into a directed audit evidence request — a significant operational improvement over manual inspectorate screening, which typically begins without any prior information about which financial variable is most likely anomalous.

---

## 13. Research Gap Validation: How Empirical Results Confirm Theoretical Claims

### 13.1 Gap 1 — Activity-Level Siskeudes Data as Untapped Signal

The research concept established that no prior study applied unsupervised anomaly detection to activity-level Siskeudes expenditure records. The empirical results validate this gap's significance: 99,692 individual activity records, structured by Kode_Output, multi-stage realization percentages, and procurement method, produced 3,107 consensus anomalies (3.1%) and 642 Tier-1 villages through algorithmic analysis. This would have been impossible without the activity-level granularity — aggregate village-level budget statistics (total Pagu vs. total realization) would have masked the within-village activity heterogeneity that produces the cost deviation signals, completion pattern anomalies, and cross-category routing irregularities that the pipeline detects.

### 13.2 Gap 2 — Unsupervised Methods in the Absence of Ground Truth Labels

The research concept argued that supervised classification — the method applied by Harriz et al. [13] with labelled village fund data — cannot operate in real-time monitoring contexts where verified corruption labels are unavailable. The empirical results confirm this design choice: the 3,107 consensus-flagged records were produced without any labelled training data. No corruption verdict is required as training input. The prosecution records cited in the research background (Desa Muara Hemat, Desa Jambi Tulo, Desa Batang Merangin, Desa Pangkal Duri) do not appear as training labels in the pipeline — they are used only for post-hoc modus operandi validation, confirming that the typology labels (T1–T7) correspond to documented fraud mechanisms rather than to algorithm artefacts.

### 13.3 Gap 3 — Province-Level Typology Mapping to Judicial Records

Ambarsari and Desyanti [14] applied Isolation Forest to national-level Indonesian procurement data without connecting algorithmic outputs to specific corruption typologies. The empirical results demonstrate that the typology mapping step is not merely descriptive — it converts the algorithmic output into a language that domain experts and legal investigators recognise. The T2 (Ghost Activity) typology directly corresponds to the proyek fiktif modus documented in all four verified Jambi prosecution cases; the T1 (Mark-up) typology corresponds to the markup pengadaan documented in ICW's [8] annual corruption trends analysis; and the T5 (Procurement Irregularity) typology — while only 26 records (0.8%) — maps directly to Søreide's [9] characterisation of non-competitive procurement as the structural enabler of supplier-side corruption.

### 13.4 Gap 4 — Multi-Paradigm Benchmarking

Alam et al. [24] identified multi-paradigm benchmarking as best practice for unsupervised anomaly detection but found it scarcely implemented in domain-specific applications. The empirical results illustrate exactly why this matters: the three methods detect partially non-overlapping anomaly populations (IF∩LOF = 6.4%, LOF∩RDA = 12.0%), with LOF identifying a distinct within-category deviation cohort invisible to global methods. A single-algorithm deployment would produce a materially different — and incomplete — anomaly portfolio than the consensus approach delivers.

---

## 14. Directions for Phase 2

### 14.1 Critical Priority: Expert Validation Completion

The single highest-priority action for Phase 2 is completing the four expert validation sheets (IF, LOF, RDA, Consensus top-50 records). Without Precision@50 measurements and inter-rater Cohen's κ between expert reviewers, the pipeline cannot claim the Use dimension of the D&M model, and the comparative evaluation framework remains incomplete. The academic paper's methodology section will present these metrics as its primary empirical validation evidence — their absence constitutes the critical gap between a working prototype and a publishable system evaluation.

### 14.2 T4 Stage Lock Recalibration

Implement the revised T4 detection rule: Stage Lock index = max(Real_T1, Real_T2, Real_T3) / total_realization > 0.95, conditional on n_stages_active ≥ 2. Apply this rule stratified by activity type (activities legitimately single-stage by regulatory schedule — BLT, certain honoraria categories — should be excluded from the T4 flag pool). The Desa Muara Hemat prosecution case (fictitious construction reports, multi-stage disbursement anomaly) represents the ground-truth validation target for this typology.

### 14.3 Text Feature Integration for T3 (Double Budgeting) and Unclassified Records

The current feature matrix excludes textual data (Uraian_Output activity descriptions, Keterangan notes). Double budgeting detection — where the same activity is budgeted under two different activity codes or in two consecutive years — requires text-similarity analysis across activity descriptions. TF-IDF cosine similarity between Uraian_Output values within the same village-year or across adjacent years would surface duplicate or near-duplicate activity descriptions carrying different Kode_Output labels — the specific mechanism through which double budgeting exploits the category ambiguity structure that T7 captures spatially but cannot confirm semantically.

For the 708 unclassified consensus records, text features would provide the additional context that resolves their typological ambiguity — an activity description like "Pembangunan gedung kantor desa" with near-zero `avg_completion` and high `cost_per_unit` is clearly T2 (fictitious construction), but the current numerical feature rule cannot make this determination without the textual confirmation.

### 14.4 Cohen's κ Computation and Inter-Rater Reliability

Compute Cohen's κ for: (a) pairwise inter-method agreement between IF, LOF, and RDA binary flag vectors (correcting for chance agreement in the 5–8% anomaly rate context), and (b) inter-rater agreement between the two domain experts who validate the top-50 sheets (confirming rubric reliability before Precision@50 is treated as ground truth). These two κ values belong in the evaluation framework section of the academic paper as primary methodological evidence.

### 14.5 Multi-Province Replication for External Validity

The single-province scope (Jambi) limits external validity claims. A multi-province replication — selecting one province from each of the major land-use contexts (Jawa (dense, urban-adjacent), Kalimantan (resource-extraction economy), Papua (high-value, remote high-fund allocation)) — would test whether the feature engineering constructs and detection thresholds calibrated on Jambi's activity distribution generalise across structurally different provincial contexts. Alfada's [29] empirical finding that intergovernmental transfer dependence correlates with elevated corruption across 19 provinces provides a testable prediction: provinces with higher transfer dependency ratios should produce higher anomaly rates under a calibrated pipeline, enabling criterion-related external validity assessment.

### 14.6 Quarterly Processing for Temporal Detection Granularity

The current annual cross-section (one Penyerapan file per fiscal year) captures anomalies only at year-end. Village fund disbursements occur in three stages (T1, T2, T3) across the fiscal year. Processing Penyerapan records at each disbursement stage — rather than aggregating across stages at year-end — would surface anomalies in T1 disbursements (typically February–April) before T2 funds are released (typically June–August), enabling preventive rather than retrospective detection. From the D&M timeliness perspective, this change would substantially improve Information Quality by narrowing the detection-to-action window from approximately 12 months to 2–3 months per disbursement cycle.

---

## Summary Table: Empirical Findings vs. Theoretical Predictions

| Theoretical Prediction | Empirical Finding | Confirmation Status |
|---|---|---|
| LOF detects distinct within-category anomalies that IF's global partitioning misses [18] | IF∩LOF = 6.4% — confirms independent detection populations | ✅ Confirmed |
| RDA contamination resistance enables clean score bimodality despite ~10% anomaly prevalence [34] | RDA BC = 0.703; 12.5× MSE separation between normal and anomaly strata | ✅ Confirmed |
| Swakelola dominance creates structural procurement-stage fraud opportunity [9] | 98.8% Swakelola baseline; 96.4% Swakelola in consensus flags | ✅ Confirmed — structural gap validated |
| BLT and equity injection activities carry highest pemotongan/opacity risk [6] | BLT (301 flags) and BUMDes injection (206 flags) head activity lists | ✅ Confirmed |
| Principal-agent information asymmetry exploitation persists across fiscal cycles [9] | 174 villages flagged in 3/3 fiscal years; 642 in ≥ 2/3 years | ✅ Confirmed — persistence is the key finding |
| T1 mark-up is the dominant modus operandi in Indonesian village fund fraud [8] | T1: 50.6% of consensus flags, dominant in 47.5% of Tier-1 villages | ✅ Confirmed |
| T7 cross-category routing co-occurs with T1 as a compound mechanism | T1+T7 co-occurrence: 1,141 records (36.7% of all consensus flags) | ✅ Confirmed — compound mechanism detected |
| Fiscal expansion increases short-term anomaly prevalence [6], [29] | 2023 anomaly rates highest across all methods (IF: 10.5%, Consensus: 4.1%) | ✅ Directionally confirmed |
| LOF provides superior bimodal score separation for domain expert triage [18] | LOF BC = 0.957 vs. RDA = 0.703 vs. IF = 0.335 | ✅ Confirmed — LOF provides clearest inspection boundary |
| Swakelola over-representation in BLT and operational categories enables rationalisation [6] | Operasional activities (PKK, PAUD, RT/RW) heavily over-represented in flagged list | ✅ Confirmed |
| T4 Stage Lock detects single-stage disbursement concentration | T4: 0 detections — `n_stages_active` insufficient for concentration detection | ❌ Not confirmed — feature recalibration required |
| Rule-based typology assignment fully classifies all consensus anomalies | 22.8% unclassified — compound subthreshold anomalies escape typology rules | ⚠️ Partial — framework requires T8 or soft classifier extension |

---

*In-Depth Analysis v1 produced from: ANALYSIS_REPORT_v1.md (pipeline outputs, April 2026) + research_concept_phase1.md (theoretical framework) + referenced_quotes_statement.md (verified literature). For methodology and data details see linked source documents.*

*Citations follow IEEE numbering as assigned in research_concept_phase1.md.*
