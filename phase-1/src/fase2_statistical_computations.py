"""
FASE 2 --- Komputasi Statistik Tambahan
Script untuk Google Colab / Jupyter --- tidak memerlukan eksperimen ulang
Jalankan ini SEBELUM re-run eksperimen v2 (Fase 3+)

Input: anomaly_flags.csv (sudah ada di output_v1/)
Output: Angka-angka yang akan dimasukkan ke draft paper

Tanggal: Juli 2026
"""

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from scipy import stats
from scipy.stats import binom, ks_2samp

# ============================================================
# LOAD DATA
# ============================================================
# Sesuaikan path jika di Colab
CSV_PATH = 'phase-1/src/output_v1/anomaly_flags.csv'

print("Loading data...")
df = pd.read_csv(CSV_PATH)
print(f"Loaded: {df.shape[0]:,} records, {df.shape[1]} columns")
print()

# ============================================================
# F2.1 --- COHEN'S KAPPA: INTER-METHOD AGREEMENT
# ============================================================
print("=" * 60)
print("F2.1 --- COHEN'S KAPPA (inter-method pairwise agreement)")
print("=" * 60)

kappa_if_lof = cohen_kappa_score(df['if_flag'], df['lof_flag'])
kappa_if_rda = cohen_kappa_score(df['if_flag'], df['rda_flag'])
kappa_lof_rda = cohen_kappa_score(df['lof_flag'], df['rda_flag'])

print(f"k(IF, LOF) = {kappa_if_lof:.4f}")
print(f"k(IF, DA)  = {kappa_if_rda:.4f}")
print(f"k(LOF, DA) = {kappa_lof_rda:.4f}")
print()
if kappa_if_lof < kappa_if_rda:
    print("CONFIRMED: k(IF,LOF) < k(IF,DA) --- supports dual-path framework rationale")

print()
print(">>> TABLE FOR para 4.3 (replace placeholders in results draft):")
print(f"| IF & LOF | 317 | 6.4% | k = {kappa_if_lof:.3f} |")
print(f"| IF & DA  | 2,506 | 50.3% | k = {kappa_if_rda:.3f} |")
print(f"| LOF & DA | 596 | 12.0% | k = {kappa_lof_rda:.3f} |")

# ============================================================
# F2.2 --- BINOMIAL TEST: TIER-1 NOT RANDOM NOISE
# ============================================================
print()
print("=" * 60)
print("F2.2 --- BINOMIAL TEST: Tier-1 (47.1%) vs. random expectation")
print("=" * 60)

total_records = len(df)
total_flagged = df['consensus_flag'].sum()
p_flag_per_activity = total_flagged / total_records
print(f"Overall consensus detection rate: {p_flag_per_activity:.4f} ({p_flag_per_activity*100:.2f}%)")

n_years = 3
p_tier1_null = 1 - binom.pmf(0, n_years, p_flag_per_activity) - binom.pmf(1, n_years, p_flag_per_activity)
print(f"Expected Tier-1 rate under null: {p_tier1_null*100:.2f}%")

n_villages = 1364
observed_tier1 = 642
binom_result = stats.binomtest(observed_tier1, n_villages, p_tier1_null, alternative='greater')
print(f"Observed Tier-1 rate: 47.1% ({observed_tier1}/{n_villages} villages)")
print(f"Exact binomial test p-value: {binom_result.pvalue:.2e}")
print()
print(">>> SENTENCE FOR para 4.6:")
print(f"P(X >= 2 | X ~ Binomial(3, {p_flag_per_activity:.4f})) = {p_tier1_null*100:.2f}%")
print(f"Observed: 47.1% -- p < {binom_result.pvalue:.1e} (exact binomial test, one-sided)")

# ============================================================
# F2.3 --- SENSITIVITY ANALYSIS: CONTAMINATION PARAMETER
# ============================================================
print()
print("=" * 60)
print("F2.3 --- SENSITIVITY ANALYSIS: Contamination thresholds")
print("=" * 60)

contamination_levels = [0.03, 0.05, 0.08, 0.10]
results_sensitivity = []

for cont in contamination_levels:
    threshold_pct = (1 - cont) * 100
    if_threshold = np.percentile(df['if_score'], threshold_pct)
    lof_threshold = np.percentile(df['lof_score'], threshold_pct)
    rda_threshold = np.percentile(df['rda_score'], threshold_pct)

    if_flags_sim = (df['if_score'] >= if_threshold).astype(int)
    lof_flags_sim = (df['lof_score'] >= lof_threshold).astype(int)
    rda_flags_sim = (df['rda_score'] >= rda_threshold).astype(int)
    consensus_sim = ((if_flags_sim + lof_flags_sim + rda_flags_sim) >= 2).astype(int)

    overlap_if_rda = (if_flags_sim & rda_flags_sim).sum()
    overlap_ratio = overlap_if_rda / max(1, min(if_flags_sim.sum(), rda_flags_sim.sum()))

    results_sensitivity.append({
        'Cont.': f"{cont*100:.0f}%",
        'IF Flags': if_flags_sim.sum(),
        'LOF Flags': lof_flags_sim.sum(),
        'DA Flags': rda_flags_sim.sum(),
        'Consensus': consensus_sim.sum(),
        'IF & DA %': f"{overlap_ratio*100:.1f}%"
    })

sens_df = pd.DataFrame(results_sensitivity)
print(sens_df.to_string(index=False))
print("Note: 5% row = v1 results baseline")

# ============================================================
# F2.4 --- PAGU BY YEAR (fiscal expansion hypothesis)
# ============================================================
print()
print("=" * 60)
print("F2.4 --- PAGU PER YEAR: fiscal expansion data")
print("=" * 60)

if 'Pagu' in df.columns and 'Tahun' in df.columns:
    pagu_by_year = df.groupby('Tahun').agg(
        N_Activities=('Pagu', 'count'),
        Mean_Pagu=('Pagu', 'mean'),
        Total_Pagu_Rp=('Pagu', 'sum')
    )
    pagu_by_year['Total_Pagu_Miliar'] = pagu_by_year['Total_Pagu_Rp'] / 1e9
    print(pagu_by_year[['N_Activities', 'Mean_Pagu', 'Total_Pagu_Miliar']].to_string())
    print("Total_Pagu_Miliar = total budget allocation in billion Rp")

# ============================================================
# F2.5 --- KS TEST: SCORE DISTRIBUTION SHIFT
# ============================================================
print()
print("=" * 60)
print("F2.5 --- KS TEST: Score distribution across fiscal years")
print("=" * 60)

if 'Tahun' in df.columns:
    df_2023 = df[df['Tahun'] == 2023]
    df_2024 = df[df['Tahun'] == 2024]
    df_2025 = df[df['Tahun'] == 2025]

    for method, score_col in [('IF', 'if_score'), ('LOF', 'lof_score'), ('DA', 'rda_score')]:
        ks_23_24 = ks_2samp(df_2023[score_col].dropna(), df_2024[score_col].dropna())
        ks_23_25 = ks_2samp(df_2023[score_col].dropna(), df_2025[score_col].dropna())
        ks_24_25 = ks_2samp(df_2024[score_col].dropna(), df_2025[score_col].dropna())
        print(f"{method}: KS(23v24)=D{ks_23_24.statistic:.3f},p{ks_23_24.pvalue:.3f} | KS(23v25)=D{ks_23_25.statistic:.3f},p{ks_23_25.pvalue:.3f} | KS(24v25)=D{ks_24_25.statistic:.3f},p{ks_24_25.pvalue:.3f}")

print()
print("FASE 2 COMPLETE - copy above values into draft §4 sections")
