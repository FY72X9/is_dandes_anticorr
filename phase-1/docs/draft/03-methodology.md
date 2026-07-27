# Chapter 3: Methodology

> **Draft Status**: v2.0 — July 2026 (revised from v1.0 April 2026)
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)
> **Word Count Target**: ~800 words
> **Citation Format**: IEEE (continuous numbering per references.md)

---

## 3. Methodology

### 3.1 Design Science Research (DSR) Framework

This study adheres to the Design Science Research (DSR) methodology for Information Systems [5, 10], structuring the artifact development and evaluation across three primary cycles:
1. **Relevance Cycle**: Addresses the institutional problem of monitoring 99,692 village fund activity records across Jambi Province under severe APIP auditor capacity constraints.
2. **Rigor Cycle**: Grounds feature selection in Agency Theory (principal-agent information asymmetry) and Fraud Triangle dynamics, drawing algorithms from multi-paradigm anomaly detection literature [18, 24, 32].
3. **Design Cycle**: Iteratively constructs the IT artifact comprising three components: (a) robust feature engineering, (b) a Dual-Path Consensus ML engine, and (c) an operational policy mapping layer.

### 3.2 Dataset and Data Sources

The study uses activity-level village fund expenditure absorption records collected via jaga.id (https://jaga.id) — the KPK-operated public monitoring portal for village fund transparency, which provides open access to village fund expenditure realization records at the provincial level [26]. The dataset encompasses two complementary data sources: (1) **Penyerapan** (expenditure absorption) records documenting realised spending per activity per disbursement stage, and (2) **Pagu** (budget ceiling) records documenting approved village budget allocations. Both sources were merged via composite key `Kode_Desa` × `Tahun` across fiscal years 2023, 2024, and 2025, yielding a final longitudinal panel of **99,692 activity-level records** (33,140 in 2023; 36,151 in 2024; 30,401 in 2025). Each record represents a single budget activity entry for a specific village in a specific year, including fields for activity description (`Uraian_Output`), activity category code (`Kode_Output`), realised expenditure per tranche (Real_T1, Real_T2, Real_T3), percentage completion per tranche (Pct_T1, Pct_T2, Pct_T3), volume and unit of output, procurement method (`Cara_Pengadaan`), and village budget ceiling.

The dataset covers Jambi Province across all kabupaten/kota jurisdictions. No pre-existing fraud labels attach to any record; the detection problem is entirely unsupervised.

### 3.3 Feature Engineering and Hyperparameter Pareto Tuning

Seven features were engineered to operationalise corruption modus operandi documented in judicial records and institutional audit reports [13, 14]:

| Feature | Construction | Modus Operandi Targeted |
|---|---|---|
| `cost_per_unit` | Total realisation ÷ Volume (normalised) | Mark-up / price inflation |
| `absorption_ratio` | Total realisation ÷ Pagu (village-level) | Fictitious project — near-zero absorption |
| `avg_completion` | Mean(Pct_T1, Pct_T2, Pct_T3) | Manipulated completion reporting |
| `swakelola_high_value` | Binary: Swakelola AND realisation > threshold | High-value uncompetitive procurement |
| `activity_category` | Kode_Output 2-digit prefix (One-Hot Encoded in v2) | Cross-category activity mismatch |
| `cost_deviation_by_category` | z-score of `cost_per_unit` within (Kode_Output, Kabupaten) group | Within-category regional price outlier |
| `n_stages_active` | Count of disbursement stages with Real > 0 | Incomplete or front-loaded disbursement (metadata annotation for typology mapping) |

> **Geographical Baseline Centering:** To prevent remote or mountainous jurisdictions (e.g., Kabupaten Kerinci) from generating systematic false-positive flags due to elevated baseline logistics costs, `cost_deviation_by_category` calculates year-stratified z-scores within the combined grouping `(Kode_Output, Kabupaten_Kota, Tahun)`. This controls for regional geographical price skew while preserving sensitivity to local price inflation.

Two candidate features from the initial design — `stage_variance` and `completion_vs_realization` — were eliminated during Variance Inflation Factor (VIF) screening (threshold VIF > 5) prior to model fitting to prevent severe multicollinearity. `n_stages_active` was retained explicitly as a **metadata annotation column** used for post-hoc typology mapping only; it is not included in the ML model input matrix. All continuous features were normalised using **RobustScaler** (median centring, IQR scaling), which resists distortion by the extreme outlier records the study intentionally targets for detection.

> **Hyperparameter Pareto Tuning Rationale:** The contamination parameter ($c = 0.05$, corresponding to the 95th-percentile anomaly threshold $q = 0.95$) was selected based on a **Pareto Frontier trade-off analysis** between inspection search space reduction and APIP audit resource constraints. Setting $c < 0.03$ risks excluding subtle local density anomalies, while $c > 0.10$ generates an alert volume exceeding district inspectorate staffing capacity. A 5% baseline contamination isolates the upper bound of irregular spending patterns while constraining the inspection pool to an operationally feasible size.

> **Encoding Note (v2.0):** In v1.0, `activity_category` was encoded as a numeric integer from the Kode_Output 2-digit prefix. In v2.0, One-Hot Encoding (OHE) is applied using `OneHotEncoder(drop='first', handle_unknown='ignore')` to eliminate implicit ordinal distance bias on categorical variables.

### 3.4 Detection Algorithms

**Isolation Forest (IF)** partitions the feature space via random axis-aligned splits; records requiring fewer partitions to isolate receive lower anomaly scores [18]. Contamination $c = 0.05$, `n_estimators = 200`, `max_samples = 256`, `random_state = 42`.

**Local Outlier Factor (LOF)** computes, for each record, the ratio of its estimated local reachability density to the mean local reachability density of its k-nearest neighbours [24]. Records with LOF >> 1.0 are locally dense isolates — statistically deviant within their Kode_Output activity peer group. `n_neighbors = 20`, contamination $c = 0.05$, scored on the full training set (novelty = False).

**Deep Autoencoder (DA)** learns a compressed representation of normal fund expenditure behaviour through an encoder–decoder architecture. During training on the unlabelled dataset, the network learns to reconstruct normal records at low error; anomalous records — whose feature patterns deviate from learned normality — produce elevated Mean Squared Error (MSE) at reconstruction. The network architecture is an 8-layer symmetric network: `[n → 64 → 32 → 16 → 8 → 16 → 32 → 64 → n]` (bottleneck dimension = 8) with ReLU activations throughout and a linear output layer. Training uses `epochs = 100` with early stopping (`patience = 10`), `batch_size = 256`, weight decay $\lambda = 1\times 10^{-3}$. Flagging threshold is the 95th percentile of reconstruction MSE ($q = 0.95$).

### 3.5 Consensus Framework and Operational Policy Mapping Layer

In v1.0, consensus anomaly detection applied a simple majority vote (≥2 of 3 methods). In v2.0, a **Dual-Path Consensus Framework** is introduced:
- **Path 1 (Local Anomaly Signal)**: Flagged by LOF (`lof_flag == 1`).
- **Path 2 (Global Anomaly Convergence)**: Flagged by both IF and DA (`if_flag == 1 AND da_flag == 1`).

Final Consensus Flag v2 is defined as `path_local OR path_global`.

> **Operational Policy Mapping Layer (Typology Module):** Rather than attempting unsupervised ML discovery of corruption taxonomies, consensus-flagged anomalies are processed through an **Operational Policy Mapping Layer** (domain-rule translation engine). This post-processing layer converts abstract multi-dimensional anomaly flags into seven concrete corruption modus operandi (T1–T7) derived from judicial prosecution records, translating mathematical outliers into actionable audit check-lists for APIP inspectors.

### 3.6 Activity-Rate Normalized Village Priority Tiering

To prevent larger villages with higher activity counts from dominating Tier-1 priority rankings, village-level priority tiers normalize anomaly occurrence by annual activity volume:
$$\text{Anomaly\_Ratio}_{v,t} = \frac{\text{Consensus\_Flagged\_Activities}_{v,t}}{N_{\text{activities}, v,t}}$$

Priority tiers are assigned across the 3-year panel:
- **Tier 1 (High Priority)**: $\text{Anomaly\_Ratio}_{v,t} \ge 0.10$ in two or more fiscal years.
- **Tier 2 (Moderate Priority)**: $\text{Anomaly\_Ratio}_{v,t} \ge 0.10$ in exactly one fiscal year, or $0 < \text{Anomaly\_Ratio}_{v,t} < 0.10$ across multiple years.
- **Tier 3 (Not Flagged)**: Zero consensus anomalies across the 3-year panel.

### 3.7 Synthetic Fraud Injection Benchmark Protocol

To address the *Unsupervised Ground Truth Paradox* (where precision and recall cannot be directly computed on unlabelled administrative records), an **Ex-Ante Synthetic Fraud Injection Experiment** was implemented. A benchmark dataset slice ($N = 10,000$) was injected with 5% ($N = 500$) synthetic fraud instances across three documented modus operandi (price markup, ghost activity, cross-category dump). Algorithms were evaluated on ground-truth recovery using Precision@K, Recall, F1-Score, and AUC-ROC.

### 3.8 Instance-Level Explainable AI (XAI) Feature Decomposition

For each consensus-flagged activity $i$, instance-level Explainable AI (XAI) feature contribution is derived from the Deep Autoencoder's per-feature reconstruction error:
$$\text{Loss\_Contribution}_{i,f} = \frac{(x_{i,f} - \hat{x}_{i,f})^2}{\sum_{k=1}^{F} (x_{i,k} - \hat{x}_{i,k})^2}$$

This provides APIP inspectors with an instance-level breakdown ranking which specific financial attribute (e.g., `avg_completion` vs `cost_per_unit`) drove the anomaly flag.

| Code | Typology | Primary Feature Signal |
|---|---|---|
| T1 | Mark-up / Price Inflation | `cost_per_unit` > 3σ AND `cost_deviation_by_category` > 2σ |
| T2 | Ghost Activity | `absorption_ratio` < 0.05 AND `avg_completion` < 10% |
| T3 | Volume Padding | `absorption_ratio` ≥ 0.98 (near-complete budget absorption in single cycle) |
| T4 | Stage Lock | `stage_concentration` > 0.95 AND `n_stages_active` ≥ 2 — where `stage_concentration` = max(Real_T1, Real_T2, Real_T3) / `total_realization` |
| T5 | Procurement Irregularity | `swakelola_high_value` = 1 AND `cost_per_unit` > 75th percentile (or Third-Party Contract with elevated unit cost) |
| T6 | Budget Exhaustion | `absorption_ratio` > 0.98 AND `avg_completion` < 50% |
| T7 | Cross-Category Dump | `cost_deviation_by_category` > 3σ relative to Kode_Output peer group |

Records that satisfy no single-rule threshold — or that satisfy multiple conflicting rules — receive an "Unclassified" assignment, which the study analyses separately as a subthreshold masking problem (Section 5.4).

### 3.5 Village Priority Tier Classification

Village-level priority tiers aggregate activity-level consensus flags into an anomaly persistence score per village across three fiscal years. Tier 1 (High Priority) villages exhibit consensus-flagged anomalies in two or more fiscal years; Tier 2 (Moderate) in exactly one year; Tier 3 (Not Flagged) in no year. This persistence dimension operationalises Cressey's Opportunity condition in the Fraud Triangle: multi-year anomaly recurrence signals an entrenched structural vulnerability rather than an incidental deviation [6].
