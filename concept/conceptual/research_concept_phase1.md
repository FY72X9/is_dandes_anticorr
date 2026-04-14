# Research Concept — Phase 1
## Corruption Indication Detection in Village Fund Activities Using Comparative Unsupervised Learning Methods

> **Status**: Phase 1 COMPLETE · Phase 2 REVISED — Scientific Gaps Resolved · Methodology Strengthened  
> **Domain**: Information Systems / Applied Machine Learning  
> **Data Scope**: Jambi Province, Indonesia — Village Fund Expenditure Absorption 2023–2025  
> **Last Updated**: April 2026

---

## 1. Background & Research Motivation

Indonesia channels approximately Rp 71 trillion annually through its Dana Desa (Village Fund) programme to 75,259 villages across the archipelago [1]. Since the programme's inception under Law No. 6 of 2014, the scale of documented corruption has grown at an alarming rate. By 2024, Indonesian Corruption Watch (ICW) catalogued 591 court verdicts involving village fund misappropriation, implicating 640 defendants and inflicting Rp 598.13 billion in documented state losses [2]. The Komisi Pemberantasan Korupsi (KPK) further identified 851 village fund corruption cases from 2015 onward, in which village heads accounted for over 60% of perpetrators [3].

Despite the volume and scale of this fraud, the dominant response has remained reactive — legal prosecution after the act — rather than proactive detection grounded in data. The government's financial reporting infrastructure, particularly the Sistem Keuangan Desa (Siskeudes/SIMDA Desa) maintained by BPKP, generates granular expenditure absorption records at the activity level: what type of activity, how much was budgeted, how much was realised per disbursement stage, and how procurement was conducted. Machine learning studies on Indonesian public financial data have yet to apply this granular, activity-level structure to anomaly detection [13, 14] — existing work either addresses aggregate national procurement indicators [14] or supervises classification on categorical village fund outputs [13], leaving systematic screening of Siskeudes activity records unaddressed in the fraud detection literature [12, 16].

Existing research on village fund corruption concentrates on legal-forensic analysis [4], governance accountability frameworks [5], or fraud triangle diagnostics [6]. Where machine learning enters the picture, it predominantly applies supervised classification — an approach that presupposes labelled ground truth, a luxury unavailable in real-time monitoring contexts. The present research addresses this gap directly: it proposes an unsupervised learning pipeline to detect expenditure anomalies from Jambi provincial data, interpretable through established corruption modus operandi derived from judicial and institutional records [7, 8].

**The selection of Jambi Province as the research site reflects a structural accountability condition that participatory oversight data renders quantifiable.** The jaga.id platform — Indonesia's civil-society monitoring portal for village fund transparency — recorded only 11 complaint submissions attributed to Jambi Province, constituting 1.4% of the 761 national reports logged on the platform (jaga.id, accessed April 2026 [27]), while provinces of comparable size such as Sumatera Utara (81) and Sumatera Selatan (48) registered substantially higher reporting volumes. Low voluntary reporting, however, does not signal low fraud exposure; it signals a low-monitoring environment. Hidajat [6] demonstrates that structural features endemic to village-level governance — geographic remoteness, single-authoriser financial control, and constrained sub-district auditor capacity — simultaneously amplify the Opportunity dimension of the Fraud Triangle, making detection contingent on proactive institutional mechanisms rather than reactive community reporting. When bottom-up transparency channels remain inactive, the information asymmetry at the core of the principal-agent relationship [9] operates unchecked: village heads face no accountability pressure between formal audit cycles. Alfada [29], through panel GMM estimation across 19 Indonesian provinces, confirms empirically that regions combining high intergovernmental transfer dependence with weak accountability structures exhibit systematically elevated corruption incidence — the structural profile directly applicable to Jambi's decentralised village fund governance. Srirejeki and Faturokhman [28] further document that kabupaten-level inspectorates lack the operational staffing to screen thousands of individual village activity records across each disbursement cycle, producing a measurable gap between the APIP mandate under Government Regulation No. 60/2008 and actual inspection coverage. An automated anomaly detection system processing SIMDA Desa absorption records closes this coverage gap by converting an existing government data infrastructure into a ranked inspection input for Aparat Pengawas Internal Pemerintah (APIP) — operationalising the information-quality-to-organisational-impact pathway that DeLone and McLean [10] identify as the criterion for IS system success in institutional contexts.

Contemporaneous prosecution records from Jambi Province furnish direct empirical grounding for this analytical framing. Four cases adjudicated or actively prosecuted between 2024 and 2026 collectively document Rp 2.301 billion in verified state losses attributable to village fund misappropriation across multiple kabupaten [30, 31, 32, 33]:

| Village (Kabupaten) | TA of Irregularity | Modus Operandi | State Loss | Status (2025–2026) |
|---|---|---|---|---|
| Desa Muara Hemat (Kerinci) | 2020–2021 | Fictitious physical construction reports | Rp 942 juta | Tahap II prosecution (Feb 2026) [30] |
| Desa Jambi Tulo (Muaro Jambi) | 2024 | Fictitious road and seedling procurement — zero field output | > Rp 300 juta | Village fund disbursement frozen by Inspektorat [31] |
| Desa Batang Merangin (Kerinci) | 2021 | Unfinished and fictitious meeting hall construction; collusion includes a village facilitator | Rp 644 juta | Three suspects named; village facilitator added Nov 2025 [32] |
| Desa Pangkal Duri (Tanjung Jabung Timur) | 2022 | Misappropriation of Dana Desa and Dana Silpa | Rp 415 juta | Suspect arrested Aug 2024 [33] |

Three analytical observations emerge from this case profile. First, the fiscal years under investigation span TA 2020 through TA 2024, yet prosecution or administrative suspension occurred no earlier than mid-2024 — establishing a detection lag ranging from approximately two to five years. This interval represents precisely the period during which contemporaneous anomaly detection, applied to Siskeudes activity records, could have surfaced irregularities for APIP review before state losses compounded across subsequent disbursement stages. Second, the modus operandi documented across these four cases — fictitious physical outputs (Muara Hemat, Batang Merangin), zero-output procurement (Jambi Tulo), and illicit carryover diversion (Pangkal Duri) — correspond directly to the engineered features in this study: `avg_completion` and `absorption_ratio` are designed to detect the completion-reporting gaps that enable fictitious project claims, while `stage_variance` surfaces the irregular multi-stage disbursement patterns characteristic of misappropriated fund flows, and `swakelola_high_value` flags the high-value self-managed procurement used in the Jambi Tulo case. Third, involvement of a village facilitator (pendamping desa) in the Batang Merangin case signals intra-network collusion, reducing the likelihood that purely community-based reporting channels would surface the irregularity — precisely the condition under which algorithmic detection from financial records serves as the more reliable primary screen. That all four cases reached prosecution through Inspektorat field verification or Kejaksaan investigation — case-level mechanisms — rather than through any systematic population-level screening of Siskeudes records underscores the monitoring gap that the present research directly addresses.

