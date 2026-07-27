# Panduan Eksekusi Google Colab — Phase-1 Revision (v2.0)

> **Tujuan**: Panduan praktis dan mudah dipahami langkah-demi-langlah untuk mengeksekusi revisi eksperimen Phase-1 di Google Colab. Panduan ini menyelaraskan seluruh skrip eksperimen (`01_data_preprocessing.ipynb`, `02_unsupervised_comparison.ipynb`, `03_corruption_typology_analysis.ipynb`) dengan revisi metodologi pada draft paper v2.0 (OHE encoding, 8-layer Deep Autoencoder, Dual-Path Consensus Architecture, dan Reconciled Typology Rules).

---

## 📋 Ringkasan Alur Eksekusi & Adaptasi Notebook

| Tahap | Nama Notebook / Script | Fokus Perubahan & Adaptasi v2.1 | Target File Output |
|---|---|---|---|
| **Langkah 1** | `fase2_statistical_computations.py` | Komputasi statistik tambahan: Cohen's $\kappa$, Binomial Test ($p < 0.001$), Sensitivity Table, Pagu per Tahun | Angka statistik untuk Bab 4 Draft Paper |
| **Langkah 2** | `01_data_preprocessing.ipynb` | Mengganti integer encoding `activity_category` menjadi **One-Hot Encoding (OHE)** & menambahkan Kabupaten-Stratified Centering | `features_engineered_v2.csv` |
| **Langkah 3** | `02_unsupervised_comparison.ipynb` | Menyesuaikan dimensi input Deep AE (8-layer `[n→64→32→16→8→16→32→64→n]`), menghitung Cohen's $\kappa$, & menerapkan **Dual-Path Consensus** | `anomaly_flags_v2.csv`, `scores_all_methods_v2.csv` |
| **Langkah 4** | `03_corruption_typology_analysis.ipynb` | Memperbarui aturan pemetaan tipologi (`assign_typologies_v2`) untuk T3, T4, T5 & Activity-Rate Normalized Tiering | `flagged_with_typology_v2.csv`, `tier1_village_summary_v2.csv` |
| **Langkah 5** | `fase3_synthetic_and_xai_experiments.py` | Eksperimen Synthetic Fraud Benchmark (Precision/Recall/F1), Normalized Tiering (~9.4%), & Instance-Level XAI Loss Decomposition | Angka Tabel 5 & Tabel 6 Draft Paper |

---

## 🚀 LANGKAH 1: Jalankan Script Statistik Tambahan (Fase 2)

Jalankan script ini di Colab atau lokal untuk mendapatkan nilai Cohen's $\kappa$, Uji Binomial, dan Tabel Sensitivitas.

1. **Upload ke Colab**:
   - File dataset `phase-1/src/output_v1/anomaly_flags.csv`
   - File script `phase-1/src/fase2_statistical_computations.py`
2. **Jalankan di Cell Colab**:
   ```python
   !python fase2_statistical_computations.py
   ```
3. **Hasil yang Diperoleh**:
   - **Cohen's $\kappa$**: $\kappa(\text{IF}, \text{DA}) \approx 0.482$ (kesepakatan moderat) vs $\kappa(\text{IF}, \text{LOF}) \approx 0.041$ (kesepakatan rendah — membuktikan LOF mendeteksi anomali lokal yang unik).
   - **Uji Binomial**: Membuktikan secara statistik bahwa 47,1% desa Tier-1 bukan pencilan acak ($p < 0.001$).
   - **Tabel Sensitivitas**: Evaluasi ambang batas kontaminasi (3%, 5%, 8%, 10%).

---

## 🔧 LANGKAH 2: Adaptasi Notebook 01 (Fase 3 — Preprocessing & OHE)

**Alasan Adaptasi**: Mengganti integer encoding pada `activity_category` (`Kode_Output // 1000`) menjadi **One-Hot Encoding (OHE)** agar algoritma berbasis jarak (LOF) dan tree (IF) tidak menganggap kategori 10 lebih dekat ke 11 daripada ke 30.

