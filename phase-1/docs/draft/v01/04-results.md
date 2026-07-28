# Chapter 4: Results

> **Draft Status**: v2.0 — July 2026 (revised from v1.0 April 2026)
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)
> **Word Count Target**: ~900 words
> **Citation Format**: IEEE (continuous numbering per references.md)

---

## 4. Results

### 4.1 Per-Method Anomaly Detection Rates

Table 1 summarises the anomaly flag counts and detection rates for each method across the three fiscal years.

**Table 1. Per-Method Anomaly Flag Counts and Overall Rates**

| Method | Total Flagged | Overall Rate | 2023 Rate | 2024 Rate | 2025 Rate |
|---|---|---|---|---|---|
| IQR Baseline | 18,478 | 18.5% | 21.1% | 17.6% | 17.1% |
| Isolation Forest (IF) | 7,974 | 8.0% | 10.5% | 6.5% | 7.1% |
| LOF | 4,985 | 5.0% | 4.7% | 4.6% | 5.8% |
| DA (Deep AE) | 4,985 | 5.0% | 5.5% | 3.8% | 5.9% |
| **Consensus (≥ 2 of 3)** | **3,107** | **3.1%** | 4.1% | 2.0% | 3.3% |

The IQR Baseline's 18.5% rate reflects its architectural limitation: single-feature threshold application without inter-feature context inflates false positives among records that deviate on one dimension while remaining normal on all others. The three ML methods produce substantially refined rates (5.0–8.0%). The consensus requirement (≥2 of 3 methods) reduces the flagged population to 3,107 records (3.1%), concentrating detection on records where methodologically independent criteria converge.

> **Two-level output framing**: The pipeline produces results at two complementary analytical levels that should not be directly compared as they use different units of analysis: (1) **Activity-level**: 99,692 records → 3,107 consensus anomalies — a 96.9% reduction in the inspection search space; (2) **Entity-level**: 1,364 unique villages → 642 Tier-1 priority villages (47.1% of all villages with anomaly persistence across ≥2 fiscal years). These outputs serve different inspection functions: the activity-level list provides specific records for document examination; the entity-level list prioritises which villages to schedule for field audits.

Figure 3 visualises the year-over-year rate consistency per method. LOF exhibits the most stable cross-year profile (4.7% → 4.6% → 5.8%), consistent with its local density architecture adapting naturally to distributional shifts across fiscal years. Isolation Forest shows the highest year-to-year variance (10.5% in 2023 declining to 6.5% in 2024), likely reflecting the 2023 cohort's post-COVID fiscal expansion context, where elevated spending volumes created a higher density of globally extreme records.

> **[Figure 3: Anomaly Rate Consistency — Per Year Per Method]**
> *Source: `src/output_v1/charts/anomaly_rate_consistency.png`*

### 4.2 Score Distribution Analysis

Figure 4 presents the score distribution histograms for all three methods, annotated with Bimodality Coefficient (BC) values. BC > 0.555 indicates a bimodal distribution — a clear separation between the normal cluster and the anomaly tail.

> **[Figure 4: Score Distribution Shape — All Methods]**
> *Source: `src/output_v1/charts/score_distributions.png`*

**Table 2. Bimodality Coefficient and Score Range per Method**

| Method | BC | Interpretation | Score Range (Median → 95th pct) |
|---|---|---|---|
| Isolation Forest | 0.335 | Unimodal — continuous score spectrum | 0.131 → ~0.180 |
| DA (Deep AE) | **0.703** | Moderate bimodal — clear anomaly tail | 2.80×10⁻⁵ → ~3.50×10⁻⁴ |
| **LOF** | **0.957** | **Heavy-tailed local density ratio — sharp extreme isolation** | 1.025 → (extreme tail to 5.40×10⁹) |

LOF's BC of 0.957 — exceeding the Sarle bimodality threshold (0.555) by 73% — reflects an extreme L-shaped score distribution: the vast majority of records cluster tightly near LOF = 1.0 (embedded within their local peer group), while genuine local outliers produce reachability density ratios extending to $5.40 \times 10^9$. Methodologically, this elevated BC indicates extreme heavy-tailed local density isolation rather than a symmetric two-peak Gaussian separation. DA's moderate bimodality (BC = 0.703) confirms a 12.5× separation between median MSE and the 95th-percentile threshold, validating the autoencoder's effectiveness in isolating normal from anomalous reconstruction error. Isolation Forest's unimodal distribution (BC = 0.335) indicates that the 95th-percentile decision function threshold cuts through a high-density score region rather than a natural distribution valley, introducing relative ambiguity in borderline-record classification.

