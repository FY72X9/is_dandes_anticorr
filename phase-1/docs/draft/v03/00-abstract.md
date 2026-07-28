# Abstract

> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)  
> **Word Count Limit**: Max 250 words  
> **Structure**: Background → Problem → Approach → Key Findings → Conclusion & Impact  

---

## Abstract

**Background:** Indonesia's *Dana Desa* (Village Fund) programme channels approximately Rp 71 trillion annually to 75,259 villages, yet post-hoc legal prosecutions reveal systemic financial diversion lagging two to five years behind disbursement windows.

**Problem:** Existing fraud monitoring relies on retrospective manual audits or supervised machine learning models that require non-existent ground-truth fraud labels in real-time administrative *Siskeudes* expenditure records.

**Approach:** Grounded in Design Science Research (DSR), Agency Theory, and the Fraud Diamond model, this study constructs an unsupervised Dual-Path Consensus Machine Learning artifact combining Isolation Forest (IF), Local Outlier Factor (LOF), and an 8-layer Reconstruction Dense Autoencoder (RDA) with an Operational Policy Mapping Layer for corruption typology translation. The pipeline was evaluated on a longitudinal panel of 96,778 activity-level expenditure records across 1,363 villages (2023–2025) in Jambi Province.

**Key Findings:** The Dual-Path Consensus Gate decouples local density isolates (LOF) from multi-model global convergence (IF $\cap$ RDA), isolating **7,153 consensus anomalous activities (7.39%)** representing **Rp 642.85 Miliar in financial realization exposure (14.89% of total provincial disbursement)** and **Rp 6.08 Trillion in budget ceiling exposure (7.46%)**. Operational policy mapping reveals a major typology shift toward **T2: Ghost Activities (58.1% of flags / 4,155 records)** and **T5: Procurement Irregularities (32.8% of flags / 2,343 records)**. Longitudinal persistence tiering identifies **702 villages (51.5%)** flagged across all three fiscal years. On an ex-ante synthetic fraud benchmark, the Dual-Path framework achieves superior recovery (**Precision = 0.846, Recall = 0.846, F1 = 0.846, AUC-ROC = 0.912**).

**Conclusion & Impact:** Operationalising the DeLone and McLean IS Success Model, the artifact reduces inspectorate screening search space by 92.6% at the activity level and translates abstract reconstruction loss into instance-level Explainable AI (XAI) audit checklists, bridging administrative Siskeudes data to actionable APIP inspectorate intervention.

**Keywords:** Village Fund Governance; Unsupervised Anomaly Detection; Design Science Research; Dual-Path Consensus; Explainable AI; Corruption Typology.
