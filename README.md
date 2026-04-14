# Corruption Indication Detection in Village Fund Activities Using Comparative Unsupervised Learning Methods

> **Domain**: Information Systems / Applied Machine Learning  
> **Data Scope**: Jambi Province, Indonesia — Village Fund Expenditure Absorption 2023–2025  
> **Last Updated**: April 2026

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

### Phase 2 — Data Acquisition & Preprocessing ⏳ IN PROGRESS

- [x] Raw data sourced: 6 Excel files (Pagu + Penyerapan, Jambi Province, 2023–2025)
- [x] CSV conversion completed for all 6 files → `data_ref/csv/`
- [x] Schema validated: Penyerapan columns confirmed (19 fields including Real_T1–T3, Pct_T1–T3, Cara_Pengadaan)
- [x] Dataset scale confirmed: ~33,405 activity records across Penyerapan 2023–2025
- [ ] Data merge: Penyerapan joined with Pagu by `Kode_Desa` + `Tahun`
- [ ] Data cleaning: handle nulls, remove header/footer rows, validate numeric ranges
- [ ] Feature engineering: compute all 10 features from engineering plan

**Data files**:

| File | Status | Location |
|---|---|---|
| `Pagu_Jambi_2023.csv` | ✅ Ready | `data_ref/csv/` |
| `Pagu_Jambi_2024.csv` | ✅ Ready | `data_ref/csv/` |
| `Pagu_Jambi_2025.csv` | ✅ Ready | `data_ref/csv/` |
| `Penyerapan_Jambi_2023.csv` | ✅ Ready | `data_ref/csv/` |
| `Penyerapan_Jambi_2024.csv` | ✅ Ready | `data_ref/csv/` |
| `Penyerapan_Jambi_2025.csv` | ✅ Ready | `data_ref/csv/` |

---

### Phase 3 — Model Development ❌ NOT STARTED

- [ ] Notebook `01_data_preprocessing.ipynb`: merge, clean, engineer features, export `features_engineered.csv`
- [ ] Notebook `02_unsupervised_comparison.ipynb`: train/apply Isolation Forest, LOF, Dense Autoencoder
- [ ] Compute evaluation metrics: anomaly rate consistency, inter-method agreement (Cohen's κ), PCA/t-SNE visualisation
- [ ] Notebook `03_corruption_typology_analysis.ipynb`: map anomaly flags to 7 modus operandi

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
│   ├── csv/                           ← Converted CSV files (ready for analysis)
│   │   ├── Pagu_Jambi_2023.csv
│   │   ├── Pagu_Jambi_2024.csv
│   │   ├── Pagu_Jambi_2025.csv
│   │   ├── Penyerapan_Jambi_2023.csv
│   │   ├── Penyerapan_Jambi_2024.csv
│   │   └── Penyerapan_Jambi_2025.csv
│   └── (source Excel files)
├── docs/
│   ├── draft/                         ← Paper draft chapters (pending)
│   ├── latex/                         ← LaTeX source (pending)
│   └── references/                    ← Reference management files (pending)
└── src/
    └── convert_xlsx_to_csv.py         ← Data conversion utility
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

1. **Build `01_data_preprocessing.ipynb`** — merge Pagu + Penyerapan, clean, engineer 10 features, export `features_engineered.csv`
2. **Build `02_unsupervised_comparison.ipynb`** — train Isolation Forest, LOF, Dense Autoencoder; compute evaluation metrics
3. **Build `03_corruption_typology_analysis.ipynb`** — map flags to modus operandi; generate summary tables and visualisations
4. **Begin paper draft** — start with Abstract and Introduction using `docs/draft/`
