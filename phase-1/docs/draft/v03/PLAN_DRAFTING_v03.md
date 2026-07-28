# Rencana Drafting & Structure Blueprint — Version 3 (v03)
## Reconstruction & Expansion of Research Draft based on v01 Structure & v3-run Empirical Results

> **Target Venue**: *Procedia Computer Science* (Elsevier) / ICCSCI  
> **Draft Version**: v03  
> **Base Structure**: `docs/draft/v01/` (Chapters 00 to 07)  
> **Primary Data & Results Source**: `src/v3-run/COMPARISON_REPORT_v3_vs_v1.md`, `src/v3-run/analysis_report_v3.md`, `docs/evaluation/pipeline_output_evaluation_v3.md`  
> **Literature & Reference Base**: `docs/draft/v01/07-references.md` (IEEE format)  
> **Knowledge Graph Audit**: `src/v3-run/graphify-out/`  

---

## 1. Executive Summary & Objective

Tujuan dari penulisan ulang draft **v03** ini adalah memperbarui keseluruhan naskah ilmiah (*research paper*) agar mencerminkan secara penuh hasil empiris dan terobosan metodologis dari pipeline **`v3-run`**, dengan tetap mempertahankan struktur bab yang teruji pada **`v01`** (`00-abstract.md` hingga `07-references.md`).

### Inovasi Metodologis Utama di v03:
1. **Dual-Path Consensus Ensemble Gate**: Menggantikan aturan *majority voting* kaku pada v1 dengan penggabungan *Local Outlier Factor* (Local Density Path) dan *Isolation Forest $\cap$ Reconstruction Dense Autoencoder* (Global Convergence Path).
2. **Lonjakan Anomaly Recall & Sensitivitas**: Consensus flags meningkat dari 3,107 rekap (3.12%) pada v1 menjadi **7,153 rekap (7.39%)** pada v3-run, mengidentifikasi Rp 642.85 Miliar (*realized expenditure at risk*).
3. **Pergeseran Tipologi Korupsi Utama**: 
   - **T2 Ghost Activity (*Kegiatan Fiktif*)** melonjak 5.4x menjadi tipologi utama (**4,155 rekap / 58.1%**).
   - **T5 Procurement Irregularity (*Swakelola High Value*)** melonjak 90x (**2,343 rekap / 32.8%**).
4. **Analisis Longitudinal & Prioritas Audit**: 
   - Desa dengan persistensi anomali 3/3 tahun bertambah 4x menjadi **702 desa (51.5%)**.
   - Desa Prioritas Audit **Tier 1** mencakup **1,172 desa (86.0%)**.
5. **Evaluasi Benchmark Synthetic Fraud**: Mencapai **Precision = 0.846, Recall = 0.846, F1 = 0.846, AUC-ROC = 0.912**.

---

## 2. Rencana Pembagian Bab & Detail Konten v03

### `00-abstract.md` — Abstract & Keywords
- **Target Line/Word Count**: Max 200–250 kata.
- **Struktur**: Background → Problem → Approach → Key Findings → Conclusion & Impact.
- **Key Empirical Updates**:
  - Panel data: 96,778 rekap kegiatan, 1,363 desa, 3 Tahun Anggaran (2023–2025) di Provinsi Jambi.
  - Dual-Path Consensus Gate: 7,153 rekap (7.39%) consensus flags.
  - Tipologi dominan: T2 Ghost Activity (58.1%) & T5 Procurement Irregularity (32.8%).
  - Risk exposure: Rp 642.85 Miliar (14.89% dari total realisasi Dana Desa Jambi).
  - Synthetic benchmark: F1 = 0.846, AUC-ROC = 0.912.
  - Reduksi pencarian audit (search space reduction): 92.6%.

---

