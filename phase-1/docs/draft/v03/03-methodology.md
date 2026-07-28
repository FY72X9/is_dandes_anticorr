# Chapter 3: Methodology

> **Draft Status**: v3.0 — July 2026 (Full mathematical formalization & Dual-Path Consensus Gate)  
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)  
> **Word Count Target**: ~1,250 words  
> **Citation Format**: IEEE (continuous numbering per references.md)  

---

## 3. Methodology

### 3.1 Design Science Research (DSR) Framework

This study adheres strictly to the Design Science Research (DSR) methodology for Information Systems [5, 10], structuring artifact iteration across three primary cycles:
1. **Relevance Cycle**: Addresses the institutional monitoring problem across 96,778 village fund activity entries in Jambi Province under severe APIP district auditor capacity constraints.
2. **Rigor Cycle**: Grounds feature construction in Agency Theory (principal-agent information asymmetry) and Fraud Diamond dynamics, drawing algorithms from multi-paradigm anomaly detection literature [18, 24, 32].
3. **Design Cycle**: Iteratively constructs the IT artifact comprising three core components: (a) robust feature engineering with regional baseline centering, (b) a Dual-Path Consensus Machine Learning engine, and (c) an Operational Policy Mapping Layer.

```mermaid
flowchart TD
    subgraph RelevanceCycle["Relevance Cycle (Environment & Problem Locus)"]
        RC1["APIP District Auditor Capacity Constraints (Jambi: 1,363 Villages, 3 Years)"]
        RC2["Monitoring Goal: Reduce 96,778 Activity Search Space to High-Confidence Audit Pool"]
    end

    subgraph RigorCycle["Rigor Cycle (Foundational Knowledge)"]
        RG1["Theoretical Grounding: Fraud Diamond & Principal-Agent Theory"]
        RG2["Multi-Paradigm ML: Isolation Forest, LOF, Reconstruction Dense Autoencoder"]
    end

    subgraph DesignCycle["Design Cycle (Artifact Iteration v3-run)"]
        DC1["Dual-Path Consensus Ensemble Engine"]
        DC2["Operational Policy Typology Engine"]
        DC3["Activity-Rate Normalized Priority Tiering"]
    end

    RelevanceCycle --> RigorCycle
    RigorCycle --> DesignCycle
    DesignCycle --> RelevanceCycle
```

### 3.2 Dataset Cleaning & Record Filtering Audit

The dataset combines two administrative data sources collected via the KPK `jaga.id` open transparency portal [26]: (1) **Penyerapan** (expenditure absorption) records documenting realised spending per activity per tranche, and (2) **Pagu** (approved budget ceiling) records. Merging via composite key `Kode_Desa` $\times$ `Tahun` across fiscal years 2023, 2024, and 2025 yielded an initial raw corpus of 99,692 activity entries.

In `v3-run`, a rigorous data hygiene audit was performed in `01_data_preprocessing.ipynb`. A total of **2,914 zero-volume or corrupted activity records** ($\text{Volume} \le 0$ or invalid `Kode_Output` codes) were filtered out. In baseline `v1`, zero-volume records caused division-by-zero errors when calculating unit cost ($\text{Realization} \div \text{Volume}$), distorting RobustScaler bounds. Eliminating these invalid records yielded a cleaned longitudinal panel of **96,778 activity-level records** across **1,363 villages** (33,065 in 2023; 34,710 in 2024; 29,003 in 2025).

### 3.3 Geographical Baseline Centering & Engineered Feature Matrix

Seven core feature constructs were engineered to operationalise documented corruption modus operandi [13, 14]:

| Feature Construct | Mathematical Expression / Definition | Targeted Modus Operandi |
|---|---|---|
| `cost_per_unit` | $\text{Realization\_Total}_i / \text{Volume}_i$ (RobustScaler OHE) | Unit price mark-up / inflation (T1) |
| `absorption_ratio` | $\text{Realization\_Total}_i / \text{Pagu\_Village}_{v,t}$ | Ghost activity / zero physical progress (T2) |
| `avg_completion` | $\frac{1}{3}(\text{Pct\_T1}_i + \text{Pct\_T2}_i + \text{Pct\_T3}_i)$ | Completion reporting manipulation |
| `swakelola_high_value` | $\mathbf{1}\left(\text{Cara\_Pengadaan}_i = \text{Swakelola} \land \text{Realization}_i > Q_{0.75}\right)$ | Uncompetitive procurement irregularity (T5) |
| `cost_deviation_by_category` | $z_{i,c,k,t} = \frac{x_{i,c,k,t} - \mu_{c,k,t}}{\sigma_{c,k,t}}$ within $(c, k, t)$ group | Within-category regional price outlier (T7) |
| `n_stages_active` | $\sum_{m=1}^{3} \mathbf{1}\left(\text{Real\_T}m_i > 0\right)$ (Metadata Annotation) | Disbursement tranche concentration |
| `activity_category` | One-Hot Encoded 2-digit `Kode_Output` prefix | Cross-category expenditure dumping (T7) |

> **Geographical Baseline Centering Protocol:** To prevent remote highland jurisdictions (e.g., Kabupaten Kerinci) from generating systematic false-positive flags due to elevated baseline transportation costs, `cost_deviation_by_category` calculates year-stratified z-scores strictly within the combined grouping $(c, k, t) = (\text{Kode\_Output}, \text{Kabupaten\_Kota}, \text{Tahun})$. This controls for regional logistics overhead while preserving sensitivity to local price manipulation.

