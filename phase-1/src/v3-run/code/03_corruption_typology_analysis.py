# Converted from 03_corruption_typology_analysis.ipynb

'''
# Notebook 03 — Corruption Typology Analysis & Expert Validation Preparation

**Research**: Anomaly Detection in Jambi Village Fund Expenditure (2023–2025)  
**Method**: Typology mapping → PCA/t-SNE visualisation → Per-feature RDA error decomposition → Expert validation export  

```
anomaly_flags.csv
df_merged_raw.csv
        │
        ▼
  Typology Mapping          ← 7 modus operandi per Section 9 of research concept
        │
        ▼
  PCA / t-SNE viz           ← flagged vs normal in 2-D
        │
        ▼
  RDA Error Decomposition   ← which feature drives each detection
        │
        ▼
  Village Persistence Rank  ← Tier 1 / Tier 2 deep-dive
        │
        ▼
  Expert Validation Export  ← Top-50 per method, binary rubric template
```

**Dependencies**: Run Notebook 01 and Notebook 02 first to generate `features_engineered.csv`, `anomaly_flags.csv`, and `df_merged_raw.csv`.
'''

from google.colab import drive
drive.mount('/content/drive')


# ── Cell 2: Imports & paths ───────────────────────────────────────────────
import os, warnings
import logging
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", palette="muted")

# ── Colab / local path resolution ────────────────────────────────────────
try:
    from google.colab import drive
    drive.mount("/content/drive", force_remount=False)
    BASE_DIR   = "/content"
    DATA_DIR   = "/content/drive/MyDrive/Colab_Notebooks/data_dandes/input"            # ← change to local path if running locally
    OUTPUT_DIR = "/content/drive/MyDrive/Colab_Notebooks/data_dandes/v3-run"
except ImportError:
    BASE_DIR   = os.path.dirname(os.path.abspath("__file__"))
    DATA_DIR   = os.path.join(BASE_DIR, "..", "..", "data_ref", "csv")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

SEED = 42
np.random.seed(SEED)

# ── Logging setup ─────────────────────────────────────────────────────────
LOG_FILE = f"{OUTPUT_DIR}/typology_analysis.log"
logger   = logging.getLogger("typology_analysis")
logger.setLevel(logging.INFO)
if logger.handlers:
    logger.handlers.clear()
_fh  = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
_sh  = logging.StreamHandler()
_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                          datefmt="%Y-%m-%d %H:%M:%S")
_fh.setFormatter(_fmt); _sh.setFormatter(_fmt)
logger.addHandler(_fh); logger.addHandler(_sh)
logger.info(f"=== Notebook 03 started  |  OUTPUT_DIR={OUTPUT_DIR} ===")
logger.info(f"Log file: {LOG_FILE}")

print(f"DATA_DIR   : {DATA_DIR}")
print(f"OUTPUT_DIR : {OUTPUT_DIR}")


# ── Cell 3: Load data ────────────────────────────────────────────────────
df_flags = pd.read_csv(f"{OUTPUT_DIR}/anomaly_flags.csv")
df_raw   = pd.read_csv(f"{OUTPUT_DIR}/df_merged_raw.csv")

# ── Identify engineered feature columns (numeric, not metadata) ──────────
META_COLS = [
    "Kode_Desa", "Nama_Desa", "Tahun",
    "Uraian_Output", "Cara_Pengadaan",
    "iqr_flag", "if_score", "if_flag",
    "lof_score", "lof_flag",
    "rda_score", "rda_flag", "consensus_flag",
    "persistence_score", "priority_tier", "years_flagged"
]
# RDA per-feature error columns
RDA_ERR_COLS = [c for c in df_flags.columns if c.startswith("rda_err_")]
META_COLS    = META_COLS + RDA_ERR_COLS + ["rda_sparse_norm"]

FEATURE_COLS = [c for c in df_flags.columns
                if c not in META_COLS and pd.api.types.is_numeric_dtype(df_flags[c])]

