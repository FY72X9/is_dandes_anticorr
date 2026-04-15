# Chapter 6: Conclusion

> **Draft Status**: v1.0 — April 2026
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)
> **Word Count Target**: ~400 words
> **Citation Format**: IEEE (continuous numbering per references.md)

---

## 6. Conclusion

This study develops and evaluates a comparative unsupervised machine learning pipeline for detecting corruption indications in village fund expenditure absorption records, applied to 99,692 activity-level village fund expenditure entries collected via jaga.id from Jambi Province across fiscal years 2023–2025. Three research questions were posed; the empirical results answer each directly.

**RQ1 — Feature discriminating power**: Seven engineered features operationalising documented corruption modus operandi [13, 14] produce a feature matrix with sufficient discriminating power for multi-paradigm anomaly detection without pre-existing fraud labels. The RDA reconstruction error diagnosis confirms that `avg_completion` is the dominant corruption signal (MSE ≈ 0.00145), followed by `cost_per_unit` and `activity_category`. The strong right-skew in `cost_per_unit` (max = 102.83σ) and `cost_deviation_by_category` (max = 42.42σ) in the raw feature distribution confirms that price inflation leaves detectable quantitative traces in Siskeudes absorption records.

**RQ2 — Algorithm performance**: LOF achieves the highest bimodality coefficient (BC = 0.957) among the three methods, demonstrating the sharpest discrimination between normal and anomalous activity profiles. This superiority is theoretically predicted: LOF's local density architecture captures within-category price inflation patterns that global partitioning (IF, BC = 0.335) and global reconstruction (RDA, BC = 0.703) structurally miss. However, the multi-paradigm consensus framework — requiring agreement from at least two of three methods — outperforms any single algorithm for operational inspection triage by aggregating complementary detection channels (global extremity via IF/RDA; local peer deviation via LOF) into a 3,107-record high-confidence flagged set.

**RQ3 — Typology mapping**: Consensus-flagged anomalies map predominantly to T1 (Mark-up, 50.6%) and T7 (Cross-Category Dump, 50.5%), consistent with judicial records from Jambi prosecution cases and prior empirical typology studies [13, 14]. T2 (Ghost Activity, 24.9%) ranks third. The 708 unclassified records (22.8%) expose a methodological limitation in single-threshold rule-based classification and constitute the primary target for Phase 2 improvement.

The pipeline operationalises the DeLone and McLean information-quality-to-organisational-impact pathway by producing a ranked inspection workplan that reduces APIP's search space from 99,692 raw records to 642 priority villages — a 93.5% reduction — without any pre-existing labels or supervised training.

**Limitations** include the absence of expert validation against ground-truth fraud labels (reliance on judicial case corroboration as a proxy), single-province data scope (limiting national generalisability), and rule-based typology assignment inadequacy for compound fraud patterns.

**Future research directions** include: (1) multi-label classifier replacement for the typology module using expert-annotated training samples; (2) extension to additional provinces (Sumatera Utara, Jawa Timur) to assess pipeline generalisability; (3) real-time dashboard integration with Siskeudes data feeds via jaga.id for within-cycle APIP screening; and (4) implementation evaluation research measuring the actual inspection conversion rate from pipeline-ranked outputs to APIP field investigations.