---

## 2. Problem Statement

Village fund expenditure absorption data contains latent signals of financial irregularities. Activities with inflated unit costs, inconsistent multi-stage realisations, or procurement method mismatches relative to their scale and category constitute detectable deviations from normal spending behaviour. However, no systematic, data-driven screening mechanism currently operates at the district or provincial level to surface these anomalies in near-real-time.

The core problem is thus: **given unlabelled activity-level expenditure data reported by villages, can unsupervised learning methods reliably surface expenditure patterns that correspond to known corruption modus operandi?** And if so, which algorithmic approach — Isolation Forest, Local Outlier Factor (LOF), or Robust Deep Autoencoder (RDA) — provides the sharpest discrimination between suspicious and baseline activity profiles?

---

## 3. Research Questions

1. What feature constructs derived from village fund absorption data serve as the most discriminating signals of expenditure anomaly, based on documented corruption modus operandi in Indonesia?
2. Which among Isolation Forest, Local Outlier Factor (LOF), and Robust Deep Autoencoder (RDA) demonstrates superior anomaly identification performance — measured by anomaly score distribution, inter-method agreement, reconstruction error analysis, IQR-baseline comparison, and domain-expert precision — on Jambi province village fund data across 2023–2025?
3. How do the algorithmically identified anomalous activities map to established corruption typologies (mark-up, fictitious projects, double budgeting, procurement irregularities) documented in judicial verdicts and institutional audit reports?

---

## 4. Theoretical Framework

### 4.1 Fraud Triangle Theory
The Fraud Triangle (Cressey, 1953) posits three conditions that converge to produce fraudulent behaviour: **Pressure** (financial or situational motives), **Opportunity** (weak controls and oversight), and **Rationalisation** (cognitive justification). In the village fund context, Hidajat [6] demonstrates that the programme's structural features — remote locations, limited auditor capacity, single-authoriser financial control — simultaneously amplify all three dimensions. This research operationalises the Fraud Triangle as a **labelling framework**: anomalies detected by ML algorithms are subsequently interpreted through the pressure-opportunity-rationalisation lens to assess corruption likelihood.

### 4.2 Principal-Agent Theory
Sutarna and Subandi [9] apply principal-agent theory to village fund corruption, identifying the village head as an agent with information asymmetry relative to the principal (district government, KPK, BPKP). The agent exploits this asymmetry through activity misreporting, fictitious outputs, and budget manipulation. This research treats **unexplained deviation from expected spending patterns** as a proximate signal of information asymmetry exploitation — the precise condition the agent exploits in the principal-agent model.

### 4.3 Anomaly Detection as an IS Problem
From an Information Systems perspective, this research situates itself within the broader discourse on decision-support systems for public financial management. The DeLone and McLean IS Success Model [10] undergirds the practical contribution: a system whose **information quality** (accurate anomaly signals) drives **individual impact** (auditor attention) and **organisational impact** (corruption deterrence) represents IS success in the anti-corruption domain. Unsupervised learning provides the algorithmic engine; IS theory provides the justification for why deploying such a system constitutes an organisationally meaningful intervention.

### 4.4 Unsupervised Anomaly Detection Methods — Adopted Framework

Based on a systematic assessment of the anomaly detection literature published between 2023 and 2026, this research adopts three methodologically distinct unsupervised algorithms that together span the current performance frontier for tabular government financial data (detailed scientific rationale follows in Section 4.5):

| Method | Paradigm | Primary Advantage for this Study |
|---|---|---|
| **Isolation Forest (IF)** | Ensemble / Path-length partitioning | Confirmed Tier-1 standard for government expenditure anomaly detection [18]; computationally efficient on 33K+ records; no distributional assumptions |
| **Local Outlier Factor (LOF)** | Local density estimation | Adapts to heterogeneous activity-category densities without a global parameter; directly validated on government spending audit data [18, 20, 25] |
| **Robust Deep Autoencoder (RDA)** | Neural network reconstruction + sparse noise decomposition | Detects non-linear compound anomaly patterns while its joint sparse-noise training objective prevents contamination by anomalous training records [34, 19]; per-feature reconstruction error provides auditor-interpretable variable-level diagnosis [20] |

This triad spans three distinct algorithmic paradigms — ensemble tree partitioning, local density deviation, and deep sparse reconstruction — providing the multi-paradigm comparison that Alam et al. [24] identify as methodological best practice for unsupervised anomaly detection benchmarking at scale.

### 4.5 Scientific Rationale for the Adopted Method Selection

This section provides the scientific argument for each chosen method and documents why two earlier candidates — DBSCAN and K-Means + Mahalanobis Distance — were replaced with LOF and Dense Autoencoder, respectively.

#### 4.5.1 Isolation Forest — Retained as Tier-1 Primary Method

Isolation Forest (Liu et al., 2008) constructs an ensemble of random trees that recursively partition the feature space. Points requiring fewer partitions to isolate receive high anomaly scores — a mechanism that exploits the key statistical property of anomalies: they are simultaneously *rare* and *different*. Three properties confirm its suitability as the primary method:

1. **No distributional assumption**: Village fund expenditure data violates normality — `cost_per_unit` distributions are right-skewed, `stage_variance` is zero-inflated, and `Cara_Pengadaan` is categorical. Isolation Forest makes no distributional assumptions, circumventing these challenges that invalidate parametric distance methods.

2. **Confirmed for government spending**: Li et al. [18] deploy Isolation Forest as the primary baseline in their 2025 audit analytics study of USA federal spending irregularities — the most structurally comparable domain to the present research. Alam et al.'s [24] systematic review of unsupervised anomaly detection benchmarks and Li et al.'s [18] direct government audit application both retain Isolation Forest as a primary benchmark in 2025 — a status reflecting its consistently competitive performance on tabular government financial data across the reviewed literature.

3. **Computational scalability**: Kumar et al. [19] confirm that with `n_estimators ≥ 100`, Isolation Forest maintains stable anomaly scores on datasets exceeding 30,000 records — matching the scale of the Jambi province Penyerapan data (33,405 activity records).

#### 4.5.2 Local Outlier Factor — Adopted to Replace DBSCAN

DBSCAN was the preliminary density-based candidate, but the literature published after 2023 consistently identifies a critical structural limitation: DBSCAN requires a single global ε (epsilon) parameter, which fails when activity categories exhibit radically different density profiles within the same dataset. In village fund absorption data, infrastructure projects, honoraria payments, and operational expenses coexist with value ranges spanning three orders of magnitude — conditions under which a single ε either misclassifies low-density categories wholesale as noise or overlooks anomalies embedded in high-density regions.