print(f"Records loaded       : {len(df_flags):,}")
print(f"Feature columns      : {len(FEATURE_COLS)} → {FEATURE_COLS}")
print(f"RDA error cols       : {RDA_ERR_COLS}")
print(f"Consensus flagged    : {df_flags['consensus_flag'].sum():,}  ({df_flags['consensus_flag'].mean()*100:.1f}%)")


'''
## 1. Corruption Typology Mapping

Seven modus operandi are derived from the research concept (Section 9).  
Each rule maps a combination of feature thresholds to a suspected typology.

| # | Typology | Primary Signal Features |
|---|---|---|
| T1 | Mark-up / price inflation | `cost_per_unit` high, `cost_deviation_by_category` high |
| T2 | Ghost activities / fictitious expenditure | `absorption_ratio` near 0 or very high in single stage |
| T3 | Volume padding (amount manipulation) | `absorption_ratio` ≥ 0.98 (near-complete single-cycle budget absorption) |
| T4 | Stage lock (zero disbursement) | `n_stages_active` = 0 (budget allocated, zero disbursement across all stages) |
| T5 | Procurement irregularity | `Cara_Pengadaan` = Pihak ke-3 / Kontrak AND high `cost_per_unit` (> 75th pct) |
| T6 | Budget exhaustion pattern | Repeated near-100% absorption every year = `persistence_score` high |
| T7 | Cross-category coordinate dumping | `cost_deviation_by_category` extreme across multiple outputs |
'''

# ── Cell 5: Typology mapping (rule-based on flagged records — v2.0) ─────
flagged = df_flags[df_flags['consensus_flag'] == 1].copy()

_thresholds = {
    'cpu_p75': df_flags['cost_per_unit'].quantile(0.75),
    'cpu_p90': df_flags['cost_per_unit'].quantile(0.90),
}
if 'cost_deviation_by_category' in df_flags.columns:
    _thresholds['cdev_p80'] = df_flags['cost_deviation_by_category'].quantile(0.80)
    _thresholds['cdev_p95'] = df_flags['cost_deviation_by_category'].quantile(0.95)
else:
    _thresholds['cdev_p80'], _thresholds['cdev_p95'] = None, None

if 'absorption_ratio' in df_flags.columns:
    _thresholds['abs_low'] = df_flags['absorption_ratio'].quantile(0.05)
    _thresholds['abs_high'] = df_flags['absorption_ratio'].quantile(0.97)
    _thresholds['abs_p90'] = df_flags['absorption_ratio'].quantile(0.90)
else:
    _thresholds['abs_low'], _thresholds['abs_high'], _thresholds['abs_p90'] = None, None, None

def assign_typologies_v2(row):
    labels = []
    cpu = row.get('cost_per_unit', 0)
    cdev = row.get('cost_deviation_by_category', 0)
    abs_r = row.get('absorption_ratio', 0)
    avg_comp = row.get('avg_completion', 0)
    swakelola_high = row.get('swakelola_high_value', 0)
    nsa = row.get('n_stages_active', 0)

    # T1 — Mark-up / Price Inflation
    if cpu > 3 and cdev > 2:
        labels.append('T1_Markup')

    # T2 — Ghost / Fictitious Activity
    if abs_r < 0.05 and avg_comp < 0.10:
        labels.append('T2_Ghost')

    # T3 — Volume Padding (Budget Exhaustion / Near-Full Absorption)
    if abs_r >= 0.98:
        labels.append('T3_VolumePadding')

    # T4 — Stage Lock (Front-loaded tranche concentration)
    reals = [row.get('Real_T1', 0), row.get('Real_T2', 0), row.get('Real_T3', 0)]
    tot_real = row.get('total_realization', 0)
    stage_conc = max(reals) / tot_real if tot_real > 0 else 0
    if stage_conc > 0.95 and nsa >= 2:
        labels.append('T4_StageLock')

    # T5 — Procurement Irregularity
    if swakelola_high == 1 and cpu > 0:
        labels.append('T5_ProcurementIrregularity')

    # T6 — Budget Exhaustion
    if abs_r > 0.98 and avg_comp < 0.50:
        labels.append('T6_BudgetExhaustion')

    # T7 — Cross-Category Dump
    if abs(cdev) > 3:
        labels.append('T7_CrossCatDump')

    return labels if labels else ['Unclassified']

