# Pipeline Output Evaluation — Version 1
## Corruption Indication Detection in Village Fund Activities: Jambi Province 2023–2025

> **Evaluator**: GitHub Copilot (IS Researcher Agent)
> **Date**: April 16, 2026
> **Sources Evaluated**:
> - `src/output_v1/notebook_run/01_data_preprocessing.ipynb`
> - `src/output_v1/notebook_run/02_unsupervised_comparison.ipynb`
> - `src/output_v1/notebook_run/03_corruption_typology_analysis.ipynb`
> - `src/output_v1/ANALYSIS_REPORT_v1.md`
> - `src/output_v1/IN_DEPTH_ANALYSIS_v1.md`
> **Evaluated Against**:
> - `concept/conceptual/research_concept_phase1.md`
> - `docs/draft/01-introduction.md` through `07-references.md`

---

## Table of Contents

1. [Evaluation Summary](#1-evaluation-summary)
2. [Notebook 01 — Preprocessing and Feature Engineering](#2-notebook-01--preprocessing-and-feature-engineering)
3. [Notebook 02 — Unsupervised Comparison](#3-notebook-02--unsupervised-comparison)
4. [Notebook 03 — Typology Analysis](#4-notebook-03--typology-analysis)
5. [Draft Alignment: Chapter-by-Chapter Assessment](#5-draft-alignment-chapter-by-chapter-assessment)
6. [Cross-Cutting Issues](#6-cross-cutting-issues)
7. [Citation Integrity Audit](#7-citation-integrity-audit)
8. [Open Gaps Requiring Action](#8-open-gaps-requiring-action)
9. [Consolidated Verdict by Research Question](#9-consolidated-verdict-by-research-question)

---

## 1. Evaluation Summary

The v1 pipeline produces a **coherent, executable empirical foundation** that is broadly aligned with the research concept. The three notebooks together generate all quantitative outputs needed to populate Chapters 3–5 of the draft. However, the evaluation identifies **five categories of discrepancy** between concept and implementation that must be resolved before the paper is submitted:

| Category | Severity | Count | Description |
|---|---|---|---|
| Architecture deviation | Moderate | 1 | RDA network depth implemented differs from concept |
| Feature set mismatch | Moderate | 2 | `stage_variance` and `completion_vs_realization` absent from final model |
| Internal draft inconsistency | Moderate | 3 | Ch.3 describes features / normalisation / architecture differently from what the notebook actually did |
| Typology rule discrepancy | Low–Moderate | 2 | T3 and T4 rule logic differs between concept, notebook, and draft |
| Citation integrity | **Critical** | 2 | Reference [18] is unverifiable; Reference [28] duplicates [12] |

---

## 2. Notebook 01 — Preprocessing and Feature Engineering

### 2.1 What Was Implemented

| Step | Concept Plan | Implementation | Status |
|---|---|---|---|
| Data load and year concatenation | 6 CSV files (Penyerapan + Pagu × 3 years) | Correct — all 6 CSV files merged | ✓ Match |
| Merge key | `Kode_Desa` + `Tahun` | `many_to_one` merge applied correctly | ✓ Match |
| VIF screening | Threshold VIF > 5, drop violators | Implemented with iterative re-check | ✓ Match |
| Normalisation | RobustScaler (median + IQR) | Applied on final feature set | ✓ Match |
| Export | `features_engineered.csv` + `df_merged_raw.csv` | Both exported with metadata columns attached | ✓ Match |

### 2.2 Feature Engineering — Discrepancy Log

The research concept (Section 4.4 table) lists **three algorithmically distinct methods**: IF, LOF, RDA. Their shared input requires a clean feature matrix. The concept design described **10 candidate features**, while the ANALYSIS_REPORT confirms the actual model input uses **7 features**. The following mapping clarifies what happened:

| Concept Feature | Status in v1 Model | Explanation |
|---|---|---|
| `cost_per_unit` | ✓ Present | Core signal for mark-up detection |
| `absorption_ratio` | ✓ Present | Ghost activity signal |
| `avg_completion` | ✓ Present | Completion manipulation |
| `stage_variance` | **⚠ Absent from model** | Replaced by `n_stages_active`; kept as metadata only |
| `n_stages_active` | ✓ Present (metadata only) | Structural zero annotation; not in ML input matrix |
| `completion_vs_realization` | **⚠ Absent from model** | Dropped — likely failed VIF or was excluded post-review |
| `swakelola_high_value` | ✓ Present | Binary procurement flag |
| `activity_category` | ✓ Present | 2-digit Kode_Output prefix |
| `year` | **⚠ Absent from model** | Not listed in ANALYSIS_REPORT feature table |
| `cost_deviation_by_category` | ✓ Present | Year-stratified z-score within category |

**Assessment**: The two dropped continuous features (`stage_variance`, `completion_vs_realization`) were the ones most explicitly discussed in the concept as methodologically important. `stage_variance` was noted as having a known zero-inflation problem from single-stage activities (Notebook 01, Step 3 comment block). `completion_vs_realization` was the most complex engineered feature, requiring within-village min-max normalisation. If VIF dropped them, the VIF results table in the notebook output should be examined in the actual run logs. If they were dropped by researcher decision, that decision must be documented and justified in the manuscript.

**Required action**: Ch.3 Methodology currently lists **seven features** in its feature table and attributes the feature selection to modus operandi grounding — but that table does not include `stage_variance` or `completion_vs_realization`. The draft is therefore internally consistent with the *actual* v1 output, but it no longer reflects the original 10-feature concept design. The draft's justification for this reduction must be made explicit with a sentence explaining VIF-based elimination.

### 2.3 Normalisation Claim Discrepancy

The concept specifies **RobustScaler** as the normalisation method (justified in Section 4.4.5 of the concept). The ANALYSIS_REPORT confirms RobustScaler was applied. However, **Ch.3 §3.2 of the draft states** "All continuous features were standardised (zero mean, unit variance)" — this describes `StandardScaler`, not `RobustScaler`. RobustScaler produces zero *median* and unit *IQR*, not zero *mean* and unit *variance*. This is a factual error in the draft text that contradicts the actual implementation.

**Required action**: Correct Ch.3 §3.2 to read: *"All features were normalised using RobustScaler (median centering, IQR scaling) to preserve resistance to the outlier records the study intentionally targets."*

---

## 3. Notebook 02 — Unsupervised Comparison

### 3.1 What Was Implemented

| Component | Concept Plan | Implementation | Status |
|---|---|---|---|
| IQR baseline | Union flag on `cost_per_unit` and `absorption_ratio` | Applied correctly using Q1/Q3 ± 1.5×IQR | ✓ Match |
| IF contamination tuning | Bimodality coefficient sweep over 5 values | Sweep over [0.03, 0.05, 0.08, 0.10, 0.15] | ✓ Match |
| LOF k-neighbour tuning | Bimodality coefficient sweep | Sweep over [10, 15, 20, 30] | ✓ Match |
| RDA λ sweep | [1e-4, 1e-3, 1e-2] | Implemented with `train_rda()` | ✓ Match |
| Consensus threshold | ≥ 2 of 3 methods | Applied correctly | ✓ Match |
| Village persistence score | Multi-year flag aggregation → Tier 1/2/3 | Implemented | ✓ Match |
| Cohen's κ | Planned in concept evaluation metrics | `cohen_kappa_score` imported but **result not visible** in exported outputs or draft | **⚠ Gap** |
| KS test | Planned diagnostic | `ks_2samp` imported but **no output present** | **⚠ Gap** |

### 3.2 RDA Architecture Deviation

The research concept (Section 4.5.3) specifies the RDA architecture as:
```
[7 → 32 → 16 → 32 → 7]
```
This is the four-layer symmetric autoencoder with a single hidden bottleneck.

The actual notebook (`build_autoencoder()`) implements:
```
Input → Dense(64,ReLU) → Dense(32,ReLU) → Dense(16,ReLU) → Dense(8,ReLU) [bottleneck]
      → Dense(16,ReLU) → Dense(32,ReLU) → Dense(64,ReLU) → Dense(n_features, Linear)
```
This is an **eight-layer symmetric autoencoder** with a 4-step encoder and 4-step decoder, bottleneck at dimension 8.

Yet **Ch.3 §3.3 of the draft** describes the architecture as:
```
[7 → 32 → 16 → 32 → 7] with ReLU activations
```
— which matches the original concept but contradicts the notebook.

**Assessment**: The deeper architecture (64→32→16→8) is arguably better suited for a 99K-record dataset and is consistent with state-of-the-art autoencoder design for tabular data. The issue is not the architectural choice per se, but the **fact that the draft reports the wrong architecture**. This constitutes a reporting accuracy error.

**Required action**: Update Ch.3 §3.3 to describe the actual 8-layer architecture. The revised text should read: `[n → 64 → 32 → 16 → 8 → 16 → 32 → 64 → n]` with n = number of input features.

### 3.3 Empirical Results Produced

The following key results were generated and are confirmed consistent across ANALYSIS_REPORT_v1.md and the draft Ch.4:

| Metric | Value | Used in Draft |
|---|---|---|
| Total records | 99,692 | ✓ Ch.4 Table 1 |
| IQR flagged | 18,478 (18.5%) | ✓ Ch.4 Table 1 |
| IF flagged | 7,974 (8.0%) | ✓ Ch.4 Table 1 |
| LOF flagged | 4,985 (5.0%) | ✓ Ch.4 Table 1 |
| RDA flagged | 4,985 (5.0%) | ✓ Ch.4 Table 1 |
| Consensus (≥2) flagged | 3,107 (3.1%) | ✓ Ch.4 Table 1 |
| BC(IF) | 0.335 | ✓ Ch.4 Table 2 |
| BC(RDA) | 0.703 | ✓ Ch.4 Table 2 |
| BC(LOF) | 0.957 | ✓ Ch.4 Table 2 |
| IF ∩ LOF overlap | 317 (6.4%) | ✓ Ch.4 Table 3 |
| IF ∩ RDA overlap | 2,506 (50.3%) | ✓ Ch.4 Table 3 |
| LOF ∩ RDA overlap | 596 (12.0%) | ✓ Ch.4 Table 3 |
| Triple consensus | 156 (1.6%) | ✓ Ch.4 §4.3 |
| Tier-1 villages | 642 (47.1%) | ✓ Ch.4 §4.6 |
| PCA variance (PC1+PC2) | 26.0% + 12.7% = 38.7% | ✓ Ch.4 §4.7 |

**Assessment**: The quantitative outputs are internally consistent and fully carried over into the draft. No numerical discrepancy was found between the ANALYSIS_REPORT, IN_DEPTH_ANALYSIS, and the draft chapters.

---

## 4. Notebook 03 — Typology Analysis

### 4.1 What Was Implemented

| Component | Concept Plan | Implementation | Status |
|---|---|---|---|
| Typology rule mapping (T1–T7) | 7 modus operandi from judicial records | Rule-based `assign_typologies()` function | ✓ Implemented |
| Multi-label assignment | One record can have ≥2 typologies | `typologies` column is a list | ✓ Match |
| PCA visualisation | 2-D projection of normal vs. flagged | Implemented with `StandardScaler` for PCA (correct) | ✓ Match |
| t-SNE visualisation | Sampled 15,000 records | Implemented with `perplexity=30, n_iter=1000` | ✓ Match |
| RDA per-feature error decomposition | Variable-level diagnosis for APIP | Implemented as heatmap + mean error per feature | ✓ Match |
| Expert validation export (top-50 per method) | Binary rubric template | 4 CSV files exported | ✓ Match |
| Village persistence deep-dive | Tier-1 narrative | Implemented in `village_persistence.csv` | ✓ Match |

### 4.2 Typology Rule Inconsistencies

Three typology rules show definitional divergence between the concept, the notebook code, and the draft methodology table:

**T3 — Volume Padding:**
| Source | Definition |
|---|---|
| Draft Ch.3 Table | `n_stages_active = 1 AND cost_per_unit within normal range` |
| Notebook Cell 5 | `(total_realization / Pagu) > 0.98` — i.e., near-100% budget absorption |
| Research Concept | `total_realization >> pagu, absorption_ratio > 1` |

The notebook implements T3 as a **near-100% absorption rule** (≥98%), while the draft defines it as **single-stage activity with normal unit cost**. These are two fundamentally different fraud mechanisms with different detection implications. The actual typology counts reported in Ch.4 Table 4 (T3 = 38 records) are based on the notebook's absorption-ratio rule.

**T4 — Stage Lock:**
| Source | Definition |
|---|---|
| Draft Ch.3 Table | `n_stages_active = 0` (budget allocated, zero disbursement) |
| Notebook Cell 5 | `stage_variance < 1e-6` (all spend in one stage — zero variance) |
| Research Concept | `n_stages_active = 0 OR 1`, `stage_variance ≈ 0` |

The notebook flags T4 when `stage_variance < 1e-6` — this actually identifies **single-stage concentration** (all funds disbursed in one tranche), not **zero disbursement**. Zero disbursement would require `n_stages_active = 0` and `total_realization = 0`. The result T4 = 0 in the output is therefore likely a VIF artefact: `stage_variance` was dropped from the model input, meaning it either no longer exists in `flagged[]` columns or equals zero for most records after scaling. This zero-detection outcome for T4 should be investigated and explained.

**T5 — Procurement Irregularity:**
| Source | Definition |
|---|---|
| Draft Ch.3 Table | `swakelola_high_value = 1 AND cost_per_unit > 5σ` |
| Notebook Cell 5 | `Cara_Pengadaan in ("Pihak ke-3", "Kontrak") AND cost_per_unit > 75th pct` |

This is a **conceptual reversal**: the draft flags high-value Swakelola (self-managed) activities, while the notebook flags third-party contract activities. Given that 98.8% of activities are Swakelola, the notebook's rule would virtually never fire on the dominant fraud channel. The 26 T5 records in Ch.4 Table 4 come from the notebook's Pihak ke-3/Kontrak rule — they are not the Swakelola-based detections the draft describes.

**Required action**: Reconcile T3, T4, and T5 definitions. Either revise the notebook rules to match the draft descriptions (and re-run to obtain updated counts), or revise the draft table to describe what the notebook actually implements. In either case, the Ch.4 typology counts must reflect whichever definition is adopted.

### 4.3 PCA Scaler Choice (Note)

Notebook 03 correctly uses `StandardScaler` for PCA visualisation (not RobustScaler), with the comment: *"do NOT use RobustScaler here to preserve visualisation scale."* This is methodologically sound — PCA projection for visualisation conventionally uses mean/std centring. This change from RobustScaler does not affect the model outputs, only the visualisation. No action required, but worth noting as deliberate.

---

## 5. Draft Alignment: Chapter-by-Chapter Assessment

### Chapter 1 — Introduction
**Alignment**: Strong. All factual claims (Rp 71 trillion, 591 court verdicts, 851 KPK cases, 11 Jambi complaints, Rp 2.301 billion from 4 cases) are grounded in cited sources and consistent with the research concept. The four-case prosecution table is accurate and the detection lag argument is well-supported.

**One issue**: The introduction refers to feature `stage_variance` indirectly through *"irregular multi-stage disbursement patterns"* as a target of one of the engineered features. Since `stage_variance` is absent from the v1 model, this claim slightly overstates the current pipeline's detection scope. Not material at introductory level, but should be harmonised with Ch.3.

### Chapter 2 — Related Work
**Alignment**: Strong. Literature review covers Fraud Triangle, Principal-Agent Theory, anomaly detection survey (Chandola et al. [24]), and Indonesian-specific dana desa fraud typology studies [13, 14, 15].

**Critical issue**: §2.3 cites **Li et al. [18]** three times ("Li et al. [18] apply LOF to USA federal expenditure data... Li et al. [18] confirm LOF's robustness advantage..."). Reference [18] has been flagged in Ch.7 as **unverifiable** ("paper not confirmed in Scopus, CrossRef, or Google Scholar databases"). All three claims attributed to [18] in Ch.2 must be re-attributed or replaced. The core LOF behaviour being described can be cited using Breunig et al. [25] (the original LOF paper) supplemented by Chandola et al. [24].

### Chapter 3 — Methodology
**Alignment**: Partially aligned. Three specific errors require correction:

1. **Normalisation description**: States "standardised (zero mean, unit variance)" — should be RobustScaler.
2. **RDA architecture**: States `[7 → 32 → 16 → 32 → 7]` — actual implementation is `[n → 64 → 32 → 16 → 8 → 16 → 32 → 64 → n]`.
3. **Typology rules T3, T4, T5**: Definitions in the methodology table do not match the notebook's rule implementation (see §4.2 above).

Additionally, the feature table in §3.2 lists 7 features but does not acknowledge the elimination of `stage_variance` and `completion_vs_realization` from the original 10-feature concept design. A brief methodological note explaining VIF-based reduction is needed.

### Chapter 4 — Results
**Alignment**: Excellent. All quantitative results — anomaly rates, bimodality coefficients, overlap tables, typology counts, village tiers, PCA variance — are internally consistent with ANALYSIS_REPORT_v1.md. Figure references are correctly linked to output chart files.

**One gap**: The PCA and t-SNE projections are described in §4.7 but the t-SNE sampling procedure (15,000 records stratified: 14,538 normal + 462 anomalous) is documented in the notebook but not mentioned in the draft. The sampling strategy affects interpretability of the t-SNE visualisation and should be noted in the methods or figure caption.

**Missing metric**: Cohen's κ between-method pairwise agreement was planned as an evaluation metric (visible in Notebook 02's import block), but no Cohen's κ values appear in the draft or in ANALYSIS_REPORT_v1.md. This metric was explicitly listed in the research concept as part of the comparative evaluation protocol and should either be computed and added, or explicitly acknowledged as deferred.

### Chapter 5 — Discussion
**Alignment**: Strong. The theoretical interpretation — LOF superiority through Fraud Triangle, principal-agent, and DeLone & McLean lenses — is coherent and grounded in the empirical outputs. The subthreshold masking problem (§5.4) is correctly identified and thoughtfully discussed.

**Minor issue**: §5.2 states "24.7% of all activities" qualify as `swakelola_high_value`. This figure is confirmed by ANALYSIS_REPORT_v1.md §2.3. However, the discussion notes "96.4% of 3,107 consensus flags" are Swakelola activities. This specific figure (96.4%) does not appear in the ANALYSIS_REPORT. Its source should be verified against the actual `anomaly_flags.csv` data before final submission.

### Chapter 6 — Conclusion
**Alignment**: Strong. All three research questions are answered directly and the limitations are honestly stated. The 93.5% search space reduction claim (from 99,692 records to 642 priority villages) is internally consistent — though the metric compares heterogeneous units (individual records vs. aggregated villages) and this should be noted as a summary heuristic rather than a precision measurement.

### Chapter 7 — References
**Alignment**: Actionable items already flagged inline in the reference list:
- **[18]**: Removed from the reference list but *still cited in Ch.2 and Ch.5 text*. All in-text citations to [18] must be updated.
- **[28]**: Confirmed duplicate of [12]. Consolidation required throughout article.
- **[29]**: Journal venue correction (Heliyon → Economies) noted; DOI requires verification.

---

## 6. Cross-Cutting Issues

### 6.1 `n_stages_active` Usage Ambiguity

`n_stages_active` appears as both a metadata column and a conceptually important corruption signal throughout the documents, but its classification is inconsistent:

- ANALYSIS_REPORT §2.1: Listed as a feature with notation "**Implementation note**: `stage_variance` and `completion_vs_realization` replaced by `n_stages_active`."
- Notebook 01 code: `n_stages_active` is computed but explicitly kept *outside* the FINAL_FEATURES list — it feeds only the metadata export, not the ML input matrix.
- Draft Ch.3: Does not list `n_stages_active` as a model feature, but does use it as a typology signal (T4: `n_stages_active = 0`).

This creates a logical inconsistency: T4 is defined in terms of a feature (`n_stages_active`) that is not part of the model input matrix, meaning T4 detections are a post-hoc rule applied to metadata rather than a direct product of the ML anomaly scoring.

**Required action**: Clarify whether `n_stages_active` should have been included in the ML model input. If it was intentionally excluded (to avoid penalising legitimate single-tranche activities), that decision should be stated explicitly. If it was inadvertently excluded, the v1 model should be noted as a limitation.

### 6.2 T4 Zero Detections — Structural or Methodological?

T4 (Stage Lock) = 0 detections in the consensus-flagged set. The draft Ch.4 §4.4 acknowledges this with: *"Stage Lock (T4) records zero detections, consistent with the finding that fully locked activities tend not to generate feature extremes that reach consensus threshold."* The IN_DEPTH_ANALYSIS provides no additional explanation.

However, given the T4 rule uses `stage_variance < 1e-6` — and `stage_variance` is absent from the model input (it cannot drive anomaly flags) — the zero T4 result may simply be **a direct consequence of `stage_variance` not being an input feature**, rather than a genuine absence of stage-lock patterns in the data. If `n_stages_active = 0` had been used as the T4 signal, results might differ. This requires clarification, as the current explanation in Ch.4 is potentially misleading.

### 6.3 Expert Validation CSV Files — Not Yet Integrated

Four expert validation CSVs were exported as outputs:
- `expert_validation_top50_CONSENSUS.csv`
- `expert_validation_top50_IF.csv`
- `expert_validation_top50_LOF.csv`
- `expert_validation_top50_RDA.csv`

These are *templates* for domain expert review using a binary rubric — they have not yet been completed. No chapter in the current draft references completed expert validation results, and the conclusion honestly states limitation: *"absence of expert validation against ground-truth fraud labels."* This is an acknowledged gap for Phase 2. **No action required for v1 submission**, but expert validation is the most material limitation for journal reviewers.

### 6.4 IQR Baseline Applied on Scaled Features

Notebook 02 Cell 5 applies the IQR baseline on the **scaled** versions of `cost_per_unit` and `absorption_ratio` (from `features_engineered.csv`). The comment acknowledges this: *"In features_engineered.csv the SCALED version is in FEATURE_COLS — We compute IQR on the same scaled column — rank-ordering is preserved."* While rank-ordering is preserved after RobustScaler transformation, the IQR fence interpretation changes (Q3+1.5×IQR in RobustScaler space ≠ Q3+1.5×IQR in raw Rp space). This is adequate for comparative purposes but should be acknowledged as a methodological note in Ch.3.

---

## 7. Citation Integrity Audit

| Ref | Status | Issue | Required Action |
|---|---|---|---|
| [18] | **CRITICAL — Removed** | Li et al. (2025) unverifiable in Scopus/CrossRef/Google Scholar. Cited in Ch.2 §2.3 ×3 and Ch.5 §5.1 ×2 | Remove all 5 in-text citations; re-attribute LOF government verification claims to [25] (Breunig et al.) and [24] (Chandola et al.) |
| [28] | **Moderate — Duplicate** | Same paper as [12] (Srirejeki & Faturokhman 2020). Referenced separately 4 times in the draft. | Consolidate to [12]; renumber [29], [30], [31], [32], [33], [34] accordingly |
| [29] | **Low — Venue correction** | Listed as Heliyon in concept; confirmed as Economies (MDPI) in references file | Verify DOI 10.3390/economies7040111 is correct paper |
| [9] | **Minor — Attribution confusion** | In Ch.2, reference [9] is used for both Søreide (2002) and for "Sutarna and Subandi." The reference list maps [9] only to Søreide. "Sutarna and Subandi" have no explicit reference number assigned. | Add Sutarna and Subandi reference with a new number; separate in-text citations |

---

## 8. Open Gaps Requiring Action

The following items represent **work in the pipeline that was planned but not yet completed or visible in outputs**:

| # | Gap | Location | Priority |
|---|---|---|---|
| G1 | Cohen's κ inter-rater agreement not computed / not reported | Planned §8.5 of concept; `cohen_kappa_score` imported in NB02 but output absent | High — core evaluation metric |
| G2 | KS test (distribution shift across years) not computed | `ks_2samp` imported in NB02 but no result visible | Medium — supports year consistency claim |
| G3 | Kabupaten-level geographic breakdown in ANALYSIS_REPORT §8, but not present in draft Ch.4 | Tier-1 village geographic concentration by kabupaten | Medium — strengthens Jambi site justification |
| G4 | t-SNE sampling strategy (15K records, stratified) not documented in draft | NB03 Cell 9 comment | Low — methodological transparency |
| G5 | RDA convergence curve (training/validation loss history) not visualised or reported | NB02 `rda_history` variable | Low — model validation evidence |
| G6 | Explanation for IQR baseline computed on scaled (not raw) features | NB02 Cell 5 comment | Low — methodological note needed |
| G7 | VIF result table from actual run not included in any output file | NB01 Cell 11 console output | Low — reproducibility record |

---

## 9. Consolidated Verdict by Research Question

### RQ1 — Feature Discriminating Power
**Verdict: Strongly supported by v1 outputs.**
The feature engineering pipeline correctly operationalises documented corruption modus operandi from judicial records. `avg_completion` as the dominant RDA reconstruction error driver (MSE ≈ 0.00145) and `cost_per_unit` max at 102.83σ confirm that the engineered features capture detectable financial signals. The absence of `stage_variance` from the final model represents a minor gap — single-stage disbursement detection is partially addressed through `n_stages_active` as a post-hoc typology signal, but not as a model-level anomaly driver.

### RQ2 — Algorithm Performance
**Verdict: Well-supported, with one reporting error to correct.**
LOF's BC superiority (0.957 vs. 0.703 for RDA vs. 0.335 for IF) is clearly demonstrated and theoretically explained. The consensus framework is correctly implemented. The key correction required is the RDA architecture description in Ch.3, which currently reports the wrong network topology.

### RQ3 — Typology Mapping
**Verdict: Partially supported, with definitional reconciliation needed.**
T1 (Mark-up) and T7 (Cross-Category Dump) co-dominance at ~50% each is empirically robust. T2 (Ghost Activity) at 24.9% is well-detected. However, T3, T4, and T5 definitions are inconsistent across the notebook code and the draft methodology table. The zero T4 result is potentially a methodological artefact rather than a validated finding. These three typologies require rule reconciliation and counts re-verification before submission.

---

## Revision Priority List

| Priority | Item | Chapter Affected |
|---|---|---|
| **P1 — Critical** | Remove all citations to [18] and re-attribute | Ch.2 (×3), Ch.5 (×2) |
| **P1 — Critical** | Reconcile T3, T4, T5 typology rule definitions | Ch.3 §3.4, Ch.4 §4.4 |
| **P2 — High** | Correct RDA architecture description | Ch.3 §3.3 |
| **P2 — High** | Correct normalisation description (RobustScaler, not StandardScaler) | Ch.3 §3.2 |
| **P2 — High** | Compute and report Cohen's κ | Ch.4 §4.3 (new table) |
| **P3 — Medium** | Consolidate [28] → [12]; renumber subsequent references | Ch.7; all chapters |
| **P3 — Medium** | Acknowledge `stage_variance` / `completion_vs_realization` removal with VIF rationale | Ch.3 §3.2 |
| **P3 — Medium** | Clarify `n_stages_active` as metadata-only (not model input) | Ch.3 §3.2, Ch.3 §3.4 |
| **P3 — Medium** | Verify Alfada [29] DOI and journal venue | Ch.7 |
| **P4 — Low** | Add Sutarna and Subandi as distinct numbered reference | Ch.2, Ch.5, Ch.7 |
| **P4 — Low** | Document t-SNE sampling strategy in figure caption | Ch.4 §4.7 |
| **P4 — Low** | Add note on IQR computed on scaled features | Ch.3 §3.4 |
| **P4 — Low** | Add kabupaten-level geographic breakdown table | Ch.4 §4.6 or supplementary |

---

*Evaluation complete. All findings are based on cross-referencing the three notebook scripts, the two analysis reports, the seven draft chapters, and the research concept document. No external sources or assumptions were introduced.*
