# Chapter 4: Results

> **Draft Status**: v3.0 — July 2026 (Full empirical pipeline results & graphics integration)  
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)  
> **Word Count Target**: ~1,500 words  
> **Citation Format**: IEEE (continuous numbering per references.md)  

---

## 4. Results

### 4.1 Per-Method Anomaly Flag Counts & Year-over-Year Consistency

Table 4.1 presents the empirical flag counts and flagging percentages across individual algorithms and ensemble gates for both `output_v1` and `v3-run`.

**Table 4.1. Per-Method Anomaly Flag Counts and Overall Rates (`output_v1` vs `v3-run`)**

| Algorithm / Ensemble Gate | `output_v1` Flagged | `output_v1` % | `v3-run` Flagged | `v3-run` % | Tuning / Architectural Change |
|---|---|---|---|---|---|
| **Isolation Forest (IF)** | 7,974 | 8.00% | 9,678 | 10.00% | Contamination tuned to 0.10 |
| **Local Outlier Factor (LOF)** | 4,985 | 5.00% | 4,839 | 5.00% | Top 5th percentile threshold ($k=20$) |
| **Reconstruction DA (RDA)** | 4,985 | 5.00% | 4,840 | 5.00% | Top 5th percentile MSE threshold |
| **Consensus Flag (Ensemble)** | **3,107** | **3.12%** | **7,153** | **7.39%** | **Dual-Path Gate ($\text{LOF} \lor (\text{IF} \land \text{RDA})$)** |

![Figure 4.1: Year-over-Year Anomaly Rate Consistency Per Method](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/anomaly_rate_consistency.png)

Figure 4.1 visualises year-over-year rate consistency across fiscal years 2023–2025. LOF exhibits remarkable cross-year stability (4.7% in 2023 $\to$ 4.6% in 2024 $\to$ 5.8% in 2025), demonstrating that its local density architecture adapts naturally to annual budget distribution shifts. In contrast, Isolation Forest shows higher year-to-year variance (10.5% in 2023 declining to 6.5% in 2024), reflecting the post-COVID fiscal expansion context where elevated spending volumes produced higher global sparsity.

### 4.2 Score Distribution & Bimodality Coefficient Analysis

Figure 4.2 presents the score distribution histograms annotated with Sarle Bimodality Coefficients (BC). A BC value exceeding 0.555 indicates a bimodal distribution with a distinct anomaly tail.

![Figure 4.2: Score Distribution Shape and Bimodality Across Methods](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/score_distributions.png)

**Table 4.2. Bimodality Coefficients and Score Range Metrics**

| Method | Sarle BC | Distribution Interpretation | Score Spectrum (Median $\to$ 95th Percentile Threshold) |
|---|---|---|---|
| **Isolation Forest** | 0.335 | Unimodal continuous spectrum | 0.131 $\to$ 0.180 (cuts high-density region) |
| **Reconstruction DA** | **0.703** | Moderate bimodal — clear anomaly tail | $2.80\times 10^{-5} \to 3.50\times 10^{-4}$ ($12.5\times$ separation) |
| **Local Outlier Factor** | **0.957** | **Heavy-tailed local density isolation** | 1.025 $\to$ extreme tail ($5.40\times 10^9$) |

LOF's BC of 0.957—exceeding Sarle's threshold by 72.4%—reflects an extreme L-shaped distribution: normal activities cluster near $\text{LOF} \approx 1.0$, while genuine local outliers produce reachability density ratios extending to $5.40 \times 10^9$. RDA's moderate bimodality (BC = 0.703) confirms a $12.5\times$ separation between median MSE and the 95th-percentile threshold.

### 4.3 Inter-Method Subspace Orthogonality & Overlap Matrix

Table 4.3 quantifies pairwise overlap and subspace relationships across algorithms.

**Table 4.3. Pairwise Flag Overlap and Cohen's $\kappa$ Metrics**

| Method Pair / Intersection | Shared Records | % of Smaller Method | Cohen's $\kappa$ | Subspace Relationship |
|---|---|---|---|---|
| IF $\cap$ LOF | 252 | 5.2% | 0.041 (Slight) | Subspace Orthogonal |
| IF $\cap$ RDA | 2,314 | **47.8%** | **0.482 (Moderate)** | Global Multi-Model Convergence |
| LOF $\cap$ RDA | 422 | 8.7% | 0.083 (Slight) | Subspace Orthogonal |
| IF $\cap$ LOF $\cap$ RDA (Triple) | 225 | 2.3% of total | — | Maximum Confidence Core |
| **LOF-Only Isolates** | **3,940** | **81.4% of LOF** | — | **Captured via Local Path** |

The empirical intersection matrix confirms that only 225 records (0.23% of total dataset) trigger all three algorithms simultaneously. Conversely, 3,940 records are flagged exclusively by LOF. In baseline `v1` (majority voting), these 3,940 local density isolates were discarded. The Dual-Path Gate ($\text{LOF} \lor (\text{IF} \land \text{RDA})$) preserves these critical density anomalies while requiring IF and RDA convergence for global outliers.

### 4.4 Corruption Typology Mapping & Shift Analysis

Figure 4.3 visualises the frequency distribution of mapped corruption typologies among consensus-flagged records.

![Figure 4.3: Corruption Typology Frequency Distribution](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/typology_distribution.png)

**Table 4.4. Comparative Typology Frequency Shift (`output_v1` vs `v3-run`)**

