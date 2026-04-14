# Corruption Indication Detection in Village Fund Activities Using Comparative Unsupervised Learning Methods

> **Domain**: Information Systems / Applied Machine Learning  
> **Data Scope**: Jambi Province, Indonesia — Village Fund Expenditure Absorption 2023–2025  
> **Last Updated**: April 2026 — Phase 3 (Model Development) complete; results available in `src/output_v1/`

---

## Research Overview

This research develops an unsupervised machine learning pipeline to detect expenditure anomalies in Indonesia's Dana Desa (Village Fund) programme, using activity-level financial absorption records from Jambi Province across three fiscal years (2023–2025). The study compares three algorithmically distinct unsupervised methods — **Isolation Forest**, **Local Outlier Factor (LOF)**, and **Dense Autoencoder** — and maps detected anomalies to known corruption modus operandi documented in KPK and ICW judicial records.

### Research Questions

1. What feature constructs derived from village fund absorption data serve as the most discriminating signals of expenditure anomaly, based on documented corruption modus operandi in Indonesia?
2. Which among Isolation Forest, LOF, and Dense Autoencoder demonstrates superior anomaly identification performance on Jambi province village fund data across 2023–2025?
3. How do algorithmically identified anomalous activities map to established corruption typologies (mark-up, fictitious projects, double budgeting, procurement irregularities)?

### Theoretical Foundations

| Theory | Role in This Study |
|---|---|
| **Fraud Triangle** (Cressey, 1953) | Labelling framework for interpreting detected anomalies |
| **Principal-Agent Theory** | Explains information asymmetry between village heads and oversight bodies |
| **DeLone & McLean IS Success Model** | Justifies the organisational value of an IS-based anomaly detection system |

---

## Research Progress

### Phase 1 — Conceptual Framework ✅ COMPLETED

- [x] Research title and problem statement formulated
- [x] Three research questions defined
- [x] Theoretical framework established (Fraud Triangle + Principal-Agent + DeLone & McLean)
- [x] Literature review completed — 33 references (refs [1]–[33]): 29 Scopus/IEEE/MDPI-indexed academic sources + 4 verified Jambi prosecution case sources
- [x] Research gap identified across five dimensions (domain, method, geography, data type, comparison)
- [x] Jambi Province site selection quantitatively justified (jaga.id complaint data, Alfada [29], Srirejeki & Faturokhman [28])
- [x] Jambi Province prosecution case evidence documented — 4 cases (TA 2020–2024), Rp 2.301 billion total state loss, 2–5 year detection lag quantified [30–33]
- [x] Method selection finalised with scientific rationale:
  - Isolation Forest retained as Tier-1 primary (Li et al., 2025 — USA federal spending)
  - LOF adopted to replace DBSCAN (density heterogeneity problem resolved)
  - Dense Autoencoder adopted to replace K-Means + Mahalanobis (non-linear compound detection)
- [x] Corruption typology mapping table produced (7 modus operandi)
- [x] 10-feature engineering plan defined
- [x] Implementation plan (3 Colab notebooks) outlined
- [x] Conceptual framework diagram drawn
- [x] Reference list compiled with DOIs/URLs verified

**Key document**: [concept/conceptual/research_concept_phase1.md](concept/conceptual/research_concept_phase1.md)

---

### Phase 2 — Data Acquisition & Preprocessing ✅ COMPLETED

- [x] Raw data sourced: 6 Excel files (Pagu + Penyerapan, Jambi Province, 2023–2025)
- [x] CSV conversion completed for all 6 files → `data_ref/csv/`
- [x] Schema validated: Penyerapan columns confirmed (19 fields including Real_T1–T3, Pct_T1–T3, Cara_Pengadaan)
- [x] Data merge: Penyerapan (all years) joined with Pagu by `Kode_Desa` + `Tahun`
- [x] Data cleaning: nulls imputed, header rows removed, numeric ranges validated
- [x] Feature engineering complete → `features_engineered.csv` (99,692 records × 27 columns)
- [x] Final merged scale: **99,692 activity records** (2023=33,140 | 2024=36,151 | 2025=30,401)