### `01-introduction.md` — Chapter 1: Introduction
- **Target Word Count**: ~700–800 kata.
- **Struktur Paragraf & Pokok Bahasan**:
  1. *Konteks Skala Dana Desa & Masalah Monitoring*: Alokasi Rp 71 Triliun/tahun, 591 vonis pengadilan (ICW 2024), 851 kasus KPK. Masalah utama: monitoring bersifat reaktif (lag 2–5 tahun).
  2. *Infrastruktur Siskeudes & Data Absorption*: Data transaksi Siskeudes via portal `jaga.id` sebagai arsip sinyal administratif real-time.
  3. *Gap Literatur & Pendekatan DSR*: Mengisi kekosongan antara analisis retrospektif dan supervised learning (yang membutuhkan label *ground truth* yang tidak tersedia).
  4. *Signifikansi Provinsi Jambi*: Rendahnya laporan komplain di `jaga.id` (1.4% nasional) menandakan *low-monitoring environment*, diperkuat oleh 4 kasus pidana riil di Jambi (Kerinci, Muaro Jambi, Tanjabtim) dengan total kerugian Rp 2.3 Miliar.
  5. *3 Kontribusi Utama & 3 Research Questions (RQs)*:
     - RQ1: Feature constructs mana yang paling diskriminatif?
     - RQ2: Algoritma mana (IF, LOF, RDA) dan arsitektur konsensus mana yang memberikan performa terbaik?
     - RQ3: Bagaimana pemetaan anomali ke tipologi korupsi riil & penjelasan XAI untuk inspektorat (APIP)?
  6. *Sistematika Organisasi Naskah*.

---

### `02-related-work.md` — Chapter 2: Related Work
- **Target Word Count**: ~800–900 kata.
- **Struktur Sub-bab & Referensi (dari v01 Part 07)**:
  - **2.1 Corruption Typology Frameworks**: Bussell [1], Graycar (TASP framework) [7], Siregar & Aminudin (5 modus Dana Desa Jatim) [13], Kartadinata et al. (analisis 200+ kasus KPK) [14], Medan et al. (2025) [15].
  - **2.2 Fraud Diamond/Triangle & Principal-Agent Foundations**: Cressey (Fraud Triangle) [17], Wolfe & Hermanson (Fraud Diamond) [17b], Hidajat (Dana Desa context) [6], Søreide (procurement corruption & Swakelola dominance 98.8%) [9], Principal-Agent Theory (Groenendijk [25], Jensen & Meckling, Sutarna & Subandi).
  - **2.3 Anomaly Detection in Public Financial Data**: Multi-paradigm unsupervised ML: Isolation Forest (Liu et al.) [18, 19], Local Outlier Factor (Breunig et al.) [24], Deep Autoencoders (Zhou & Paffenroth) [32], Survey Anomaly Detection (Chandola et al.) [23].
  - **2.4 Information Systems Grounding**: DeLone & McLean IS Success Model (2003) [10] (Information Quality → Individual/Organizational Impact), Mutungi et al. (digital anti-corruption typology) [5], Hevner et al. (DSR methodology) [10].

---

### `03-methodology.md` — Chapter 3: Methodology
- **Target Word Count**: ~1,100–1,300 kata.
- **Struktur Sub-bab & Formalisasi Matematika**:
  - **3.1 Design Science Research (DSR) Framework**: 3 DSR Cycles (Relevance, Rigor, Design).
  - **3.2 Dataset & Data Cleaning Audit**: Pagu + Penyerapan longitudinal panel (2023–2025). Audit pembersihan data: pemfilteran 2,914 rekap invalid/volume nol (dari 99,692 di v1 menjadi 96,778 rekap di v3).
  - **3.3 Geographical Baseline Centering & Feature Engineering**: 
    - Formulasi `cost_deviation_by_category` tersentralisasi per `(Kode_Output, Kabupaten_Kota, Tahun)`.
    - Matriks 27 fitur (termasuk `cost_per_unit`, `avg_completion`, `swakelola_high_value`, dll.).
    - RobustScaler & eliminasi VIF multicollinearity.
  - **3.4 Detection Algorithms Mathematical Specification**:
    - Isolation Forest ($s(x,n) = 2^{-\frac{\mathbb{E}(h(x))}{c(n)}}$, contamination $c=0.10$).
    - Local Outlier Factor ($\text{LOF}_k(p)$, $k=20$, 95th percentile threshold).
    - Reconstruction Dense Autoencoder (RDA 8-layer `[27 -> 64 -> 32 -> 16 -> 8 -> 16 -> 32 -> 64 -> 27]`, MSE loss + $L_2$ regularization).
  - **3.5 Dual-Path Consensus Ensemble Gate**:
    - Formulasi: $\text{Consensus-Flag}_i = \text{LOF-Flag}_i \lor \left(\text{IF-Flag}_i \land \text{RDA-Flag}_i\right)$.
    - Justifikasi teoretis ortogonalitas ruang bagian (subspace orthogonality) & analisis 5-Whys.
  - **3.6 Operational Policy Mapping Layer (Typology Engine)**: Regulasi aturan bisnis untuk T1–T7.
  - **3.7 Synthetic Fraud Injection Benchmark Protocol**: Protokol pengujian eks-ante ($N=10,000$, 500 sampel fraud sintetis).
  - **3.8 Instance-Level XAI Loss Attribution**: Dekomposisi per-fitur MSE loss $e_{i,f} = \frac{(x_{i,f} - \hat{x}_{i,f})^2}{E_i}$.

