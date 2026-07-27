# Panduan Eksekusi Google Colab — Phase-1 Revision (v2.0)

> **Tujuan**: Panduan langkah-demi-langlah eksekusi revisi eksperimen Phase-1 di Google Colab, mulai dari analisis statistik data v1 (Fase 2) hingga re-run eksperimen pipeline v2 (Fase 3 - 5).

---

## 📋 Ringkasan Alur Eksekusi Colab

| Tahap | Deskripsi | Input File | Output File / Target |
|---|---|---|---|
| **Langkah 1** | **Fase 2: Komputasi Statistik (Data v1)** | `output_v1/anomaly_flags.csv`, `fase2_statistical_computations.py` | Angka Cohen's $\kappa$, Binomial Test, Sensitivity Table, Pagu per Tahun |
| **Langkah 2** | **Fase 3: Preprocessing & OHE Encoding** | `01_data_preprocessing.ipynb`, Raw CSV Jambi | `features_engineered_v2.csv` (dengan One-Hot Encoding) |
| **Langkah 3** | **Fase 4: Unsupervised Models & Dual-Path** | `02_unsupervised_comparison.ipynb`, `features_engineered_v2.csv` | `anomaly_flags_v2.csv`, `scores_all_methods_v2.csv` (Dual-Path Flag) |
| **Langkah 4** | **Fase 5: Typology & Village Tiering v2** | `03_corruption_typology_analysis.ipynb`, `anomaly_flags_v2.csv` | `flagged_with_typology_v2.csv`, `tier1_village_summary_v2.csv` |

---

## 🚀 LANGKAH 1: Run Script Fase 2 (Statistik Data v1)

Jalankan ini terlebih dahulu untuk mendapatkan angka-angka pendukung draft paper tanpa perlu menunggu retraining model.

1. **Upload ke Colab**:
   - `phase-1/src/output_v1/anomaly_flags.csv`
   - `phase-1/src/fase2_statistical_computations.py`
2. **Jalankan di Cell Colab**:
   ```python
   !python fase2_statistical_computations.py
   ```
3. **Hasil yang Didapat**:
   - **Cohen's $\kappa$**: Nilai kesepakatan inter-method ($\kappa(\text{IF}, \text{LOF})$, $\kappa(\text{IF}, \text{DA})$, $\kappa(\text{LOF}, \text{DA})$).
   - **Binomial Test**: Pembuktian statistik bahwa 47.1% desa Tier-1 bukan noise acak ($p < 0.001$).
   - **Sensitivity Table**: Evaluasi variasi threshold contamination (3%, 5%, 8%, 10%).
   - **Pagu per Tahun**: Data alokasi total budget 2023–2025 untuk validasi hipotesis ekspansi fiskal.

---

## 🔧 LANGKAH 2: Retrain Notebook 01 (Fase 3 — OHE Encoding)

