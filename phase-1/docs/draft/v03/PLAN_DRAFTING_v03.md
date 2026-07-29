# Cetak Biru & Rencana Detail Penulisan Naskah — Protocol 2
## Master Blueprint: Deep Academic Elaboration, Mathematical Formalization, LaTeX Pseudocode, & Empirical Data Integration

> **Target Venue**: *Procedia Computer Science* (Elsevier) / ICCSCI  
> **Master Blueprint**: Protocol 2 Implementation & Comparison Report  
> **Structure**: Bab 00 – 07  
> **Citation Standard**: IEEE Continuous Numbering ([1] – [32])  

---

## 1. Filosofi & Strategi Pendalaman Naskah Protocol 2

Dokumen rencana ini menyatukan seluruh elemen akademik, theoretical grounding, formulasi matematika, 3 pseudocode LaTeX, evaluasi data empiris, dan 9 integrasi visual secara utuh tanpa ada ringkasan yang memangkas kedalaman analisis (*no summarization loss*).

### Prinsip Eksekusi Utama:
1. **Tidak Ada Pemangkasan Informasi (Zero Data Loss)**: Seluruh argumen teoretis, rumus matematika, langkah 5-Whys, pseudocode LaTeX, dan tabel data empiris akan diuraikan secara komprehensif dalam paragraf-paragraf akademik bertaraf internasional (*Elsevier Procedia Computer Science*).
2. **Integrasi Visual & Data Komprehensif**: Mengintegrasikan seluruh 9 gambar grafik `.png` dengan analisis naratif yang mendalam pada setiap gambar, disertai tabel-tabel empiris pendukung.
3. **Formalisasi Matematika & 3 Pseudocode LaTeX**: Menyajikan seluruh persamaan matematis dan 3 pseudocode berformat LaTeX (gaya `algorithm` / `algorithmic` Elsevier) untuk kejelasan metodologis dan *reproducibility*.
4. **Pembahasan Kausal & Kebijakan ("Last Mile" Protocol)**: Menguraikan rantai kausal 5-Whys untuk ledakan T2 dan T5, fenomena *sub-threshold masking* ($N=1.227$), serta alur praktis penerbitan Surat Perintah Tugas (SPT) Inspektorat APIP.

---

## 2. Hasil Audit Data Empiris & Poin Data Konkret

Berdasarkan audit mendalam terhadap seluruh artefak data eksperimen, berikut adalah poin-poin data empiris konkret yang diintegrasikan secara penuh ke dalam naskah Protocol 2:

### 2.1 Studi Kasus Kegiatan Riil Siskeudes (Top-50 Expert Validation Set Audit)
Menyajikan contoh kegiatan dari transaksi *Siskeudes* riil pada tabel & analisis naratif:
- *Desa Rantau Makmur & Desa Sungai Raya (2025)*: Kegiatan "Penyertaan Modal BUMDes" (Swakelola) dengan skor LOF ekstrem mencapai **$4,78 \times 10^9$ dan $5,54 \times 10^9$** (terisolasi sebagai *local density outlier* paling tajam).
- *Desa Kedemangan (2025)*: "Kios milik Desa" (Swakelola, RDA score 0.0549, T2 Ghost).
- *Desa Bukit Suban (2024)*: "Operasional Pos Kesehatan Desa (PKD)" yang memicu **4 tipologi sekaligus** (T1 Markup, T2 Ghost, T5 Swakelola, T7 Cross-Category).
- *Desa Danau, Dsn. Baru P. Tengah, & Desa Ngaol*: Kegiatan pengadaan "Alat Produksi Peternakan", "Embung Desa", dan "Ambulance" via Pihak ke-3 yang memicu T1 Markup & T5 Procurement.

### 2.2 Profil Desa Prioritas Ekstrem (Tier 1 Summary Audit)
Menampilkan contoh desa-desa dengan akumulasi anomali terbanyak dalam panel 3 tahun:
- *Desa Maliki Air* (16 rekap anomali konsensus, T2 Ghost)
- *Desa Gedang* (13 rekap anomali konsensus, T5 Swakelola)
- *Desa Paling Serumpun* (12 rekap anomali konsensus, T5 Swakelola)
- *Desa Amar Sakti & Kampung Diilir* (11 rekap anomali konsensus)
- *Desa Lempur Mudik & Kebun Baru* (10 rekap anomali konsensus)

### 2.3 Dual Metric Exposure (Pagu vs Realisasi Keuangan)
- *Total Pagu Exposure*: Rp 6,08 Triliun dari Rp 81,49 Triliun alokasi pagu provinsi (7,46%).
- *Total Realization Exposure*: Rp 642,85 Miliar dari Rp 4,32 Triliun realisasi belanja (14,89%).