flagged['typologies'] = flagged.apply(assign_typologies_v2, axis=1)
flagged['typology_primary'] = flagged['typologies'].apply(lambda x: x[0])
flagged['typology_count'] = flagged['typologies'].apply(len)
print('[OK] Reconciled typologies v2 applied successfully.')


from collections import Counter

# __ Cell 6: Typology bar chart ───────────────────────────────────────────

# Note: Keys updated to match assign_typologies_v2 function labels
typology_labels = {
    "T1_Markup"      : "T1: Mark-up",
    "T2_Ghost"       : "T2: Ghost Activity",
    "T3_VolumePadding"   : "T3: Volume Padding",
    "T4_StageLock"   : "T4: Stage Lock",
    "T5_ProcurementIrregularity"  : "T5: Procurement Irr.",
    "T6_BudgetExhaustion": "T6: Budget Exhaustion",
    "T7_CrossCatDump": "T7: Cross-Category Dump",
    "Unclassified"   : "Unclassified",
}
palette = ["#d62728","#ff7f0e","#2ca02c","#1f77b4","#9467bd","#8c564b","#e377c2","#7f7f7f"]

# Flatten the list of lists in the 'typologies' column to get all individual labels
all_labels = [label for sublist in flagged['typologies'] for label in sublist]

counts = pd.Series(Counter(all_labels)).reindex(typology_labels.keys(), fill_value=0)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(
    [typology_labels[k] for k in counts.index],
    counts.values,
    color=palette[:len(counts)]
)
for bar, v in zip(bars, counts.values):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
            str(v), va="center", fontsize=9)
ax.set_xlabel("Number of Flagged Records (multi-label)")
ax.set_title("Corruption Typology Distribution Among Consensus-Flagged Records", fontsize=11)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/typology_distribution.png", dpi=150)
plt.show()
print("Saved: typology_distribution.png")


'''
## 2. PCA and t-SNE Visualisation

Project all records into 2-D space to visually confirm that anomalous records cluster separately from normal ones. Two approaches:
- **PCA**: Linear projection — fast, interpretable loadings
- **t-SNE**: Non-linear projection — reveals local cluster structure

Points are coloured by `consensus_flag` (0 = normal, 1 = anomaly).
'''

# ── Cell 8: PCA projection ───────────────────────────────────────────────

X_all  = df_flags[FEATURE_COLS].fillna(0).values
labels = df_flags["consensus_flag"].values

# Standardise for PCA (separate scaler — do NOT use RobustScaler here to preserve
# visualisation scale, StandardScaler is conventional for PCA biplots)
scaler_pca = StandardScaler()
X_std = scaler_pca.fit_transform(X_all)

pca  = PCA(n_components=2, random_state=SEED)
Xpca = pca.fit_transform(X_std)

var_explained = pca.explained_variance_ratio_
print(f"PCA explained variance: PC1={var_explained[0]*100:.1f}%  PC2={var_explained[1]*100:.1f}%")

fig, ax = plt.subplots(figsize=(8, 6))
colors = {0: "#aec7e8", 1: "#d62728"}
for flag, label_str in [(0, "Normal"), (1, "Anomaly (consensus)")]:
    mask = labels == flag
    ax.scatter(Xpca[mask, 0], Xpca[mask, 1],
               c=colors[flag], s=8, alpha=0.5, label=f"{label_str} (n={mask.sum():,})")
ax.set_xlabel(f"PC1 ({var_explained[0]*100:.1f}% var)")
ax.set_ylabel(f"PC2 ({var_explained[1]*100:.1f}% var)")
ax.set_title("PCA Projection — Normal vs Consensus-Flagged Records", fontsize=11)
ax.legend(markerscale=3)

# Feature loadings biplot (top 5 features by PC1 loading)
loadings = pd.Series(pca.components_[0], index=FEATURE_COLS).abs().nlargest(5)
print("\nTop 5 features driving PC1:")
print(loadings.to_string())

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/pca_projection.png", dpi=150)
plt.show()
print("Saved: pca_projection.png")