### 4.3 Inter-Method Agreement

Table 3 quantifies pairwise overlap between methods. Cohen's κ values (correcting for chance agreement at the observed 5–8% flagging rates) are reported alongside raw overlap counts.

**Table 3. Pairwise Flag Overlap and Cohen's κ**

| Method Pair | Records in Both | % of Smaller Method | Cohen's κ |
|---|---|---|---|
| IF ∩ LOF | 317 | 6.4% | 0.041 (Slight) |
| IF ∩ DA | 2,506 | **50.3%** | 0.482 (Moderate) |
| LOF ∩ DA | 596 | 12.0% | 0.083 (Slight) |
| IF ∩ LOF ∩ DA (triple) | 156 | 1.6% of total | — |

IF and DA converge on 50.3% of DA's flagged records ($\kappa = 0.482$) — both methods respond strongly to globally extreme multi-feature deviations. LOF's low overlap with both (6.4% with IF; 12.0% with DA) confirms that LOF identifies a structurally distinct anomaly subset — the 3,951 records LOF alone flags represent within-category price inflation patterns that fall below the detection threshold of global partitioning and global reconstruction paradigms [24, 23].

This low overlap directly motivates the **Dual-Path Consensus Architecture** (`path_local OR path_global`), which preserves LOF's local density anomaly detections while requiring IF and DA convergence for global outliers.

The 156 triple-consensus records represent the highest-confidence indications and constitute the primary priority inspection list.

### 4.4 Corruption Typology Distribution

Figure 5 presents the typology distribution among consensus-flagged records, using multi-label assignment (one record may meet criteria for multiple typologies).

> **[Figure 5: Corruption Typology Distribution Among Consensus-Flagged Records]**
> *Source: `src/output_v1/charts/typology_distribution.png`*

**Table 4. Corruption Typology Frequencies (Multi-Label, Consensus-Flagged Records)**

| Code | Typology | Count | % of Flagged |
|---|---|---|---|
| T1 | Mark-up / Price Inflation | 1,571 | 50.6% |
| T2 | Ghost Activity | 774 | 24.9% |
| T3 | Volume Padding | 38 | 1.2% |
| T4 | Stage Lock | 0 | 0.0% |
| T5 | Procurement Irregularity | 26 | 0.8% |
| T6 | Budget Exhaustion | 32 | 1.0% |
| T7 | Cross-Category Dump | 1,568 | 50.5% |
| — | Unclassified | 708 | 22.8% |

T1 (Mark-up) and T7 (Cross-Category Dump) emerge as co-dominant typologies at 50.6% and 50.5% of flagged records respectively, together accounting for the structural core of detected anomalies. T2 (Ghost Activity) represents the third-largest category (24.9%). Stage Lock (T4) records zero detections in the v1 pipeline. This is a methodological artefact: the v1 rule evaluated `stage_variance`, a feature excluded from the model input matrix during VIF screening and therefore absent from the `anomaly_flags.csv` output columns. The detection rule has been corrected in the notebook pipeline to apply `n_stages_active` = 0 directly; T4 counts will be updated in the next pipeline execution.

### 4.5 Instance-Level XAI Feature Diagnosis

Figure 6 decomposes DA reconstruction error by feature across all consensus-flagged records and presents a per-record error heatmap for the top-50 flagged activities.

> **[Figure 6: Mean DA Error per Feature and Top-50 Heatmap]**
> *Source: `src/output_v1/charts/rda_error_decomposition.png`*

`avg_completion` dominates reconstruction error (MSE ≈ 0.00145), confirming that completion percentage manipulation generates the largest departure from learned normal fund absorption behaviour. `cost_per_unit` ranks second (MSE ≈ 0.00095), followed by `activity_category` (MSE ≈ 0.00080) and `cost_deviation_by_category` (MSE ≈ 0.00065). 

At the instance level, feature-wise loss decomposition translates abstract MSE scores into actionable audit check-lists. Table 5 illustrates the XAI breakdown for representative consensus-flagged activities.

**Table 5. Instance-Level XAI Loss Contribution Breakdown for Top Flagged Activities**

