# Chapter 5: Discussion

> **Draft Status**: v2.1 — July 2026 (Revised IEEE continuous numbering & DSR primary study alignment)
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)
> **Word Count Target**: ~900 words
> **Citation Format**: IEEE (continuous numbering per references.md)

---

## 5.1 Principal Empirical Findings

This study developed and evaluated an unsupervised Dual-Path machine learning artifact for detecting expenditure anomalies in Siskeudes administrative records across 99,692 activity entries (2023–2025) in Jambi Province. Three core empirical insights emerge from the evaluation:

### 5.1.1 Operationalizing the Operationalization Chasm
Prior literature in public financial governance divides into non-communicating computational ML models on centralized data and qualitative governance studies lacking algorithmic operationalization. This study bridges this chasm by constructing a DSR artifact [10] that ingests decentralized activity-level Siskeudes absorption data from jaga.id [26], proving that administrative absorption signals contain quantifiable traces of expenditure distortion without requiring pre-existing fraud labels.

### 5.1.2 Overcoming the Ground Truth Paradox via Synthetic Benchmarking
The absence of labelled ground truth in public sector fraud detection creates an epistemological paradox: supervised methods trained on historical prosecution labels detect only previously discovered fraud, missing hidden diversions. By deploying an unsupervised Dual-Path Consensus framework (`path_local OR path_global`), this study isolates local density outliers (LOF) and global anomaly convergence (IF $\cap$ DA). The ex-ante synthetic fraud benchmark confirms superior anomaly recovery (**Precision = 0.884, Recall = 0.826, F1 = 0.854, AUC = 0.908**), outperforming single-algorithm baselines.

### 5.1.3 Mitigating Geographical Baseline Skew via Kabupaten Centering
Standard global anomaly detection models confuse remote geographical baseline costs with price markup. Implementing kabupaten-stratified z-score centering (`(Kode_Output, Kabupaten_Kota, Tahun)`) eliminates systematic false positives for isolated jurisdictions (e.g., Kerinci), preserving true anomaly sensitivity.

---

## 5.2 Research Contribution and DSR Evaluation Framework

**Table 4. DSR Evaluation Matrix — Primary Study Findings**

| DSR Evaluation Dimension | Operationalization in Primary Artifact | Empirical Target Metric | Observed Outcome |
|---|---|---|---|
| **Relevance Cycle** | Search space reduction for APIP inspectorates | Activity screening overhead reduction | **96.9% reduction** (99,692 → 3,107 records) |
| **Rigor Cycle** | Agency Theory operationalization in Siskeudes features | Multi-method convergence ($\kappa$) | **$\kappa(\text{IF}, \text{DA}) = 0.482$** (Moderate convergence) |
| **Design Cycle** | Activity-rate normalized village priority tiering | Operationally feasible Tier-1 village count | **128 Tier-1 villages (9.4%)** |
| **Ex-Ante Benchmark** | Synthetic fraud injection recovery | Precision, Recall, F1, AUC-ROC | **F1 = 0.854, AUC = 0.908** |

---

## 5.3 Theoretical Implications

**For IS Theory & Agency Theory**: Grounding feature engineering in Agency Theory [25] frames the village head as an agent exploiting information asymmetry relative to the principal (kabupaten district government and KPK). Unexplained unit cost deviations and completion falsifications represent proximate quantitative evidence of information asymmetry exploitation.

**For Design Science Research (DSR)**: The DSR three-cycle model (Hevner et al., 2004) [10] predicts that artifacts developed in isolation from relevance environments will fail in deployment. In this study, the **Ex-Ante Computational DSR Evaluation** protocol evaluates artifact utility prior to field deployment across three complementary dimensions: (1) cross-paradigm algorithm agreement ($\kappa = 0.482$), (2) Pareto frontier search space reduction (96.9% reduction at $c = 0.05$), and (3) qualitative alignment with Jambi judicial case records [28, 29, 30, 31].

**For Development Informatics**: The concentration of fraud detection literature on high-capacity institutional contexts (banking, federal systems) leaves decentralized, low-capacity governance underserved. Applying unsupervised ML to 74,000 fragmented administrative units addresses the core development informatics imperative.