# ── Cell 9: t-SNE projection ─────────────────────────────────────────────
# t-SNE on a sample (max 15,000) to keep runtime manageable on Colab

MAX_TSNE = 15_000
if len(X_std) > MAX_TSNE:
    rng  = np.random.default_rng(SEED)
    idx  = rng.choice(len(X_std), MAX_TSNE, replace=False)
    Xs   = X_std[idx]
    ys   = labels[idx]
else:
    Xs, ys = X_std, labels

print(f"Running t-SNE on {len(Xs):,} records (perplexity=30) …")
tsne  = TSNE(n_components=2, perplexity=30, n_iter=1000, random_state=SEED, init="pca", verbose=1)
Xtsne = tsne.fit_transform(Xs)

fig, ax = plt.subplots(figsize=(8, 6))
for flag, label_str in [(0, "Normal"), (1, "Anomaly (consensus)")]:
    mask = ys == flag
    ax.scatter(Xtsne[mask, 0], Xtsne[mask, 1],
               c=colors[flag], s=8, alpha=0.5, label=f"{label_str} (n={mask.sum():,})")
ax.set_xlabel("t-SNE dim 1")
ax.set_ylabel("t-SNE dim 2")
ax.set_title("t-SNE Projection — Normal vs Consensus-Flagged Records", fontsize=11)
ax.legend(markerscale=3)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/tsne_projection.png", dpi=150)
plt.show()
print("Saved: tsne_projection.png")


'''
## 3. RDA Per-Feature Reconstruction Error Decomposition

For each consensus-flagged record, the RDA reconstruction error per feature (`rda_err_{feat}`) reveals **which financial attribute drives the anomaly signal** — directly informing the typology assignment and the expert validator's focus areas.
'''

# ── Cell 11: RDA error decomposition heatmap ─────────────────────────────

if RDA_ERR_COLS:
    err_df = flagged[RDA_ERR_COLS].copy()
    # Rename for display: strip "rda_err_" prefix
    err_df.columns = [c.replace("rda_err_", "") for c in err_df.columns]

    # Mean error per feature across all consensus-flagged records
    mean_err = err_df.mean().sort_values(ascending=False)
    print("Mean RDA reconstruction error per feature (consensus-flagged records):")
    print(mean_err.to_string())

    # Heatmap of top-50 flagged records (sorted by total rda_score)
    top50 = flagged.nlargest(50, "rda_score")
    top50_err = top50[RDA_ERR_COLS].set_index(top50["Kode_Desa"].astype(str) + "_" + top50["Tahun"].astype(str))
    top50_err.columns = [c.replace("rda_err_", "") for c in top50_err.columns]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Left: bar chart of mean feature errors
    ax = axes[0]
    mean_err.plot(kind="barh", ax=ax, color="#1f77b4")
    ax.set_title("Mean RDA Error per Feature\n(All Consensus-Flagged)", fontsize=10)
    ax.set_xlabel("Mean Squared Error")
    ax.invert_yaxis()

    # Right: heatmap for top-50 records
    ax = axes[1]
    sns.heatmap(top50_err.T, ax=ax, cmap="Reds", linewidths=0.2,
                xticklabels=False, yticklabels=True, cbar_kws={"label": "Recon. Error"})
    ax.set_title("RDA Error Heatmap — Top-50 Flagged Records", fontsize=10)
    ax.set_xlabel("Records (sorted by RDA score)")
    ax.tick_params(axis="y", labelsize=8)

    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/rda_error_decomposition.png", dpi=150)
    plt.show()
    print("Saved: rda_error_decomposition.png")

    # Add 'top_error_feature' column to flagged for export
    flagged["top_error_feature"] = flagged[RDA_ERR_COLS].idxmax(axis=1).str.replace("rda_err_", "")
else:
    print("No RDA error columns found — skipping decomposition (run Notebook 02 with per-feature errors enabled).")
    flagged["top_error_feature"] = "N/A"