---

### `04-results.md` — Chapter 4: Results
- **Target Word Count**: ~1,400–1,600 kata.
- **Daftar Grafik `.png` yang Wajib Diintegrasikan**:
  1. `anomaly_rate_consistency.png` → Integrasi di **§4.1**: Stabilitas flagging per-metode per-tahun.
  2. `score_distributions.png` → Integrasi di **§4.2**: Histogram skor & Bimodality Coefficient (LOF BC=0.957, RDA BC=0.703, IF BC=0.335).
  3. `typology_distribution.png` → Integrasi di **§4.4**: Distribusi 7 tipologi korupsi (T2 Ghost 58.1%, T5 Procurement 32.8%, T7 Cross-Cat 18.0%, T1 Markup 16.5%, T4 Stage Lock 0.4%, Unclassified 17.2%).
  4. `rda_error_decomposition.png` → Integrasi di **§4.5**: Fitur pemicu RDA error utama (`cost_deviation_by_category` & `cost_per_unit`) & Top-50 heatmap.
  5. `village_persistence_tiers.png` → Integrasi di **§4.6**: Persistensi desa 3/3 tahun (702 desa / 51.5%) & Prioritas Tier 1 (1,172 desa / 86.0%).
  6. `pca_projection.png` → Integrasi di **§4.7**: Proyeksi PCA 2D normal vs anomali.
  7. `tsne_projection.png` → Integrasi di **§4.7**: Proyeksi t-SNE 2D kluster anomali.
  8. `feature_correlation_heatmap.png` → Integrasi di **§4.8**: Heatmap korelasi 27 fitur.
  9. `feature_distributions.png` → Integrasi di **§4.8**: Distribusi bentuk fitur-fitur utama.

- **Detail Sub-bab & Tabel Hasil Utama**:
  - **Tabel 4.1**: Per-Method Anomaly Rates (IF: 9,678 / 10.0%, LOF: 4,839 / 5.0%, RDA: 4,840 / 5.0%, Consensus: 7,153 / 7.39%).
  - **Tabel 4.2**: Bimodality Coefficient & Range Score.
  - **Tabel 4.3**: Matriks Overlap Inter-Metode & Jaccard Index Top-50 (Ortogonalitas sub-ruang).
  - **Tabel 4.4**: Frekuensi & Pergeseran Tipologi Korupsi v1 vs v3-run.
  - **Tabel 4.5**: Breakdown XAI Instance-Level Top Flagged Activities.
  - **Tabel 4.6**: Matriks Prioritas Desa & Persistensi Multi-Tahun.
  - **Tabel 4.7**: Hasil Evaluasi Benchmark Synthetic Fraud (Precision, Recall, F1=0.846, AUC=0.912).
  - **Tabel 4.8**: Financial Exposure & Konsentrasi Risiko Regional (Kabupaten Batanghari 15.75% anomaly rate, Rp 115.7M at risk).

---

### `05-discussion.md` — Chapter 5: Discussion
- **Target Word Count**: ~1,100–1,300 kata.
- **Struktur Discussion**:
  - **5.1 Principal Empirical Findings & Terobosan v3-run**: Mengatasi *Operationalization Chasm*, *Ground Truth Paradox*, dan *Geographical Baseline Skew*.
  - **5.2 Analisis Kausal 5-Whys**:
    - *5-Whys Ledakan T2 Ghost Activity ($N=4,155$)*: Mengapa LOF menangkap kegiatan fiktif yang terlewat oleh IF global splits.
    - *5-Whys Lonjakan T5 Procurement Irregularity ($N=2,343$)*: Mengapa RDA non-linear interaksi menangkap manipulasi Swakelola tanpa bidding.
  - **5.3 Sub-Threshold Masking & Subspace Unclassified ($N=1,227$)**: Mengapa 1,227 rekap lolos dari rule heuristik tunggal tetapi tertangkap oleh ensemble ML multi-dimensi (risiko terselubung Rp 125.07 Miliar).
  - **5.4 Implikasi Teoretis**: Kontribusi pada IS Theory, Agency Theory, Fraud Diamond, dan DSR Evaluation Framework.
  - **5.5 Implikasi Praktis & D&M IS Success Model**: Operationalisasi *Information Quality $\to$ Individual Impact* (reduksi search space 92.6%, checklist audit XAI) dan *System Quality $\to$ Organizational Impact* ("Last Mile" Protokol Audit APIP / Surat Perintah Tugas).
  - **5.6 Audit Knowledge Graph Topology (`graphify`)**: Hasil audit grafik pengetahuan 38 node, 35 edge di `v3-run/graphify-out/` (God nodes: Flagged Anomaly Records, Feature Matrix, Consensus Gate).
  - **5.7 Keterbatasan Penelitian (Limitations)**.

