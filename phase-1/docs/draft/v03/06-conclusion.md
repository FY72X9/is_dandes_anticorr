# Chapter 6: Conclusion

> **Draft Status**: July 2026 (Final synthesis & research directions)  
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)  
> **Word Count Target**: ~500 words  
> **Citation Format**: IEEE (continuous numbering per references.md)  

---

## 6. Conclusion

This study developed and evaluated an unsupervised Dual-Path Machine Learning artifact (Protocol 2), framed within Design Science Research (DSR) [10], for detecting expenditure anomalies in village fund absorption records across 96,778 activity entries (1,363 villages, 2023–2025) in Jambi Province.

In response to **RQ1**, seven engineered feature constructs incorporating kabupaten-stratified z-score baseline centering (`cost_deviation_by_category`) deliver superior discriminating power. Neural autoencoder loss decomposition confirms that within-category unit cost deviation and unit price inflation constitute the primary statistical drivers of financial distortion in Siskeudes records.

In response to **RQ2**, LOF isolates extreme heavy-tailed local density anomalies (BC = 0.957), while Isolation Forest (BC = 0.335) and Deep Autoencoder (BC = 0.703) partition global multi-feature outliers. The Dual-Path Consensus Ensemble ($\text{LOF} \lor (\text{IF} \land \text{RDA})$) resolves the mutual cancellation limitation of traditional majority voting, achieving **Precision = 0.846, Recall = 0.846, F1-Score = 0.846, and AUC-ROC = 0.912** on an ex-ante synthetic fraud benchmark.

In response to **RQ3**, an Operational Policy Mapping Layer translates mathematical outliers into seven corruption typologies dominated by **T2: Ghost Activities (58.1% / 4,155 records)** and **T5: Procurement Irregularities (32.8% / 2,343 records)**, isolating **Rp 642.85 billion** in realized expenditure risk. Instance-level XAI loss decomposition transforms neural MSE into actionable field inspection checklists for district APIP auditors.

Future research will extend this framework along four primary trajectories: implementing semi-supervised Graph Neural Networks (GNNs) on transaction graphs to capture compound sub-threshold fraud networks; scaling the longitudinal pipeline to multi-province national panels; deploying streaming API microservices integrated with BPKP Siskeudes endpoints for real-time pre-disbursement alert generation; and conducting ex-post empirical field studies measuring APIP audit referral conversion rates and recovered state financial losses.
