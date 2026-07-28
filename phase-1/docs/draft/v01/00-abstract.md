# Abstract

> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)
> **Word Count Limit**: Max 200 words
> **Structure**: Background → Problem → Approach → Key Findings → Conclusion & Impact

---

## Abstract

**Background:** Indonesia's Dana Desa programme channels Rp 71 trillion annually to 75,259 villages, yet post-hoc prosecutions reveal systemic financial diversion lagging two to five years behind disbursement.

**Problem:** Existing fraud monitoring relies on retrospective manual audits or supervised machine learning requiring non-existent ground-truth fraud labels in real-time administrative Siskeudes records.

**Approach:** Grounded in Design Science Research (DSR) and Agency Theory, this study develops an unsupervised Dual-Path anomaly detection artifact combining Isolation Forest (IF), Local Outlier Factor (LOF), and an 8-layer Deep Autoencoder (DA) with an Operational Policy Mapping Layer for typology translation. The pipeline was evaluated on a longitudinal panel of 99,692 activity-level expenditure records (2023–2025) from Jambi Province.

**Key Findings:** LOF isolates extreme heavy-tailed local density anomalies (BC = 0.957), while IF and DA capture global outliers ($\kappa = 0.482$). On a 10,000-record synthetic fraud benchmark, the Dual-Path framework achieves superior recovery (**Precision = 0.884, Recall = 0.826, F1 = 0.854, AUC-ROC = 0.908**). Activity-rate normalized tiering isolates **128 Tier-1 villages (9.4%)**, reducing activity screening search space by 96.9%.

**Conclusion & Impact:** Operationalising the DeLone and McLean IS Success Model, the artifact translates abstract reconstruction loss into instance-level Explainable AI (XAI) audit checklists, bridging Siskeudes administrative data to actionable APIP inspectorate intervention.

**Keywords:** Village Fund Governance; Unsupervised Anomaly Detection; Design Science Research; Dual-Path Consensus; Explainable AI.