> **Implementation note**: `stage_variance` and `completion_vs_realization` from the original plan were superseded by `n_stages_active` (count of active disbursement stages per record) in the final implementation. The RDA sub-model uses 5 core features: `cost_per_unit`, `avg_completion`, `swakelola_high_value`, `activity_category`, `cost_deviation_by_category`.

**Output**: [src/output_v1/features_engineered.csv](src/output_v1/features_engineered.csv)

---

### Phase 3 — Model Development ✅ COMPLETED

- [x] Notebook `01_data_preprocessing.ipynb` — merge, clean, engineer features → `features_engineered.csv`
- [x] Notebook `02_unsupervised_comparison.ipynb` — Isolation Forest, LOF, RDA (Dense Autoencoder) trained and applied
- [x] Anomaly rate consistency computed across 2023/2024/2025
- [x] Score distribution bimodality assessed (Bimodality Coefficient per method)
- [x] Inter-method consensus flags produced (≥2 of 3 methods)
- [x] PCA and t-SNE visualisation generated
- [x] Notebook `03_corruption_typology_analysis.ipynb` — consensus flags mapped to 7 typologies
- [x] Tier-1 village summary produced (642 high-priority villages)
- [x] Expert validation sheets prepared (top-50 per method, awaiting domain review)

**Outputs**: [src/output_v1/](src/output_v1/)

---

---

## Key Results — Version 1 (April 2026)

### Dataset Scale

| Year | Records | Consensus Anomalies |
|---|---|---|
| 2023 | 33,140 | 1,364 |
| 2024 | 36,151 | 728 |
| 2025 | 30,401 | 1,015 |
| **Total** | **99,692** | **3,107 (3.1%)** |

### Anomaly Rate per Method

| Method | Flagged (Total) | Overall Rate | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| IQR Baseline | 18,478 | 18.5% | 21.1% | 17.6% | 17.1% |
| Isolation Forest | 7,974 | 8.0% | 10.5% | 6.5% | 7.1% |
| LOF | 4,985 | 5.0% | 4.7% | 4.6% | 5.8% |
| RDA (Dense AE) | 4,985 | 5.0% | 5.5% | 3.8% | 5.9% |
| **Consensus (≥2)** | **3,107** | **3.1%** | 4.1% | 2.0% | 3.3% |

### Score Distribution Bimodality (Bimodality Coefficient)

| Method | BC Score | Interpretation |
|---|---|---|
| Isolation Forest | 0.335 | Weak separation — broad, overlapping score range |
| RDA (Dense AE) | 0.703 | Moderate-strong bimodal — clear anomaly tail |
| **LOF** | **0.957** | **Strong bimodal — sharpest normal/anomaly discrimination** |

> LOF achieves the highest BC score, confirming its superiority in separating densely-packed normal patterns from locally-deviant anomalies across heterogeneous activity categories.

### Top RDA Error Features (Consensus-Flagged Records)

Among consensus-flagged records, the mean per-feature reconstruction error (MSE) ranks:

1. `avg_completion` — highest mean error (manipulated completion reports)
2. `cost_per_unit` — second-highest (price inflation)
3. `activity_category` — cross-category activity code mismatch
4. `cost_deviation_by_category` — within-category cost outlier
5. `swakelola_high_value` — uncompetitive high-value procurement

### Corruption Typology Distribution (Consensus-Flagged, Multi-label)

| Typology | Count | % of Flagged |
|---|---|---|
| T1: Mark-up / Price Inflation | 1,571 | 50.6% |
| T7: Cross-Category Dump | 1,568 | 50.5% |
| T2: Ghost Activity | 774 | 24.9% |
| Unclassified | 708 | 22.8% |
| T3: Volume Padding | 38 | 1.2% |
| T6: Budget Exhaustion | 32 | 1.0% |
| T5: Procurement Irregularity | 26 | 0.8% |
| T4: Stage Lock | 0 | 0.0% |