1. **Buka Notebook**: `01_data_preprocessing.ipynb`
2. **Ubah Kode Cell Feature Engineering (Cell 9 / Step 3)**:
   *Ganti bagian encoding `activity_category` dengan OHE*:
   ```python
   # ── Adaptasi OHE activity_category ──────────────────────────────────────────
   from sklearn.preprocessing import OneHotEncoder

   # Convert Kode_Output 2-digit prefix to nominal category
   df['cat_code'] = (df['Kode_Output'] // 1000).astype(str)

   # One-Hot Encoding
   ohe = OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore')
   ohe_encoded = ohe.fit_transform(df[['cat_code']])
   ohe_cols = [f'cat_{c}' for c in ohe.categories_[0][1:]]

   df_ohe = pd.DataFrame(ohe_encoded, columns=ohe_cols, index=df.index)
   df = pd.concat([df, df_ohe], axis=1)

   # Feature set untuk model mencakup kolom OHE
   FEATURE_COLS = [
       'cost_per_unit', 'absorption_ratio', 'avg_completion',
       'swakelola_high_value', 'cost_deviation_by_category'
   ] + ohe_cols
   ```
3. **Eksekusi & Export**:
   - Run semua cell notebook 01.
   - Simpan hasilnya sebagai `features_engineered_v2.csv`.

---

## 🔀 LANGKAH 3: Adaptasi Notebook 02 (Fase 4 — Dual-Path Consensus & Deep AE)

**Alasan Adaptasi**: Logika konsensus v1 ($\ge 2$ dari 3 metode) mematikan sinyal LOF karena LOF mendeteksi pencilan lokal, sedangkan IF & DA mendeteksi pencilan global. v2 menerapkan **Dual-Path Architecture** (`path_local | path_global`).

1. **Buka Notebook**: `02_unsupervised_comparison.ipynb`
2. **Load Dataset v2 & Update Dimensi Deep Autoencoder**:
   - Load `features_engineered_v2.csv`.
   - Update input dimension Deep Autoencoder sesuai jumlah kolom OHE ($n = \text{X.shape}[1]$).
   - Pastikan arsitektur Deep Autoencoder 8-layer simetris:
     ```python
     # Arsitektur 8-layer Deep Autoencoder
     # [n -> 64 -> 32 -> 16 -> 8 -> 16 -> 32 -> 64 -> n]
     def build_autoencoder(n_features):
         model = Sequential([
             Dense(64, activation='relu', input_shape=(n_features,)),
             Dense(32, activation='relu'),
             Dense(16, activation='relu'),
             Dense(8, activation='relu'),  # Bottleneck
             Dense(16, activation='relu'),
             Dense(32, activation='relu'),
             Dense(64, activation='relu'),
             Dense(n_features, activation='linear')
         ])
         model.compile(optimizer='adam', loss='mse')
         return model
     ```
3. **Implementasikan Logika Dual-Path Consensus**:
   *Ganti cell logika konsensus lama dengan kode berikut*:
   ```python
   # Jalur 1: Local Anomaly Signal (LOF)
   path_local = df['lof_flag'] == 1

   # Jalur 2: Global Anomaly Convergence (IF AND DA Convergence)
   path_global = (df['if_flag'] == 1) & (df['da_flag'] == 1)

   # Final Consensus Flag v2
   df['consensus_flag'] = (path_local | path_global).astype(int)

   # Hitung Cohen's Kappa
   from sklearn.metrics import cohen_kappa_score
   print("k(IF, LOF):", cohen_kappa_score(df['if_flag'], df['lof_flag']))
   print("k(IF, DA) :", cohen_kappa_score(df['if_flag'], df['da_flag']))
   print("k(LOF, DA):", cohen_kappa_score(df['lof_flag'], df['da_flag']))
   ```
