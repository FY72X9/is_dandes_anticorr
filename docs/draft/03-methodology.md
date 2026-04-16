# Chapter 3: Methodology

> **Draft Status**: v1.0 — April 2026
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)
> **Word Count Target**: ~800 words
> **Citation Format**: IEEE (continuous numbering per references.md)

---

## 3. Methodology

### 3.1 Dataset and Data Sources

The study uses activity-level village fund expenditure absorption records collected via jaga.id (https://jaga.id) — the KPK-operated public monitoring portal for village fund transparency, which provides open access to village fund expenditure realization records at the provincial level [27]. The dataset encompasses two complementary data sources: (1) **Penyerapan** (expenditure absorption) records documenting realised spending per activity per disbursement stage, and (2) **Pagu** (budget ceiling) records documenting approved village budget allocations. Both sources were merged via composite key `Kode_Desa` × `Tahun` across fiscal years 2023, 2024, and 2025, yielding a final longitudinal panel of **99,692 activity-level records** (33,140 in 2023; 36,151 in 2024; 30,401 in 2025). Each record represents a single budget activity entry for a specific village in a specific year, including fields for activity description (`Uraian_Output`), activity category code (`Kode_Output`), realised expenditure per tranche (Real_T1, Real_T2, Real_T3), percentage completion per tranche (Pct_T1, Pct_T2, Pct_T3), volume and unit of output, procurement method (`Cara_Pengadaan`), and village budget ceiling.

The dataset covers Jambi Province across all kabupaten/kota jurisdictions. No pre-existing fraud labels attach to any record; the detection problem is entirely unsupervised.

### 3.2 Feature Engineering

Seven features were engineered to operationalise corruption modus operandi documented in judicial records and institutional audit reports [13, 14]:

| Feature | Construction | Modus Operandi Targeted |
|---|---|---|
| `cost_per_unit` | Total realisation ÷ Volume (normalised) | Mark-up / price inflation |
| `absorption_ratio` | Total realisation ÷ Pagu (village-level) | Fictitious project — near-zero absorption |
| `avg_completion` | Mean(Pct_T1, Pct_T2, Pct_T3) | Manipulated completion reporting |
| `swakelola_high_value` | Binary: Swakelola AND realisation > threshold | High-value uncompetitive procurement |
| `activity_category` | Kode_Output 2-digit prefix (ordinally encoded) | Cross-category activity mismatch |
| `cost_deviation_by_category` | z-score of `cost_per_unit` within Kode_Output group | Within-category price outlier |
| `n_stages_active` | Count of disbursement stages with Real > 0 | Incomplete or front-loaded disbursement (metadata annotation; used for post-hoc typology mapping, not ML model input) |

Two candidate features from the initial design — `stage_variance` and `completion_vs_realization` — were eliminated during Variance Inflation Factor (VIF) screening (threshold VIF > 5) prior to model fitting. `n_stages_active` was retained as a metadata column for typology mapping rather than as a model input feature. All remaining features were normalised using RobustScaler (median centring, IQR scaling), which resists distortion by the outlier records the study intentionally targets for detection. The Robust Deep Autoencoder (RDA) uses the five core features (`cost_per_unit`, `avg_completion`, `swakelola_high_value`, `activity_category`, `cost_deviation_by_category`) for reconstruction-error-based detection, while IF and LOF consume the full 6-feature model input matrix. Figure 1 depicts the raw (pre-normalisation) distributions of six key features, confirming extreme right-skew in `cost_per_unit` (median = Rp 5,440,000; max = Rp 2.8 × 10⁸ clipped at 99th percentile) and near-binary concentration in `absorption_ratio` (median = 0.02), consistent with the prevalence of incomplete fund absorption documented in prior studies [12].

> **[Figure 1: Feature Distributions — Jambi Village Fund 2023–2025]**
> *Source: `src/output_v1/charts/feature_distributions.png`*

Figure 2 presents the feature correlation matrix. The strongest pairwise correlation is between `cost_deviation_by_category` and `cost_per_unit` (r = 0.59), which is expected by construction — the former is a within-group z-score of the latter. The moderate correlation between `swakelola_high_value` and `cost_per_unit` (r = 0.38) confirms that high-value self-managed activities tend to exhibit elevated unit costs, consistent with Søreide's [9] procurement corruption argument. All other correlations remain below ±0.25, indicating feature independence sufficient for multi-method detection without multicollinearity concerns.

> **[Figure 2: Feature Correlation Heatmap — Jambi Village Fund 2023–2025]**
> *Source: `src/output_v1/charts/feature_correlation_heatmap.png`*

### 3.3 Detection Algorithms

**Isolation Forest (IF)** partitions the feature space via random axis-aligned splits; records requiring fewer partitions to isolate receive lower anomaly scores [19]. The contamination parameter was set to 5% (95th-percentile threshold) to reflect the expected upper bound of anomaly prevalence in village fund data. `n_estimators = 200`, `max_samples = 256`, `random_state = 42`.

**Local Outlier Factor (LOF)** computes, for each record, the ratio of its estimated local reachability density to the mean local reachability density of its k-nearest neighbours [25]. Records with LOF >> 1.0 are locally dense isolates — statistically deviant within their Kode_Output activity peer group. `n_neighbors = 20`, scored on the full training set (novelty = False).

**Robust Deep Autoencoder (RDA)** decomposes the input matrix **X** into a learned normal representation **L** (encoded and decoded by a deep autoencoder) and a sparse noise matrix **S** capturing anomalous patterns (L1-penalised). Per-record anomaly scores are the Mean Squared Error between the original feature vector and its reconstruction **L̂**. The network architecture is `[n → 64 → 32 → 16 → 8 → 16 → 32 → 64 → n]` (n = number of input features; 8-layer symmetric encoder–decoder with bottleneck at dimension 8) with ReLU activations throughout and a linear output layer. Training uses `epochs = 100` with early stopping at `patience = 10`, `batch_size = 256`. The regularisation parameter λ is selected by validation reconstruction MSE from a sweep over {1×10⁻⁴, 1×10⁻³, 1×10⁻²}. Flagging threshold is the 95th percentile of reconstruction MSE on the full dataset.

### 3.4 Consensus Anomaly Identification and Typology Mapping

A record receives `consensus_flag = 1` if it is flagged by at least two of the three methods. This multi-paradigm consensus requirement reduces method-specific false positives and surfaces records where algorithmically independent reasoning converges on the same signal.

Consensus-flagged records are post-processed through a rule-based typology assignment module that maps feature value combinations to seven typology labels (T1–T7) derived from documented corruption modus operandi:

| Code | Typology | Primary Feature Signal |
|---|---|---|
| T1 | Mark-up / Price Inflation | `cost_per_unit` > 3σ AND `cost_deviation_by_category` > 2σ |
| T2 | Ghost Activity | `absorption_ratio` < 0.05 AND `avg_completion` < 10% |
| T3 | Volume Padding | `absorption_ratio` ≥ 0.98 (near-complete single-cycle budget absorption) |
| T4 | Stage Lock | `n_stages_active` = 0 (budget allocated, zero disbursement) |
| T5 | Procurement Irregularity | `Cara_Pengadaan` = Pihak ke-3 / Kontrak AND `cost_per_unit` > 75th percentile |
| T6 | Budget Exhaustion | `absorption_ratio` > 0.98 AND `avg_completion` < 50% |
| T7 | Cross-Category Dump | `activity_category` mismatch signal relative to Kode_Output peer group |

Records that satisfy no single-rule threshold — or that satisfy multiple conflicting rules — receive an "Unclassified" assignment, which the study analyses separately as a subthreshold masking problem (Section 5.4).

### 3.5 Village Priority Tier Classification

Village-level priority tiers aggregate activity-level consensus flags into an anomaly persistence score per village across three fiscal years. Tier 1 (High Priority) villages exhibit consensus-flagged anomalies in two or more fiscal years; Tier 2 (Moderate) in exactly one year; Tier 3 (Not Flagged) in no year. This persistence dimension operationalises Cressey's Opportunity condition in the Fraud Triangle: multi-year anomaly recurrence signals an entrenched structural vulnerability rather than an incidental deviation [6].
