# Chapter 5: Discussion

> **Draft Status**: July 2026 (Updated for diagnostic root-cause analysis, XAI attribution, DSR evaluation matrix, Algorithmic Effectiveness & Legal Indications)  
> **Target Venue**: ICCSCI (Procedia Computer Science, Elsevier)  
> **Word Count Target**: ~1,800 words  
> **Citation Format**: IEEE (continuous numbering per references.md)  

---

## 5. Discussion

### 5.1 Principal Empirical Findings & Artifact Evolution

This study developed and evaluated Protocol 2, an unsupervised Dual-Path Machine Learning artifact for detecting expenditure anomalies across 96,778 activity entries (2023–2025) in Jambi Province. Three core empirical insights emerge from the evaluation:

1. **Resolving the Operationalization Chasm**: Prior literature in public financial governance divides into qualitative studies lacking algorithmic operationalization and non-communicating computational models on synthetic data. Protocol 2 bridges this chasm by constructing a DSR artifact [10] that ingests decentralized administrative Siskeudes absorption data from `jaga.id` [26], proving that administrative absorption signals contain quantifiable traces of expenditure distortion without requiring pre-existing fraud labels.
2. **Overcoming the Ground Truth Paradox via Dual-Path Gating**: By replacing majority voting with a Dual-Path Consensus Gate ($\text{LOF} \lor (\text{IF} \land \text{RDA})$), Protocol 2 expands anomaly recall from 3,107 to 7,153 records (7.39%). The ex-ante synthetic fraud benchmark confirms superior anomaly recovery (**Precision = 0.846, Recall = 0.846, F1 = 0.846, AUC-ROC = 0.912**), outperforming single-algorithm baselines.
3. **Mitigating Geographical Baseline Skew via Kabupaten Centering**: Implementing kabupaten-stratified z-score centering (`(Kode_Output, Kabupaten_Kota, Tahun)`) eliminated systematic false positives for isolated highland jurisdictions (e.g., Kabupaten Kerinci), reducing Kerinci false flags from 31.0% to 4.2% while preserving sensitivity to genuine local price manipulation.

### 5.2 Algorithmic Effectiveness and Operational Screening Performance

The empirical results establish the multi-dimensional effectiveness of **Protocol 2** across four primary operational dimensions:

1. **Resolution of Mutual Cancellation in Multi-Detector Ensembles**: Traditional majority voting (**Protocol 1**: $\text{IF} \land \text{LOF} \land \text{RDA}$) suffered from severe mutual cancellation because LOF evaluates local reachability density ratios, whereas IF and RDA evaluate global feature space partitioning. Demanding simultaneous consensus across all three algorithms discarded localized density anomalies (such as zero-progress ghost projects occurring within small output categories), capping recall at 3,107 records (3.12%). **Protocol 2** resolves this conflict through Dual-Path Gating ($\text{LOF} \lor (\text{IF} \land \text{RDA})$), expanding recall to **7,153 consensus anomalous activities (7.39% of total provincial absorption)**, capturing **Rp 642.85 billion** in financial realization risk (14.89% of total provincial disbursement) and **Rp 6.08 trillion** in budget ceiling exposure (7.46%).
2. **Ex-Ante Synthetic Benchmark Superiority**: Evaluating **Protocol 2** on a controlled synthetic fraud benchmark ($N=10,000$, 500 injected fraud cases / 5.0% prevalence) validates its superior recovery performance. **Protocol 2** achieves **Precision = 0.846, Recall = 0.846, F1-Score = 0.846, and AUC-ROC = 0.912**, outperforming individual base detectors—Isolation Forest ($\text{F1} = 0.724$), Local Outlier Factor ($\text{F1} = 0.686$), and Reconstruction Dense Autoencoder ($\text{F1} = 0.812$)—as well as Protocol 1 majority voting ($\text{F1} = 0.568$, $\text{Recall} = 0.510$).
3. **Audit Search Space Optimization and Target Prioritization**: **Protocol 2** achieves a **92.6% reduction** in audit search space, filtering 96,778 activity entries down to 7,153 high-priority targets. Given that municipal inspectorates (*APIP*) typically operate with only 5 to 15 auditors per kabupaten [12], manual review of 96k records is physically impossible. Furthermore, longitudinal persistence tracking across the 3-year panel isolates **702 Tier-1 persistent high-risk villages (51.5% of tracked jurisdictions)** flagged continuously from 2023 to 2025 ($P_v = 1.0$).
4. **Sub-Threshold Sensitivity and Compound Risk Capture**: **Protocol 2** demonstrates unique effectiveness in detecting sub-threshold financial manipulation. Perpetrators frequently calibrate expenditure anomalies just below single-variable heuristic thresholds (e.g., setting unit cost deviation at $+1.8\sigma$ versus a $+2.0\sigma$ flag limit). Single-rule policy engines fail to detect these calibrated distortions, whereas joint non-linear feature space evaluation in LOF and RDA exposes joint multi-variable shifts, capturing **1,227 sub-threshold masked activities** accounting for **Rp 125.07 billion** in latent financial risk.

### 5.3 Diagnostic Root-Cause Analysis of Anomaly Typology Shifts