LOF (Breunig et al., 2000 [25]) eliminates this problem by computing *local* reachability density relative to each point's k-nearest neighbourhood, then comparing that density to its neighbours' own densities. The LOF score expresses genuine local deviation, independently of global data distribution. Three empirical properties justify this substitution:

1. **Direct government spending validation**: Li et al. [18] apply LOF to USA federal expenditure data alongside Isolation Forest in 2025, finding that LOF identifies a distinct subset of anomalies — particularly those embedded in high-frequency activity categories — that Isolation Forest's global path-length metric structurally misses due to its insensitivity to local density variation.

2. **Robustness to heterogeneous feature scales**: Unlike DBSCAN's ε and min_samples pair (both sensitive to global density), LOF's sole tuning parameter is k (number of neighbours), which is substantially more stable across heterogeneous tabular datasets [20]. De Meulemeester et al. [20] confirm LOF's robustness advantage over DBSCAN specifically on government institutional financial data with feature distributions comparable to village fund absorption records.

3. **Continuous scoring enables audit prioritisation**: LOF produces a continuous score (values near 1.0 indicate normality; values significantly above 1.5 indicate anomaly), enabling a rank-ordered anomaly list directly actionable for inspection triage — more operationally useful than DBSCAN's binary noise label, which provides no severity gradient.

#### 4.5.3 Robust Deep Autoencoder — Adopted to Replace K-Means + Mahalanobis Distance

K-Means + Mahalanobis Distance was the preliminary cluster-based candidate, valued for its interpretability. However, the Mahalanobis distance is a fundamentally linear measure: it captures deviation from a cluster centroid within the space described by the feature covariance matrix. It cannot detect anomalies that emerge from non-linear interactions across features — precisely the compound patterns that characterise village fund corruption, where simultaneous irregularity across `cost_per_unit`, `avg_completion`, `stage_variance`, and `swakelola_high_value` constitutes stronger evidence of manipulation than any single variable extreme.

A Robust Deep Autoencoder (RDA) [34] extends the standard autoencoder by jointly decomposing the input matrix **X** into two components during training: a low-rank normal component reconstructed by the neural network, and a sparse noise matrix **S** that absorbs anomalous feature combinations. The joint optimisation objective is:

`Loss = MSE(AE(X − S), (X − S)) + λ‖S‖₁`

The L1 penalty forces anomalous records — which the network cannot reconstruct faithfully — into the sparse matrix S rather than distorting the learned latent representation. This property makes RDA architecturally resistant to training set contamination: even with ~10% anomalous records present in the unlabelled training set, the sparse decomposition isolates them from the network's encoding of normal behaviour. Reconstruction error on **(X − S)** at inference serves as both the anomaly score and the variable-level explanation vector. Four properties justify this substitution over both K-Means + Mahalanobis Distance and a standard Dense Autoencoder:

1. **Training contamination resistance**: Standard autoencoders trained on contaminated datasets learn to partially reconstruct anomaly patterns, suppressing their reconstruction error and reducing detection recall for those anomaly types. RDA's sparse noise matrix S absorbs contaminating records during training, isolating normal behaviour in the learned latent space [34]. This property is critical given the estimated ~10% anomaly prevalence in the Jambi dataset — a contamination rate that would meaningfully bias a standard autoencoder's learned representation.

2. **Non-linear compound anomaly detection**: The Mahalanobis distance captures linear covariance deviations only. Village fund corruption anomalies manifest as compound non-linear interactions — e.g., simultaneously high `cost_per_unit`, inflated `avg_completion`, near-zero `Real_T3`, and `swakelola_high_value` = 1. RDA's encoder layers learn these compound patterns through non-linear activations, producing detection capabilities that linear distance metrics structurally cannot replicate [19].

3. **AUC-ROC superiority on government financial data**: Shi and Weng [22] demonstrate in a 2024 study of government billing anomaly detection that autoencoders achieve higher AUC-ROC than centroid-distance methods. The performance advantage increases as the number of engineered features exceeds five — the condition present in this study's input matrix. RDA's contamination-resistant training objective is expected to sustain or exceed this advantage on the Jambi dataset.

4. **Per-feature reconstruction error as interpretable explanation**: De Meulemeester et al. [20] demonstrate that decomposing reconstruction error per input feature equips domain experts with actionable diagnostic information: the specific financial variable responsible for the anomaly flag is directly observable from the per-feature MSE vector computed on **(X − S)**. Auditors see not only *that* an activity is flagged, but *which spending variable* drives the suspicion — preserving and substantially enhancing the interpretability purpose originally attributed to K-Means cluster profiles.

#### 4.5.4 Summary Comparison: Replaced vs. Adopted Methods

| Dimension | DBSCAN (Replaced) | LOF (Adopted) | K-Means + Mahalanobis (Replaced) | Robust Deep Autoencoder (Adopted) |
|---|---|---|---|---|
| **Parameter sensitivity** | High — global ε fails on mixed-density data | Low — k stable across densities | Medium — k must be pre-specified | Low — architecture fixed; λ robust to cross-validation; early stopping handles overfitting |
| **Government data validation** | Limited: primarily applied to homogeneous datasets | Direct: Li et al. [18] on USA federal spending 2025 | Partial: analogous to Wu [21] on Chinese budget audit | Direct: Shi & Weng [22] on government billing 2024; Zhou & Paffenroth [34] KDD 2017 |
| **Anomaly signal type** | Binary noise label only | Continuous score — enables triage ranking | Linear distance from centroid | Non-linear reconstruction error on (X−S) per feature |
| **Compound irregularity detection** | No — single density parameter | Partial — local density deviation | No — linear covariance only | Yes — non-linear encoding + sparse noise isolation [19, 34] |
| **Training contamination resistance** | N/A | N/A — non-parametric, no training required | None — contaminated cluster centroids absorb anomaly influence | High — sparse noise matrix S absorbs anomalous training records [34] |
| **Auditor interpretability** | Low — unlabelled noise | Medium — score rank | High — cluster profile | High — per-feature error decomposition on (X−S) [20] |

---

## 5. Research Gap