---

## 5.4 Practical Implications and IS Success Model Operationalization

The empirical findings carry direct operational implications for Indonesian anti-corruption and oversight agencies (KPK, BPKP, Kemendesa, and Kabupaten APIP inspectorates), operationalising the **DeLone and McLean IS Success Model (2003)** [10] across three structural dimensions:

### 5.4.1 Information Quality → Individual Impact (Auditor Decision Support)
- **Search Space Reduction**: Filtering 99,692 activity records to 3,107 consensus anomalies yields a 96.9% reduction in document screening overhead for APIP auditors.
- **Activity-Rate Normalized Tiering**: Refining village priority classification to an activity-rate threshold ($\text{Anomaly\_Ratio} \ge 0.10$) isolates **128 Tier-1 villages (9.4%)**, providing an operationally feasible annual audit scheduling list for kabupaten inspectorates with 5–15 auditors.
- **Instance-Level XAI Checklists**: Transforming abstract mathematical reconstruction loss into feature contribution rankings (Table 5) provides field auditors with instance-level audit checklists (e.g., specifying physical output measurement for $82.5\%$ completion loss vs price benchmarking for $74.2\%$ unit cost loss).

### 5.4.2 System Quality → Audit Work Product Translation ("Last Mile" Protocol)
- **Human-in-the-Loop Workflow**: The pipeline operates as a decision-support system, translating top-ranked consensus anomalies and XAI checklists directly into formal APIP audit assignment orders (*Surat Perintah Tugas Inspektorat*).
- **Tranche-Specific Investigation Protocols**:
  - *T1 (Mark-up)* and *T5 (Procurement Irregularity)* trigger physical volume verification and local market benchmark comparison.
  - *T2 (Ghost Activity)* and *T4 (Stage Lock)* trigger bank statement reconciliation and physical completion auditing prior to final tranche disbursement.

### 5.4.3 Subthreshold Masking and Unclassified Anomalies Analysis
- The **708 consensus-flagged records (22.8%) categorized as "Unclassified"** highlight a structural limitation of static rule-based typology assignment. These records represent compound fraud patterns — such as simultaneous moderate price inflation combined with volume padding — where individual feature values fall below single-rule thresholds despite joint multi-feature anomaly convergence across IF, LOF, and DA.
- This finding motivates the **Phase 2 research trajectory**: transitioning from static policy mapping rules to semi-supervised graph neural networks (GNNs) capable of learning latent compound fraud topologies directly from transaction graph structures.

### 5.4.4 Organizational Impact (Deterrence and Lag Mitigation)
- Deploying continuous, automated screening via Siskeudes administrative data feeds mitigates the documented 2-to-5 year prosecution lag [28, 29, 30, 31], enabling intervention *within* disbursement cycles before state funds are permanently dissipated.

## 5.5 Limitations of the Review

Several limitations constrain the scope of this review's conclusions:

**Language bias**: The search strategy retrieved only English-language publications.
Indonesian-language research on Dana Desa governance (published in national journals)
was not systematically captured, potentially underrepresenting governance-specific
feature engineering knowledge.

**Publication bias**: Null results and failed ML deployments are underreported in the
corpus. The high AUC scores in the ML cluster may reflect publication bias toward
positive technical results.

**Temporal limitation**: The corpus covers 2018–2025. The rapid pace of LLM and
foundation model development means detection methods based on transformer architectures
(emerging 2023–2025) may be underrepresented relative to their actual capability level.

**Sensitivity analysis caveat**: The three-tier sensitivity analysis (F6) reveals that
6 of 10 descriptive themes show proportional shifts when quality thresholds are raised.
This indicates that medium-quality papers (quality score 4.0–4.5) contribute substantially
to the thematic picture; researchers requiring a higher-confidence sub-corpus should
apply the T2 threshold (≥4.5, N=23) for replication studies.

---

_This discussion section was generated by Phase F7 gap matrix synthesis._
_All analytical claims are traceable to specific codes, papers, and quantitative evidence in the SLR analysis files._