'''
## 4. Village Persistence Ranking Deep-Dive

Focus on Tier 1 villages (flagged in ≥ 2/3 years). For each, summarise:
- Total flagged records per year
- Dominant typology
- Top anomaly driving feature (from RDA error)
'''

# ── Cell 13: Tier 1 village deep-dive ────────────────────────────────────

tier1_villages = df_flags[df_flags["priority_tier"] == "Tier 1 – High Priority"]["Kode_Desa"].unique()
print(f"Tier 1 villages: {len(tier1_villages):,}")

if len(tier1_villages) == 0:
    print("No Tier 1 villages detected — lower persistence threshold or check consensus_flag.")
else:
    tier1_df = flagged[flagged["Kode_Desa"].isin(tier1_villages)].copy()

    # Get dominant typology per village
    def dominant_typology(ts_series):
        all_t = [t for ts in ts_series for t in ts]
        if not all_t:
            return "Unclassified"
        return Counter(all_t).most_common(1)[0][0]

    tier1_summary = (
        tier1_df.groupby("Kode_Desa")
        .agg(
            n_flagged_records=("consensus_flag", "count"),
            dominant_typology=("typologies", dominant_typology),
            top_rda_feature=("top_error_feature", lambda x: x.mode()[0] if len(x) > 0 else "N/A"),
            persistence_score=("persistence_score", "first"),
            years_flagged=("years_flagged", "first"),
        )
        .reset_index()
        .sort_values("persistence_score", ascending=False)
    )

    if "Nama_Desa" in tier1_df.columns:
        name_map = tier1_df.drop_duplicates("Kode_Desa")[["Kode_Desa","Nama_Desa"]]
        tier1_summary = tier1_summary.merge(name_map, on="Kode_Desa", how="left")

    print(f"\nTier 1 village summary ({len(tier1_summary)} villages, top 30 shown):")
    print(tier1_summary.head(30).to_string(index=False))


'''
## 5. Expert Validation Export

For each method (IF, LOF, RDA, Consensus), export the **Top-50 records** ranked by score.  
The sheet includes a blank `expert_verdict` column (Suspicious / Not Suspicious) and a `modus_operandi_notes` column for the validators.

Expert validation protocol (from research concept Section 8.5):
- **Raters**: 2 independent domain experts (anti-corruption / village finance)
- **Rubric**: Binary verdict per 7 modus operandi indicators
- **Agreement**: Inter-rater Cohen's κ computed after both sheets returned
'''

# ── Cell 15: Expert validation Top-50 export per method ──────────────────

# Columns to include in the expert sheet
raw_cost_cols = [c for c in df_raw.columns if "Realisasi" in c or "Pagu" in c or "Volume" in c]
base_cols     = ["Kode_Desa", "Tahun"]
name_col      = ["Nama_Desa"] if "Nama_Desa" in df_flags.columns else []
output_col    = ["Uraian_Output"] if "Uraian_Output" in df_flags.columns else []
cara_col      = ["Cara_Pengadaan"] if "Cara_Pengadaan" in df_flags.columns else []
score_flag    = ["if_score","if_flag","lof_score","lof_flag","rda_score","rda_flag","consensus_flag"]
typology_col  = ["typology_primary","typologies","top_error_feature"]

export_base_cols = base_cols + name_col + output_col + cara_col

# ── Transfer typology columns back to df_flags via index alignment ──────────
# flagged is a direct .copy() filtered subset of df_flags, so their index spaces
# are aligned.  Index-based assignment avoids the multi-key merge that would
# produce duplicate rows when (Kode_Desa, Tahun, Uraian_Output) is non-unique.
flagged_export = df_flags.copy()
flagged_export["typology_primary"]  = "Unclassified"
flagged_export["top_error_feature"] = "N/A"
flagged_export["typologies"]        = None

# String columns can use .loc directly; list column needs .at to preserve dtype
flagged_export.loc[flagged.index, ["typology_primary", "top_error_feature"]] = \
    flagged[["typology_primary", "top_error_feature"]].values
for idx in flagged.index:
    flagged_export.at[idx, "typologies"] = flagged.at[idx, "typologies"]

