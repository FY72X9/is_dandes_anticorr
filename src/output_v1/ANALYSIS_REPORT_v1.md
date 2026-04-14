# Analysis Report — Version 1
## Corruption Indication Detection in Village Fund Activities: Jambi Province 2023–2025

> **Report Date**: April 2026  
> **Pipeline Version**: v1  
> **Data Source**: Siskeudes / SIMDA Desa — Penyerapan + Pagu, Jambi Province  
> **Methods**: Isolation Forest (IF) · Local Outlier Factor (LOF) · Reconstruction-based Dense Autoencoder (RDA)  
> **Output Folder**: `src/output_v1/`

---

## Table of Contents

1. [Dataset Overview](#1-dataset-overview)
2. [Feature Engineering Results](#2-feature-engineering-results)
3. [Anomaly Detection Results](#3-anomaly-detection-results)
4. [Score Distribution Analysis](#4-score-distribution-analysis)
5. [Consensus Anomaly Analysis](#5-consensus-anomaly-analysis)
6. [Corruption Typology Mapping](#6-corruption-typology-mapping)
7. [Village Priority Tier Classification](#7-village-priority-tier-classification)
8. [Geographic Distribution](#8-geographic-distribution)
9. [RDA Feature Importance Diagnosis](#9-rda-feature-importance-diagnosis)
10. [Limitations & Open Issues](#10-limitations--open-issues)
11. [Output File Inventory](#11-output-file-inventory)

---

## 1. Dataset Overview

### 1.1 Record Count After Merge

The Penyerapan dataset (activity-level expenditure absorption records) was merged with the Pagu dataset (village budget ceiling) via `Kode_Desa` + `Tahun` as composite keys. The final merged and cleaned dataset spans three fiscal years:

| Year | Records | % of Total |
|---|---|---|
| 2023 | 33,140 | 33.2% |
| 2024 | 36,151 | 36.3% |
| 2025 | 30,401 | 30.5% |
| **Total** | **99,692** | 100% |

The record count is substantially higher than the preliminary estimate of ~33,405 (derived from a single-year Penyerapan file), because the final merge pools all three years into one longitudinal panel, enabling cross-year anomaly consistency analysis.

### 1.2 Procurement Method Distribution

The overwhelming majority of village fund activities are executed through Swakelola (self-managed procurement), which requires no competitive bidding:

| Cara_Pengadaan | Count | % |
|---|---|---|
| Swakelola | 98,520 | 98.8% |
| Penyertaan Modal | 841 | 0.8% |
| Pihak ke-3 | 240 | 0.2% |
| Kerjasama antar Desa | 56 | 0.1% |
| Kontrak | 35 | < 0.1% |

The near-total dominance of Swakelola (98.8%) confirms the theoretical argument that competitive-bidding safeguards are structurally absent from village fund expenditure — creating the accountability vacuum that the `swakelola_high_value` feature is designed to detect.

---

## 2. Feature Engineering Results

### 2.1 Final Feature Matrix

The preprocessed dataset (`features_engineered.csv`) contains 99,692 records × 27 columns. The ML input feature set (used by IF, LOF, and RDA) comprises the following engineered variables:

| Feature | Description | Corruption Modus Addressed |
|---|---|---|
| `cost_per_unit` | `total_realization / Volume` (normalised) | Mark-up / price inflation |
| `absorption_ratio` | `total_realization / Pagu` (village-level) | Proyek fiktif — near-zero absorption |
| `avg_completion` | Mean of Pct_T1, Pct_T2, Pct_T3 (normalised) | Manipulated completion claims |
| `swakelola_high_value` | Binary flag: Swakelola AND realization > threshold | Uncompetitive high-value procurement |
| `activity_category` | Kode_Output 2-digit prefix (encoded) | Cross-category activity mismatch |
| `cost_deviation_by_category` | z-score of cost_per_unit within Kode_Output group | Within-category price outlier |
| `n_stages_active` | Count of disbursement stages with Real > 0 | Incomplete / front-loaded disbursement |

> **Implementation note**: `stage_variance` and `completion_vs_realization` from the conceptual plan were replaced in the v1 implementation by `n_stages_active`. The RDA sub-model (Dense Autoencoder) uses the 5 core features: `cost_per_unit`, `avg_completion`, `swakelola_high_value`, `activity_category`, `cost_deviation_by_category`.

### 2.2 Feature Distribution Summary (Normalised Values)

| Feature | Min | Median | Mean | Max | Std |
|---|---|---|---|---|---|
| `cost_per_unit` | −0.34 | 0.00 | 0.98 | 102.83 | 3.53 |
| `avg_completion` | −2.00 | 0.00 | 0.47 | 4.00 | 0.84 |
| `cost_deviation_by_category` | −2.99 | 0.00 | 0.40 | 42.42 | 1.73 |

Key observations:
- `cost_per_unit` has a max of **102.83** (vs. median 0.00), confirming extreme right-skew from price mark-up outliers.
- `avg_completion` median = 0.00 indicates the majority of activities have near-zero or uniform stage completion percentages; extreme values (up to 4.00 normalised) signal inflated completion reporting.
- `cost_deviation_by_category` max of 42.42 standard deviations above category mean identifies severe within-category price outliers — a direct mark-up signal.

### 2.3 High-Value Swakelola Prevalence

| `swakelola_high_value` | Count | % |
|---|---|---|
| 0 (below threshold / non-Swakelola) | 75,051 | 75.3% |
| **1 (Swakelola AND high value)** | **24,641** | **24.7%** |

Approximately one in four activity records (24.7%) qualifies as a high-value activity executed through Swakelola without competitive procurement — the structural condition that Søreide (2002) identifies as the principal enabler of procurement-stage corruption.

---

## 3. Anomaly Detection Results

### 3.1 Per-Method Flag Count and Anomaly Rate

| Method | Total Flagged | Overall Rate | 2023 Rate | 2024 Rate | 2025 Rate |
|---|---|---|---|---|---|
| IQR Baseline | 18,478 | 18.5% | 21.1% | 17.6% | 17.1% |
| Isolation Forest (IF) | 7,974 | 8.0% | 10.5% | 6.5% | 7.1% |
| LOF | 4,985 | 5.0% | 4.7% | 4.6% | 5.8% |
| RDA (Dense AE) | 4,985 | 5.0% | 5.5% | 3.8% | 5.9% |
| **Consensus (≥ 2 of 3)** | **3,107** | **3.1%** | 4.1% | 2.0% | 3.3% |

### 3.2 Anomaly Rate Consistency Interpretation

**IQR Baseline (18.5%)**: Simple box-plot threshold applied independently per feature. The high rate (21% in 2023 declining to 17% in 2025) reflects the IQR method's inability to account for inter-feature relationships — it flags any single-feature outlier regardless of multi-feature context.

**Isolation Forest (8.0%)**: Year-over-year variance is notable (10.5% → 6.5% → 7.1%), suggesting moderate sensitivity to the 2023 cohort's spending patterns. The higher 2023 rate may reflect genuine elevated anomaly prevalence in the first year post-COVID recovery period when village budgets expanded significantly.

**LOF (5.0%)**: Most consistent rate across years (4.7% → 4.6% → 5.8%), demonstrating cross-year stability predicted by local density adaptation. The 2025 uptick (5.8%) deserves investigation — it may signal structural changes in village spending behaviour.

**RDA — Dense Autoencoder (5.0%)**: Mirrors LOF in total count by design (both set to 95th-percentile threshold), but the year-by-year profile differs (5.5% → 3.8% → 5.9%), suggesting RDA captures a partially different subset of anomalies from LOF.

### 3.3 Inter-Method Agreement (Pairwise Overlap)

| Pair | Records Flagged by Both | % of Smaller Method |
|---|---|---|
| IF ∩ LOF | 317 | 6.4% of LOF |
| IF ∩ RDA | 2,506 | 50.3% of RDA |
| LOF ∩ RDA | 596 | 12.0% of LOF |
| **IF ∩ LOF ∩ RDA (all three)** | **156** | **1.6% of total dataset** |
| Consensus (≥ 2) | 3,107 | — |

**Key finding**: IF and RDA share over half of RDA's flagged records (2,506 / 4,985 = 50.3%), indicating strong convergence between tree partitioning and autoencoder reconstruction on the same anomalous patterns. By contrast, LOF shows lower overlap with both IF (6.4%) and RDA (12.0%), confirming that LOF identifies a **distinct subset** of locally-deviant anomalies that the other two paradigms structurally miss — consistent with Li et al. (2025) [18] findings on USA federal spending data.

The 156 records flagged by all three methods represent **triple consensus** — the highest-confidence indications for priority inspection.

---

## 4. Score Distribution Analysis

### 4.1 Bimodality Coefficient (BC)

The Bimodality Coefficient tests whether the score distribution exhibits two distinct modes (normal cluster vs. anomaly tail). BC > 0.555 indicates bimodal distribution.

| Method | BC Score | Interpretation |
|---|---|---|
| Isolation Forest | **0.335** | Unimodal — broad, overlapping score range; no clear separation |
| RDA (Dense AE) | **0.703** | Moderate bimodal — clear anomaly tail distinct from normal mass |
| **LOF** | **0.957** | **Strong bimodal — sharpest normal/anomaly discrimination** |

**Isolation Forest (BC = 0.335)**: The decision function score ranges from −0.22 to +0.20 with a roughly uniform distribution above 0.05. The 95th-percentile threshold (≈ +0.18) falls within a dense region of scores — meaning IF draws its anomaly boundary through a high-density area rather than a natural valley, risking false positives among borderline-normal records.

**RDA (BC = 0.703)**: The MSE distribution is highly right-skewed with a pronounced heavy tail. The median MSE ≈ 2.8×10⁻⁵ versus the 95th-percentile threshold ≈ 3.5×10⁻⁴ represents a **12.5× separation** — a clean gap between normal reconstruction fidelity and anomalous records where the autoencoder fails to reconstruct.

**LOF (BC = 0.957)**: The LOF score distribution is extremely L-shaped — the vast majority of records cluster near LOF = 1.0 (normal), while a small extreme tail extends to LOF > 10⁹. This confirms LOF's theoretical advantage: normal records appear perfectly embedded in their local neighbourhood (LOF ≈ 1.0), while genuine local outliers produce dramatically elevated scores. The BC of 0.957 is the highest among the three methods and exceeds the 0.555 bimodality threshold by 73%.

### 4.2 Score Range Summary

| Method | Min | Median | Mean | 95th pct (threshold) | Max |
|---|---|---|---|---|---|
| IF (decision function) | −0.223 | 0.131 | 0.110 | ~0.180 | 0.198 |
| LOF | 0.922 | 1.025 | 5.21×10⁶ | — | 5.40×10⁹ |
| RDA (MSE) | 1.67×10⁻⁷ | 2.80×10⁻⁵ | 8.94×10⁻⁵ | ~3.5×10⁻⁴ | 5.50×10⁻² |

### 4.3 PCA Projection

The PCA 2D projection (PC1 = 26.0% variance, PC2 = 12.7% variance, cumulative 38.7%) shows that consensus-flagged anomalies (n=3,107, red) form a visible projection gradient toward positive PC1 values, with extreme outliers reaching PC1 > 30. The distribution is not fully separable in 2D PCA space (38.7% variance captured), consistent with the 10-dimensional feature matrix encoding corruption patterns that are distributed across multiple features simultaneously rather than along a single dominant axis.

### 4.4 t-SNE Projection

The t-SNE 2D projection (computed on a 15,000-record random sample: 14,538 normal + 462 consensus-flagged) reveals a more informative picture than PCA: consensus anomalies (red) concentrate in **specific sub-clusters** on the right periphery of the t-SNE map, with several dense red clusters visible around t-SNE coordinates (50–80, −30 to −50). This localisation supports the fraud triangle interpretation: anomalous activities cluster by activity-type neighbourhood, indicating that corruption patterns within specific Kode_Output categories repeat systematically across villages rather than appearing randomly.

---

## 5. Consensus Anomaly Analysis

### 5.1 Consensus Flag Definition

A record is marked `consensus_flag = 1` if flagged by **at least 2 of the 3 methods** (IF, LOF, RDA). This multi-paradigm consensus requirement reduces method-specific false positives and surfaces records where independent algorithmic reasoning converges.

**Total consensus-flagged records: 3,107 (3.1% of 99,692)**

### 5.2 Top Flagged Activity Names

The 15 most frequently flagged activity descriptions (by `Uraian_Output`) among consensus records:

| Rank | Activity Description | Count |
|---|---|---|
| 1 | Bantuan Langsung Tunai (BLT) - Dana Desa | 301 |
| 2 | Penyertaan Modal BUMDes | 206 |
| 3 | Terselenggaranya Operasional PKD/Polindes | 129 |
| 4 | Penyelenggaraan Festival Kesenian / Kebudayaan / Keagamaan | 106 |
| 5 | Operasional PAUD/TK/TPA/TKA/TPQ | 91 |
| 6 | Terselenggaranya Pembinaan PKK | 89 |
| 7 | Jumlah Frekwensi Pelatihan/Penyuluhan Pemberdayaan Perempuan | 78 |
| 8 | Makanan Tambahan | 75 |
| 9 | Jumlah alat produksi dan pengolahan pertanian yang diserahkan | 73 |
| 10 | Jumlah Peserta Peningkatan kapasitas perangkat Desa | 71 |
| 11 | Biaya Koordinasi Pemerintah Desa | 63 |
| 12 | Gedung Balai Desa / Balai Kemasyarakatan | 63 |
| 13 | Operasional RT/RW | 57 |
| 14 | Gedung/Bangunan PAUD | 54 |
| 15 | Jumlah Peserta Peningkatan kapasitas BPD | 54 |

**Interpretation**: The dominance of **BLT Dana Desa** (301 records) is structurally concerning: direct cash transfers are high-value, low-accountability activities that Hidajat (2025) [6] identifies as particularly vulnerable to pemotongan (disbursement deductions at the point of distribution). **Penyertaan Modal BUMDes** (206 records) constitutes one of the most documented fraud vectors — equity injections into village-owned enterprises are difficult to audit and frequently fictitious.

Operasional activities (PKD, PAUD, RT/RW, PKK) appearing uniformly high in the flagged list are consistent with the typical **mark-up pattern**: operational categories have no fixed unit benchmark, enabling cost inflation that evades category-mean comparison.

### 5.3 Procurement Pattern of Flagged Records

| Cara_Pengadaan | Count in Consensus | % of Consensus |
|---|---|---|
| Swakelola | 2,994 | 96.4% |
| Penyertaan Modal | 83 | 2.7% |
| Pihak ke-3 | 24 | 0.8% |
| Kerjasama antar Desa | 3 | 0.1% |
| Kontrak | 3 | 0.1% |

Consensus anomalies are **96.4% Swakelola** — slightly higher than the baseline prevalence (98.8%), suggesting that non-Swakelola procurement is marginally over-represented in Penyertaan Modal flags (2.7% of consensus vs. 0.8% baseline), consistent with the equity-injection fraud vector.

---

## 6. Corruption Typology Mapping

### 6.1 Typology Definitions

Each consensus-flagged record was assigned one or more typology labels based on feature threshold rules derived from the modus operandi taxonomy in Hidajat (2025) [6] and ICW (2024) [8]:

| Code | Label | Detection Rule |
|---|---|---|
| T1 | Mark-up / Price Inflation | `cost_per_unit` OR `cost_deviation_by_category` above threshold |
| T2 | Ghost Activity (Proyek Fiktif) | Near-zero `absorption_ratio` OR near-zero `avg_completion` |
| T3 | Volume Padding | `cost_deviation_by_category` above threshold with `cost_per_unit` normal |
| T4 | Stage Lock | All realization concentrated in single disbursement stage (no `n_stages_active` variance) |
| T5 | Procurement Irregularity | `swakelola_high_value` = 1 AND activity code inconsistent with Swakelola category norms |
| T6 | Budget Exhaustion | `absorption_ratio` near 1.00 with zero completion reports |
| T7 | Cross-Category Dump | `activity_category` z-score extreme — activity code mismatched to expenditure type |

### 6.2 Typology Frequency Distribution (Multi-label)

| Typology | Flagged Records | % of Consensus (multi-label) |
|---|---|---|
| **T1: Mark-up** | **1,571** | **50.6%** |
| **T7: Cross-Category Dump** | **1,568** | **50.5%** |
| T2: Ghost Activity | 774 | 24.9% |
| Unclassified | 708 | 22.8% |
| T3: Volume Padding | 38 | 1.2% |
| T6: Budget Exhaustion | 32 | 1.0% |
| T5: Procurement Irregularity | 26 | 0.8% |
| T4: Stage Lock | 0 | 0.0% |

### 6.3 Typology Combination Patterns

The most prevalent **multi-label combinations** (records often receive more than one typology):

| Combination | Count | Interpretation |
|---|---|---|
| T1 + T7 | 1,141 | Mark-up within misclassified category — strongest compound signal |
| Unclassified | 759 | Anomaly detected but no single typology rule triggered robustly |
| T2 alone | 450 | Clean ghost activity — low absorption, no price signal |
| T1 alone | 413 | Pure price inflation without category anomaly |
| T2 + T7 | 297 | Ghost activity with cross-category budget routing |
| T7 alone | 112 | Category mismatch without price signal |
| T1+T2+T3+T6+T7 (full compound) | 23 | Most severe multi-signal records |
| T1+T2+T7 | 21 | Mark-up + ghost + category compounds |

**Key interpretation**: The T1+T7 combination (1,141 records = 36.7% of all consensus flags) indicates that price inflation and activity code misuse co-occur systematically — consistent with the fraud mechanism where village officials exploit activity code ambiguity to route inflated expenditure through operationally flexible categories.

### 6.4 T4 Stage Lock — Zero Detections

T4 (Stage Lock, where all expenditure is concentrated in a single disbursement stage indicating fabricated multi-stage reporting) produced **zero detections** in v1. This is attributable to the `n_stages_active` implementation replacing `stage_variance`: `n_stages_active` counts stages with Real > 0, which may not discriminate sufficiently when activities legitimately have only one or two disbursement stages by regulatory schedule. Recalibration of this typology rule — using the ratio `max(Real_T1, Real_T2, Real_T3) / total_realization` as a concentration index — is recommended for v2.

---

## 7. Village Priority Tier Classification

### 7.1 Tier Definition

Villages are classified based on **anomaly persistence** — the proportion of fiscal years (2023–2025) in which the village generated at least one consensus-flagged activity:

| Tier | Persistence Score | Years Flagged | Villages |
|---|---|---|---|
| **Tier 1 — High Priority** | ≥ 0.67 | 2 or 3 of 3 | **642** |
| Tier 2 — Moderate | 0.33 | 1 of 3 | 459 |
| Tier 3 — Not Flagged | 0.00 | 0 of 3 | 263 |
| **Total unique villages** | — | — | **1,364** |

### 7.2 Fully Persistent Villages (3/3 Years Flagged)

**174 villages** generated consensus anomalies in all three fiscal years 2023, 2024, and 2025. These villages carry the highest anomaly persistence score (1.0) and warrant immediate inspection priority.

Top 15 fully persistent villages by flagged record count:

| Village Name | Kode_Desa | Flagged Records | Dominant Typology |
|---|---|---|---|
| Karya Harapan Mukti | 1508092016 | 14 | T1: Mark-up |
| Sungai Arang | 1508122004 | 14 | T2: Ghost Activity |
| Pasar Rantau Embacang | 1508052017 | 11 | T1: Mark-up |
| Simpang Bebeko | 1508102004 | 11 | T7: Cross-Category Dump |
| Pinggir Air | 1572052006 | 10 | T1: Mark-up |
| Datar | 1508082007 | 10 | T7: Cross-Category Dump |
| Peninjau | 1508152002 | 10 | T7: Cross-Category Dump |
| Maliki Air | 1572032003 | 10 | Unclassified |
| Lembah Kuamang | 1508092006 | 9 | Unclassified |
| Tuo Lbk. Mengkuang | 1508072002 | 9 | T2: Ghost Activity |
| Timbolasi | 1508142005 | 9 | T7: Cross-Category Dump |
| Sungai Ruan Ilir | 1504062013 | 9 | T1: Mark-up |
| Bungku | 1504072001 | 9 | T1: Mark-up |
| Lempur Mudik | 1501012003 | 4 | T1: Mark-up |
| Pelayang Raya | 1572082004 | 5 | T7: Cross-Category Dump |

### 7.3 Dominant Typology Distribution Among Tier-1 Villages

| Dominant Typology | Tier-1 Villages | % of Tier-1 |
|---|---|---|
| T1: Mark-up | 305 | 47.5% |
| Unclassified | 121 | 18.8% |
| T7: Cross-Category Dump | 109 | 17.0% |
| T2: Ghost Activity | 105 | 16.4% |
| T5: Procurement Irregularity | 2 | 0.3% |

Mark-up (T1) is the dominant typology at village level (47.5%), reinforcing its status as the most prevalent structural corruption mechanism in Jambi village fund expenditure.

---

## 8. Geographic Distribution

### 8.1 Consensus Anomalies by Kabupaten

| Kabupaten/Kota | Consensus Anomalies | Tier-1 Villages |
|---|---|---|
| **KAB. BUNGO** | **577** | **103** |
| KAB. BATANGHARI | 415 | 85 |
| KAB. KERINCI | 403 | 86 |
| KAB. MERANGIN | 367 | 84 |
| KOTA SUNGAI PENUH | 309 | 47 |
| KAB. T E B O | 280 | 66 |
| KAB. SAROLANGUN | 246 | 62 |
| KAB. MUARO JAMBI | 237 | 49 |
| KAB. TANJUNG JABUNG BARAT | 169 | 41 |
| KAB. TANJUNG JABUNG TIMUR | 104 | 21 |
| **TOTAL** | **3,107** | **642** |

**KAB. BUNGO** records the highest absolute anomaly count (577 records, 103 Tier-1 villages) across all three years. KOTA SUNGAI PENUH's anomaly-to-village ratio is particularly elevated — 309 consensus records concentrated in a Kota (urban municipality), where per-activity expenditure values tend to be higher, amplifying mark-up financial impact.

### 8.2 Peak-Year Anomaly by Kabupaten (2023)

The 2023 fiscal year produced the highest consensus anomaly count (1,364 records). Top kabupaten in 2023:

| Kabupaten | 2023 Consensus | % of 2023 Total |
|---|---|---|
| KAB. BUNGO | 319 | 23.4% |
| KOTA SUNGAI PENUH | 221 | 16.2% |
| KAB. MERANGIN | 183 | 13.4% |
| KAB. BATANGHARI | 145 | 10.6% |

The concentration of 2023 anomalies in Bungo and Sungai Penuh suggests regional structural factors — potentially related to post-COVID budget expansion in those kabupaten creating mark-up opportunities during a period of reduced audit oversight.

---

## 9. RDA Feature Importance Diagnosis

### 9.1 Mean Reconstruction Error per Feature (Consensus-Flagged Records)

The Dense Autoencoder (RDA) decomposes reconstruction error per input feature, enabling per-record diagnosis of which financial variable drives the anomaly signal:

| Rank | Feature | Mean MSE | Interpretation |
|---|---|---|---|
| 1 | `avg_completion` | Highest | Abnormal completion percentage patterns dominate anomaly reconstruction failure |
| 2 | `cost_per_unit` | 2nd | Price inflation drives the second largest reconstruction error |
| 3 | `activity_category` | 3rd | Activity code mismatches — cross-category expenditure routing |
| 4 | `cost_deviation_by_category` | 4th | Within-category cost deviation |
| 5 | `swakelola_high_value` | 5th | High-value Swakelola procurement flag |

### 9.2 Top RDA Diagnosis Feature per Village (Tier-1)

Among 642 Tier-1 villages, the primary RDA driver is:

| Top Error Feature | Tier-1 Villages | % |
|---|---|---|
| `avg_completion` | 279 | 43.5% |
| `activity_category` | 200 | 31.2% |
| `cost_per_unit` | 96 | 14.9% |
| `cost_deviation_by_category` | 45 | 7.0% |
| `swakelola_high_value` | 22 | 3.4% |

**`avg_completion` dominates** (43.5% of Tier-1 villages): the autoencoder identifies completion percentage manipulation as the most structurally abnormal feature — consistent with the common practice of reporting 100% completion on T1 disbursement while T2 and T3 receipts show near-zero realisation (Laporan Pertanggungjawaban Palsu).

### 9.3 Feature Correlation Key Findings

From the feature correlation heatmap (Jambi Village Fund 2023–2025):

| Pair | Correlation | Significance |
|---|---|---|
| `cost_per_unit` ↔ `cost_deviation_by_category` | **0.59** | Strong positive — price outliers within a category reinforce the global price signal |
| `cost_per_unit` ↔ `swakelola_high_value` | 0.38 | Moderate — Swakelola activities carry higher unit costs |
| `avg_completion` ↔ `swakelola_high_value` | 0.25 | Weak-moderate |
| `activity_category` ↔ `cost_per_unit` | −0.02 | Near-zero — activity category is largely orthogonal to price signal |

The strong correlation between `cost_per_unit` and `cost_deviation_by_category` (0.59) confirms redundant information between these two features. In a v2 refinement, PCA pre-processing or feature selection may improve RDA reconstruction efficiency by reducing this collinearity.

---

## 10. Limitations & Open Issues

### 10.1 Expert Validation Pending

The four expert validation sheets (`expert_validation_top50_*.csv`) have been prepared with the top-50 highest-scoring records per method. The columns `expert_verdict` and `modus_operandi_notes` remain unfilled pending domain expert review. **No Precision@50 metric is available from this report** — this is the primary outstanding deliverable before academic writing can proceed.

### 10.2 T4 Stage Lock — Zero Detections

As noted in Section 6.4, T4 produced no detections. The `n_stages_active` implementation counts active realization stages, which does not adequately capture single-stage concentration fraud. Recommended fix for v2:

```
T4_stage_lock = 1  if  max(Real_T1, Real_T2, Real_T3) / total_realization > 0.95
                       AND  n_stages_active >= 2
```

### 10.3 Cohen's κ Not Computed

Inter-method agreement was assessed via pairwise overlap counts (Section 3.3), but the formal Cohen's κ statistic has not been computed. This metric is required for the evaluation framework section of the academic paper. Computation is straightforward from the binary flag vectors in `anomaly_flags.csv`.

### 10.4 Unclassified Records (708 / 22.8%)

708 consensus-flagged records carry no typology assignment — the anomaly signal is strong enough to trigger multi-method consensus, but no single typology rule threshold is exceeded. This suggests a compound anomaly pattern not captured by any individual rule. Two options for v2: (a) introduce a T8 "Compound Irregular" typology for multi-feature edge cases, or (b) apply a soft classification model trained on the existing T1–T7 labelled subset.

### 10.5 Feature Collinearity

`cost_per_unit` and `cost_deviation_by_category` exhibit r = 0.59 — moderate collinearity. This inflates the relative contribution of the price signal across both features in the RDA model. A LASSO-regularised feature selection step or PCA → ML pipeline is recommended for v2.

### 10.6 Single Province Scope

All findings are scoped to Jambi Province (99,692 records). Generalisation to other provinces requires replication — particularly provinces with different land-use compositions (urban vs. rural density ratios can shift activity-category distributions substantially).

### 10.7 Kode_Desa = −1 Anomaly

One row in `tier1_village_summary.csv` shows `Kode_Desa = −1` with 80 flagged records and `Nama_Desa = NaN` — this is a data artefact from the merge, representing records where no village code could be matched to the Pagu dataset. These 80 records should be isolated and investigated for merge key quality issues.

---

## 11. Output File Inventory

| File | Records | Description |
|---|---|---|
| `features_engineered.csv` | 99,692 × 27 | Merged and cleaned dataset with all engineered features |
| `df_merged_raw.csv` | — | Raw merged dataset before feature engineering |
| `anomaly_flags.csv` | 99,692 × 45 | All scores (if_score, lof_score, rda_score) + binary flags + consensus + persistence + typology |
| `scores_all_methods.csv` | — | Village-level score summary (one row per village-year) |
| `flagged_with_typology.csv` | 3,265 × 21 | All consensus-flagged records + typology labels + RDA error diagnosis |
| `typology_frequency.csv` | 8 × 4 | Typology count, label, and % of flagged |
| `village_persistence.csv` | 1,364 × 6 | Unique village persistence scores and priority tier |
| `tier1_village_summary.csv` | 642 × 7 | Tier-1 high-priority villages with dominant typology and top RDA feature |
| `expert_validation_top50_IF.csv` | 50 × 19 | Top-50 IF-scored records for expert review |
| `expert_validation_top50_LOF.csv` | 50 × 19 | Top-50 LOF-scored records for expert review |
| `expert_validation_top50_RDA.csv` | 50 × 19 | Top-50 RDA-scored records for expert review |
| `expert_validation_top50_CONSENSUS.csv` | 50 × 19 | Top-50 consensus-scored records for expert review |
| `notebook_run/01_data_preprocessing.ipynb` | — | Data merge, cleaning, and feature engineering notebook |
| `notebook_run/02_unsupervised_comparison.ipynb` | — | IF + LOF + RDA training, evaluation, and visualisation |
| `notebook_run/03_corruption_typology_analysis.ipynb` | — | Typology mapping, persistence scoring, village prioritisation |

---

## Summary of Key Findings

| Finding | Value |
|---|---|
| Total activity records analysed | 99,692 |
| Consensus anomalies detected (≥ 2 of 3 methods) | 3,107 (3.1%) |
| Triple-consensus anomalies (all 3 methods) | 156 (0.16%) |
| Method with sharpest score bimodality | LOF (BC = 0.957) |
| Dominant corruption typology | T1: Mark-up (50.6%) co-dominant with T7: Cross-Category Dump (50.5%) |
| Most flagged activity | BLT Dana Desa (301 records) |
| Most flagged kabupaten | Kab. Bungo (577 records, 103 Tier-1 villages) |
| Tier-1 high-priority villages | 642 of 1,364 unique villages |
| Fully persistent villages (3/3 years) | 174 |
| Primary RDA driver in Tier-1 | `avg_completion` (43.5% of Tier-1 villages) |
| Expert validation status | ⏳ Pending — 4 × top-50 sheets awaiting review |
| T4 Stage Lock detections | 0 — rule recalibration required |

---

*Report generated from `src/output_v1/` pipeline outputs, April 2026. For methodology details see [research_concept_phase1.md](../../concept/conceptual/research_concept_phase1.md).*