### 2.4 Matriks Konsentrasi Risiko 10 Kabupaten/Kota di Jambi
Menyajikan data 10 kabupaten secara menyeluruh di Bab 4: dari Kabupaten Batanghari (#1, rate 15,75%, 823 rekap, Rp 115,71 Miliar *at risk*) hingga Kabupaten Tanjung Jabung Barat (#10, rate 4,28%, Rp 45,23 Miliar *at risk*).

### 2.5 Matriks Overlap Jaccard Eksak Top-50 Anomali
Menjabarkan persentase irisan eksak antar-metode pada Top-50 anomali: IF vs LOF (1,01%), IF vs RDA (0,00%), LOF vs RDA (3,09%), Consensus vs RDA (96,08% capture), Consensus vs IF (0,00%).

### 2.6 Detail Audit Topology Knowledge Graph (`graphify`)
Struktur 38 nodes, 35 edges, 97% *EXTRACTED audit trail*, serta analisis *God Nodes* (`Flagged Anomaly Records`, `Engineered Feature Matrix`, `Consensus Ensemble Gate`).

---

## 3. Kajian Teori Lintas Disiplin (Interdisciplinary Theoretical Grounding)

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
   - *Relevance Cycle*, *Rigor Cycle*, *Design Cycle* (Iterasi artifact Protocol 2).

---

## 4. Formalisasi 3 Algoritma Pseudocode LaTeX (Logic Notation)

Ketiga pseudocode berformat LaTeX (gaya `algorithm` / `algorithmic` Elsevier Procedia) dimasukkan secara eksplisit pada **Bab 3 (Methodology)**:

### Algorithm 1: Year-Stratified Regional Baseline Centering and Scaling
```latex
\begin{algorithm}[H]
\caption{Year-Stratified Regional Baseline Centering and Scaling}
\label{alg:baseline_centering}
\begin{algorithmic}[1]
\REQUIRE Raw Activity Dataset $\mathcal{D} = \{x_1, x_2, \dots, x_N\}$, Category Code $c_i \in \text{Kode\_Output}$, Jurisdiction $k_i \in \text{Kabupaten\_Kota}$, Fiscal Year $t_i \in \text{Tahun}$.
\ENSURE Scaled Feature Matrix $\mathbf{X} \in \mathbb{R}^{N \times d}$.
\STATE Filter invalid records: $\mathcal{D}_{\text{clean}} \leftarrow \{x_i \in \mathcal{D} \mid \text{Volume}_i > 0 \land \text{ValidCode}(c_i)\}$.
\FOR{each unique stratum tuple $(c, k, t)$}
    \STATE Extract subgroup records: $\mathcal{S}_{c,k,t} \leftarrow \{x_i \in \mathcal{D}_{\text{clean}} \mid c_i = c \land k_i = k \land t_i = t\}$.
    \STATE Compute mean unit cost: $\mu_{c,k,t} \leftarrow \frac{1}{|\mathcal{S}_{c,k,t}|} \sum_{x \in \mathcal{S}_{c,k,t}} \text{CostPerUnit}(x)$.
    \STATE Compute std unit cost: $\sigma_{c,k,t} \leftarrow \sqrt{\frac{1}{|\mathcal{S}_{c,k,t}| - 1} \sum_{x \in \mathcal{S}_{c,k,t}} \left(\text{CostPerUnit}(x) - \mu_{c,k,t}\right)^2}$.
    \FOR{each record $x_i \in \mathcal{S}_{c,k,t}$}
        \STATE Compute centered z-score: $z_{i, \text{cat}} \leftarrow \frac{\text{CostPerUnit}(x_i) - \mu_{c,k,t}}{\sigma_{c,k,t} + \epsilon}$.
    \ENDFOR
\ENDFOR
\STATE Apply RobustScaler to continuous columns: $\mathbf{x}_i \leftarrow \frac{\mathbf{x}_i - \text{Median}(\mathbf{X})}{\text{IQR}(\mathbf{X})}$.
\RETURN Feature Matrix $\mathbf{X}$.
\end{algorithmic}
\end{algorithm}
```

---

### Algorithm 2: Dual-Path Consensus Ensemble Detection Gate
```latex
\begin{algorithm}[H]
\caption{Dual-Path Consensus Ensemble Detection Gate}
\label{alg:dual_path_ensemble}
\begin{algorithmic}[1]
\REQUIRE Feature Matrix $\mathbf{X} \in \mathbb{R}^{N \times d}$, IF contamination $c = 0.10$, LOF neighbors $k = 20$, RDA bottleneck $h = 8$, percentile threshold $q = 0.95$.
\ENSURE Consensus Flag Vector $\mathbf{y}_{\text{consensus}} \in \{0, 1\}^N$.
\STATE \textbf{Path A (Global Sparsity):} Fit Isolation Forest $\mathcal{M}_{\text{IF}}(\mathbf{X})$ with $T=200$ trees.
\FOR{each instance $i \in \{1, \dots, N\}$}
    \STATE Compute average path length $\mathbb{E}(h(x_i))$ and score $s_{\text{IF}}(x_i) = 2^{-\mathbb{E}(h(x_i))/c(n)}$.
    \STATE Assign flag: $y_{i, \text{IF}} \leftarrow \mathbf{1}\left(s_{\text{IF}}(x_i) \ge \text{Quantile}_{0.90}(s_{\text{IF}})\right)$.
\ENDFOR
\STATE \textbf{Path B (Local Density Ratio):} Compute LOF scores $\text{LOF}_k(x_i)$ using reachability distance.
\FOR{each instance $i \in \{1, \dots, N\}$}
    \STATE Assign flag: $y_{i, \text{LOF}} \leftarrow \mathbf{1}\left(\text{LOF}_k(x_i) \ge \text{Quantile}_{0.95}(\text{LOF})\right)$.
\ENDFOR
\STATE \textbf{Path C (Neural Reconstruction):} Train Autoencoder $\hat{\mathbf{x}}_i = g_{\phi}(f_{\theta}(\mathbf{x}_i))$ via MSE loss $\mathcal{L}_{\text{MSE}}$.
\FOR{each instance $i \in \{1, \dots, N\}$}
    \STATE Compute reconstruction error: $E_i = \|\mathbf{x}_i - \hat{\mathbf{x}}_i\|_2^2$.
    \STATE Assign flag: $y_{i, \text{RDA}} \leftarrow \mathbf{1}\left(E_i \ge \text{Quantile}_{0.95}(E)\right)$.
\ENDFOR
\STATE \textbf{Dual-Path Consensus Gating Logic:}
\FOR{each instance $i \in \{1, \dots, N\}$}
    \STATE $y_{i, \text{consensus}} \leftarrow y_{i, \text{LOF}} \lor \left(y_{i, \text{IF}} \land y_{i, \text{RDA}}\right)$.
\ENDFOR
\RETURN $\mathbf{y}_{\text{consensus}}$.
\end{algorithmic}
\end{algorithm}
```

---

### Algorithm 3: Operational Policy Typology Mapping and XAI Loss Attribution
```latex
\begin{algorithm}[H]
\caption{Operational Policy Typology Mapping and XAI Loss Attribution}
\label{alg:typology_xai}
\begin{algorithmic}[1]
\REQUIRE Consensus Flagged Set $\mathcal{A} = \{x_i \mid y_{i, \text{consensus}} = 1\}$, Reconstruction Errors $\{E_i\}$, Feature Matrix $\mathbf{X}$.
\ENSURE Mapped Typologies $\mathcal{T}_i \subseteq \{T_1, \dots, T_7\}$ and XAI Audit Checklists $\mathcal{C}_i$.
\FOR{each flagged instance $x_i \in \mathcal{A}$}
    \STATE Initialize typology set: $\mathcal{T}_i \leftarrow \emptyset$.
    \IF{$z_{i, \text{unit\_cost}} > 3.0 \sigma$}
        \STATE $\mathcal{T}_i \leftarrow \mathcal{T}_i \cup \{T_1 \text{ (Mark-Up)}\}$.
    \ENDIF
    \IF{$\text{AbsorptionRatio}(x_i) < 0.05 \land \text{AvgCompletion}(x_i) < 0.10$}
        \STATE $\mathcal{T}_i \leftarrow \mathcal{T}_i \cup \{T_2 \text{ (Ghost Activity)}\}$.
    \ENDIF
    \IF{$\text{SwakelolaHighValue}(x_i) = 1 \land \text{CostPerUnit}(x_i) > Q_{0.75}$}
        \STATE $\mathcal{T}_i \leftarrow \mathcal{T}_i \cup \{T_5 \text{ (Procurement Irregularity)}\}$.
    \ENDIF
    \IF{$z_{i, \text{cat}} > 3.0 \sigma$}
        \STATE $\mathcal{T}_i \leftarrow \mathcal{T}_i \cup \{T_7 \text{ (Cross-Category Dumping)}\}$.
    \ENDIF
    \IF{$\mathcal{T}_i = \emptyset$}
        \STATE $\mathcal{T}_i \leftarrow \{\text{Unclassified Subthreshold Risk}\}$.
    \ENDIF
    \FOR{each feature dimension $f \in \{1, \dots, d\}$}
        \STATE Compute per-feature loss contribution: $e_{i,f} \leftarrow \frac{(x_{i,f} - \hat{x}_{i,f})^2}{E_i}$.
    \ENDFOR
    \STATE Rank features by $e_{i,f}$ descending to construct audit checklist $\mathcal{C}_i$.
\ENDFOR
\RETURN $\{\mathcal{T}_i\}_{x_i \in \mathcal{A}}$ and $\{\mathcal{C}_i\}_{x_i \in \mathcal{A}}$.
\end{algorithmic}
\end{algorithm}
```

---

## 5. Rincian Pembagian Bab & Detail Eksekusi Naskah Protocol 2

---

### BAB 00: ABSTRACT (`00-abstract.md`)
- **Word Count Target**: ~220–250 kata.
- **Struktur Paragraf**:
  1. **Background**: Program Dana Desa (Rp 71 T/tahun, 75.259 desa) & penindakan retrospektif (lag 2–5 tahun).
  2. **Problem**: Manual audit APIP & kendala supervised ML tanpa label *ground truth* pada transaksi *Siskeudes*.
  3. **Approach**: DSR framework, Agency Theory, & Fraud Diamond. Artifact Protocol 2 menggabungkan Isolation Forest, LOF, dan 8-layer Reconstruction Dense Autoencoder (RDA) dengan *Dual-Path Consensus Gate* dan *Operational Policy Mapping Layer* pada panel 96.778 rekap kegiatan, 1.363 desa (2023–2025) di Jambi.
  4. **Key Findings**: 
     - *Dual-Path Gate* mengisolasi **7.153 rekap anomali konsensus (7,39%)**, mencakup **Rp 642,85 Miliar realisasi keuangan at risk (14,89% total alokasi Jambi)** dan **Rp 6,08 Triliun pagu exposure (7,46%)**.
     - Pergeseran tipologi utama: **T2 Ghost Activity (58,1% / 4.155 rekap)** dan **T5 Procurement Irregularity (32,8% / 2.343 rekap)**.
     - Persistensi longitudinal: **702 desa (51,5%)** terflagging 3 tahun berturut-turut.
     - Synthetic benchmark: **Precision = 0,846, Recall = 0,846, F1 = 0,846, AUC-ROC = 0,912**.
  5. **Conclusion & Impact**: Operationalisasi DeLone & McLean IS Success Model, reduksi *search space* sebesar 92,6%, dan penyediaan checklist audit XAI untuk APIP.
  6. **Keywords**: *Village Fund Governance; Unsupervised Anomaly Detection; Design Science Research; Dual-Path Consensus; Explainable AI; Corruption Typology.*

---

### BAB 01: INTRODUCTION (`01-introduction.md`)
- **Word Count Target**: ~850–1.000 kata.
- **Sub-bagian & Elaborasi Paragraf**:
  - **1.1 Background & Institutional Locus**:
    - Skala fiskal UU No. 6/2014 (Rp 71 Triliun/tahun).
    - Data empiris ICW 2024: 591 vonis pengadilan, 640 terdakwa, Rp 598,13 Miliar kerugian negara [2].
    - Statistik KPK: 851 kasus korupsi Dana Desa, >60% melibatkan Kepala Desa [3].
    - Karakteristik masalah: Penindakan reaktif (post-hoc) vs kebutuhan deteksi proaktif dalam siklus pencairan (*disbursement tranche*).
  - **1.2 Siskeudes Information System & Data Absorption Archive**:
    - Peran Siskeudes (BPKP/Kemendagri) dalam mencatat transaksi kegiatan, pagu, realisasi per tahap (T1, T2, T3), dan cara pengadaan.
    - Siskeudes sebagai *administrative signal archive* yang menyimpan pola latensi penyimpangan keuangan.
  - **1.3 Literature Gap & Design Science Research (DSR) Approach**:
    - Keterbatasan riset kualitatif retrospektif [4, 5, 6] & supervised ML [13, 14].
    - Solusi DSR (Hevner et al. [5, 10]): Mengembangkan artifact ML unsupervised multi-paradigm pada panel longitudinal 96.778 rekap (2023–2025).
  - **1.4 Case Study Locus: Jambi Province & Low-Monitoring Paradox**:
    - Anomali portal `jaga.id`: Jambi hanya mencatat 11 laporan komplain (1,4% nasional) vs Sumut (81 laporan) dan Sumsel (48 laporan) [26].
    - Teori threshold panel GMM Alfada: Ketergantungan transfer tinggi dengan pengawasan lemah menandakan *low-monitoring environment* [27].
    - 4 Kasus Yudisial Riil di Jambi:
      1. *Kasus Muara Hemat (Kerinci)*: Kerugian Rp 644 Juta, lag penindakan 5 tahun [28, 30].
      2. *Kasus Jambi Tulo (Muaro Jambi)*: Pembekuan dana desa akibat proyek fiktif >Rp 300 Juta [29].
      3. *Kasus Mantan Kades Kerinci*: Penyalahgunaan anggaran fisik Rp 644 Juta [30].
      4. *Kasus Pangkal Duri (Tanjabtim)*: Kerugian negara Rp 415 Juta [31].
    - Kesenjangan kapasitas APIP (PP No. 60/2008 & Srirejeki & Faturokhman [12]): Rasio 5–15 auditor per kabupaten.
  - **1.5 Research Questions & Academic Contributions**:
    - Formulasi RQ1, RQ2, dan RQ3.
    - 3 Kontribusi Utama: (1) *Methodological DSR Artifact*, (2) *Theoretical Agency & Fraud Diamond Grounding*, (3) *Practical APIP Decision Support & 92,6% Search Space Reduction*.

---

### BAB 02: RELATED WORK (`02-related-work.md`)
- **Word Count Target**: ~1.000–1.200 kata.
- **Sub-bagian & Elaborasi Pustaka**:
  - **2.1 Corruption Typology Frameworks**:
    - Kerangka 2 dimensi Bussell [1] (monetary vs preferential access, bureaucratic vs political governance level).
    - TASP Framework Graycar [7] (Types, Activities, Sectors, Places).
    - Taksonomi empiris Dana Desa Siregar & Aminudin [13] (5 modus: mark-up, proyek fiktif, double budgeting, manipulasi pengadaan, penyalahgunaan honorarium).
    - Analisis 200+ kasus KPK oleh Kartadinata et al. [14].
    - Validasi kontemporer Medan et al. (2025) di NTT [15].
  - **2.2 Fraud Diamond Model & Principal-Agent Foundations**:
    - Cressey's Fraud Triangle [17] & Hidajat [6]: *Pressure*, *Opportunity*, *Rationalisation*.
    - Fraud Diamond Wolfe & Hermanson [17b]: Dimensi **Capability** (monopoli otorisasi digital Siskeudes & spesimen tanda tangan rekening bank desa oleh Kepala Desa dan Kaur Keuangan).
    - Dominasi Pengadaan Swakelola (98,8% data Jambi) & Teori Pengadaan Søreide [9]: Ketidakberadaan kompetisi pasar terbuka (*competitive bidding*) sebagai enabler utama manipulasi harga dan vendor kroni.
    - Principal-Agent Theory (Groenendijk [25], Jensen & Meckling, Sutarna & Subandi): Formulasi asimetri informasi:
      $$\text{Information Asymmetry} = \mathcal{I}_{\text{Agent}}(\text{Physical Realization}, \text{True Cost}) - \mathcal{I}_{\text{Principal}}(\text{Siskeudes Reports})$$
  - **2.3 Anomaly Detection Paradigms in Public Financial Data**:
    - Isolation Forest (Liu et al. [18, 19]), Local Outlier Factor (Breunig et al. [24] — *within-group price inflation*), Deep Autoencoders (Zhou & Paffenroth [32]), Survey Multi-Paradigm (Chandola et al. [23], Stripling et al. [16]).
  - **2.4 Information Systems Success & DSR Grounding**:
    - DeLone & McLean IS Success Model (2003) [10] (*System Quality $\to$ Information Quality $\to$ Individual Impact $\to$ Organizational Impact*).
    - Mutungi et al. [5]: Penyesuaian desain algoritma dengan titik interaksi administratif (*administrative interaction points*).
    - Framework 3-Cycle Design Science Research Hevner et al. [10].

---

### BAB 03: METHODOLOGY (`03-methodology.md`)
- **Word Count Target**: ~1.400–1.600 kata.
- **Sub-bagian, Formulasi Matematika, & Diagram**:
  - **3.1 Design Science Research (DSR) Framework**:
    - 3 DSR Cycles (Relevance, Rigor, Design) + Diagram Mermaid.
  - **3.2 Dataset Pipeline & Data Hygiene Cleaning Audit**:
    - Gabungan data *Penyerapan* & *Pagu* dari portal `jaga.id` KPK [26].
    - Audit Pembersihan Data: Eliminasi **2.914 rekap invalid/volume nol** ($\text{Volume} \le 0$, kode `Kode_Output` terdistorsi, atau rekap koreksi akuntansi). Panel bersih: **96.778 rekap kegiatan**, **1.363 desa**, 3 Tahun Anggaran.
  - **3.3 Geographical Baseline Centering & Feature Matrix Table**:
    - Formulasi Matematika Z-Score Terpusat Kabupaten:
      $$z_{i,c,k,t} = \frac{x_{i,c,k,t} - \mu_{c,k,t}}{\sigma_{c,k,t}} \quad \text{dalam kelompok } (c, k, t) = (\text{Kode\_Output}, \text{Kabupaten\_Kota}, \text{Tahun})$$
    - **Tabel Matriks 27 Fitur**: Nama fitur, formulasi matematika, tipe data, dan modus korupsi yang ditargetkan (`cost_per_unit`, `absorption_ratio`, `avg_completion`, `swakelola_high_value`, `cost_deviation_by_category`, `n_stages_active`, One-Hot Encoded `activity_category`).
    - RobustScaler & Skrining Multicollinearity VIF > 5.
  - **3.4 Algorithmic Paradigm Specifications**:
    - **1. Isolation Forest**: $s(x,n) = 2^{-\frac{\mathbb{E}(h(x))}{c(n)}}$, $c=0,10$ ($N_{\text{IF}} = 9.678$ rekap / 10,0%).
    - **2. Local Outlier Factor (LOF)**: $k$-distance, reachability distance, local reachability density $\text{lrd}_k(p)$, skor $\text{LOF}_k(p)$ ($k=20$, threshold 95th percentile, $N_{\text{LOF}} = 4.839$ rekap / 5,0%).
    - **3. Reconstruction Dense Autoencoder (RDA)**: Arsitektur simetris 8-layer `[27 -> 64 -> 32 -> 16 -> 8 -> 16 -> 32 -> 64 -> 27]`, MSE loss $\mathcal{L}_{\text{MSE}}$ dengan $L_2$ regularization ($\lambda = 1\times 10^{-3}$), per-feature loss contribution $e_{i,f} = \frac{(x_{i,f} - \hat{x}_{i,f})^2}{E_i}$ ($N_{\text{RDA}} = 4.840$ rekap / 5,0%).
  - **3.5 Dual-Path Consensus Ensemble Gate**:
    - Logika Boolean: $\text{Consensus-Flag}_i = \text{LOF-Flag}_i \lor \left(\text{IF-Flag}_i \land \text{RDA-Flag}_i\right)$ + Diagram Mermaid.
    - Analisis teoretis ortogonalitas sub-ruang (*Subspace Orthogonality*).
  - **3.6 Three Formal LaTeX Pseudocode Algorithms**:
    - **Algorithm 1**: Year-Stratified Regional Baseline Centering and Scaling.
    - **Algorithm 2**: Dual-Path Consensus Ensemble Detection Gate.
    - **Algorithm 3**: Operational Policy Typology Mapping and XAI Loss Attribution.
  - **3.7 Operational Policy Mapping Layer (Typology Engine)**:
    - Aturan logika bisnis presisi untuk T1 (Mark-Up), T2 (Ghost Activity), T5 (Procurement Irregularity), T7 (Cross-Category Dumping), T4 (Stage Lock).
  - **3.8 Synthetic Fraud Benchmark Protocol**:
    - Pengujian eks-ante ($N=10.000$, 500 sampel fraud sintetis / 5,0% prevalensi).
  - **3.9 Instance-Level XAI Feature Loss Attribution**:
    - Ranking persentase kontribusi atribut untuk auditor APIP.

---

### BAB 04: RESULTS (`04-results.md`)
- **Word Count Target**: ~1.800–2.200 kata.
- **Penataan Terperinci Sub-bab, Tabel, & 9 File Grafik `.png`**:
  - **4.1 Per-Method Anomaly Rates & Year-over-Year Consistency**:
    - **Tabel 4.1**: Perbandingan Per-Metode Protocol 1 vs Protocol 2.
    - **Integrasi Grafik 1**: `![Figure 4.1: Year-over-Year Anomaly Rate Consistency Per Method](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/anomaly_rate_consistency.png)`
    - Narasi: Stabilitas LOF (4,7% $\to$ 4,6% $\to$ 5,8%) vs variansi IF (10,5% $\to$ 6,5%).
  - **4.2 Score Distribution & Bimodality Coefficient Analysis**:
    - **Tabel 4.2**: Koefisien Bimodal Sarle & Rentang Skor.
    - **Integrasi Grafik 2**: `![Figure 4.2: Score Distribution Shape and Bimodality Across Methods](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/score_distributions.png)`
    - Narasi: LOF BC = 0,957 (heavy-tailed local density isolation hingga $5,40\times 10^9$), RDA BC = 0,703 ($12.5\times$ deviasi median), IF BC = 0,335.
  - **4.3 Inter-Method Subspace Orthogonality & Overlap Matrix**:
    - **Tabel 4.3**: Matriks Irisan Pasangan Metode & Koefisien Cohen's $\kappa$.
    - Narasi: 225 rekap (0,23%) di-flag oleh ketiga metode; 3.940 rekap di-flag khusus oleh LOF.
  - **4.4 Corruption Typology Mapping & Shift Analysis**:
    - **Tabel 4.4**: Frekuensi & Pergeseran Tipologi Korupsi Protocol 1 vs Protocol 2.
    - **Integrasi Grafik 3**: `![Figure 4.3: Corruption Typology Frequency Distribution](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/typology_distribution.png)`
    - Narasi: **T2 Ghost Activity (4.155 rekap / 58,1%)** (+436,8% relatif) dan **T5 Procurement Irregularity (2.343 rekap / 32,8%)** (+8911,5% relatif).
  - **4.5 Instance-Level XAI Feature Diagnosis & RDA Error Drivers**:
    - **Integrasi Grafik 4**: `![Figure 4.4: Mean RDA Reconstruction Error per Feature and Top-50 Anomaly Heatmap](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/rda_error_decomposition.png)`
    - Narasi: Pemicu RDA error utama `cost_deviation_by_category` (2.065 rekap) dan `cost_per_unit` (1.551 rekap).
    - **Tabel 4.5**: Breakdown XAI Instance-Level Top Flagged Activities dari data *Siskeudes* riil (menyebutkan contoh *Kios milik Desa* Kedemangan, *Penyertaan Modal BUMDes* Rantau Makmur [LOF $4,78\times 10^9$], *Ambulance* Ngaol, *Pos Kesehatan Desa* Bukit Suban).
  - **4.6 Longitudinal Village Persistence & Priority Tier Classification**:
    - **Tabel 4.6**: Distribusi Tier Prioritas Desa & Persistensi Anomali.
    - **Integrasi Grafik 5**: `![Figure 4.5: Longitudinal Village Priority Tiers and Anomaly Persistence](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/village_persistence_tiers.png)`
    - Narasi: Lonjakan desa Persistensi 1,0 (3/3 tahun di-flag) dari 177 desa (13,0%) menjadi **702 desa (51,5%)**. Tier 1 mencakup **1.172 desa (86,0%)**.
    - **Highlight Desa Ekstrem Tier 1**: Menampilkan data *Desa Maliki Air* (16 rekap anomali), *Desa Gedang* (13 rekap), *Desa Paling Serumpun* (12 rekap), *Desa Amar Sakti & Kampung Diilir* (11 rekap), *Desa Lempur Mudik & Kebun Baru* (10 rekap).
  - **4.7 Spatial Projections (PCA & t-SNE)**:
    - **Integrasi Grafik 6**: `![Figure 4.6: PCA Projection — Normal vs Consensus Flagged Anomaly Records](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/pca_projection.png)`
    - **Integrasi Grafik 7**: `![Figure 4.7: t-SNE Projection — Visual Representation of Anomaly Clusters](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/tsne_projection.png)`
  - **4.8 Feature Matrix Explorations**:
    - **Integrasi Grafik 8**: `![Figure 4.8: Feature Correlation Heatmap Across 27 Variables](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/feature_correlation_heatmap.png)`
    - **Integrasi Grafik 9**: `![Figure 4.9: Feature Distributions Across Main Engineered Variables](file:///d:/Codes/research_banks/anticorr/is_dandes_anticorr/phase-1/src/v3-run/feature_distributions.png)`
  - **4.9 Synthetic Fraud Injection Benchmark Performance**:
    - **Tabel 4.7**: Hasil Evaluasi Benchmark Synthetic Fraud (IF, LOF, RDA, Protocol 1 majority, Protocol 2 Dual-Path: Precision 0.846, Recall 0.846, F1 = 0,846, AUC = 0,912).
  - **4.10 Financial Exposure & Regional Concentration Matrix**:
    - Analisis Exposure Dual Metrik: Rp 642,85 Miliar realisasi keuangan at risk (14,89%) dan Rp 6,08 Triliun Pagu Exposure (7,46%).
    - Breakdown exposure per tipologi: T1 (Rp 298,12 B), T2 (Rp 181,22 B), T5 (Rp 137,77 B), Unclassified (Rp 125,07 B).
    - **Tabel 4.8**: Matriks Konsentrasi Risiko 10 Kabupaten/Kota di Jambi Lengkap (Kabupaten Batanghari #1 dengan Anomaly Rate 15,75%, 823 rekap, Rp 115,71 Miliar at risk hingga Kabupaten Tanjung Jabung Barat #10 dengan rate 4,28%).

---

### BAB 05: DISCUSSION (`05-discussion.md`)
- **Word Count Target**: ~1.500–1.800 kata.
- **Sub-bagian & Elaborasi Temuan**:
  - **5.1 Principal Empirical Findings & Terobosan Metodologis**:
    - *Operationalizing the Operationalization Chasm*, *Overcoming Ground Truth Paradox*, *Mitigating Geographical Baseline Skew*.
  - **5.2 Deep 5-Whys Causal Chains for Typology Explosions**:
    - **Rantai Kausal 5-Whys T2 Ghost Activity ($N=4.155$)** (5 langkah eksplisit).
    - **Rantai Kausal 5-Whys T5 Procurement Irregularity ($N=2.343$)** (5 langkah eksplisit).
  - **5.3 Sub-Threshold Masking & Unclassified Anomaly Subspace ($N=1.227$)**:
    - Analisis manipulasi perataan sub-threshold (cost per unit $+1.8\sigma$, completion $-1.7\sigma$) dan pembuktian lojik jarak probabilitas gabungan LOF & RDA mengisolasi risiko Rp 125,07 Miliar.
  - **5.4 Top-50 Expert Validation Audit & Jaccard Overlap Matrix**:
    - **Tabel 5.1**: Matriks Overlap Jaccard Top-50 Antar-Model (Top 50 IF vs Top 50 RDA = 0.00% overlap; Top 50 Consensus vs Top 50 RDA = 96.08% overlap).
  - **5.5 Theoretical Implications & DSR Evaluation Matrix**:
    - **Tabel 5.2**: Matriks Evaluasi DSR Empiris (Relevance, Rigor, Design, Benchmark). Implikasi pada Agency Theory & Fraud Diamond.
  - **5.6 Practical Implications & DeLone & McLean IS Success Model**:
    - Path 1: *Information Quality $\to$ Individual Impact* (Reduksi search space 92,6%, isolasi 702 desa persistensi tinggi, XAI audit checklist).
    - Path 2: *System Quality $\to$ Organizational Impact* ("Last Mile" Protokol Audit APIP / penerbitan Surat Perintah Tugas Inspektorat).
  - **5.7 Knowledge Graph Topology Audit**:
    - Audit grafik pengetahuan 38 node, 35 edge pada Protocol 2 (God Nodes: Flagged Anomaly Records, Feature Matrix, Consensus Gate; Audit Trail 97% EXTRACTED).
  - **5.8 Study Limitations & Threats to Validity**.

---

### BAB 06: CONCLUSION (`06-conclusion.md`)
- **Word Count Target**: ~550–650 kata.
- **Sub-bagian & Sintesis Akhir**:
  - **6.1 Sintesis Jawaban RQ1, RQ2, & RQ3**.
  - **6.2 Kontribusi Akademik & Dampak Operasional**.
  - **6.3 Arah Penelitian Masa Depan**: (1) Semi-Supervised GNNs, (2) Ekstensi Multi-Provinsi, (3) Streaming API Dashboard, (4) Ex-Post Audit Referral Recovery Study.

---

### BAB 07: REFERENCES (`07-references.md`)
- **Format**: IEEE Continuous Numbering ([1] – [32]).

---

## 6. Status Rencana & Penghentian Eksekusi Total

1. Dokumen rencana ini telah **selesai diperbarui dan difinalisasi** menggabungkan seluruh detail empiris, kajian teori, dan 3 Pseudocode Algoritma LaTeX tanpa ada pemangkasan.
2. File `implementation_plan.md` telah diperbarui mencerminkan status **MASTER COMPLETE PLAN APPROVED — EXECUTION TERMINATED AS REQUESTED**.
3. **EKSEKUSI PENULISAN FILE CHAPTER (Bab 00 - 07) DIHENTIKAN SEPENUHNYA.** Agent mengakhiri giliran dan tidak melakukan penulisan file lebih lanjut.