---

### `06-conclusion.md` — Chapter 6: Conclusion
- **Target Word Count**: ~450–550 kata.
- **Struktur**:
  - Jawaban atas RQ1 (Fitur diskriminatif & pergeseran ke `cost_deviation_by_category`), RQ2 (Superioritas Dual-Path Consensus AUC=0.912), dan RQ3 (Tipologi T2/T5 & XAI audit checklist).
  - Ringkasan Dampak Operasional: 96,778 rekap $\to$ 7,153 anomali konsensus (reduksi 92.6%), 702 desa persistensi tinggi.
  - Keterbatasan utama (skop 1 provinsi).
  - Arah Penelitian Masa Depan: Graph Neural Networks (GNN) semi-supervised untuk compound fraud, ekstensi multi-provinsi, integrasi dashboard real-time API Siskeudes.

---

### `07-references.md` — Chapter 7: References
- **Format**: IEEE (penomoran kontinu [1] – [32]).
- **Sumber**: Mempertahankan daftar referensi terverifikasi dari v01 Part 07 (Undang-Undang, laporan ICW/KPK, jurnal Scopus/ISI, literatur ML & DSR).

---

## 3. Matriks Pemetaan Grafik `.png` ke Bab

| Nama File Grafik `.png` (di `src/v3-run/`) | Bab Penempatan | Nomor Gambar & Deskripsi |
|---|---|---|
| `anomaly_rate_consistency.png` | `04-results.md` | **Figure 4.1**: Trend & konsistensi anomaly rate per-tahun per-metode |
| `score_distributions.png` | `04-results.md` | **Figure 4.2**: Histogram skor anomaly & Bimodality Coefficient |
| `typology_distribution.png` | `04-results.md` | **Figure 4.3**: Distribusi frekuensi 7 tipologi korupsi (v3-run) |
| `rda_error_decomposition.png` | `04-results.md` | **Figure 4.4**: Dekomposisi RDA reconstruction error & Top-50 Heatmap |
| `village_persistence_tiers.png` | `04-results.md` | **Figure 4.5**: Klasifikasi desa prioritas audit (Tier 1, 2, 3) & Persistensi |
| `pca_projection.png` | `04-results.md` | **Figure 4.6**: Proyeksi PCA 2D normal vs consensus-flagged anomalies |
| `tsne_projection.png` | `04-results.md` | **Figure 4.7**: Proyeksi t-SNE 2D representasi visual anomaly clusters |
| `feature_correlation_heatmap.png` | `04-results.md` | **Figure 4.8**: Heatmap korelasi inter-fitur pada matriks 27 variabel |
| `feature_distributions.png` | `04-results.md` | **Figure 4.9**: Distribusi statistik fitur-fitur penanda korupsi |

---

## 4. Checklist Eksekusi Drafting v03

- [x] Membuat blueprint rencana drafting `PLAN_DRAFTING_v03.md` di `docs/draft/v03/`
- [ ] Membuat file `docs/draft/v03/00-abstract.md`
- [ ] Membuat file `docs/draft/v03/01-introduction.md`
- [ ] Membuat file `docs/draft/v03/02-related-work.md`
- [ ] Membuat file `docs/draft/v03/03-methodology.md`
- [ ] Membuat file `docs/draft/v03/04-results.md`
- [ ] Membuat file `docs/draft/v03/05-discussion.md`
- [ ] Membuat file `docs/draft/v03/06-conclusion.md`
- [ ] Membuat file `docs/draft/v03/07-references.md`