| Dimension | Existing State | This Study's Contribution |
|---|---|---|
| **Domain** | Village fund research concentrates on legal-forensic analysis [4], governance accountability [5], and fraud triangle diagnostics [6]; reviewed IS/ML studies on Indonesian public finance address procurement patterns [14] but not village fund expenditure records | Applies unsupervised anomaly detection to village fund absorption data — a domain addressed through legal and governance lenses in the reviewed literature [12, 16] rather than computational screening |
| **Method** | Harriz et al. [13], the only ML study specific to village funds, applies supervised CatBoost classification requiring labelled training data; Husnaningtyas and Dewayanto [16] observe unsupervised approaches remain rare in Indonesian financial fraud detection | Employs three unsupervised methods operating on unlabelled absorption records, aligned with real-time monitoring constraints where verified corruption labels are unavailable [16] |
| **Geography** | Ambarsari and Desyanti [14] apply Isolation Forest to national-level Indonesian procurement data without connecting algorithmic outputs to specific corruption typologies | Conducts province-level, village-activity analysis and maps anomaly flags to modus operandi documented in judicial verdicts [7] and institutional audit reports [8] |
| **Data Type** | Reviewed studies use aggregate budget statistics or governance survey instruments [12, 16]; Siskeudes activity-level variables — procurement method codes, multi-stage realization amounts, activity identifiers — have not been modelled as anomaly detection features | Constructs a ten-variable feature matrix directly from Siskeudes activity records, operationalising each feature as a computational proxy for a documented corruption modus operandi [7, 8, 15] |
| **Comparison** | Indonesian public finance anomaly detection studies apply single algorithms [14]; Alam et al. [24] identify multi-paradigm benchmarking as best practice but find it scarcely implemented in domain-specific applications | Benchmarks three algorithmically distinct paradigms — ensemble partitioning (IF), local density estimation (LOF), and deep sparse reconstruction (RDA) — providing the comparative evaluation recommended by Alam et al. [24] for rigorous unsupervised detection |

---

## 6. Data Overview

### 6.1 Source
Six Excel files covering Jambi Province, 2023–2025:

| File Category | Description | Years Available |
|---|---|---|
| **Pagu** (Budget Allocation) | Per-village budget ceiling for the fiscal year | 2023, 2024, 2025 |
| **Penyerapan** (Expenditure Absorption) | Per-activity realization per village, per disbursement stage | 2023, 2024, 2025 |

### 6.2 Key Variables — Penyerapan (Unit of Analysis: Activity per Village per Year)

| Variable | Description | Corruption Signal Potential |
|---|---|---|
| `Kode_Output` | Activity category code (e.g., 110801, 210101) | Activity-category mismatch |
| `Uraian_Output` | Activity textual description | Similar-name duplicate detection |
| `Volume` | Planned quantity output | Volume inflation relative to cost |
| `Satuan` | Unit of measurement | Ambiguous units enabling cost manipulation |
| `Cara_Pengadaan` | Procurement method (Swakelola / Kontrak / Pihak ke-3 / Kerjasama / Penyertaan Modal) | High-value activities using Swakelola (no competitive bidding) |
| `Real_T1, T2, T3` | Realization amount per disbursement stage | Incomplete realization; front-loaded payments |
| `Pct_T1, T2, T3` | Completion percentage per stage | Inconsistent or inflated percentages |

### 6.3 Linked Variable — Pagu (joined by Kode_Desa + Tahun)

| Variable | Corruption Signal Potential |
|---|---|
| `Pagu` | Aggregate village budget ceiling; enables absorption ratio calculation |

---

## 7. Feature Engineering Plan

All features derive from the Penyerapan dataset joined with Pagu. The following constructs operationalise known corruption modus operandi [7, 8, 15]:

| Feature Name | Formula / Logic | Modus Operandi Addressed |
|---|---|---|
| `total_realization` | Real_T1 + Real_T2 + Real_T3 | Baseline expenditure per activity |
| `cost_per_unit` | total_realization / Volume (if Volume > 0) | Mark-up: inflated unit cost |
| `absorption_ratio` | total_realization / Pagu (village level) | Proyek fiktif: zero/near-zero absorption |
| `avg_completion` | mean(Pct_T1, Pct_T2, Pct_T3) | Incomplete / manipulated completion reports |
| `stage_variance` | std(Real_T1, Real_T2, Real_T3) | Irregular disbursement pattern |
| `completion_vs_realization` | avg_completion vs normalised total_realization | Inconsistency between reported % and actual spend |
| `swakelola_high_value` | 1 if Cara_Pengadaan == 'Swakelola' AND total_realization > threshold | High-value procurement without competitive bidding |
| `activity_category` | Kode_Output prefix (2-digit) encoded numerically | Activity type for cluster grouping |
| `year` | 2023/2024/2025 | Inter-year drift in costs for same activity type |
| `cost_deviation_by_category` | z-score of `cost_per_unit` within same `Kode_Output` group, computed **year-stratified** (2023, 2024, 2025 independently) to prevent temporal leakage from pooled-year distribution | Within-category cost outlier — temporally isolated |

*Note: Text-based features (Uraian_Output, Keterangan) — useful for detecting duplicate activity names and fictitious project labels — are excluded from the current numerical feature matrix. Their inclusion via TF-IDF or sentence embeddings constitutes an identified limitation and a designated direction for future work.*

*Note 2: `stage_variance` is computed as `std(Real_T1, Real_T2, Real_T3)` uniformly across all three stages. Activities legitimately disbursed entirely in Stage 1 (T2 = T3 = 0 by single-stage design, per village fund regulation) will exhibit high computed variance, producing structural false positives for this feature specifically. This zero-inflation property is acknowledged as a known limitation; the remaining features provide cross-contextual evidence when interpreting stage_variance-driven flags. Stage-activity type filtering as a mitigation is identified as future work.*

---

## 8. Methodology — Comparative Unsupervised Learning

### 8.1 Study Design Overview

```
Raw Data (Pagu + Penyerapan, 2023-2025, Jambi)
        ↓
Data Preprocessing
  · Structural zero annotation (n_stages_active per record)
  · VIF screening — drop/merge features with VIF > 5 (documented)
  · Year-stratified z-scores for cost_deviation_by_category
        ↓
Feature Engineering (post-VIF feature matrix)
        ↓
Normalisation (RobustScaler — median/IQR, resistant to anomaly-induced scale distortion)
        ↓
┌─────────────┬──────────────┬──────────────┬────────────────────────────┐
│ Baseline:   │ Method 1:    │ Method 2:    │ Method 3:                  │
│ IQR Rule-   │ Isolation    │ Local        │ Robust Deep               │
│ based       │ Forest (IF)  │ Outlier      │ Autoencoder (RDA)         │
│             │              │ Factor (LOF) │ [sparse noise decomp.]    │
└──────┬──────┘─────┬───────┘──────┬───────┘─────────┬───────────────┘
       ↓             ↓              ↓                  ↓
   IQR Flag      Anomaly        LOF Score         Reconstruction
                 Scores        (continuous)       Error on (X−S)
       └─────────────┘─────────────┘──────────────────┘
                              ↓
             Comparative Evaluation
   (IQR Baseline · Anomaly Rate Consistency · Score Distribution
    Cohen's κ · Precision@K · Village Persistence Score · PCA/t-SNE)
                              ↓
           Corruption Typology Mapping
   (Modus: Mark-up · Fiktif · Double Budget · etc.)
                              ↓
      Village-Level Anomaly Persistence Analysis
  (cross-year flags 2023–2024–2025 per desa → top inspection targets)
```