> T1 Mark-up and T7 Cross-Category Dump co-dominate at ~50% each (multi-label), consistent with KPK audit findings that price manipulation and activity code misuse are the most prevalent village fund fraud mechanisms.

### Village Priority Tiers (Unique Villages: 1,364)

| Tier | Villages | Basis |
|---|---|---|
| Tier 1 – High Priority | **642** | Flagged in ≥2 years; persistence score ≥ 0.67 |
| Tier 2 – Moderate | 459 | Flagged in 1 year |
| Tier 3 – Not Flagged | 263 | No consensus anomaly across all years |

> 642 Tier-1 villages represent the primary inspection recommendation list for Inspectorate/BPKP triage.

### Expert Validation Status

| Sheet | Records | Status |
|---|---|---|
| `expert_validation_top50_IF.csv` | 50 | ⏳ Awaiting domain expert review |
| `expert_validation_top50_LOF.csv` | 50 | ⏳ Awaiting domain expert review |
| `expert_validation_top50_RDA.csv` | 50 | ⏳ Awaiting domain expert review |
| `expert_validation_top50_CONSENSUS.csv` | 50 | ⏳ Awaiting domain expert review |

---

### Phase 4 — Academic Writing ❌ NOT STARTED

- [ ] Abstract (≤250 words, IEEE format)
- [ ] Introduction & Background
- [ ] Literature Review
- [ ] Theoretical Framework
- [ ] Methodology
- [ ] Data Analysis & Results
- [ ] Discussion
- [ ] Conclusion & Future Work
- [ ] References (IEEE sequential, DOI-verified)

---

## Repository Structure

```
is_dandes_anticorr/
├── README.md                          ← This file (progress report)
├── .venv/                             ← Python virtual environment
├── concept/
│   └── conceptual/
│       ├── research_concept_phase1.md ← Full conceptual framework (Phase 1)
│       ├── references.md              ← Verified reference list (IEEE format)
│       ├── download_papers.py         ← Script to fetch PDF literature
│       └── papers-literatures/        ← Reference PDFs (5/29 downloaded)
├── data_ref/
│   ├── csv/                           ← Converted CSV files (analysis inputs)
│   │   ├── Pagu_Jambi_{2023-2025}.csv
│   │   └── Penyerapan_Jambi_{2023-2025}.csv
│   └── (source Excel files)
├── docs/
│   ├── draft/                         ← Paper draft chapters (pending)
│   ├── latex/                         ← LaTeX source (pending)
│   └── references/                    ← Reference management files (pending)
└── src/
    ├── convert_xlsx_to_csv.py         ← Data conversion utility
    └── output_v1/                     ← Phase 3 results (v1)
        ├── features_engineered.csv    ← 99,692 records × 27 columns
        ├── anomaly_flags.csv          ← All scores + flags per record
        ├── scores_all_methods.csv     ← Village-level score summary
        ├── flagged_with_typology.csv  ← 3,265 flagged records + typology labels
        ├── typology_frequency.csv     ← Typology distribution counts
        ├── village_persistence.csv    ← Tier 1/2/3 per unique village (1,364)
        ├── tier1_village_summary.csv  ← 642 Tier-1 villages + dominant typology
        ├── expert_validation_top50_*.csv ← Top-50 per method (awaiting review)
        └── notebook_run/
            ├── 01_data_preprocessing.ipynb
            ├── 02_unsupervised_comparison.ipynb
            └── 03_corruption_typology_analysis.ipynb
```

---

## Methodology Summary

### Algorithmic Approaches

| Method | Paradigm | Key Advantage |
|---|---|---|
| **Isolation Forest** | Ensemble / Path-length partitioning | Tier-1 standard for government expenditure data; no distributional assumptions |
| **Local Outlier Factor (LOF)** | Local density estimation | Adapts to heterogeneous activity-category densities; continuous score for triage |
| **Dense Autoencoder (AE)** | Neural network reconstruction | Detects non-linear compound anomalies; per-feature error enables auditor diagnosis |