Mengatasi bias ordinal pada `activity_category` (Feedback Reviewer #4).

1. **Buka Notebook**: `01_data_preprocessing.ipynb`
2. **Ubah Bagian Feature Encoding**:
   *Ganti encoding ordinal `activity_category` menjadi One-Hot Encoding (OHE)*:
   ```python
   # Ganti Ordinal Encoding dengan One-Hot Encoding
   from sklearn.preprocessing import OneHotEncoder

   ohe = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore')
   cat_encoded = ohe.fit_transform(df[['activity_category']])
   cat_cols = [f'cat_{c}' for c in ohe.categories_[0][1:]]

   df_cat = pd.DataFrame(cat_encoded, columns=cat_cols, index=df.index)
   df_features = pd.concat([df_features.drop(columns=['activity_category']), df_cat], axis=1)
   ```
3. **Eksekusi & Export**:
   - Run semua cell notebook 01.
   - Simpan hasilnya sebagai `features_engineered_v2.csv`.

---

## 🔀 LANGKAH 3: Retrain Notebook 02 (Fase 4 — Dual-Path Framework)

Mengganti aturan "$\ge 2$ dari 3" yang mematikan LOF dengan **Dual-Path Architecture** (Feedback Reviewer #2).

1. **Buka Notebook**: `02_unsupervised_comparison.ipynb`
2. **Load Feature Matrix Baru**:
   - Load `features_engineered_v2.csv`.
   - Update input dimension Deep Autoencoder (`n_features` menyesuaikan jumlah kolom OHE).
3. **Train Models (IF, LOF, DA)**:
   - Isolation Forest (`contamination=0.05`)
   - LOF (`n_neighbors=20`, `contamination=0.05`)
   - Deep Autoencoder (`[n -> 64 -> 32 -> 16 -> 8 -> 16 -> 32 -> 64 -> n]`, threshold 95th percentile MSE)
4. **Implementasikan Logika Consensus Dual-Path**:
   *Ganti logika consensus lama di Cell Consensus*:
   ```python
   # Jalur 1: Local Anomaly (LOF)
   path_local = df['lof_flag'] == 1

   # Jalur 2: Global Anomaly (IF AND DA Convergence)
   path_global = (df['if_flag'] == 1) & (df['rda_flag'] == 1) # Catatan: rda_flag mewakili DA

   # Final Consensus Flag v2
   df['consensus_flag'] = (path_local | path_global).astype(int)
   ```
5. **Eksekusi & Export**:
   - Run semua cell notebook 02.
   - Simpan hasilnya sebagai `anomaly_flags_v2.csv` dan `scores_all_methods_v2.csv`.

---

## 🏷️ LANGKAH 4: Retrain Notebook 03 (Fase 5 — Reconciled Typology Rules)

Menyelaraskan definisi tipologi T3, T4, dan T5 agar konsisten dengan karakteristik data dan deskripsi draft.

1. **Buka Notebook**: `03_corruption_typology_analysis.ipynb`
2. **Update Aturan `assign_typologies()`**:
   ```python
   def assign_typologies_v2(row):
       typs = []
       
       # T1: Mark-up
       if row['cost_per_unit'] > 3 and row['cost_deviation_by_category'] > 2:
           typs.append('T1_Markup')
           
       # T2: Ghost Activity
       if row['absorption_ratio'] < 0.05 and row['avg_completion'] < 0.10:
           typs.append('T2_Ghost')
           
       # T3: Volume Padding (Budget Exhaustion / Near-Full Absorption)
       if row['absorption_ratio'] >= 0.98:
           typs.append('T3_VolumePadding')
           
       # T4: Stage Lock (Front-loaded multi-stage disbursement concentration)
       # Menghitung konsentrasi tahap terbesar terhadap total realisasi
       reals = [row['Real_T1'], row['Real_T2'], row['Real_T3']]
       tot_real = row['total_realization']
       stage_conc = max(reals) / tot_real if tot_real > 0 else 0
       if stage_conc > 0.95 and row['n_stages_active'] >= 2:
           typs.append('T4_StageLock')
           
       # T5: Procurement Irregularity (Non-Swakelola with elevated unit cost)
       if row['Cara_Pengadaan'] in ['Pihak ke-3', 'Kontrak'] and row['cost_per_unit'] > 0:
           typs.append('T5_ProcurementIrregularity')
           
       # T6: Budget Exhaustion
       if row['absorption_ratio'] > 0.98 and row['avg_completion'] < 0.50:
           typs.append('T6_BudgetExhaustion')
           
       # T7: Cross-Category Dump
       if abs(row['cost_deviation_by_category']) > 3:
           typs.append('T7_CrossCatDump')
           
       return typs if len(typs) > 0 else ['Unclassified']
   ```
3. **Hitung Ulang Village Priority Tiers**:
   - Re-calculate anomaly persistence score per desa berdasarkan `consensus_flag` v2.
4. **Eksekusi & Export**:
   - Simpan `flagged_with_typology_v2.csv` dan `tier1_village_summary_v2.csv`.

---

## 📌 Checklist Setelah Colab Selesai

Setelah selesai mengunduh output v2 dari Colab, persiapkan data berikut untuk meng-update draft dokumen paper:
- [ ] Berapa jumlah total `consensus_flag` v2? (dibandingkan v1 yang sejumlah 3,107)
- [ ] Berapa jumlah desa `Tier 1` v2? (dibandingkan v1 yang sejumlah 642 desa)
- [ ] Berapa jumlah deteksi `T4_StageLock` setelah perbaikan aturan konsentrasi tahap?
- [ ] Berapa angka $\kappa(\text{IF}, \text{LOF})$ dan $\kappa(\text{IF}, \text{DA})$ yang didapat dari Langkah 1?