### 8.2 Method 1 — Isolation Forest
**Rationale**: Liu et al.'s (2008) Isolation Forest isolates anomalies by recursively partitioning the feature space; observations that require fewer splits to isolate score as outliers. Its resistance to the curse of dimensionality and computational efficiency make it well-suited to tabular government expenditure data [11, 14].

**Key Parameters**:
- `n_estimators`: 100–300 (tuned via contamination rate sweep)
- `contamination`: 0.05–0.15 (informed by ~10% estimated anomaly rate from ICW statistics [8])
- `max_features`: auto

**Output**: Anomaly score per activity record (-1 = anomaly, 1 = normal)

### 8.3 Method 2 — Local Outlier Factor (LOF)

**Rationale**: LOF (Breunig et al., 2000 [25]) computes the local reachability density of each record relative to its k-nearest neighbours, then expresses how much that density deviates from the neighbourhood's own average density. Records situated in locally sparse regions — whose immediate peers form dense clusters — receive high LOF scores and are flagged as anomalies. This local comparison mechanism addresses the fundamental limitation of DBSCAN: it requires no global density parameter (ε), adapting independently to the density of each local region.

Two properties make LOF the superior density-based method for village fund absorption data:

1. **Local adaptation to heterogeneous activity categories**: Village fund data contains activity types spanning radically different value ranges — infrastructure contracts in the hundreds of millions versus honoraria in the tens of thousands. A single global ε (as required by DBSCAN) cannot simultaneously accommodate both density regimes. LOF computes local density deviation within each activity neighbourhood independently, correctly handling mixed-density data without parameter re-tuning [18, 20].

2. **Continuous scoring enables audit triage**: LOF produces a continuous score (values near 1.0 indicate normality; values significantly above 1.5 indicate anomaly), enabling rank-ordered anomaly lists directly actionable for inspection prioritisation. Li et al. [18] confirm this property as particularly valuable in government spending audit contexts, where limited inspector capacity requires severity-ranked output rather than binary noise labels.

**Key Parameters**:
- `n_neighbors` (k): 10–30 (tuned via LOF score distribution stability analysis)
- Anomaly threshold: records at ≥ 95th percentile of LOF score distribution
- Feature input: same normalised feature set as Isolation Forest

**Output**: Continuous LOF score per activity record + binary anomaly flag

### 8.4 Method 3 — Robust Deep Autoencoder (RDA)

**Rationale**: A Robust Deep Autoencoder (RDA) [34] extends the standard autoencoder by jointly decomposing the input matrix **X** into two components during training: a reconstructed normal component produced by the neural network, and a sparse noise matrix **S** (same dimensions as the input) that absorbs anomalous feature combinations. The joint optimisation objective is:

`Loss = MSE(AE(X − S), (X − S)) + λ‖S‖₁`

The L1 penalty on **S** forces anomalous records — whose feature combinations the network cannot faithfully reconstruct — into the sparse noise matrix rather than distorting the learned latent representation. This separation means the autoencoder learns exclusively from normal expenditure behaviour even when the training set contains the estimated ~10% anomalous records. At inference, per-record reconstruction error on **(X − S)** serves as both the anomaly score and the variable-level explanation vector.

Four properties justify replacing K-Means + Mahalanobis Distance with RDA as the third detection paradigm:

1. **Training contamination resistance**: Standard autoencoders trained on contaminated datasets learn to partially reconstruct anomaly patterns, suppressing their reconstruction error and reducing detection recall for those anomaly types. RDA's sparse noise matrix absorbs contaminating records during training, isolating normal expenditure behaviour in the learned latent space [34]. This property is critical given the estimated ~10% anomaly prevalence in the Jambi dataset — a contamination rate that would meaningfully bias a standard autoencoder's learned representation.

2. **Non-linear compound anomaly detection**: The Mahalanobis distance captures linear covariance deviations only. Village fund corruption anomalies manifest as compound non-linear interactions — e.g., simultaneously high `cost_per_unit`, inflated `avg_completion`, near-zero `Real_T3`, and `swakelola_high_value` = 1. RDA's encoder layers learn these compound patterns through non-linear activations, producing detection capabilities that linear distance metrics structurally cannot replicate [19].

3. **AUC-ROC superiority on government financial data**: Shi and Weng [22] demonstrate in a 2024 comparative study of government billing anomaly detection that autoencoders achieve higher AUC-ROC than centroid-distance methods, with the performance advantage increasing as the number of engineered input features exceeds five — the condition present here. RDA's contamination-resistant training objective is expected to sustain or exceed this performance advantage on the Jambi dataset.

4. **Per-feature reconstruction error as interpretable explanation**: De Meulemeester et al. [20] demonstrate that decomposing reconstruction error per input feature equips domain experts with actionable diagnostic information: the specific financial variable responsible for the anomaly flag is directly observable from the per-feature MSE vector computed on **(X − S)**. Auditors receive not only *that* an activity is suspicious, but *which spending variable* is anomalous — preserving and substantially enhancing the interpretability purpose originally attributed to K-Means cluster profiles.

**Architecture**:
- Input: RobustScaler-normalised feature matrix **X** (post-VIF screening)
- Sparse noise matrix **S**: same shape as input, jointly optimised with the autoencoder
- Encoder: Dense(64, ReLU) → Dense(32, ReLU) → Dense(16, ReLU)
- Bottleneck: Dense(8, ReLU)
- Decoder: Dense(16, ReLU) → Dense(32, ReLU) → Dense(64, ReLU) → Dense(output_dim, Linear)
- Loss: `MSE(AE(X − S), (X − S)) + λ‖S‖₁`
- λ (sparse regularisation): swept over [1e-4, 1e-3, 1e-2]; selected via validation MSE
- Optimiser: Adam (lr = 0.001)
- Training: 50–100 epochs with early stopping (patience = 10, monitored on validation MSE)

**Key Parameters**:
- λ: 1e-3 (default); tuned via cross-validated reconstruction error on held-out records
- Anomaly threshold: records at ≥ 95th/97.5th percentile of reconstruction error distribution on (X − S)
- Feature input: same RobustScaler-normalised feature set as other methods

**Output**: Total reconstruction error per activity record + per-feature error decomposition vector on (X − S) + sparse noise component **S** per record + binary anomaly flag

### 8.5 Evaluation Framework

Since ground truth corruption labels are unavailable (unsupervised setting), evaluation uses the following metrics:

