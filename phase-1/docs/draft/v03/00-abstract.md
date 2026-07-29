# Abstract

> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)  
> **Word Count Limit**: Max 250 words  
> **Structure**: Background → Problem → Approach → Key Findings → Conclusion & Impact  

---

## Abstract

**Background:** Indonesia's *Dana Desa* (Village Fund) channels Rp 71 trillion annually to 75,259 villages, yet legal prosecutions reveal systemic financial diversion lagging two to five years behind disbursement windows.

**Problem:** Existing monitoring relies on retrospective manual audits or supervised machine learning requiring non-existent ground-truth fraud labels in real-time administrative *Siskeudes* records.

**Approach:** Grounded in Design Science Research (DSR), Agency Theory, and Fraud Diamond, this study constructs an unsupervised Dual-Path Consensus framework (**Protocol 2**) combining Isolation Forest (IF), Local Outlier Factor (LOF), and an 8-layer Reconstruction Dense Autoencoder (RDA) with an Operational Policy Mapping Layer on 96,778 activity records across 1,363 villages (2023–2025) in Jambi Province.

**Key Findings:** Compared to baseline majority voting (**Protocol 1**), **Protocol 2** decouples local density isolates (LOF) from multi-model global convergence (IF $\cap$ RDA), expanding anomaly recall from 3,107 (3.12%) to **7,153 consensus anomalous activities (7.39%)** representing **Rp 642.85 billion in financial realization exposure (14.89%)** and **Rp 6.08 trillion in budget ceiling exposure (7.46%)**. Operational policy mapping reveals a major typology shift toward **T2: Ghost Activities (58.1% / 4,155 records)** and **T5: Procurement Irregularities (32.8% / 2,343 records)**. Longitudinal persistence identifies **702 villages (51.5%)** flagged across all three fiscal years. On an ex-ante synthetic benchmark, **Protocol 2** achieves superior recovery (**Precision = 0.846, Recall = 0.846, F1 = 0.846, AUC-ROC = 0.912** vs. **Protocol 1** F1 = 0.612).

**Conclusion & Impact:** Operationalising the DeLone & McLean IS Success Model, **Protocol 2** reduces inspectorate search space by 92.6% and translates neural loss into Explainable AI (XAI) audit checklists for APIP field inspections.

**Keywords:** Village Fund Governance; Unsupervised Anomaly Detection; Design Science Research; Dual-Path Consensus; Explainable AI; Corruption Typology.
