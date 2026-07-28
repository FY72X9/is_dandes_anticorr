# Rencana Drafting & Blueprint Detail Penulisan Naskah — Version 3 (v03)
## Final Comprehensive Academic & Empirical Integration Blueprint

> **Target Venue**: *Procedia Computer Science* (Elsevier) / ICCSCI  
> **Draft Version**: v03 (Fully Audited & Finalized Plan)  
> **Base Structure**: `docs/draft/v01/` (Bab 00 – 07)  
> **Primary Empirical & Theoretical Sources**: `docs/evaluation/pipeline_output_evaluation_v3.md` (632 baris evaluasi akademik), `src/v3-run/COMPARISON_REPORT_v3_vs_v1.md`, `src/v3-run/tier1_village_summary.csv`, `src/v3-run/expert_validation_top50_CONSENSUS.csv`, `src/v3-run/graphify-out/GRAPH_REPORT.md`  
> **Visualizations**: 9 File Grafik `.png` di `src/v3-run/`  
> **Citation Standard**: IEEE Continuous Numbering ([1] – [32])  

---

## 1. Tinjauan Hasil Evaluasi Output & Kajian Teori Lengkap

Berdasarkan audit mendalam terhadap `pipeline_output_evaluation_v3.md` dan landasan teori riset, seluruh poin output dan teori telah dirangkum ke dalam 7 bab rencana naskah v03:

### A. Kajian Teori Lintas Disiplin (Interdisciplinary Theoretical Grounding):
1. **Principal-Agent Theory & Asimetri Informasi**:
   - Memetakan relasi Principal (APIP Inspektorat, BPKP, KPK) vs Agent (Kepala Desa & TPK).
   - Formulasi matematis asimetri informasi:
     $$\text{Information Asymmetry} = \mathcal{I}_{\text{Agent}}(\text{Physical Realization}, \text{Supplier Price}) - \mathcal{I}_{\text{Principal}}(\text{Siskeudes Financial Reports})$$
   - Eksploitasi *moral hazard* akibat keterbatasan kapasitas verifikasi fisik APIP (PP No. 60/2008).
2. **Fraud Diamond Model dalam Eksekusi Dana Desa**:
   - *Pressure*: Target jadwal pencairan per tahap (`Pct_T1`, `Pct_T2`, `Pct_T3`).
   - *Opportunity*: Dominasi Pengadaan Swakelola 98,8% (Teori Pengadaan Søreide [9] tanpa *competitive bidding*).
   - *Rationalisation*: Budaya normatif penyesuaian honorarium administratif.
   - *Capability*: Monopoli kredensial otorisasi digital Siskeudes & spesimen tanda tangan rekening bank desa oleh Kepala Desa dan Kaur Keuangan (Wolfe & Hermanson [17b]).
3. **DeLone & McLean IS Success Model (2003)**:
   - Alur 6-Box: *System Quality (Siskeudes API / Jaga.id)* $\to$ *Information Quality (Dual-Path Ensemble XAI)* $\to$ *Use & Adoption (APIP Inspection Planning)* + *Individual Impact (Reduksi Search Space 92,6% & XAI Checklists)* $\to$ *Organizational Impact (Deterrence & Penyelamatan Kerugian Negara)*.
4. **Design Science Research (DSR) 3-Cycle Model (Hevner et al.)**:
   - *Relevance Cycle*, *Rigor Cycle*, *Design Cycle* (Iterasi artifact `v3-run`).

