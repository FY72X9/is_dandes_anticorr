# Analysis & Comparison Report: Version 3 (v3-run) vs. Version 1 (output_v1)
## Corruption Indication Detection in Village Fund Activities: Jambi Province (2023–2025)

> **Report Location**: [v3-run/analysis_report_v3.md](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/analysis_report_v3.md)  
> **Full Detailed Comparative Audit**: [v3-run/COMPARISON_REPORT_v3_vs_v1.md](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/COMPARISON_REPORT_v3_vs_v1.md)  
> **Graphify Knowledge Graph Output**: [v3-run/graphify-out/](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/graphify-out/)

---

## 1. Summary of Graphify Knowledge Graph (`v3-run/graphify-out`)

The `/graphify` pipeline was successfully executed on `v3-run`. It converted the workflow notebooks (`01_data_preprocessing.ipynb`, `02_unsupervised_comparison.ipynb`, `03_corruption_typology_analysis.ipynb`) into executable modules and built a 38-node, 35-edge knowledge graph mapping feature engineering, machine learning detection models (IF, LOF, RDA), corruption typologies, and longitudinal persistence summaries.

- **Graph Report**: [v3-run/graphify-out/GRAPH_REPORT.md](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/graphify-out/GRAPH_REPORT.md)
- **Interactive Graph HTML**: [v3-run/graphify-out/graph.html](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/graphify-out/graph.html)
- **Graph JSON Data**: [v3-run/graphify-out/graph.json](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/graphify-out/graph.json)

---

## 2. Key Differences: `v3-run` vs. `output_v1`

### 2.1 Dataset & Anomaly Flagging
- **Dataset Size**: `v3-run` processes **96,778 records** (vs. 99,692 in `v1`), removing 2,914 zero-volume/invalid records.
- **Consensus Flagged Anomalies**: Increased from **3,107 records (3.12%)** in `v1` to **7,153 records (7.39%)** in `v3-run`, providing broader recall across subtle corruption patterns.

### 2.2 Shift in Corruption Typologies
- **T2: Ghost Activity (*Kegiatan Fiktif*)**: Expanded to become the **#1 typology** in `v3-run` with **4,155 records (58.1% of flagged)**, up from 774 records (24.9%) in `v1`.
- **T5: Procurement Irregularities (*Swakelola High Value*)**: Surged from 26 records (0.8%) in `v1` to **2,343 records (32.8%)** in `v3-run`.

### 2.3 Longitudinal Village Persistence & Audit Tiers
- **Multi-Year Persistence (3/3 Years Flagged)**: Jumped from **177 villages (13.0%)** in `v1` to **702 villages (51.5%)** in `v3-run`.
- **Tier 1 (High Priority Audit Target)**: Expanded from **642 villages (47.1%)** in `v1` to **1,172 villages (86.0%)** in `v3-run`.

---
*For the complete detailed numerical breakdown and diagnostic visualizations, see [COMPARISON_REPORT_v3_vs_v1.md](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/COMPARISON_REPORT_v3_vs_v1.md).*