| Metric | Purpose | Applicable To |
|---|---|---|
| **IQR Rule-Based Baseline** | Flag records outside Q1 − 1.5×IQR / Q3 + 1.5×IQR on `cost_per_unit` and `absorption_ratio`; overlap and false-positive rates compared against all three ML methods to demonstrate whether ML methods add detection value beyond simple statistical screening | Baseline vs. IF, LOF, RDA |
| **Anomaly Rate Consistency** | Stability of % anomalies across 2023/2024/2025 — instability indicates parameter sensitivity rather than genuine signal | Baseline, IF, LOF, RDA |
| **Score Distribution Shape** | Bimodal separation between normal and anomalous tails confirms effective discrimination | IF (anomaly score), LOF (LOF score), RDA (MSE on X−S) |
| **Inter-Method Agreement (Cohen's κ)** | Proportion of records flagged by ≥ 2 of 3 ML methods; high consensus = highest-confidence corruption indications | IF, LOF, RDA |
| **Precision @ K (Expert Validation)** | Top-50 flagged records per method reviewed by 2 domain experts (APIP operative or IS/audit academic with village fund experience) using a binary Suspicious / Not Suspicious rubric mapped to the 7 modus operandi in Section 9; inter-rater Cohen's κ computed between experts to verify rubric reliability — primary ground-truth proxy | IF, LOF, RDA |
| **Village Anomaly Persistence Score** | Village-level metric: proportion of fiscal years (2023, 2024, 2025) in which the village's activities include ≥ 1 flagged record; villages flagged in ≥ 2 of 3 years constitute the highest-priority inspection targets, signalling systematic rather than incidental irregularity | IF, LOF, RDA (consensus flags) |
| **Per-Feature Reconstruction Error** | Identifies which specific financial variable drives each anomaly flag — variable-level diagnostic for auditors derived from per-feature MSE on (X − S) | RDA only |
| **Visualisation (PCA / t-SNE)** | 2D projection confirms visual separation of flagged vs. normal records across all scoring spaces | IF, LOF, RDA |

---

## 9. Corruption Typology Mapping

Upon anomaly identification, each flagged record is cross-referenced with the 12 modus operandi documented by ICW [8] and further elaborated in judicial analysis [7, 15]:

| Modus | Primary Detection Feature | Expected ML Signal |
|---|---|---|
| Mark-up / Price Inflation | `cost_per_unit`, `cost_deviation_by_category` | High z-score within category; Isolation Forest anomaly |
| Proyek Fiktif (Fictitious Project) | `absorption_ratio`, `avg_completion` | Near-zero total realisation despite full percentage claims |
| Anggaran Ganda (Double Budget) | `Uraian_Output` similarity + high activity count per village + duplicated cost patterns | Cluster proximity in LOF + high reconstruction error in RDA for semantically repeated entries; full text-similarity detection identified as future work |
| Pemotongan Honor | Keterangan contains "honor"; low avg_completion | Honoraria line items with anomalously low realization |
| Laporan Pertanggungjawaban Palsu | `completion_vs_realization` gap | High Pct values with low Real values |
| Pengadaan without Competition | `swakelola_high_value` = 1 | High-value Swakelola procurement flag |
| Penyertaan Modal Irregular | Cara_Pengadaan = Penyertaan Modal + anomaly score | Equity injection pattern in non-enterprise villages |

---

## 10. Implementation Plan (Google Colab Notebooks)

Three `.ipynb` notebooks, executable in Google Colab:

| Notebook | Content |
|---|---|
| `01_data_preprocessing.ipynb` | Load Pagu + Penyerapan (2023–2025), merge, clean; annotate structural zeros (n_stages_active); compute year-stratified z-scores for `cost_deviation_by_category`; run VIF screening (drop/merge features with VIF > 5); apply RobustScaler; export `features_engineered.csv` |
| `02_unsupervised_comparison.ipynb` | Apply IQR baseline; train and apply IF, LOF, RDA (all on RobustScaler-normalised features); compute IQR vs. ML overlap; compute anomaly rate consistency, score distribution, inter-method Cohen's κ; compute village anomaly persistence scores; export anomaly flags |
| `03_corruption_typology_analysis.ipynb` | Map anomaly flags to modus operandi; visualise with PCA/t-SNE; produce summary tables; export Top-50 flagged records per method for expert validation (binary Suspicious / Not Suspicious rubric per Section 9); compute inter-rater Cohen's κ; produce village persistence ranking |

**Libraries**: `pandas`, `numpy`, `scikit-learn`, `tensorflow` / `keras`, `matplotlib`, `seaborn`, `plotly`, `scipy`

---

## 11. Expected Contributions

### Theoretical Contributions
1. Extends IS-grounded anomaly detection frameworks — demonstrated in health insurance data [20] and US federal spending contexts [18] — to Indonesian village fund expenditure, a domain previously approached through legal-forensic and governance lenses [4, 5, 6] rather than computational anomaly screening.
2. Advances the operationalisation of the Fraud Triangle through computational features derived from expenditure absorption records, including the novel village-level anomaly persistence score as a proxy for sustained opportunity exploitation across fiscal cycles.
3. Demonstrates the applicability of Robust Deep Autoencoders [34] — an architecture designed for contaminated training sets — to public financial monitoring contexts where ground-truth labels are unavailable and training set purity cannot be guaranteed.

### Practical Contributions
1. Produces a replicable, open-source screening tool (Colab notebooks) applicable to any province with equivalent Siskeudes-format data.
2. Generates a rank-ordered list of suspicious village activities for Inspectorate/BPKP follow-up, reducing audit triage effort.
3. Demonstrates how three years of longitudinal data (2023–2025) enable inter-year cost deviation analysis beyond the single-period scope characteristic of reviewed Indonesian public finance anomaly studies [14, 17].
4. Introduces a village-level anomaly persistence score that identifies villages exhibiting repeated anomalous expenditure patterns across multiple fiscal years, providing principled cross-year inspection prioritisation beyond single-cycle screening.

---

## 12. Conceptual Framework Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         THEORETICAL UNDERPINNING                         │
│                                                                          │
│  Fraud Triangle [Cressey, 1953]  ←──►  Principal-Agent Theory           │
│  Pressure · Opportunity ·               [Sutarna & Subandi, 2023;       │
│  Rationalisation                         Groenendijk, 1997]             │
│  → Frames anomaly interpretation        → Information asymmetry maps    │
│    via pressure-opportunity lens          to unexplained spending dev.   │
│              ↕                                         ↕                │
│         DeLone & McLean IS Success Model [D&M, 2003]                    │
│         Information quality → Individual impact → Organisational impact  │
│         → System contribution measured by corruption deterrence at scale │
└───────────────────────────────────────────┬─────────────────────────────┘
                                            │  operationalisation
              ┌─────────────────────────────▼─────────────────────────────┐
              │              DATA INPUT — Jambi Province                  │
              │           Siskeudes / SIMDA Desa, 2023–2025               │
              │   ┌──────────────────────┐   ┌──────────────────────┐    │
              │   │      Penyerapan      │   │        Pagu          │    │
              │   │  Activity-level      │   │  Budget ceiling per  │    │
              │   │  realisation per     │   │  village, per year   │    │
              │   │  disbursement stage  │   │                      │    │
              │   └──────────────────────┘   └──────────────────────┘    │
              └─────────────────────────────┬─────────────────────────────┘
                                            │  merge on Kode_Desa + Tahun
              ┌─────────────────────────────▼─────────────────────────────┐
              │          PREPROCESSING & FEATURE ENGINEERING              │
              │       Clean · Impute · Join · Engineer · Normalise        │
              │  ┌──────────────────────────────────────────────────────┐ │
              │  │                10-variable feature matrix            │ │
              │  │  cost_per_unit           · absorption_ratio          │ │
              │  │  avg_completion          · stage_variance            │ │
              │  │  completion_vs_realization                           │ │
              │  │  swakelola_high_value    · activity_category         │ │
              │  │  year                   · cost_deviation_by_category │ │
              │  └──────────────────────────────────────────────────────┘ │
              └────────────┬──────────────────────┬──────────┬────────────┘
                           │                      │          │
       ┌───────────────────▼─┐  ┌─────────────────▼─┐  ┌────▼──────────────────┐
       │  Isolation Forest   │  │  Local Outlier     │  │  Robust Deep AE    │
       │       (IF)          │  │  Factor (LOF)      │  │       (RDA)        │
       │                     │  │                    │  │                    │
       │  Path-partitioning  │  │  Local density     │  │  Encoder →          │
       │  ensemble           │  │  estimation        │  │   Bottleneck (dim. ↓)│
       │  No distr. assump.  │  │  (k-NN based)      │  │  → (X−S) decomp.    │
       └──────────┬──────────┘  └─────────┬──────────┘  └──────────┬───────────┘
        Anomaly   │ score         LOF      │ score        MSE per   │ feature
                  └─────────────────────────┴────────────────────────┘
                                            │
              ┌─────────────────────────────▼─────────────────────────────┐
              │                  COMPARATIVE EVALUATION                   │
              │   IQR Baseline · Anomaly Rate Consistency               │
              │   Score Distribution Shape   (bimodal separation test)    │
              │   Inter-Method Agreement     (Cohen's κ)                  │
              │   Precision @ K              (expert rubric, 2 raters)    │
              │   Village Persistence Score  (cross-year flagging)        │
              │   PCA / t-SNE                (2D cluster projection)      │
              └─────────────────────────────┬─────────────────────────────┘
                                            │  consensus flags (≥ 2 of 3 methods)
              ┌─────────────────────────────▼─────────────────────────────┐
              │              CORRUPTION TYPOLOGY MAPPING                  │
              │   Mark-up · Proyek Fiktif · Anggaran Ganda                │
              │   Pemotongan Honor · Laporan Pertanggungjawaban Palsu     │
              │   Pengadaan tanpa Tender · Penyertaan Modal Irregular     │
              └─────────────────────────────┬─────────────────────────────┘
                                            │
              ┌─────────────────────────────▼─────────────────────────────┐
              │                       AUDIT OUTPUT                        │
              │   Rank-ordered suspicious activity list                   │
              │   → Inspectorate / BPKP inspection triage                 │
              └────────────────────────────────────────────────────────────┘
```

---

## 13. Preliminary References

*Note: All references are from Scopus/ISI-indexed sources or reputable institutional reports. DOI/URLs provided for verification. Numbering follows IEEE format as assigned in this document.*

[1] Kementerian Koordinator Bidang PMK, "Evaluasi Dana Desa 2023–2024," Antara News, Sep. 2024. [Online]. Available: https://www.antaranews.com/berita/4323375/kemenko-pmk-sebut-korupsi-dana-desa-masih-perlu-perhatian-khusus

[2] Kompas.id, "10 Tahun Dana Desa, 10 Kisah Korupsi yang Membawa Nestapa," Feb. 2025. [Online]. Available: https://www.kompas.id/artikel/en-10-tahun-dana-desa-10-kisah-korupsi-yang-membawa-nestapa

[3] Komisi Pemberantasan Korupsi (KPK), *Laporan Tahunan KPK 2023*, Jakarta: KPK, 2023. [Online]. Available: https://www.kpk.go.id/id/publikasi/laporan-tahunan/3398-laporan-tahunan-kpk-2023/

[4] R. B. Purba, F. Aulia, V. C. E. Tarigan, A. J. Pramono, and H. Umar, "Detection of corruption in village fund management using fraud analysis," *Calitatea*, vol. 23, 2022. [Online]. Available: https://www.academia.edu/download/92271721/Detection_of_Corruption_in_Village_Fund_Management_using_Fraud_Analysis.pdf

[5] P. Permatasari, A. Budiarso, and T. Dartanto, "Village fund management and reporting systems: are they accountable?" *Transforming Government: People, Process and Policy*, vol. 18, no. 4, pp. 512–529, 2024, doi: 10.1108/TG-07-2023-0098.

[6] T. Hidajat, "Village fund corruption mode: an anti-corruption perspective in Indonesia," *Journal of Financial Crime*, vol. 32, no. 2, pp. 444–458, 2025, doi: 10.1108/JFC-01-2024-0042.

[7] H. N. Prihatmanto, A. D. Artha, et al., "Recognising and detecting patterns of village corruption in Indonesia," *Integritas: Jurnal Antikorupsi*, 2022. [Online]. Available: https://pdfs.semanticscholar.org/e081/cd0e420cd3deeb4e1e5c9ee106e34504fda3.pdf

[8] Indonesian Corruption Watch (ICW), *Laporan Hasil Pemantauan Tren Korupsi Tahun 2023*, Jakarta: ICW, May 2024. [Online]. Available: https://www.antikorupsi.org/sites/default/files/dokumen/Narasi%20Laporan%20Hasil%20Pemantauan%20Tren%20Korupsi%20Tahun%202023.pdf

[9] I. T. Sutarna and A. Subandi, "Korupsi dana desa dalam perspektif principal-agent," *Jurnal Administrasi Pemerintahan Desa*, vol. 4, no. 2, Aug. 2023, doi: 10.47134/villages.v4i2.52.

[10] W. H. DeLone and E. R. McLean, "The DeLone and McLean model of information systems success: a ten-year update," *Journal of Management Information Systems*, vol. 19, no. 4, pp. 9–30, 2003, doi: 10.1080/07421222.2003.11045748.

[11] A. Herreros-Martínez and R. Magdalena-Benedicto, "Applied machine learning to anomaly detection in enterprise purchase processes: a hybrid approach using clustering and isolation forest," *Information*, vol. 16, no. 3, p. 177, 2025, doi: 10.3390/info16030177.

[12] M. S. Lyra, B. Damásio, F. L. Pinheiro, and F. Bacao, "Fraud, corruption, and collusion in public procurement activities, a systematic literature review on data-driven methods," *Applied Network Science*, vol. 7, no. 1, p. 78, 2022, doi: 10.1007/s41109-022-00523-6.

[13] M. A. Harriz, N. V. Akbariani, and H. Setiyowati, "Classifying village fund in West Java, Indonesia using catboost algorithm," *Jurnal Indonesia Manajemen Informatika dan Komunikasi*, vol. 4, no. 2, 2023. [Online]. Available: http://journal.stmiki.ac.id/index.php/jimik/article/view/269

[14] E. W. Ambarsari and D. Desyanti, "Hybrid chaos-isolation forest framework for anomaly detection in Indonesia's public procurement," *Bulletin of Informatics and Data Science*, 2025, doi: 10.ejurnal.pdsi.or.id/index.php/bids/article/view/137.

[15] M. Maulana, "Risiko korupsi pengelolaan anggaran desa," *ARMADA: Jurnal Penelitian Multidisiplin*, vol. 1, no. 3, Mar. 2023, doi: 10.55681/armada.v1i3.435.

[16] N. Husnaningtyas and T. Dewayanto, "Financial fraud detection and machine learning algorithm (unsupervised learning): systematic literature review," *Jurnal Riset Akuntansi dan Bisnis Airlangga*, 2023. [Online]. Available: https://e-journal.unair.ac.id/jraba/article/download/49927/26752

[17] B. Nunes, T. Colliri, M. Lauretto, W. Liu, and L. Zhao, "Anomaly detection in Brazilian federal government purchase cards through unsupervised learning techniques," in *Brazilian Conference on Intelligent Systems*, Springer, 2021, doi: 10.1007/978-3-030-91699-2_2.

[18] B. Li, B. Kaplan, M. Lazirko, and A. Kogan, "Unsupervised outlier detection in audit analytics: a case study using USA spending data," arXiv preprint arXiv:2509.19366, 2025. [Online]. Available: https://arxiv.org/abs/2509.19366

[19] A. Kumar, A. Kumar, R. Raja, and A. K. Dewangan, "Revolutionising anomaly detection: a hybrid framework integrating isolation forest, autoencoder, and Conv. LSTM," *Knowledge and Information Systems*, 2025, doi: 10.1007/s10115-025-02580-6.

[20] H. De Meulemeester, F. De Smet, J. van Dorst, et al., "Explainable unsupervised anomaly detection for healthcare insurance data," *BMC Medical Informatics and Decision Making*, vol. 25, 2025, doi: 10.1186/s12911-024-02823-6.

[21] X. Wu, "A unified global and local outlier detection framework with application to Chinese financial budget auditing," *Systems*, vol. 13, no. 11, p. 978, 2025, doi: 10.3390/systems13110978.

[22] X. Shi and H. Weng, "Comparative analysis of unsupervised learning approaches for anomalous billing pattern detection in healthcare payment integrity," *Journal of Computing Innovations and Applications*, vol. 2, no. 1, 2024. [Online]. Available: https://ciajournal.com/index.php/jcia/article/view/45

[23] G. Maheswari and A. Vinith, "An ensemble framework for network anomaly detection using isolation forest and autoencoders," in *2024 International Conference on Intelligent Systems*, IEEE, 2024, doi: 10.1109/10533499.

[24] M. N. Alam, V. Laxmi, N. Kumar, and R. Kumari, "Unsupervised machine learning for anomaly detection: a systematic review," *International Journal of Intelligent Systems*, 2025. [Online]. Available: https://www.researchgate.net/publication/394263593

[25] M. M. Breunig, H.-P. Kriegel, R. T. Ng, and J. Sander, "LOF: Identifying density-based local outliers," in *Proc. ACM SIGMOD International Conference on Management of Data*, Dallas, TX, 2000, pp. 93–104, doi: 10.1145/342009.335388.

[26] R. Chalapathy and S. Chawla, "Deep learning for anomaly detection: a survey," arXiv preprint arXiv:1901.03407, 2019. [Online]. Available: https://arxiv.org/abs/1901.03407

[27] Jaga.id, "Rekap Laporan Dana Desa per Provinsi," Platform Pemantauan Dana Desa, Indonesia, accessed Apr. 2026. [Online]. Available: https://jaga.id

[28] K. Srirejeki and A. Faturokhman, "In search of corruption prevention model: case study from Indonesia village fund," *Acta Universitatis Danubius. Oeconomica*, vol. 16, no. 3, pp. 214–229, 2020. [Online]. Available: https://doaj.org/article/01b1588b59f149ba82d6ef47dddaca0a

[29] A. Alfada, "Does fiscal decentralization encourage corruption in local governments? Evidence from Indonesia," *Journal of Risk and Financial Management*, vol. 12, no. 3, article 118, 2019, doi: 10.3390/jrfm12030118.

[30] JambiTV Disway, "Eks Kades Muara Hemat jalani tahap 2 kasus dugaan korupsi dana desa," Feb. 2026. [Online]. Available: https://jambitv.disway.id/hukum/read/12500/eks-kades-muara-hemat-jalani-tahap-2-kasus-dugaan-korupsi-dana-desa

[31] JambiTV Disway, "Dana desa Jambi Tulo dibekukan: Inspektorat temukan dugaan kegiatan fiktif Rp300 juta lebih," 2025. [Online]. Available: https://jambitv.disway.id/muaro-jambi/read/12087/dana-desa-jambi-tulo-dibekukan-inspektorat-temukan-dugaan-kegiat-fiktif-rp300-juta-lebih

[32] Kompas.com, "Kades hingga mantan kades di Kerinci, Jambi korupsi Rp 644 juta dana desa," Aug. 2025. [Online]. Available: https://regional.kompas.com/read/2025/08/20/213221778/kades-hingga-mantan-kades-di-kerinci-jambi-korupsi-rp-644-juta-dana-desa

[33] JambiLINK.id, "Tersangka korupsi dana desa Pangkal Duri ditangkap, kerugian negara capai Rp 415 juta," Aug. 2024. [Online]. Available: https://jambilink.id/post/951/tersangka-korupsi-dana-desa-pangkal-duri-ditangkap-kerugian-negara-capai-rp-415-juta

[34] C. Zhou and R. C. Paffenroth, "Anomaly detection with robust deep autoencoders," in *Proc. 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, Halifax, Canada, 2017, pp. 665–674, doi: 10.1145/3097983.3098052. [Online]. Available: https://dl.acm.org/doi/10.1145/3097983.3098052

---

*Limitations and Future Work: (1) `stage_variance` is vulnerable to zero-inflation from legitimately single-stage activities (T2 = T3 = 0 by design), producing structural false positives for this feature; stage-activity type filtering is designated as future work. (2) Text-based features (`Uraian_Output`, `Keterangan`) useful for detecting duplicate activity names and fictitious project labels are excluded from the current numerical feature matrix; their inclusion via TF-IDF or sentence embeddings constitutes a primary future direction. (3) Expert validation requires access to APIP operatives or IS/audit academics with village fund experience; the study's Precision@K findings are contingent on this resource. (4) Province-level analysis of Jambi limits generalisability; cross-provincial comparative analysis is identified as a subsequent research direction.*
