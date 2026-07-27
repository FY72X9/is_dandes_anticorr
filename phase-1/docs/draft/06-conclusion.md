# Chapter 6: Conclusion

> **Draft Status**: v2.1 — July 2026 (Revised IEEE continuous numbering & Part 3 final polish)
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)
> **Word Count Target**: ~450 words
> **Citation Format**: IEEE (continuous numbering per references.md)

---

## 6. Conclusion

This study develops and evaluates a comparative unsupervised machine learning pipeline framed as a Design Science Research (DSR) artifact [10] for detecting corruption indications in village fund expenditure absorption records. Applied to 99,692 activity-level entries collected via jaga.id from Jambi Province across fiscal years 2023–2025, empirical results answer all three research questions:

**RQ1 — Feature discriminating power**: Seven engineered features operationalising documented corruption modus operandi [13, 14], incorporating kabupaten-stratified z-score baseline centering, produce a feature matrix with high discriminating power. Deep Autoencoder reconstruction error diagnosis confirms that `avg_completion` (MSE ≈ 0.00145) and `cost_per_unit` (MSE ≈ 0.00095) represent the dominant signals of financial distortion in Siskeudes records.

**RQ2 — Algorithm performance & synthetic benchmark**: LOF isolates extreme heavy-tailed local density anomalies (BC = 0.957), while Isolation Forest (BC = 0.335) and Deep Autoencoder (BC = 0.703) partition global outliers. The Dual-Path Consensus Framework (`path_local OR path_global`) aggregates complementary anomaly channels, outperforming individual algorithms on a 10,000-record synthetic benchmark slice with **Precision = 0.884, Recall = 0.826, F1-Score = 0.854, and AUC-ROC = 0.908**.

**RQ3 — Typology mapping & XAI translation**: An Operational Policy Mapping Layer translates mathematical anomalies into seven corruption typologies dominated by Mark-up (T1, 50.6%) and Cross-Category Dump (T7, 50.5%), aligned with Jambi judicial prosecution records [28, 29, 30, 31]. Instance-level XAI feature decomposition (Table 5) translates abstract MSE scores into specific audit checklists for field inspectors.

The artifact operationalises the DeLone and McLean information-quality-to-organisational-impact pathway [10]: at the **activity level**, 99,692 records are filtered to 3,107 consensus anomalies (96.9% search space reduction); at the **entity level**, activity-rate normalized persistence scoring ($\text{Anomaly\_Ratio} \ge 0.10$) isolates **128 Tier-1 villages (9.4%)**, providing an operationally feasible annual audit scheduling pool for kabupaten APIP inspectorates.

**Limitations** include single-province data scope (limiting immediate national generalisability) and rule-based typology mapping limitations for compound fraud patterns (22.8% unclassified anomalies).

**Future research directions** include: (1) Phase 2 semi-supervised graph neural network (GNN) implementation for compound typology discovery; (2) multi-province panel extension (Sumatera Utara, Jawa Timur); (3) real-time Siskeudes API dashboard integration; and (4) ex-post implementation research measuring APIP audit referral conversion rates.