### Engineered Features (10 total)

| Feature | Corruption Modus Operandi |
|---|---|
| `cost_per_unit` | Mark-up / price inflation |
| `absorption_ratio` | Fictitious project (proyek fiktif) |
| `avg_completion` | Incomplete / manipulated completion reports |
| `stage_variance` | Irregular multi-stage disbursement |
| `completion_vs_realization` | False accountability reports |
| `swakelola_high_value` | High-value procurement without competitive bidding |
| `cost_deviation_by_category` | Within-category cost outlier |
| `total_realization` | Absolute expenditure baseline |
| `activity_category` | Activity-type cluster grouping |
| `year` | Inter-year cost drift |

### Evaluation (Unsupervised Setting — No Ground Truth Labels)

- Anomaly rate consistency across 2023/2024/2025
- Inter-method agreement via Cohen's κ
- PCA / t-SNE anomaly distribution visualisation
- Qualitative domain-expert validation of sampled flagged records

---

## Key References

| # | Source | Relevance |
|---|---|---|
| [6] | Hidajat (2025), *Journal of Financial Crime* | Village fund corruption modus operandi taxonomy |
| [10] | DeLone & McLean (2003), *JMIS* | IS Success Model — theoretical anchor |
| [11] | Herreros-Martínez & Magdalena-Benedicto (2025), *Information* | Hybrid clustering + Isolation Forest on procurement data |
| [18] | Li et al. (2025), arXiv:2509.19366 | Isolation Forest + LOF on USA federal spending — closest structural analogue |
| [19] | Kumar et al. (2025), *KAIS* | Hybrid IF + Autoencoder framework — compound anomaly detection |
| [20] | De Meulemeester et al. (2025), *BMC MIDM* | Explainable unsupervised anomaly detection; per-feature reconstruction error |
| [22] | Shi & Weng (2024), *JCIA* | Autoencoder vs. other methods on government billing data |
| [27] | Jaga.id (2026) | Community complaint data — Jambi under-reporting quantification |
| [28] | Srirejeki & Faturokhman (2020), *Acta Univ. Danubius* | Inspectorate staffing gap — APIP audit coverage limitation |
| [29] | Alfada (2019), *JRFM* | Panel GMM evidence: fiscal decentralisation + weak accountability → elevated corruption |
| [30] | JambiTV Disway (2026) | Desa Muara Hemat — fictitious construction, Rp 942 juta, Tahap II prosecution |
| [31] | JambiTV Disway (2025) | Desa Jambi Tulo — fictitious procurement, disbursement frozen by Inspektorat |
| [32] | Kompas.com (2025) | Desa Batang Merangin — pendamping desa collusion, Rp 644 juta |
| [33] | JambiLINK.id (2024) | Desa Pangkal Duri — Dana Silpa misappropriation, Rp 415 juta |

Full reference list: [concept/conceptual/references.md](concept/conceptual/references.md)

---

## Next Actions

1. **Domain expert review** — complete `expert_validation_top50_CONSENSUS.csv` (fill `expert_verdict` + `modus_operandi_notes` columns) to establish Precision@50 ground truth
2. **Compute Cohen's κ** — inter-method agreement between IF, LOF, and RDA flag vectors across full 99,692-record dataset
3. **Begin paper draft** — write Abstract + Introduction using `docs/draft/`; ground findings in confirmed result numbers above
4. **Investigate T4 Stage Lock = 0** — verify whether `stage_variance` / `n_stages_active` threshold is calibrated correctly; T4 should theoretically flag records with all disbursement concentrated in a single stage
5. **Consider feature alignment review** — reconcile planned features (`stage_variance`, `completion_vs_realization`, `year`) vs. implemented features (`n_stages_active`) for methodology section accuracy
