# Chapter 3: Methodology

> **Draft Status**: v2.0 — July 2026 (revised from v1.0 April 2026)
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
| `activity_category` | Kode_Output 2-digit prefix (numerically encoded; **see encoding note below**) | Cross-category activity mismatch |
| `cost_deviation_by_category` | z-score of `cost_per_unit` within Kode_Output group | Within-category price outlier |
| `n_stages_active` | Count of disbursement stages with Real > 0 | Incomplete or front-loaded disbursement (metadata annotation; used for post-hoc typology mapping, not ML model input) |

Two candidate features from the initial design — `stage_variance` and `completion_vs_realization` — were eliminated during Variance Inflation Factor (VIF) screening (threshold VIF > 5) prior to model fitting. `n_stages_active` was retained explicitly as a **metadata annotation column** used for post-hoc typology mapping only; it is not included in the ML model input matrix. All remaining features were normalised using RobustScaler (median centring, IQR scaling), which resists distortion by the outlier records the study intentionally targets for detection. The Deep Autoencoder (DA) uses the five core features (`cost_per_unit`, `avg_completion`, `swakelola_high_value`, `activity_category`, `cost_deviation_by_category`) for reconstruction-error-based detection, while IF and LOF consume the full 6-feature model input matrix. Figure 1 depicts the raw (pre-normalisation) distributions of six key features, confirming extreme right-skew in `cost_per_unit` (median = Rp 5,440,000; max = Rp 2.8 × 10⁸ clipped at 99th percentile) and near-binary concentration in `absorption_ratio` (median = 0.02), consistent with the prevalence of incomplete fund absorption documented in prior studies [12].

> **Encoding Note (v2.0):** `activity_category` is currently encoded as a numeric integer from the Kode_Output 2-digit prefix. This encoding imposes implicit ordinal proximity (e.g., category 10 treated as closer to 11 than to 30) on a fundamentally nominal categorical variable, which may bias distance-based algorithms (LOF, IF). One-Hot Encoding (OHE) is the methodologically preferred approach and will be applied in v2 pipeline re-runs. Results reported in this paper reflect the v1 numeric encoding; OHE comparison is included in the sensitivity discussion (Section 5).

> **[Figure 1: Feature Distributions — Jambi Village Fund 2023–2025]**
> *Source: `src/output_v1/charts/feature_distributions.png`*

Figure 2 presents the feature correlation matrix. The strongest pairwise correlation is between `cost_deviation_by_category` and `cost_per_unit` (r = 0.59), which is expected by construction — the former is a within-group z-score of the latter. The moderate correlation between `swakelola_high_value` and `cost_per_unit` (r = 0.38) confirms that high-value self-managed activities tend to exhibit elevated unit costs, consistent with Søreide's [9] procurement corruption argument. All other correlations remain below ±0.25, indicating feature independence sufficient for multi-method detection without multicollinearity concerns.

> **[Figure 2: Feature Correlation Heatmap — Jambi Village Fund 2023–2025]**
> *Source: `src/output_v1/charts/feature_correlation_heatmap.png`*

### 3.3 Detection Algorithms

**Isolation Forest (IF)** partitions the feature space via random axis-aligned splits; records requiring fewer partitions to isolate receive lower anomaly scores [19]. The contamination parameter was set to 5% (95th-percentile threshold) to reflect the expected upper bound of anomaly prevalence in village fund data. `n_estimators = 200`, `max_samples = 256`, `random_state = 42`.

**Local Outlier Factor (LOF)** computes, for each record, the ratio of its estimated local reachability density to the mean local reachability density of its k-nearest neighbours [25]. Records with LOF >> 1.0 are locally dense isolates — statistically deviant within their Kode_Output activity peer group. `n_neighbors = 20`, scored on the full training set (novelty = False).

**Deep Autoencoder (DA)** learns a compressed representation of normal fund expenditure behaviour through an encoder–decoder architecture. During training on the unlabelled dataset, the network learns to reconstruct normal records at low error; anomalous records — whose feature patterns deviate from learned normality — produce elevated Mean Squared Error (MSE) at reconstruction, which serves as the anomaly score. The network architecture is `[n → 64 → 32 → 16 → 8 → 16 → 32 → 64 → n]` (n = number of input features; 8-layer symmetric encoder–decoder with bottleneck at dimension 8) with ReLU activations throughout and a linear output layer. Training uses `epochs = 100` with early stopping (`patience = 10`), `batch_size = 256`. The regularisation sweep over λ ∈ {1×10⁻⁴, 1×10⁻³, 1×10⁻²} selects the weight decay parameter by validation reconstruction MSE. Flagging threshold is the 95th percentile of reconstruction MSE on the full dataset. This architecture is referred to as **DA** throughout (replacing the earlier draft's "RDA" label, which erroneously suggested a separate sparse decomposition component not present in the implementation).

### 3.4 Consensus Anomaly Identification and Typology Mapping

A record receives `consensus_flag = 1` if it is flagged by at least two of the three methods. This multi-paradigm consensus requirement is designed to reduce method-specific false positives by requiring convergence across algorithmically independent detection paradigms. The degree to which this design achieves precision improvement is empirically bounded by the expert validation results reported in Section 4 (Precision@50); in the absence of ground-truth labels, consensus serves as a proxy for detection confidence rather than a confirmed precision guarantee.

Consensus-flagged records are post-processed through a rule-based typology assignment module that maps feature value combinations to seven typology labels (T1–T7) derived from documented corruption modus operandi:

| Code | Typology | Primary Feature Signal |
|---|---|---|
| T1 | Mark-up / Price Inflation | `cost_per_unit` > 3σ AND `cost_deviation_by_category` > 2σ |
| T2 | Ghost Activity | `absorption_ratio` < 0.05 AND `avg_completion` < 10% |
| T3 | Volume Padding | `absorption_ratio` ≥ 0.98 (near-complete budget absorption in single cycle) |
| T4 | Stage Lock | `stage_concentration` > 0.95 AND `n_stages_active` ≥ 2 — where `stage_concentration` = max(Real_T1, Real_T2, Real_T3) / `total_realization`; detects front-loaded multi-stage disbursement |
| T5 | Procurement Irregularity | `Cara_Pengadaan` ∈ {Pihak ke-3, Kontrak} AND `cost_per_unit` > 75th percentile — flags third-party contract activities with elevated unit costs |
| T6 | Budget Exhaustion | `absorption_ratio` > 0.98 AND `avg_completion` < 50% |
| T7 | Cross-Category Dump | `activity_category` mismatch signal relative to Kode_Output peer group |

Records that satisfy no single-rule threshold — or that satisfy multiple conflicting rules — receive an "Unclassified" assignment, which the study analyses separately as a subthreshold masking problem (Section 5.4).

### 3.5 Village Priority Tier Classification

Village-level priority tiers aggregate activity-level consensus flags into an anomaly persistence score per village across three fiscal years. Tier 1 (High Priority) villages exhibit consensus-flagged anomalies in two or more fiscal years; Tier 2 (Moderate) in exactly one year; Tier 3 (Not Flagged) in no year. This persistence dimension operationalises Cressey's Opportunity condition in the Fraud Triangle: multi-year anomaly recurrence signals an entrenched structural vulnerability rather than an incidental deviation [6].