flagged_export["typologies_str"] = flagged_export["typologies"].apply(
    lambda x: "|".join(x) if isinstance(x, list) else "Unclassified"
)

# Expert verdict template columns
flagged_export["expert_verdict"]       = ""   # Suspicious / Not Suspicious
flagged_export["modus_operandi_notes"] = ""   # Free-text notes from expert

EXPERT_COLS = (
    export_base_cols
    + score_flag
    + ["typology_primary","typologies_str","top_error_feature"]
    + ["persistence_score","priority_tier"]
    + ["expert_verdict","modus_operandi_notes"]
)
EXPERT_COLS = [c for c in EXPERT_COLS if c in flagged_export.columns]

methods = {
    "IF"       : ("if_score",  "if_flag"),
    "LOF"      : ("lof_score", "lof_flag"),
    "RDA"      : ("rda_score", "rda_flag"),
    "CONSENSUS": ("rda_score", "consensus_flag"),    # sort by RDA score within consensus
}

for method_name, (score_col, flag_col) in methods.items():
    subset = flagged_export[flagged_export[flag_col] == 1].nlargest(50, score_col)
    out_path = f"{OUTPUT_DIR}/expert_validation_top50_{method_name}.csv"
    subset[EXPERT_COLS].to_csv(out_path, index=False)
    print(f"Saved: {out_path}  ({len(subset)} records)")

print("\nExpert validation templates ready for distribution.")


'''
## 6. Final Exports

All analysis artefacts consolidated for Notebook 04 (results write-up) and expert reviewers.
'''

# ── Cell 17: Final export — enriched flagged dataset + tier 1 deep-dive ──

# Full flagged-record dataset with typology labels
out_full = f"{OUTPUT_DIR}/flagged_with_typology.csv"
export_full_cols = EXPERT_COLS + [c for c in ["years_flagged","lof_flag","rda_sparse_norm"] if c in flagged_export.columns]
export_full_cols = list(dict.fromkeys(export_full_cols))     # deduplicate, preserve order
flagged_export[flagged_export["consensus_flag"] == 1][export_full_cols].to_csv(out_full, index=False)
print(f"Saved: {out_full}")

# Tier-1 summary table
if len(tier1_villages) > 0:
    out_tier1 = f"{OUTPUT_DIR}/tier1_village_summary.csv"
    tier1_summary.to_csv(out_tier1, index=False)
    print(f"Saved: {out_tier1}")

# Typology frequency CSV for paper table
typology_freq = pd.DataFrame(Counter(all_labels).items(), columns=["Typology","Count"])
typology_freq["Label"] = typology_freq["Typology"].map(typology_labels)
typology_freq["Pct_of_Flagged"] = (typology_freq["Count"] / len(flagged) * 100).round(1)
typology_freq.sort_values("Count", ascending=False, inplace=True)
out_typo = f"{OUTPUT_DIR}/typology_frequency.csv"
typology_freq.to_csv(out_typo, index=False)
print(f"Saved: {out_typo}")

print("\n=== NOTEBOOK 03 COMPLETE — Artefact Summary ===")
artefacts = [
    "pca_projection.png",
    "tsne_projection.png",
    "typology_distribution.png",
    "rda_error_decomposition.png",
    "village_persistence_tiers.png",
    "flagged_with_typology.csv",
    "tier1_village_summary.csv",
    "typology_frequency.csv",
    "expert_validation_top50_IF.csv",
    "expert_validation_top50_LOF.csv",
    "expert_validation_top50_RDA.csv",
    "expert_validation_top50_CONSENSUS.csv",
]
found, missing = [], []
for a in artefacts:
    fpath = f"{OUTPUT_DIR}/{a}"
    if os.path.exists(fpath):
        found.append(a)
        print(f"  ✓  {a}")
    else:
        missing.append(a)
        print(f"  ✗ NOT FOUND  {a}")

logger.info(f"Notebook 03 finished  |  artefacts_found={len(found)}  missing={missing}")
logger.info("=== Notebook 03 finished ===")