To understand the structural mechanisms driving the primary typology shifts between Protocol 1 and Protocol 2, systematic root-cause diagnostic inquiries were conducted and synthesized into cohesive analytical narratives:

#### 1. Causal Mechanics of T2 Ghost Activity Explosion ($N=4,155$)
The dramatic surge in T2 Ghost Activity flags—jumping from 774 records (24.9%) in Protocol 1 to 4,155 records (58.1%) in Protocol 2—stems from a fundamental diagnostic capability shift. Protocol 2 successfully isolates thousands of expenditure activities where budget funds were fully drawn down across tranches while physical output completion remained near zero. In baseline Protocol 1, these zero-progress activities were systematically missed because majority voting relied heavily on Isolation Forest's global feature path lengths. Because zero physical progress occurring within small output categories creates localized clusters, these entries appeared globally normal to random decision tree splits. Protocol 2 overcomes this diagnostic blindness through Local Outlier Factor (LOF), which evaluates local reachability density ratios relative to adjacent peer villages that completed physical infrastructure under identical output codes. By exposing zero-progress activities as extreme local density isolates, Protocol 2 targets ghost projects (*proyek fiktif*)—the most severe physical fraud modus in Indonesian rural administration, accounting for Rp 181.22 billion in direct financial realization risk.

#### 2. Causal Mechanics of T5 Procurement Irregularity Surge ($N=2,343$)
Similarly, the surge in T5 Procurement Irregularity flags—expanding from 26 records (0.8%) in Protocol 1 to 2,343 records (32.8%) in Protocol 2—reflects the neural autoencoder's capacity to capture non-linear feature interactions. Protocol 2 incorporates the `swakelola_high_value` indicator directly into the Reconstruction Dense Autoencoder (RDA) feature matrix. In contrast, Protocol 1 failed to isolate uncompetitive high-value Swakelola procurement because it enforced rigid linear rule combinations requiring simultaneous violations across multiple continuous cost metrics. In practice, procurement manipulation operates through subtle non-linear interactions between categorical procurement modes (Swakelola) and continuous unit cost distributions. The 8-layer bottleneck neural network in RDA learns these complex feature correlations during unsupervised training, producing elevated reconstruction Mean Squared Error (MSE) whenever high-value projects bypass competitive bidding. Capturing T5 irregularities is essential for governance reform because 98.8% of village activities in Jambi Province rely on Swakelola; isolating uncompetitive high-value projects directly targets the structural vulnerability identified in Søreide's procurement corruption theory [9].

### 5.4 Sub-Threshold Masking & Unclassified Anomaly Subspace ($N=1,227$)

Why do 1,227 consensus-flagged records (17.2% of the flagged pool) remain Unclassified under heuristic business rules? This phenomenon results from **sub-threshold masking**, a fraud strategy where perpetrators intentionally manipulate multiple financial variables just below individual heuristic thresholds (e.g., unit cost deviation at $+1.8\sigma$ vs $+2.0\sigma$ threshold; completion delay at $-1.7\sigma$ vs $-2.0\sigma$ threshold).

While single-rule policy heuristics classify each attribute as safe, multi-dimensional ML models (LOF and RDA) detect the joint probability distance across all features simultaneously. Consequently, the ensemble correctly flags the activity as anomalous while the policy mapping engine leaves it Unclassified, capturing **Rp 125.07 Miliar** in sub-threshold financial risk.

### 5.5 Legal Indications and Evidentiary Boundaries for Public Sector Audits

Operationalizing machine learning within public sector corruption oversight requires strict alignment with administrative law and criminal procedure boundaries:

1. **Statutory Status as Preliminary Audit Indication (*Indikasi Awal / Bukti Permulaan*)**: Machine learning anomaly scores generated by **Protocol 2** do **not** constitute direct judicial evidence of criminal corruption (*bukan bukti pidana instan*) under Indonesian Criminal Procedure Code (KUHAP Art. 184) or the Corruption Eradication Act (Law No. 31/1999 jo. Law No. 20/2001). Under Government Regulation (*Peraturan Pemerintah*) No. 60/2008 on the Government Internal Control System (*SPIP*), algorithmic flags serve strictly as **statutory preliminary audit indications** (*indikasi awal* or *bukti permulaan*). They provide public sector oversight bodies—*Aparat Pengawasan Intern Pemerintah* (APIP), the Supreme Audit Agency (*BPK*), and the Financial and Development Supervisory Board (*BPKP*)—with an objective, data-driven trigger to initiate formal internal audits (*Audit Tujuan Tertentu* or *Audit Investigatif*).
2. **Differentiating Administrative Irregularity from Criminal Intent (*Mens Rea*)**: A fundamental boundary in public sector anomaly detection is distinguishing non-malicious operational failure from criminal corruption. High reconstruction MSE or density outlier scores may reflect non-corrupt causes: severe rural administrative capacity deficits, delayed milestone entry by village secretaries (*Sekretaris Desa*), emergency procurement during local natural disasters, or unrecorded localized material cost inflation. To establish criminal corruption under Law No. 31/1999 Art. 2 & 3, legal authorities must prove two distinct elements: (a) an unlawful act or abuse of official authority (*perbuatan melawan hukum / menyalahgunakan kewenangan*), and (b) intentional state financial loss (*merugikan keuangan negara*) or self/corporate enrichment. Algorithmic outputs measure statistical deviation, not legal culpability; they direct human auditors to transactions where the probability of underlying unlawful behavior is statistically concentrated.
3. **XAI-to-Evidence Chain of Custody for APIP Field Inspections**: Standard "black-box" machine learning predictions are inadmissible in formal administrative disciplinary hearings or judicial proceedings. By decomposing neural RDA reconstruction loss into per-feature error contributions, **Protocol 2** constructs a transparent evidentiary chain of custody:
   - **Unit Cost Inflation Errors** ($\text{MSE}_{\text{cost}} > 0.04$) $\to$ APIP issue audit assignment orders (*Surat Perintah Tugas Inspektorat*) to subpoena supplier invoices, receipt vouchers (*Kwitansi*), and verify alignment with official regional price standards (*Standar Satuan Harga -- SSH*).
   - **Completion vs. Disbursement Mismatches** (T2 Ghost Activity) $\to$ APIP conduct physical field inspections (*Cek Fisik Lapangan*) using GPS-tagged physical volume measurements combined with bank statement reconciliation (*Rekening Kas Desa*).
   - **Procurement Anomalies** (T5 Swakelola High-Value) $\to$ APIP examine procurement committee minutes (*Berita Acara Pengadaan*) and Activity Management Team (*TPK*) authorization logs.

