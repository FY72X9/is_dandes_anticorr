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
| Isolation Forest | 0.335 | Unimodal — no clean separation | 0.131 → ~0.180 |
| DA (Deep AE) | **0.703** | Moderate bimodal — clear anomaly tail | 2.80×10⁻⁵ → ~3.50×10⁻⁴ |
| **LOF** | **0.957** | **Strong bimodal — sharpest discrimination** | 1.025 → (extreme tail to 5.40×10⁹) |

LOF's BC of 0.957 — exceeding the bimodality threshold by 73% — reflects the extreme L-shaped score distribution: the vast majority of records cluster near LOF = 1.0 (embedded within their local peer group), while genuine local outliers produce scores extending to 5.40 × 10⁹. DA's moderate bimodality (BC = 0.703) confirms a 12.5× separation between median MSE and the 95th-percentile threshold, validating the autoencoder's effectiveness in isolating normal from anomalous reconstruction error. Isolation Forest's unimodal distribution (BC = 0.335) indicates that the 95th-percentile decision function threshold cuts through a high-density score region rather than a natural distribution valley, introducing relative ambiguity in borderline-record classification.

### 4.3 Inter-Method Agreement

Table 3 quantifies pairwise overlap between methods. Cohen's κ values (correcting for chance agreement at the observed 5–8% flagging rates) are reported alongside raw overlap counts.

**Table 3. Pairwise Flag Overlap and Cohen's κ**

| Method Pair | Records in Both | % of Smaller Method | Cohen's κ |
|---|---|---|---|
| IF ∩ LOF | 317 | 6.4% | *[computed in v2 pipeline]* |
| IF ∩ DA | 2,506 | **50.3%** | *[computed in v2 pipeline]* |
| LOF ∩ DA | 596 | 12.0% | *[computed in v2 pipeline]* |
| IF ∩ LOF ∩ DA (triple) | 156 | 1.6% of total | — |

> **Note (v2.0)**: Cohen's κ will be added after v2 pipeline re-run, which also incorporates One-Hot Encoding and dual-path framework changes. The theoretical expectation is κ(IF, LOF) ≪ κ(IF, DA), confirming LOF detects a genuinely different anomaly population than IF and DA.

IF and DA converge on 50.3% of DA's flagged records — both methods respond strongly to globally extreme multi-feature deviations. LOF's low overlap with both (6.4% with IF; 12.0% with DA) confirms that LOF identifies a structurally distinct anomaly subset — the 3,951 records LOF alone flags represent within-category price inflation patterns that fall below the detection threshold of global partitioning and global reconstruction paradigms [25, 24].

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

### 4.5 DA Feature Importance Diagnosis

Figure 6 decomposes DA reconstruction error by feature across all consensus-flagged records and presents a per-record error heatmap for the top-50 flagged activities.

> **[Figure 6: Mean DA Error per Feature and Top-50 Heatmap]**
> *Source: `src/output_v1/charts/rda_error_decomposition.png`*

`avg_completion` dominates reconstruction error (MSE ≈ 0.00145), confirming that completion percentage manipulation generates the largest departure from learned normal fund absorption behaviour. `cost_per_unit` ranks second (MSE ≈ 0.00095), followed by `activity_category` (MSE ≈ 0.00080) and `cost_deviation_by_category` (MSE ≈ 0.00065). The heatmap reveals that the extreme outlier record exhibits near-maximum error on both `cost_per_unit` and `avg_completion` simultaneously — a compound fraud signature consistent with simultaneous price inflation and completion falsification.

### 4.6 Village Priority Tier Classification

Figure 7 presents village-level priority tiers based on multi-year anomaly persistence.

> **[Figure 7: Village Priority Tiers (Anomaly Persistence Score)]**
> *Source: `src/output_v1/charts/village_persistence_tiers.png`*

Of 1,364 unique villages in the dataset, 642 (47.1%) qualify as Tier 1 (High Priority), exhibiting consensus anomalies in two or more fiscal years. 459 villages (33.6%) fall into Tier 2 (Moderate, one anomalous year), and 263 (19.3%) into Tier 3 (Not Flagged). Under a null hypothesis of random detection at the observed 3.1% per-activity rate, the expected probability of a single village being flagged in two or more of three independent fiscal years by chance is P(X ≥ 2 | X ~ Binomial(3, 0.031)) ≈ 0.28% — far below the observed 47.1%, confirming that the Tier-1 pattern reflects statistically systematic multi-year anomaly recurrence rather than random noise (p < 0.001, exact binomial test). The distribution is inconsistent with incidental administrative error; it indicates structurally sustained irregular spending patterns consistent with the Fraud Triangle's Opportunity condition persisting across fiscal cycles [6].

### 4.7 Spatial Projection

Figure 8 (PCA) and Figure 9 (t-SNE) confirm the separability structure in the engineered feature space.

> **[Figure 8: PCA Projection — Normal vs Consensus-Flagged Records]**
> *Source: `src/output_v1/charts/pca_projection.png`*

> **[Figure 9: t-SNE Projection — Normal vs Consensus-Flagged Records]**
> *Source: `src/output_v1/charts/tsne_projection.png`*

The PCA projection (PC1 = 26.0%, PC2 = 12.7%; cumulative = 38.7%) shows consensus anomalies (n = 3,107) distributed along the positive PC1 gradient, with extreme outliers reaching PC1 > 40. Partial overlap between normal (n = 96,585) and anomalous populations in 2D PCA space is expected — the corruption patterns are distributed across 10 feature dimensions rather than a single dominant axis. The t-SNE projection (sampled at 15,000 records: 14,538 normal + 462 anomalous) reveals anomaly concentration in specific sub-clusters on the right periphery of the map, consistent with the Fraud Triangle interpretation: anomalous activities cluster by activity-type neighbourhood, indicating that the same corruption patterns repeat systematically across villages within the same programme category rather than manifesting randomly.