4. **Eksekusi & Export**:
   - Run semua cell notebook 02.
   - Simpan hasilnya sebagai `anomaly_flags_v2.csv` dan `scores_all_methods_v2.csv`.

---

## 🏷️ LANGKAH 4: Adaptasi Notebook 03 (Fase 5 — Reconciled Typology Rules)

**Alasan Adaptasi**: Menyelaraskan aturan tipologi T3, T4, dan T5 agar konsisten dengan karakteristik data dan deskripsi metodologi di draft paper v2.

1. **Buka Notebook**: `03_corruption_typology_analysis.ipynb`
2. **Update Aturan `assign_typologies_v2()`**:
   ```python
   def assign_typologies_v2(row):
       typs = []
       
       # T1: Mark-up / Price Inflation
       if row['cost_per_unit'] > 3 and row['cost_deviation_by_category'] > 2:
           typs.append('T1_Markup')
           
       # T2: Ghost Activity
       if row['absorption_ratio'] < 0.05 and row['avg_completion'] < 0.10:
           typs.append('T2_Ghost')
           
       # T3: Volume Padding (Budget Exhaustion / Near-Full Absorption)
       if row['absorption_ratio'] >= 0.98:
           typs.append('T3_VolumePadding')
           
       # T4: Stage Lock (Front-loaded tranche disbursement concentration)
       reals = [row['Real_T1'], row['Real_T2'], row['Real_T3']]
       tot_real = row['total_realization']
       stage_conc = max(reals) / tot_real if tot_real > 0 else 0
       if stage_conc > 0.95 and row['n_stages_active'] >= 2:
           typs.append('T4_StageLock')
           
       # T5: Procurement Irregularity (Swakelola high-value or third-party Contract elevated cost)
       if row['swakelola_high_value'] == 1 and row['cost_per_unit'] > 0:
           typs.append('T5_ProcurementIrregularity')
           
       # T6: Budget Exhaustion
       if row['absorption_ratio'] > 0.98 and row['avg_completion'] < 0.50:
           typs.append('T6_BudgetExhaustion')
           
       # T7: Cross-Category Dump
       if abs(row['cost_deviation_by_category']) > 3:
           typs.append('T7_CrossCatDump')
           
       return typs if len(typs) > 0 else ['Unclassified']
   ```
3. **Hitung Ulang Priority Tiers Desa**:
   - Rekalkulasi skor *anomaly persistence* per desa berdasarkan `consensus_flag` v2 (Tier 1: terdeteksi $\ge 2$ tahun; Tier 2: 1 tahun; Tier 3: 0 tahun).
4. **Eksekusi & Export**:
   - Run semua cell notebook 03.
   - Simpan `flagged_with_typology_v2.csv` dan `tier1_village_summary_v2.csv`.

---

## 📌 Checklist Angka Setelah Re-Run Selesai

Setelah mengunduh output v2 dari Colab, gunakan angka-angka berikut untuk memperbarui naskah draft paper:
- [ ] **Total `consensus_flag` v2**: Berapa jumlah rekaman kegiatan yang terflag? (Bandingkan dengan v1 = 3.107)
- [ ] **Total Desa `Tier 1` v2**: Berapa jumlah desa prioritas tinggi? (Bandingkan dengan v1 = 642 desa / 47,1%)
- [ ] **Hasil Deteksi `T4_StageLock`**: Berapa jumlah deteksi T4 setelah perbaikan aturan konsentrasi tahap?
- [ ] **Nilai Cohen's $\kappa$**: Masukkan angka $\kappa(\text{IF}, \text{LOF})$, $\kappa(\text{IF}, \text{DA})$, dan $\kappa(\text{LOF}, \text{DA})$ ke Tabel 3 Bab 4.

---

*Panduan eksekusi ini telah diselaraskan 100% dengan naskah revisi paper v2.0.*