### 5.6 Theoretical Implications & DSR Evaluation Matrix

Table 5.1 summarizes the DSR evaluation matrix across the four core dimensions.

**Table 5.1. DSR Evaluation Matrix — Protocol 2 Primary Study Findings**

| DSR Evaluation Dimension | Operationalization in Protocol 2 Artifact | Empirical Target Metric | Observed Outcome |
|---|---|---|---|
| **Relevance Cycle** | Search space reduction for APIP inspectorates | Activity screening overhead reduction | **92.6% reduction** (96,778 $\to$ 7,153 records) |
| **Rigor Cycle** | Agency Theory operationalization in Siskeudes features | Multi-method convergence ($\kappa$) | **$\kappa(\text{IF}, \text{RDA}) = 0.482$** (Moderate convergence) |
| **Design Cycle** | Activity-rate normalized village priority tiering | High-priority Tier 1 village coverage | **1,172 Tier 1 villages (86.0%)** |
| **Ex-Ante Benchmark** | Synthetic fraud injection recovery | Precision, Recall, F1, AUC-ROC | **F1 = 0.846, AUC = 0.912** |

### 5.7 Practical Implications & DeLone & McLean IS Success Model Operationalization

The empirical findings operationalise the **DeLone and McLean IS Success Model (2003)** [10] across two core pathways:

1. **Information Quality $\to$ Individual Impact (Auditor Decision Support)**:
   - *Search Space Reduction*: Filtering 96,778 activity records to 7,153 consensus anomalies yields a 92.6% reduction in document screening overhead.
   - *Longitudinal Priority Tiering*: Isolating 702 persistent Tier-1 villages (flagged continuously across 2023–2025) provides an operationally feasible audit scheduling list for kabupaten inspectorates with 5–15 auditors.
   - *Instance-Level XAI Checklists*: Transforming abstract MSE loss into feature contribution rankings (e.g., specifying physical output measurement for 82.5% completion loss vs price benchmarking for 74.2% unit cost loss) provides field auditors with actionable checklists.
2. **System Quality $\to$ Organizational Impact ("Last Mile" APIP Audit Protocol)**:
   - *Human-in-the-Loop Workflow*: The pipeline translates top consensus anomalies and XAI checklists directly into formal APIP audit assignment orders (*Surat Perintah Tugas Inspektorat*).
   - *Tranche-Specific Investigation Protocols*: T1 (Mark-Up) and T5 (Procurement Irregularity) trigger physical volume verification and local market benchmark comparison; T2 (Ghost Activity) and T4 (Stage Lock) trigger bank statement reconciliation prior to final tranche disbursement.

### 5.8 Knowledge Graph Topology Audit

Generating graph topology analysis on Protocol 2 produced a 38-node, 35-edge knowledge graph with 97% EXTRACTED audit trail integrity. Key central hub nodes include:
1. `Flagged Anomaly Records with Mapped Typology (7,153 records)` (Degree: 7) — Primary data bridge between ML ensemble outputs and typology mapping.
2. `Engineered Feature Matrix (96,778 records x 27 cols)` (Degree: 4) — Central feature matrix feeding IF, LOF, and RDA models.
3. `Consensus Ensemble & High RDA Error Gate` (Degree: 4) — Decision threshold combining unsupervised models.

### 5.9 Study Limitations

Key limitations include: (1) single-province geographic scope (Jambi Province), requiring multi-province panel extension for national generalisability; (2) static heuristic rules for typology mapping, leaving 17.2% of compound anomalies Unclassified; and (3) reliance on open administrative data from `jaga.id`, which depends on timely provincial Siskeudes uploads.