| Typology Code | Typology Name | `v1` Count | `v1` % | `v3-run` Count | `v3` % | Relative Shift & Impact |
|---|---|---|---|---|---|---|
| **T2_Ghost** | Ghost Activity (*Kegiatan Fiktif*) | 774 | 24.9% | **4,155** | **58.1%** | **+436.8% — Primary Modus** |
| **T5_ProcureIrr** | Procurement Irregularity (*Swakelola High Value*) | 26 | 0.8% | **2,343** | **32.8%** | **+8911.5% — Major Sensitivity Gain** |
| **T7_CrossCatDump** | Cross-Category Activity Dumping | 1,568 | 50.5% | **1,284** | **18.0%** | −18.1% (Specific reclassification) |
| **T1_Markup** | Unit Price Mark-Up (*Penggelembungan*) | 1,571 | 50.6% | **1,180** | **16.5%** | −24.9% (Refined price isolation) |
| **T4_StageLock** | Disbursement Stage Lock | 0 | 0.0% | **28** | **0.4%** | Newly captured in v3 |
| **Unclassified** | Sub-threshold Masking Anomaly | 708 | 22.8% | **1,227** | **17.2%** | Proportion reduced from 22.8% to 17.2% |

### 4.5 Instance-Level XAI Feature Diagnosis & RDA Error Drivers

Figure 4.4 decomposes RDA reconstruction error across features and presents a top-50 record heatmap.

![Figure 4.4: Mean RDA Reconstruction Error per Feature and Top-50 Anomaly Heatmap](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/rda_error_decomposition.png)

In `v3-run`, the primary reconstruction error drivers shifted dramatically: **`cost_deviation_by_category`** (top driver in 2,065 records) and **`cost_per_unit`** (1,551 records) surpassed `avg_completion` (1,114 records). This shift confirms that the autoencoder adapted from detecting simple completion reporting delays to isolating actionable price manipulation and uncompetitive procurement.

### 4.6 Longitudinal Village Persistence & Priority Tier Classification

Figure 4.5 presents village priority tiering based on multi-year anomaly persistence ($P_v = N_{\text{flagged}} / N_{\text{years}}$).

![Figure 4.5: Longitudinal Village Priority Tiers and Anomaly Persistence](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/village_persistence_tiers.png)

**Table 4.5. Longitudinal Village Persistence & Priority Tier Distribution**

| Priority Tier | Criteria / Persistence Score | `v1` Villages | `v1` % | `v3-run` Villages | `v3-run` % | Shift & Impact |
|---|---|---|---|---|---|---|
| **Tier 1 — High Priority** | Flagged in $\ge 2$ years ($P_v \ge 0.67$) | 642 | 47.1% | **1,172** | **86.0%** | **+530 Villages (+82.6%)** |
| **Tier 2 — Moderate Priority** | Flagged in 1 year ($P_v = 0.33$) | 459 | 33.7% | **163** | **12.0%** | −296 Villages |
| **Tier 3 — Clean / Unflagged** | Zero anomalies ($P_v = 0.00$) | 263 | 19.3% | **28** | **2.0%** | −235 Villages |
| **Persistence 1.0 (3/3 Yrs)** | Flagged continuously 2023–2025 | **177** | **13.0%** | **702** | **51.5%** | **+525 Villages (+296.6%)** |

### 4.7 Spatial Projections (PCA & t-SNE)

Figures 4.6 and 4.7 present 2D spatial projections of the engineered feature space.

![Figure 4.6: PCA Projection — Normal vs Consensus Flagged Anomaly Records](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/pca_projection.png)

![Figure 4.7: t-SNE Projection — Visual Representation of Anomaly Clusters](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/tsne_projection.png)

PCA projection (PC1 = 26.0%, PC2 = 12.7%) shows consensus anomalies extending along the positive PC1 gradient. t-SNE projection (sampled at 15,000 records) reveals dense anomaly clustering on the right periphery, confirming that expenditure anomalies group into specific activity-type neighborhoods rather than scattering randomly.

### 4.8 Feature Matrix Explorations

Figures 4.8 and 4.9 present inter-feature correlations and feature distribution shapes across the 27 engineered variables.

![Figure 4.8: Feature Correlation Heatmap Across 27 Variables](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/feature_correlation_heatmap.png)

![Figure 4.9: Feature Distributions Across Main Engineered Variables](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/feature_distributions.png)

### 4.9 Synthetic Fraud Injection Benchmark Performance

Table 4.6 reports benchmark evaluation results on the $N=10,000$ synthetic fraud slice (500 injected fraud cases).

**Table 4.6. Synthetic Fraud Injection Benchmark Evaluation Metrics**

| Algorithm / Ensemble Model | Precision@5% | Recall | F1-Score | AUC-ROC Curve |
|---|---|---|---|---|
| Isolation Forest (IF) | 0.724 | 0.724 | 0.724 | 0.782 |
| Local Outlier Factor (LOF) | 0.686 | 0.686 | 0.686 | 0.745 |
| Reconstruction DA (RDA) | 0.812 | 0.812 | 0.812 | 0.811 |
| `v1` Majority Vote Ensemble | 0.642 | 0.510 | 0.568 | 0.720 |
| **`v3-run` Dual-Path Gate** | **0.846** | **0.846** | **0.846** | **0.912 (Best)** |

The Dual-Path Gate achieved an **AUC-ROC of 0.912** and **F1-Score of 0.846**, outperforming all single models and exceeding baseline majority voting by +0.278 in F1-score.

### 4.10 Financial Exposure & Regional Concentration in Kabupaten Batanghari

Financial exposure analysis reveals that the 7,153 consensus-flagged activities in `v3-run` account for **Rp 642.85 Miliar** in realized expenditure (14.89% of total provincial disbursement).

Evaluating risk density across kabupaten jurisdictions reveals that **Kabupaten Batanghari exhibits the highest systemic risk concentration**, with **15.75% of activity entries flagged (823 activities)**, accounting for **Rp 115.71 Miliar in realization at risk**.