### B. Output Empiris & Analisis Spesifik:
1. **Dual Metric Exposure**: Rp 642,85 Miliar realisasi keuangan *at risk* (14,89%) dan Rp 6,08 Triliun Pagu Exposure (7,46%).
2. **Matriks Konsentrasi Risiko 10 Kabupaten/Kota di Jambi**: Peringkat dari Kab. Batanghari (#1, rate 15,75%, 823 rekap, Rp 115,71 B *at risk*) hingga Kab. Tanjung Jabung Barat (#10, rate 4,28%, Rp 45,23 B).
3. **Studi Kasus Kegiatan Riil Siskeudes (Top-50 Expert Validation)**: Kegiatan BUMDes Rantau Makmur ($LOF = 4,78 \times 10^9$), Kios Desa Kedemangan, Pos Kesehatan Desa Bukit Suban (4 tipologi sekaligus), Ambulance Ngaol, dll.
4. **Profil Desa Prioritas Ekstrem Tier 1**: Desa Maliki Air (16 rekap), Desa Gedang (13 rekap), Desa Paling Serumpun (12 rekap), Desa Amar Sakti & Kampung Diilir (11 rekap).
5. **Rantai Kausal 5-Whys**: 5 langkah eksplisit untuk ledakan T2 Ghost Activity (4.155 rekap / 58,1%) dan lonjakan T5 Swakelola (2.343 rekap / 32,8%).
6. **Sub-Threshold Masking & Unclassified Subspace ($N=1.227$)**: Manipulasi perataan multi-fitur di bawah threshold tunggal yang diisolasi oleh LOF & RDA (risiko Rp 125,07 Miliar).
7. **Jaccard Overlap Matrix Top-50**: IF vs RDA (0,00% overlap), Consensus vs RDA (96,08% capture).
8. **Knowledge Graph Topology (`graphify`)**: 38 nodes, 35 edges, 97% EXTRACTED audit trail, God Nodes analysis.
9. **"Last Mile" APIP Audit Protocol**: Penerbitan Surat Perintah Tugas (SPT) Inspektorat berdasarkan XAI loss contribution.

---

## 2. Rincian Pembagian Bab Naskah v03

### BAB 00: ABSTRACT (`00-abstract.md`)
- Background, Problem, Approach (DSR, Agency Theory, Fraud Diamond), Key Findings (96.778 rekap, 7.153 consensus flags / 7,39%, T2 Ghost 58,1%, T5 Swakelola 32,8%, 702 desa persistensi 3/3 tahun, Rp 642,85 B realisasi exposure, Rp 6,08 T pagu exposure, F1 = 0,846, AUC = 0,912), Conclusion & Impact (reduksi search space 92,6%, XAI checklists), Keywords.

### BAB 01: INTRODUCTION (`01-introduction.md`)
- Skala fiskal Dana Desa (Rp 71 T/tahun), ICW 2024 (591 vonis, Rp 598,13 B rugi), KPK stats (851 kasus), Siskeudes archive & `jaga.id`, Jambi low-monitoring paradox (11 komplain vs Sumut 81 & Sumsel 48), GMM threshold Alfada, 4 kasus yudisial Jambi (Muara Hemat, Jambi Tulo, Kerinci, Pangkal Duri), kesenjangan APIP (PP No. 60/2008), 3 RQs & 3 kontribusi.

### BAB 02: RELATED WORK (`02-related-work.md`)
- Bussell & Graycar TASP frameworks, Siregar & Aminudin (5 modus), Kartadinata (200+ kasus KPK), Medan 2025 NTT study, Fraud Diamond (dimensi Capability & monopoli kredensial Siskeudes), Swakelola 98,8% & teori Søreide, Principal-Agent Asymmetry formula, perbandingan 3 paradigma ML (IF global sparsity, LOF local reachability density, RDA neural reconstruction loss), DeLone & McLean IS Success Model, DSR 3 cycles.

### BAB 03: METHODOLOGY (`03-methodology.md`)
- DSR 3 cycles (+ diagram Mermaid), pembersihan data (eliminasi 2.914 rekap volume nol), *geographical baseline centering* z-score tersentralisasi kabupaten per `(Kode_Output, Kabupaten_Kota, Tahun)`, tabel matriks 27 fitur lengkap, spesifikasi matematika IF ($c=0,10$), LOF ($k$-distance & reachability density), RDA (8-layer symmetric bottleneck, MSE loss + $L_2$), *Dual-Path Consensus Gate* ($\text{LOF} \lor (\text{IF} \land \text{RDA})$ + diagram Mermaid), *Operational Policy Mapping Layer* (aturan T1–T7), benchmark fraud sintetis ($N=10.000$), XAI loss attribution formula.

### BAB 04: RESULTS (`04-results.md`)
- Hasil empiris komprehensif mengintegrasikan **9 grafik `.png`**:
  1. `anomaly_rate_consistency.png` (Figure 4.1: Stabilitas LOF vs variansi IF).
  2. `score_distributions.png` (Figure 4.2: Histogram skor & Sarle BC LOF 0,957, RDA 0,703, IF 0,335).
  3. `typology_distribution.png` (Figure 4.3: Pergeseran T2 Ghost 58,1% & T5 Swakelola 32,8%).
  4. `rda_error_decomposition.png` (Figure 4.4: Dekomposisi RDA loss per fitur & Top-50 Heatmap).
  5. `village_persistence_tiers.png` (Figure 4.5: Prioritas Tier 1 86,0% & Persistensi 3/3 tahun 51,5%).
  6. `pca_projection.png` (Figure 4.6: Proyeksi PCA 2D).
  7. `tsne_projection.png` (Figure 4.7: Proyeksi t-SNE 2D).
  8. `feature_correlation_heatmap.png` (Figure 4.8: Heatmap korelasi 27 variabel).
  9. `feature_distributions.png` (Figure 4.9: Distribusi statistik fitur).
- Tabel per-method rates, Sarle BC, irisan Cohen's $\kappa$, pergeseran tipologi, XAI instance-level Top-50 (contoh kegiatan Siskeudes riil), persistensi desa (highlight Desa Maliki Air 16 rekap, Gedang 13 rekap, dll), benchmark sintetis (AUC=0,912, F1=0,846), exposure keuangan dual-metrik, dan tabel matriks konsentrasi risiko 10 kabupaten (Batanghari #1 15.75% rate).

### BAB 05: DISCUSSION (`05-discussion.md`)
- Operationalization Chasm, Ground Truth Paradox, Geographical Skew mitigation, **rantai kausal 5-Whys 5-langkah untuk T2 Ghost dan T5 Swakelola**, *sub-threshold masking* ($N=1.227$, Rp 125,07 B masked risk), matriks overlap Jaccard Top-50, matriks evaluasi DSR, operationalisasi DeLone & McLean IS Success Model ("Last Mile" APIP audit protocol / Surat Perintah Tugas Inspektorat), audit Knowledge Graph (`graphify` 38 nodes, 35 edges, 97% EXTRACTED), *threats to validity*.

### BAB 06: CONCLUSION (`06-conclusion.md`)
- Sintesis jawaban RQ1–RQ3, dampak operasional (reduksi search space 92,6%), 4 arah penelitian masa depan (Semi-supervised GNNs, ekstensi multi-provinsi, streaming API dashboard, ex-post APIP audit referral recovery study).

### BAB 07: REFERENCES (`07-references.md`)
- Referensi IEEE continuous format [1]–[32].

---

## 3. Status Rencana & Penghentian Eksekusi Total

1. Dokumen rencana ini (`PLAN_DRAFTING_v03.md`) telah **selesai diperbarui dan difinalisasi** mencakup seluruh aspek data empiris dan kajian teori.
2. File `implementation_plan.md` telah diperbarui mencerminkan status **FINAL PLAN APPROVED — EXECUTION TERMINATED AS REQUESTED**.
3. **EKSEKUSI PENULISAN FILE CHAPTER (Bab 00 - 07) DIHENTIKAN SEPENUHNYA.** Agent mengakhiri giliran dan tidak melakukan penulisan file lebih lanjut.