All continuous features were scaled using **RobustScaler** (median centring, IQR scaling), resisting distortion by extreme outlier records.

### 3.4 Algorithmic Paradigm Specifications

#### 1. Isolation Forest (Global Sparsity Engine)
Isolation Forest partitions the feature space via recursive random splits [18]. For sample $x$, path length $h(x)$ across $T=200$ trees determines anomaly score $s(x, n) = 2^{-\mathbb{E}(h(x))/c(n)}$. Contamination $c = 0.10$ sets the decision function at the 90th percentile:
$$\text{IF-Flag}_i = \mathbf{1}\left(s(x_i, n) \ge \text{Quantile}_{0.90}(s)\right) \implies N_{\text{IF}} = 9,678 \text{ records (10.00\%)}$$

#### 2. Local Outlier Factor (Density Ratio Engine)
LOF computes the local reachability density ($\text{lrd}_k$) ratio between instance $p$ and its $k=20$ nearest neighbors [24]:
$$\text{LOF}_k(p) = \frac{\sum_{o \in N_k(p)} \frac{\text{lrd}_k(o)}{\text{lrd}_k(p)}}{|N_k(p)|}$$
Flagging threshold is set at the 95th percentile:
$$\text{LOF-Flag}_i = \mathbf{1}\left(\text{LOF}_k(x_i) \ge \text{Quantile}_{0.95}(\text{LOF})\right) \implies N_{\text{LOF}} = 4,839 \text{ records (5.00\%)}$$

#### 3. Reconstruction Dense Autoencoder (RDA & Neural Loss Attribution)
The RDA network features an 8-layer symmetric bottleneck structure `[27 -> 64 -> 32 -> 16 -> 8 -> 16 -> 32 -> 64 -> 27]` trained with MSE loss and $L_2$ weight regularization ($\lambda = 1\times 10^{-3}$). Reconstruction error $E_i$ and per-feature contribution $e_{i,f}$ are computed as:
$$E_i = \sum_{f=1}^{d} \left(x_{i,f} - \hat{x}_{i,f}\right)^2, \quad e_{i,f} = \frac{\left(x_{i,f} - \hat{x}_{i,f}\right)^2}{E_i}$$
$$\text{RDA-Flag}_i = \mathbf{1}\left(E_i \ge \text{Quantile}_{0.95}(E)\right) \implies N_{\text{RDA}} = 4,840 \text{ records (5.00\%)}$$

### 3.5 Dual-Path Consensus Ensemble Gate

In baseline `v1`, simple majority voting ($\sum \text{Flag}_m \ge 2$) suffered from severe mutual cancellation because algorithms project onto orthogonal statistical subspaces. In `v3-run`, the **Dual-Path Consensus Ensemble Gate** explicitly decouples local density detection from multi-model global convergence:

```mermaid
flowchart TD
    INPUT["INPUT FEATURE MATRIX (96,778 x 27)"] --> IF["ISOLATION FOREST (Contamination c = 0.10, Top 10%)"]
    INPUT --> LOF["LOCAL OUTLIER FACTOR (k = 20, Top 5%)"]
    INPUT --> RDA["DEEP AUTOENCODER (MSE Loss, Top 5%)"]

    IF --> GLOBAL["GLOBAL CONVERGENCE PATH (IF Flag AND RDA Flag)"]
    RDA --> GLOBAL
    LOF --> LOCAL["LOCAL DENSITY PATH (LOF Flag == 1)"]

    GLOBAL --> ORGATE["OR GATE"]
    LOCAL --> ORGATE
    ORGATE --> CONSENSUS["CONSENSUS FLAG (v3-run: N = 7,153 records / 7.39%)"]
```

$$\text{Consensus-Flag}_i = \text{LOF-Flag}_i \lor \left(\text{IF-Flag}_i \land \text{RDA-Flag}_i\right)$$

This dual-path gate admits **7,153 consensus anomalous records (7.39%)**, capturing 3,940 local density isolates (LOF only) and 2,314 global multi-model convergence records (IF $\cap$ RDA) without admitting uncoordinated single-model noise.

### 3.6 Operational Policy Mapping Layer & Synthetic Benchmark Protocol

Consensus-flagged anomalies are processed through domain-heuristic business rules mapping multi-dimensional flags into seven corruption typologies (T1–T7):
- **T1 (Mark-Up)**: `cost_per_unit` $> 3.0\sigma$.
- **T2 (Ghost Activity)**: `absorption_ratio` $< 0.05$ AND `avg_completion` $< 10\%$.
- **T5 (Procurement Irregularity)**: `swakelola_high_value` $= 1$ AND `cost_per_unit` $> Q_{0.75}$.
- **T7 (Cross-Category Dumping)**: `cost_deviation_by_category` $> 3.0\sigma$.
- **T4 (Stage Lock)**: `n_stages_active` $\ge 2$ AND tranche concentration $> 0.95$.

To resolve the *Unsupervised Ground Truth Paradox*, an **Ex-Ante Synthetic Fraud Benchmark** ($N=10,000$ slice, 5% $N=500$ synthetic fraud injections across markup, ghost, and dumping moduses) was evaluated using Precision@K, Recall, F1-Score, and AUC-ROC.