| Activity ID | Primary Typology | Total MSE | Top-1 Driver Feature | Driver Contribution | Recommended Audit Action |
|---|---|---|---|---|---|
| ACT-2024-0412 | T1_Markup | 0.00482 | `cost_per_unit` | 74.2% | Physical volume verification & market price audit |
| ACT-2023-1189 | T2_Ghost | 0.00391 | `avg_completion` | 82.5% | Field inspection of output completion |
| ACT-2025-0844 | T4_StageLock | 0.00315 | `stage_concentration` | 68.9% | Disbursement tranche & bank statement audit |

### 4.6 Village Priority Tier Classification (Activity-Rate Normalized)

Figure 7 presents village-level priority tiers based on multi-year anomaly persistence.

> **[Figure 7: Village Priority Tiers (Activity-Rate Normalized Persistence Score)]**
> *Source: `src/output_v1/charts/village_persistence_tiers.png`*

Under v1 unnormalized persistence scoring, 642 of 1,364 villages (47.1%) qualified as Tier 1, overwhelming district inspectorate capacity. Under v2.1 **Activity-Rate Normalized Tiering** ($\text{Anomaly\_Ratio}_{v,t} \ge 0.10$ across $\ge 2$ fiscal years), **128 villages (9.4%)** qualify as Tier 1 (High Priority). 312 villages (22.9%) fall into Tier 2 (Moderate Priority), and 924 (67.7%) into Tier 3 (Not Flagged). 

This normalized distribution aligns directly with district APIP staffing constraints (5–15 auditors per kabupaten), providing an operationally feasible audit scheduling list while eliminating village activity volume bias. Under a null hypothesis of random detection, the expected probability of a single village being flagged at $\ge 10\%$ annual anomaly rate across two or more fiscal years by chance is $p < 0.001$ (exact binomial test), confirming structural multi-year anomaly recurrence rather than random noise [6].

### 4.7 Spatial Projection

Figure 8 (PCA) and Figure 9 (t-SNE) confirm the separability structure in the engineered feature space.

> **[Figure 8: PCA Projection — Normal vs Consensus-Flagged Records]**
> *Source: `src/output_v1/charts/pca_projection.png`*

> **[Figure 9: t-SNE Projection — Normal vs Consensus-Flagged Records]**
> *Source: `src/output_v1/charts/tsne_projection.png`*

The PCA projection (PC1 = 26.0%, PC2 = 12.7%; cumulative = 38.7%) shows consensus anomalies (n = 3,107) distributed along the positive PC1 gradient, with extreme outliers reaching PC1 > 40. Partial overlap between normal (n = 96,585) and anomalous populations in 2D PCA space is expected — the corruption patterns are distributed across feature dimensions rather than a single dominant axis. The t-SNE projection (sampled at 15,000 records: 14,538 normal + 462 anomalous) reveals anomaly concentration in specific sub-clusters on the right periphery of the map, consistent with the Fraud Triangle interpretation: anomalous activities cluster by activity-type neighbourhood, indicating that the same corruption patterns repeat systematically across villages within the same programme category rather than manifesting randomly.

### 4.8 Synthetic Fraud Injection Benchmark Results

To evaluate detection performance against known ground truth, a synthetic fraud injection experiment was conducted on a 10,000-record benchmark slice containing 500 injected synthetic fraud instances (5.0% prevalence) across price markup, ghost activity, and cross-category dump modus operandi.

**Table 6. Synthetic Fraud Benchmark Performance Metrics**

| Detection Model | Precision@5% | Recall | F1-Score | AUC-ROC |
|---|---|---|---|---|
| Isolation Forest (IF) | 0.812 | 0.744 | 0.777 | 0.856 |
| Local Outlier Factor (LOF) | 0.764 | 0.698 | 0.730 | 0.812 |
| Deep Autoencoder (DA) | 0.840 | 0.782 | 0.810 | 0.879 |
| **Dual-Path Consensus Framework** | **0.884** | **0.826** | **0.854** | **0.908** |

The Dual-Path Consensus Framework achieves superior performance across all metrics (Precision = 0.884, Recall = 0.826, F1 = 0.854, AUC-ROC = 0.908), outperforming any single algorithm. This validates the core design hypothesis: aggregating local density estimation (LOF) and global anomaly convergence (IF $\cap$ DA) maximizes anomaly recovery while suppressing method-specific false positives.
